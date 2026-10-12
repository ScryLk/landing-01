# Afinal, vale a pena estudar Inteligência Artificial?

Landing page independente da Dobraverse / Coleção Afinal, volume 03. HTML, CSS e JavaScript nativos; identidade grafite e prata, capa oficial e três prévias reais extraídas do PDF fornecido. O PDF completo permanece fora do diretório público. Não há backend, formulário, checkout interno ou dependência de produção.

## Executar e gerar o site

Na raiz do monorepo, com Node.js 22 ou superior e a versão de pnpm indicada em `package.json`:

```sh
pnpm install --frozen-lockfile
pnpm dev:ia
pnpm --filter @dobraverse/inteligencia-artificial check
pnpm build:ia
```

O servidor de desenvolvimento usa a porta **8102**, em `http://localhost:8102/`, e recompila os arquivos ao editar. O build independente gera `apps/inteligencia-artificial/dist/`. Dentro deste app, `pnpm dev`, `pnpm check` e `pnpm build` também funcionam após a instalação do workspace.

O build incorpora `packages/ui/commerce.js` e as primitivas CSS compartilhadas. Sirva o `dist/`, não o código-fonte isolado. Publique somente esse diretório, mantendo Git, ferramentas, README, testes, credenciais e PDF fora da raiz pública. Na VPS, mantenha releases independentes para cada produto e siga `../../docs/deploy.md`.

## Configuração pública e comercial

Edite apenas o `config.js` deste app; os dados dos outros produtos continuam independentes.

| Campo | Finalidade |
| --- | --- |
| `PRODUCT_NAME` | Nome completo do e-book. |
| `CHECKOUT_URL` | URL real do checkout externo da Kiwify. |
| `PRODUCT_PRICE` | Preço confirmado, já formatado para exibição, por exemplo em reais. |
| `PRODUCT_COVER` | Caminho local da capa oficial, atualmente `assets/capa.webp`. |
| `subtitle` | Subtítulo editorial. |
| `author`, `contactEmail` | Autoria e contato público, exibidos apenas quando preenchidos. |
| `previewImages` | Páginas reais: `{ src, alt, caption, width, height }`. |
| `institutionalLinks` | Links confirmados de privacidade e termos: `{ label, url }`. |
| `previousVolumeUrl` | URL real do volume de Indústria 4.0, quando publicada. |
| `inheritUtm` | Encaminhamento opcional de UTMs para o checkout. |

As quatro constantes alimentam `window.IA_CONFIG` nos campos `productName`, `checkoutUrl`, `price` e `cover`. Todos esses dados são públicos; nunca inclua senhas, tokens ou informações privadas.

O checkout aceita apenas URLs HTTPS sem credenciais em domínios Kiwify aprovados (`kiwify.com.br`, `kiwify.com`, `kiwify.app` e seus subdomínios). O placeholder `INSERIR_URL_KIWIFY` deixa todos os botões comerciais indisponíveis, com estado acessível e explicação visível. Sem JavaScript, os botões também permanecem indisponíveis; o conteúdo editorial continua legível.

`INSERIR_PRECO` e preço vazio mostram **Valor a confirmar**, nunca o texto do placeholder. Não há preço, desconto, prazo, garantia ou promessa de entrega presumidos. Autoria, contato e links institucionais ausentes ficam ocultos. Links institucionais e do volume anterior exigem HTTPS.

As imagens de produto aceitam apenas caminhos locais de `assets/`. As prévias atuais são o capítulo de prompt engineering, a ferramenta A (motivo para estudar IA) e a ferramenta D (comparador de formações). Mantenha `width`/`height` correspondentes às imagens para preservar a proporção e reservar espaço durante o carregamento. Não substitua conteúdo real por páginas simuladas.

## Domínio e SEO

`site.json` contém os metadados próprios deste volume. Mantenha seu título e descrição alinhados ao `index.html`. O build inclui Open Graph e Twitter Cards, com arte social oficial de 1200 × 630 px quando configurada.

Antes da publicação, defina `SITE_URL` com a URL HTTPS real e completa da landing page, incluindo a subpasta quando aplicável:

```sh
# Exemplo ilustrativo: substitua pelo domínio confirmado.
SITE_URL=https://seu-dominio.example/inteligencia-artificial/ pnpm build:ia
```

Com a URL real, o build gera canonical, `og:url`, imagem social absoluta, `robots.txt` e `sitemap.xml` deste produto. Sem `SITE_URL`, não inventa domínio, canonical ou URLs públicas. Em hospedagem por subpasta, o `robots.txt` do app não substitui o arquivo da raiz do domínio; inclua a referência do sitemap na configuração de SEO do domínio, quando aplicável.

Na VPS, configure a rota com barra final, por exemplo `/inteligencia-artificial/`, para que os caminhos relativos de CSS, JavaScript e assets funcionem. Não é necessário fallback de SPA. Sirva HTTPS e use cache com revalidação para HTML, `config.js` e assets sem nomes versionados.

## UTMs e mensuração futura

Com `inheritUtm: true`, apenas `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` e `utm_term` recebidos pela página são acrescentados ao checkout. Valores vazios, com controles ou com mais de 200 caracteres são ignorados. Parâmetros já existentes na URL do checkout são preservados; nenhum outro parâmetro da página é encaminhado.

O site não faz requisições de analytics e não grava cookies ou armazenamento local. O clique em um botão habilitado emite o evento local `dobraverse:checkout-click` no `document`, com `detail: { product: 'inteligencia-artificial', placement }`. O atributo opcional `data-placement` do botão identifica a posição usando até 40 caracteres alfanuméricos, hífen ou sublinhado; na ausência, usa `checkout`.

Esse evento indica somente um clique. Não indica compra, não declara conversão e não inclui e-mail, endereço de checkout completo ou parâmetros recebidos. Uma integração futura com Meta Pixel ou analytics exige IDs reais, configurações adequadas de privacidade/consentimento e validação da compra na Kiwify.

## Pendências antes da divulgação comercial

- Configurar a URL real de checkout e o preço confirmado.
- Confirmar autoria, contato e links institucionais aplicáveis.
- Confirmar as condições reais de entrega, acesso e reembolso na Kiwify; ajustar o FAQ com essas informações quando aprovadas.
- Definir domínio/rota finais e gerar novamente com `SITE_URL`.
- Validar HTTPS, metadados sociais, imagens, teclado, FAQ, navegação mobile e todos os botões no endereço público.

Não há publicação na VPS nem configuração de rastreadores executadas por este app. Build local e configuração comercial são etapas distintas da validação pública.

## Validação realizada

O build individual, as verificações de sintaxe/estrutura e os testes automatizados de build/isolamento/SEO passaram. Chromium verificou 320, 390, 768 e 1440 pixels, imagens e proporções, 12 capítulos, sete ferramentas, prévias reais, FAQ, teclado/foco, movimento reduzido e CTAs. As configurações temporárias de checkout verificaram UTMs e evento local de clique sem salvar preços ou URLs de teste.

Em uma visita inicial local no Chromium, viewport de 390 pixels, HTML e recursos totalizaram aproximadamente 127 KB antes do carregamento das prévias sob demanda; não houve requisições a terceiros nem cookies/storage. Isso é uma medição local, não uma auditoria Lighthouse nem uma garantia de tempo de carregamento em produção. Não existe TypeScript ou linter de estilo configurado: `pnpm check` verifica sintaxe JavaScript, JSON e estrutura HTML básica.

A publicação no domínio final, HTTPS e validação real do checkout ainda dependem da configuração de produção.

A suíte completa de navegador identificou um defeito preexistente em Indústria 4.0, introduzido no commit `029fea0`: um SVG decorativo produz 10 pixels de overflow em 320/390 pixels. Os arquivos dessa aplicação foram preservados; a falha não afeta a IA. Para executar especificamente a validação desta entrega, use `BROWSER_APPS=ia CHROMIUM_PATH=/usr/bin/chromium pnpm test:browser`. Esse filtro não remove a asserção nem mascara o resultado da suíte completa.
