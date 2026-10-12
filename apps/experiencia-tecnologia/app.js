(() => {
  'use strict';
  const config = window.BOOK_CONFIG;
  const safeUrl = value => {
    try { const url = new URL(value); return url.protocol === 'https:' ? url.href : null; }
    catch { return null; }
  };
  const checkout = safeUrl(config.CHECKOUT_URL);
  document.querySelectorAll('[data-buy]').forEach(link => {
    if (checkout) link.href = checkout;
    else {
      link.removeAttribute('href');
      link.setAttribute('role', 'link');
      link.setAttribute('aria-disabled', 'true');
      link.setAttribute('aria-describedby', 'checkout-status');
      link.setAttribute('tabindex', '0');
    }
  });
  document.getElementById('checkout-status').textContent = checkout
    ? 'Você será direcionado à plataforma de compra.'
    : 'Compra ainda indisponível: link de checkout em configuração.';
  if (config.price && config.price.trim()) document.getElementById('price').textContent = config.price;
  if (config.originalPrice && document.getElementById('price-original')) document.getElementById('price-original').textContent = config.originalPrice;
  document.querySelectorAll('[data-cover]').forEach(img => {
    img.src = config.coverUrl;
    img.alt = 'Capa do e-book Da sua experiência à tecnologia';
  });
  const previews = document.getElementById('previews');
  config.previewImages.forEach(item => {
    const figure = document.createElement('figure');
    const img = document.createElement('img');
    img.src = item.src; img.alt = item.alt; img.loading = 'lazy';
    img.width = 1237; img.height = 1600;
    const link = document.createElement('a');
    link.href = item.src; link.target = '_blank'; link.rel = 'noopener';
    link.setAttribute('aria-label', `Ampliar prévia: ${item.alt} (abre em nova aba)`);
    link.append(img);
    const caption = document.createElement('figcaption');
    const title = document.createElement('strong'); title.textContent = item.alt;
    const description = document.createElement('p'); description.textContent = item.description || '';
    caption.append(title, description);
    figure.append(link, caption); previews.append(figure);
  });
  previews.hidden = !config.previewImages.length;
  if (config.author.trim()) {
    const author = document.getElementById('author'); author.textContent = `Autoria: ${config.author}`; author.hidden = false;
  }
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(config.contactEmail)) {
    const contact = document.getElementById('contact'); contact.href = `mailto:${config.contactEmail}`;
    contact.textContent = 'Contato'; contact.hidden = false;
  }
  const institutional = document.getElementById('institutional');
  config.institutionalLinks.forEach(item => {
    const url = safeUrl(item.url); if (!url) return;
    const link = document.createElement('a'); link.href = url; link.textContent = item.label; institutional.append(link);
  });
  institutional.hidden = !institutional.children.length;
})();
