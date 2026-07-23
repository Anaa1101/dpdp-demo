1 | // DPDP-025: personal data stored in browser localStorage
       2 | function saveSession(user) {
       3 |   // Removed storing PII in localStorage
       4 |   // Instead, store a session token on the server-side
       5 |   fetch('/set-session', {
       6 |     method: 'POST',
       7 |     headers: {
       8 |       'Content-Type': 'application/json',
  // DPDP-028: PII sent to a third-party analytics SDK
  mixpanel.identify(user.email);
11 |   analytics.track("login", { email: user.email, phone: user.phone });
      12 | }
      13 | 
      14 | // DPDP-024: user input rendered as raw HTML (XSS / data exposure)
      15 | function renderProfile(req) {
>>>   16 |   document.getElementById("bio").textContent = req.query.name;
      17 | }
      18 |