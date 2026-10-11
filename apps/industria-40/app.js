import { bindCheckout, httpsUrl } from './shared/commerce.js';

const product = window.INDUSTRIA_CONFIG;
bindCheckout(document, {
  url: product.checkoutUrl,
  hosts: ['kiwify.com.br', 'kiwify.com', 'kiwify.app'],
  statusId: 'checkout-status',
  messages: {
    available: 'Compra e entrega pela Kiwify. Você será direcionado ao checkout externo.',
    unavailable: 'Compra ainda indisponível. O link da Kiwify será disponibilizado em breve.'
  }
});
document.querySelectorAll('[data-product-title]').forEach(node => { node.textContent = product.title; });
document.querySelectorAll('[data-product-subtitle]').forEach(node => { node.textContent = product.subtitle; });
if (product.price.trim()) document.getElementById('price').textContent = product.price;

const localAsset = value => {
  if (typeof value !== 'string' || !value.startsWith('assets/') || value.includes('..') || /[?#\\]/.test(value)) return null;
  return value;
};
if (localAsset(product.cover)) {
  document.querySelectorAll('[data-cover]').forEach(img => {
    // Hidden lazy images cannot load; the same local cover is reused from cache.
    img.loading = 'eager';
    img.src = product.cover;
    img.alt = `Capa oficial de ${product.title}`;
    img.addEventListener('load', () => {
      img.hidden = false;
      img.parentElement.querySelectorAll('[data-cover-placeholder]').forEach(node => { node.hidden = true; });
      const caption = img.parentElement.querySelector('[data-cover-caption]');
      if (caption) caption.textContent = 'COLEÇÃO AFINAL / CAPA OFICIAL';
    }, { once:true });
  });
}
const previews = document.getElementById('previews');
product.previewImages.forEach(item => {
  if (!localAsset(item.src)) return;
  const figure = document.createElement('figure');
  const link = document.createElement('a'); link.href = item.src; link.target = '_blank'; link.rel = 'noopener';
  link.setAttribute('aria-label', `Ampliar ${item.alt} (abre em nova aba)`);
  const img = document.createElement('img'); img.src = item.src; img.alt = item.alt; img.loading = 'lazy';
  if (item.width && item.height) { img.width = item.width; img.height = item.height; }
  const caption = document.createElement('figcaption'); caption.textContent = item.alt;
  link.append(img); figure.append(link, caption); previews.append(figure);
});
document.getElementById('preview-section').hidden = !previews.children.length;
const chapters = product.chapterGroups.flatMap(group => group.chapters);
const numbers = chapters.map(chapter => chapter.number).sort((a,b) => a-b);
const completeChapters = chapters.length === 12 && numbers.every((number,index) => number === index+1)
  && chapters.every(chapter => typeof chapter.title === 'string' && chapter.title.trim());
if (completeChapters) {
  const groups = document.getElementById('chapter-groups');
  product.chapterGroups.forEach(group => {
    const section = document.createElement('section'); section.className = 'chapter-group';
    const heading = document.createElement('h4'); heading.textContent = group.title;
    const list = document.createElement('ul');
    group.chapters.forEach(chapter => {
      const row = document.createElement('li');
      const number = document.createElement('span'); number.textContent = String(chapter.number).padStart(2,'0');
      row.append(number, document.createTextNode(chapter.title)); list.append(row);
    });
    section.append(heading,list); groups.append(section);
  });
  document.getElementById('chapters').hidden = false;
  document.getElementById('chapter-note').hidden = true;
  document.getElementById('faq-content-description').textContent = 'O material apresenta uma introdução à Indústria 4.0 e às relações entre máquinas, pessoas, processos e dados. Confira os 12 capítulos no sumário desta página.';
}
if (product.author.trim()) {
  const author = document.getElementById('author'); author.textContent = `Autoria: ${product.author}`; author.hidden = false;
}
if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(product.contactEmail)) {
  const contact = document.getElementById('contact'); contact.href = `mailto:${product.contactEmail}`;
  contact.textContent = 'Contato'; contact.hidden = false;
}
const institutions = document.getElementById('institutional');
product.institutionalLinks.forEach(item => {
  const url = httpsUrl(item.url); if (!url) return;
  const link = document.createElement('a'); link.href = url; link.textContent = item.label; institutions.append(link);
});
institutions.hidden = !institutions.children.length;
