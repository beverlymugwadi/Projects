// Simplified Sign-In Function
function signIn() {
    console.log("Sign in function called"); // Debug log

    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const signInSection = document.getElementById('sign-in-section');
    const dashboardSection = document.getElementById('dashboard-section');

    // Log input values for debugging
    console.log("Username:", usernameInput.value);
    console.log("Password:", passwordInput.value);

    // Validate inputs
    if (usernameInput.value.trim() === '') {
        alert('Please enter a username');
        return;
    }

    if (passwordInput.value.trim() === '') {
        alert('Please enter a password');
        return;
    }

    // Simple validation logic
    if (usernameInput.value.length >= 3 && passwordInput.value.length >= 4) {
        // Hide sign-in section
        signInSection.style.display = 'none';
        
        // Show dashboard section
        dashboardSection.style.display = 'block';
        
        console.log("Sign in successful"); // Debug log
    } else {
        alert('Username must be at least 3 characters and password at least 4 characters');
    }
}

// Add event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded"); // Debug log

    // Ensure sign in button exists and add click event
    const signInButton = document.getElementById('sign-in-btn');
    if (signInButton) {
        signInButton.addEventListener('click', signIn);
        console.log("Click event added to sign-in button");
    } else {
        console.error("Sign-in button not found");
    }

    // Add enter key support for inputs
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    if (usernameInput) {
        usernameInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                signIn();
            }
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                signIn();
            }
        });
    }
});

// Placeholder functions for other features
function setAlarm() {
    console.log("Alarm set");
}

function addReminder() {
    console.log("Reminder added");
}