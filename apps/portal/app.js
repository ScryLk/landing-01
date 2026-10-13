// Dobraverse Portal — Interações da página inicial
const config = window.PORTAL_CONFIG || {};

// Preservação transparente de parâmetros UTM ao navegar para as páginas filhas
const utmNames = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
const incoming = new URLSearchParams(window.location.search);

if (Array.from(incoming.keys()).some(k => utmNames.includes(k))) {
  document.querySelectorAll('a[href^="https://"]').forEach(link => {
    try {
      const url = new URL(link.href);
      if (url.hostname.endsWith('dobraverse.io') || url.hostname.includes('kiwify')) {
        for (const key of utmNames) {
          const val = incoming.get(key);
          if (val && !url.searchParams.has(key)) {
            url.searchParams.set(key, val);
          }
        }
        link.href = url.href;
      }
    } catch {
      // Ignora URLs não parseáveis
    }
  });
}
