 // https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById         ACCESSED - 12/12/24
 // https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener    ACCESSED - 12/12/24

 document.addEventListener("DOMContentLoaded", function() {
    // Get elements for "back-to-login" and "forgot-password-link"
    const backToLogin = document.getElementById("back-to-login");
    const forgotPasswordLink = document.getElementById("forgot-password-link");

    if (backToLogin) {
        backToLogin.addEventListener("click", function(event) {
            event.preventDefault();
            document.getElementById("reset-password-container").style.display = "none";
            document.getElementById("sign-in-container").style.display = "block";
        });
    }

    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener("click", function(event) {
            event.preventDefault();
            document.getElementById("sign-in-container").style.display = "none";
            document.getElementById("reset-password-container").style.display = "block";
        });
    }

    // SIGN UP AND LOGIN CONTENT
    const container = document.getElementById('container-login');
    const overlayBtnSignIn = document.getElementById('signIn');
    const overlayBtnSignUp = document.getElementById('signUp');

    if (overlayBtnSignIn && container) {
        overlayBtnSignIn.addEventListener('click', () => {
            container.classList.toggle('right-panel-active');
            overlayBtnSignIn.classList.remove('btnScaled');
            window.requestAnimationFrame(() => {
                overlayBtnSignIn.classList.add('btnScaled');
            });
        });
    }

    if (overlayBtnSignUp && container) {
        overlayBtnSignUp.addEventListener('click', () => {
            container.classList.toggle('right-panel-active');
            overlayBtnSignUp.classList.remove('btnScaled');
            window.requestAnimationFrame(() => {
                overlayBtnSignUp.classList.add('btnScaled');
            });
        });
    }

    // Book Driver functionality
    document.querySelectorAll(".book-driver").forEach(function (text) {
        text.addEventListener("click", function (event) {
            event.preventDefault();

            const driverInfo = this.getAttribute("data-driver");
            const messageBox = document.getElementById("message");

            messageBox.value = `Driver requested: ${driverInfo}`;
            messageBox.scrollIntoView({ behavior: "smooth", block: "center" });
        });
    });

    // SIGN UP INFO SECTION
    function updateContent() {
        const container = document.getElementById('container-login'); 
        const registrationTxt = document.querySelector('.registration-txt');
        const signInTxt = document.querySelector('.SignIn-txt');

        if (window.innerWidth <= 800) {
            registrationTxt.innerHTML = `Use your email for registration OR <a href='#' id='go-to-sign-in'>Sign In</a>`;
            signInTxt.innerHTML = `Use your personal account OR <a href='#' id='go-to-sign-up'> Sign Up </a>`;

            document.addEventListener('click', function (e) {
                if (e.target && e.target.id === 'go-to-sign-in') {
                    container.classList.remove('right-panel-active'); 
                    e.preventDefault();
                } else if (e.target && e.target.id === 'go-to-sign-up') {
                    container.classList.add('right-panel-active'); 
                    e.preventDefault();
                }
            });
        } else {
            registrationTxt.innerHTML = `or register your email for an account`;
            signInTxt.innerHTML = `Use your previous personal account`;
        }
    }

    updateContent();
    window.addEventListener('resize', updateContent);
});
document.addEventListener('DOMContentLoaded', function() {
    // Existing code...
    
    // Auto-close burger menu when clicking a link
    const navbarLinks = document.querySelectorAll('.navbar a');
    const menuCheckbox = document.getElementById('check');
    
    if (navbarLinks && menuCheckbox) {
        navbarLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Uncheck the checkbox to close the menu
                menuCheckbox.checked = false;
            });
        });
    }
});