// Product data is provided by each independent application.
export function httpsUrl(value, hosts = []) {
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password) return null;
    if (hosts.length && !hosts.some(host => url.hostname === host || url.hostname.endsWith(`.${host}`))) return null;
    return url.href;
  } catch { return null; }
}
export function bindCheckout(root, { url, hosts, statusId, messages = {} }) {
  const checkout = httpsUrl(url, hosts);
  root.querySelectorAll('[data-buy]').forEach(link => {
    if (checkout) {
      link.href = checkout;
      link.removeAttribute('aria-disabled');
      link.removeAttribute('role');
      link.removeAttribute('tabindex');
    } else {
      link.removeAttribute('href');
      link.setAttribute('role', 'link');
      link.setAttribute('tabindex', '0');
      link.setAttribute('aria-disabled', 'true');
    }
    link.setAttribute('aria-describedby', statusId);
  });
  const status = root.getElementById(statusId);
  if (status) status.textContent = checkout
    ? (messages.available || 'Você será direcionado ao checkout externo.')
    : (messages.unavailable || 'Compra ainda indisponível.');
  return checkout;
}
