// DPDP-025: personal data stored in browser localStorage
function saveSession(user) {
  localStorage.setItem("email", user.email);
  localStorage.setItem("phone", user.phone);

  // DPDP-002: PII written to the browser console
  console.log("logged in user", user.email, user.aadhaar);

  // DPDP-028: PII sent to a third-party analytics SDK
  mixpanel.identify(user.email);
  analytics.track("login", { email: user.email, phone: user.phone });
}

// DPDP-024: user input rendered as raw HTML (XSS / data exposure)
function renderProfile(req) {
  document.getElementById("bio").innerHTML = req.query.name;
}
