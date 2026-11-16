// Connectify mockup — purely cosmetic toggle between the Log In and
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
      loginCard.classList.add("is-hidden");
      signupCard.classList.remove("is-hidden");
    });
  }

  if (showLoginBtn) {
    showLoginBtn.addEventListener("click", function () {
      signupCard.classList.add("is-hidden");
      loginCard.classList.remove("is-hidden");
      if (loginHeading) loginHeading.classList.remove("is-hidden");
    });
  }
});
