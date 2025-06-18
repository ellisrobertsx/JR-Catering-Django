// nav.js

document.addEventListener('DOMContentLoaded', function() {
    // Burger menu toggle for mobile
    const burgerBtn = document.querySelector('.burger-btn');
    const navLinks = document.querySelector('.nav-links');
    if (burgerBtn && navLinks) {
        burgerBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Close nav on link click (for mobile UX)
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
        });
    });

    // Optionally, show a message on login/logout (client-side only)
    // Actual login/logout is handled by Django server-side
    // This is just for UI feedback if needed
    if (window.location.pathname === '/login/') {
        // Example: Show a message or highlight login
        // document.body.classList.add('login-page');
    }
    if (window.location.pathname === '/logout/') {
        // Example: Show a message or highlight logout
        // document.body.classList.add('logout-page');
    }
}); 