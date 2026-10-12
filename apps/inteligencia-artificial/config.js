// Dados públicos deste produto. Nunca coloque senhas, tokens ou informações privadas aqui.
const PRODUCT_NAME = 'Afinal, vale a pena estudar Inteligência Artificial?';
const CHECKOUT_URL = 'INSERIR_URL_KIWIFY';
const PRODUCT_PRICE = 'R$ 29,00';
const ORIGINAL_PRICE = 'R$ 58,00';
const PRODUCT_COVER = 'assets/capa.webp';

window.IA_CONFIG = Object.freeze({
  productName: PRODUCT_NAME,
  subtitle: 'Uma reflexão sobre inteligência artificial, formação acadêmica e as decisões que tomamos diante de um futuro em transformação.',
  checkoutUrl: CHECKOUT_URL,
  price: PRODUCT_PRICE,
  originalPrice: ORIGINAL_PRICE,
  discountBadge: '50% OFF',
  cover: PRODUCT_COVER,
  author: '', // Preencher somente com a autoria confirmada.
  contactEmail: '', // E-mail público confirmado, sem dados de acesso.
  // Páginas reais extraídas do PDF fornecido, com proporções preservadas.
  previewImages: [
    {
      src: 'assets/previa-prompt.webp',
      alt: 'Abertura real do capítulo 5, O caso do prompt engineering, com título e grafismos de engrenagens.',
      caption: 'Capítulo 5 · O caso do prompt engineering',
      width: 960,
      height: 1242
    },
    {
      src: 'assets/previa-caderno.webp',
      alt: 'Página real do caderno prático, ferramenta A: Meu motivo para estudar IA.',
      caption: 'Ferramenta A · Meu motivo para estudar IA',
      width: 960,
      height: 1358
    },
    {
      src: 'assets/previa-formacoes.webp',
      alt: 'Página real do caderno prático, ferramenta D: Comparador de formações.',
      caption: 'Ferramenta D · Comparador de formações',
      width: 960,
      height: 1358
    }
  ],
  institutionalLinks: [], // Links reais de privacidade/termos: [{ label, url }], somente HTTPS.
  previousVolumeUrl: 'https://industria.dobraverse.io/', // URL real de “Afinal, o que é Indústria 4.0?”
  inheritUtm: true // Encaminha apenas os cinco parâmetros UTM documentados, sem rastreador.
});
