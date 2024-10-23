import os

from flask import Flask, request, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuring OAuth with Google
oauth = OAuth(app)
google = oauth.register(
    name='google',

    #client_id='307232269225-3bqj6tsta04bbl4vqkuo3cbburui051h.apps.googleusercontent.com',
    #client_secret='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',
    google_client_id = os.getenv('GOOGLE_CLIENT_ID'),
    google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',  # User info endpoint
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid profile email'}
)


# PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host="pg-18968f70-pocresto.j.aivencloud.com",
        database="myapp",
        user="avnadmin",
        aiven_password=os.getenv('AIVEN_PASSWORD'),
        port="12600"
    )
    return conn

# Route for Google OAuth login
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Route to handle the OAuth callback
@app.route('/auth/callback')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)

    # Retrieve user data from Google
    email = user_info.get('email')
    username = user_info.get('name')

    # Check if the user exists in the database, if not, insert the user
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()

    if user is None:
        cur.execute('INSERT INTO users (username, email) VALUES (%s, %s)', (username, email))
        conn.commit()

    cur.close()
    conn.close()

    session['profile'] = user_info
    return redirect('/welcome')



# Route for user registration via form
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')  # In production, make sure to hash passwords!

    # Insert user into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                (username, email, password))
    conn.commit()
    cur.close()
    conn.close()

    return "Registration successful!"


# Welcome page after login
@app.route('/welcome')
def welcome():
    if 'profile' not in session:
        return redirect('/login')  # Redirect to login if no profile data
    return render_template('welcome.html', name=session['profile']['name'], email=session['profile']['email'])


if __name__ == '__main__':
    app.run(debug=True)
