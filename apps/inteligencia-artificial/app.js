import { bindCheckout, httpsUrl } from './shared/commerce.js';

const product = window.IA_CONFIG || {};
const text = value => typeof value === 'string' ? value.trim() : '';
const checkoutHosts = ['kiwify.com.br', 'kiwify.com', 'kiwify.app'];
const utmNames = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

// UTMs stay in the external checkout URL. No cookies, storage, tracker or network call.
function checkoutWithUtm(value) {
  const valid = httpsUrl(value, checkoutHosts);
  if (!valid || product.inheritUtm !== true) return valid;
  const checkout = new URL(valid);
  const incoming = new URLSearchParams(window.location.search);
  for (const key of utmNames) {
    const value = incoming.get(key);
    if (checkout.searchParams.has(key) || !value || value.length > 200 || /[\u0000-\u001f\u007f]/.test(value)) continue;
    checkout.searchParams.set(key, value);
  }
  return checkout.href;
}

const checkout = bindCheckout(document, {
  url: checkoutWithUtm(product.checkoutUrl),
  hosts: checkoutHosts,
  statusId: 'checkout-status',
  messages: {
    available: 'Você será direcionado ao checkout externo da Kiwify. Consulte as condições de compra e acesso na plataforma.',
    unavailable: 'Compra ainda indisponível. O link da Kiwify precisa ser configurado.'
  }
});

document.querySelectorAll('[data-buy]').forEach(link => {
  link.addEventListener('click', event => {
    if (!checkout) {
      event.preventDefault();
      return;
    }
    // This local event represents a checkout click, never a sale or a conversion.
    const candidate = text(link.dataset.placement);
    const placement = /^[a-z0-9_-]{1,40}$/i.test(candidate) ? candidate : 'checkout';
    document.dispatchEvent(new CustomEvent('dobraverse:checkout-click', {
      detail: Object.freeze({ product: 'inteligencia-artificial', placement })
    }));
  });
});

if (text(product.productName)) {
  document.querySelectorAll('[data-product-name]').forEach(node => { node.textContent = text(product.productName); });
}
if (text(product.subtitle)) {
  document.querySelectorAll('[data-product-subtitle]').forEach(node => { node.textContent = text(product.subtitle); });
}
const price = document.getElementById('price');
if (price) {
  const configured = text(product.price);
  price.textContent = configured && !/^INSERIR(?:_|\s|$)/i.test(configured) ? configured : 'Valor a confirmar';
}
if (product.originalPrice && document.getElementById('price-original')) {
  document.getElementById('price-original').textContent = text(product.originalPrice);
}

// Restrict product images to local assets, avoiding remote services and traversals.
function localAsset(value) {
  if (typeof value !== 'string' || !/^assets\/[a-z0-9_/-]+\.(?:webp|png|jpe?g|avif|svg)$/i.test(value)) return null;
  if (value.split('/').some(segment => !segment || segment === '.' || segment === '..')) return null;
  return value;
}

const cover = localAsset(product.cover);
if (cover) {
  document.querySelectorAll('[data-cover]').forEach(img => {
    img.src = cover;
    img.alt = `Capa oficial de ${text(product.productName) || 'Afinal, vale a pena estudar Inteligência Artificial?'}`;
  });
}

const previews = document.getElementById('previews');
if (previews) {
  for (const item of Array.isArray(product.previewImages) ? product.previewImages : []) {
    if (!item || !localAsset(item.src) || !text(item.alt)) continue;
    const figure = document.createElement('figure');
    const link = document.createElement('a');
    link.href = item.src;
    link.target = '_blank';
    link.rel = 'noopener';
    link.setAttribute('aria-label', `Ampliar: ${text(item.alt)} (abre em nova aba)`);
    const img = document.createElement('img');
    img.src = item.src;
    img.alt = text(item.alt);
    img.loading = 'lazy';
    img.decoding = 'async';
    if (Number.isSafeInteger(item.width) && item.width > 0 && Number.isSafeInteger(item.height) && item.height > 0) {
      img.width = item.width;
      img.height = item.height;
    }
    const caption = document.createElement('figcaption');
    caption.textContent = text(item.caption) || text(item.alt);
    link.append(img);
    figure.append(link, caption);
    previews.append(figure);
  }
  previews.hidden = !previews.children.length;
}

const author = document.getElementById('author');
if (author) {
  author.hidden = !text(product.author);
  if (!author.hidden) author.textContent = `Autoria: ${text(product.author)}`;
}
const contact = document.getElementById('contact');
if (contact) {
  const email = text(product.contactEmail);
  contact.hidden = !/^[a-z0-9._+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i.test(email);
  if (!contact.hidden) {
    contact.href = `mailto:${email}`;
    contact.textContent = 'Contato';
  }
}
const institutions = document.getElementById('institutional');
if (institutions) {
  for (const item of Array.isArray(product.institutionalLinks) ? product.institutionalLinks : []) {
    if (!item) continue;
    const url = httpsUrl(item.url);
    if (!url || !text(item.label)) continue;
    const link = document.createElement('a');
    link.href = url;
    link.textContent = text(item.label);
    institutions.append(link);
  }
  institutions.hidden = !institutions.children.length;
}
const previousVolume = document.getElementById('previous-volume-link');
if (previousVolume) {
  const url = httpsUrl(product.previousVolumeUrl);
  previousVolume.hidden = !url;
  if (url) previousVolume.href = url;
}
