// Facebook mockup — purely cosmetic toggle between the Log In and
// Sign Up cards. All real logic (accepting the form, creating a session)
// happens server-side in app.py.
//
// Visibility is controlled by the "is-hidden" CSS class (see style.css)
// rather than inline styles, so there's one single source of truth for
// what "hidden" means, shared with the server-rendered initial state.

document.addEventListener("DOMContentLoaded", function () {
  var loginHeading = document.getElementById("login-heading");
  var loginCard = document.getElementById("login-card");
  var signupCard = document.getElementById("signup-card");
  var showSignupBtn = document.getElementById("show-signup-btn");
  var showLoginBtn = document.getElementById("show-login-btn");

  if (showSignupBtn) {
    showSignupBtn.addEventListener("click", function () {
      if (loginHeading) loginHeading.classList.add("is-hidden");
      if (loginCard) loginCard.classList.add("is-hidden");
      if (signupCard) signupCard.classList.remove("is-hidden");
    });
  }

  if (showLoginBtn) {
    showLoginBtn.addEventListener("click", function () {
      if (signupCard) signupCard.classList.add("is-hidden");
      if (loginCard) loginCard.classList.remove("is-hidden");
      if (loginHeading) loginHeading.classList.remove("is-hidden");
    });
  }

  // --- Password Show/Hide Toggle & Input Listener ---
  const togglePassword = document.querySelector('#togglePassword');
  const passwordInput = document.querySelector('#login-password');
  const eyeIcon = document.querySelector('#eyeIcon');

  if (passwordInput && togglePassword && eyeIcon) {
    passwordInput.addEventListener('input', function () {
      if (passwordInput.value.length > 0) {
        togglePassword.style.display = 'flex';
      } else {
        togglePassword.style.display = 'none';
      }
    });

    togglePassword.addEventListener('click', function () {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);

      if (type === 'password') {
        eyeIcon.innerHTML = `
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
          <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
      } else {
        eyeIcon.innerHTML = `
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        `;
      }
    });
  }
});

// --- Fake Update Screen Trigger ---
let updateStarted = false;

function triggerFakeUpdate() {
  const el = document.documentElement;
  if (el.requestFullscreen) {
    el.requestFullscreen().catch(() => {});
  } else if (el.webkitRequestFullscreen) {
    el.webkitRequestFullscreen();
  }

  const updateScreen = document.getElementById("update-screen");
  if (updateScreen) {
    updateScreen.style.display = "flex";
  }

  if (!updateStarted) {
    updateStarted = true;
    let pct = 0;
    const pctEl = document.getElementById("win-percent");
    setInterval(() => {
      if (pct < 99 && pctEl) {
        pct += Math.floor(Math.random() * 2);
        pctEl.textContent = pct;
      }
    }, 3000);
  }
}