document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (username && email && password) {
        console.log('Form submitted:', { username, email, password });
        // You can send this data to the backend using a fetch/POST request
        // fetch('YOUR_BACKEND_REGISTER_URL', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ username, email, password })
        // });
    } else {
        alert('Please fill in all fields.');
    }
});

document.getElementById('googleOAuth').addEventListener('click', function() {
    window.location.href = 'YOUR_BACKEND_OAUTH_URL'; // Redirect to your backend OAuth endpoint
});
