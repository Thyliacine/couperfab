(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector("nav.primary");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function statusEl(form, type, text) {
    var el = form.querySelector(".form-status");
    if (!el) return;
    el.className = "form-status " + (type || "");
    el.textContent = text;
  }

  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var lang = form.getAttribute("data-lang") || "fr";
      var type = form.getAttribute("data-form");
      var consent = form.querySelector('input[name="consent"]');
      if (consent && !consent.checked) {
        statusEl(form, "err", lang === "en"
          ? "Please check the consent box to continue."
          : "Veuillez cocher la case de consentement pour continuer.");
        return;
      }
      var data = {
        type: type,
        lang: lang,
        name: (form.querySelector('[name="name"]') || {}).value || "",
        email: (form.querySelector('[name="email"]') || {}).value || "",
        message: (form.querySelector('[name="message"]') || {}).value || "",
        consent: !!(consent && consent.checked),
        website: (form.querySelector('[name="website"]') || {}).value || ""
      };
      if (btn) btn.disabled = true;
      statusEl(form, "", lang === "en" ? "Sending…" : "Envoi en cours…");
      try {
        var res = await fetch("/api/subscribe", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(data)
        });
        var body = await res.json().catch(function () { return {}; });
        if (!res.ok || !body.ok) {
          throw new Error(body.error || "request failed");
        }
        form.reset();
        statusEl(form, "ok", lang === "en"
          ? (type === "contact"
            ? "Message received. We will reply as soon as we can."
            : "You are on the list. Thank you — you can unsubscribe at any time.")
          : (type === "contact"
            ? "Message reçu. Nous répondrons dès que possible."
            : "Vous êtes bien inscrit. Merci — vous pourrez vous désabonner en tout temps."));
      } catch (err) {
        statusEl(form, "err", lang === "en"
          ? "Something went wrong. Please try again, or write to us from the contact page."
          : "Un problème est survenu. Réessayez, ou écrivez-nous depuis la page contact.");
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  });
})();
