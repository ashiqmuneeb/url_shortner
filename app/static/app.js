function copyText(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event?.target;
    if (btn) {
      const prev = btn.textContent;
      btn.textContent = "Copied!";
      setTimeout(() => (btn.textContent = prev), 1200);
    }
  });
}
