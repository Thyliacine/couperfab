/**
 * CoupeFab newsletter + contact intake.
 * Persists to a webhook (Google Apps Script / Sheet) when NEWSLETTER_WEBHOOK_URL is set.
 * Also forwards to FormSubmit when NEWSLETTER_INBOX is set (confirm the first message by email).
 * Always appends to /tmp as a last-resort log (ephemeral on serverless).
 * CASL: consent must be explicitly true. Honeypot field "website" drops bots.
 */
const fs = require("fs");
const path = require("path");

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const TMP_FILE = path.join("/tmp", "couperfab-submissions.json");

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.setHeader("access-control-allow-origin", "*");
  res.setHeader("access-control-allow-methods", "POST, OPTIONS");
  res.setHeader("access-control-allow-headers", "content-type");
  res.end(JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (c) => {
      raw += c;
      if (raw.length > 50_000) {
        reject(new Error("too large"));
        req.destroy();
      }
    });
    req.on("end", () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch {
        reject(new Error("invalid json"));
      }
    });
    req.on("error", reject);
  });
}

function appendLocal(entry) {
  let list = [];
  try {
    list = JSON.parse(fs.readFileSync(TMP_FILE, "utf8"));
    if (!Array.isArray(list)) list = [];
  } catch {
    list = [];
  }
  list.push(entry);
  fs.writeFileSync(TMP_FILE, JSON.stringify(list, null, 2));
}

async function forwardWebhook(entry) {
  const url = process.env.NEWSLETTER_WEBHOOK_URL;
  if (!url) return false;
  const res = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(entry),
  });
  if (!res.ok) throw new Error("webhook " + res.status);
  return true;
}

async function forwardFormsubmit(entry) {
  const inbox = process.env.NEWSLETTER_INBOX;
  if (!inbox) return false;
  const res = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(inbox), {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify({
      _subject: entry.type === "contact" ? "CoupeFab — message" : "CoupeFab — inscription infolettre",
      type: entry.type,
      name: entry.name || "(non fourni)",
      email: entry.email,
      message: entry.message || "",
      lang: entry.lang,
      consent: entry.consent,
      submittedAt: entry.submittedAt,
    }),
  });
  if (!res.ok) throw new Error("formsubmit " + res.status);
  return true;
}

module.exports = async function handler(req, res) {
  if (req.method === "OPTIONS") {
    json(res, 204, {});
    return;
  }
  if (req.method !== "POST") {
    json(res, 405, { ok: false, error: "method not allowed" });
    return;
  }

  let body;
  try {
    body = await readBody(req);
  } catch {
    json(res, 400, { ok: false, error: "invalid body" });
    return;
  }

  if (body.website) {
    json(res, 200, { ok: true });
    return;
  }

  const type = body.type === "contact" ? "contact" : "newsletter";
  const email = String(body.email || "").trim().toLowerCase();
  const name = String(body.name || "").trim().slice(0, 200);
  const message = String(body.message || "").trim().slice(0, 4000);
  const lang = body.lang === "en" ? "en" : "fr";
  const consent = body.consent === true;

  if (!EMAIL_RE.test(email)) {
    json(res, 400, { ok: false, error: "invalid email" });
    return;
  }
  if (type === "newsletter" && !consent) {
    json(res, 400, { ok: false, error: "consent required" });
    return;
  }
  if (type === "contact" && !message) {
    json(res, 400, { ok: false, error: "message required" });
    return;
  }

  const entry = {
    type,
    email,
    name,
    message,
    lang,
    consent,
    submittedAt: new Date().toISOString(),
  };

  try {
    appendLocal(entry);
  } catch (err) {
    console.error("local append failed", err);
  }

  let stored = false;
  const errors = [];
  try {
    stored = (await forwardWebhook(entry)) || stored;
  } catch (err) {
    errors.push(String(err));
  }
  try {
    stored = (await forwardFormsubmit(entry)) || stored;
  } catch (err) {
    errors.push(String(err));
  }

  if (errors.length) console.error("forward errors", errors);

  // Accept the signup even if only the ephemeral log succeeded, so the form
  // does not fail closed on a fresh project. Operators should set NEWSLETTER_INBOX
  // or NEWSLETTER_WEBHOOK_URL for durable storage (see README).
  json(res, 200, {
    ok: true,
    persisted: stored,
  });
};
