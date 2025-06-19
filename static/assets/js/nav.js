// nav.js

document.addEventListener('DOMContentLoaded', function() {
    // Burger menu toggle for mobile
    const burgerBtn = document.querySelector('.burger-btn');
    const navLinks = document.querySelector('.nav-links');
    if (burgerBtn && navLinks) {
        burgerBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            burgerBtn.classList.toggle('open');
        });
    }

    // Dropdown functionality for mobile
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const dropdownContent = dropdown.querySelector('.dropdown-content');
        const dropdownLink = dropdown.querySelector('a');
        
        if (dropdownLink && dropdownContent) {
            dropdownLink.addEventListener('click', function(e) {
                e.preventDefault();
                dropdownContent.classList.toggle('show');
            });
        }
    });

    // Close nav on link click (for mobile UX)
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            // Don't close nav if it's a dropdown toggle
            if (!this.parentElement.classList.contains('dropdown')) {
                navLinks.classList.remove('active');
                burgerBtn.classList.remove('open');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.classList.remove('show');
            });
        }
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