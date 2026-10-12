# Dobraverse · Landing pages

Monorepo estático para produtos digitais independentes. HTML, CSS e JavaScript nativos; sem backend, banco de dados, autenticação ou pagamento interno.

## Estrutura

```text
apps/
  experiencia-tecnologia/   # Primeira página, preservada
  industria-40/            # Coleção Afinal, identidade laranja
  inteligencia-artificial/ # Volume 03, grafite e prata, capa real
packages/
  config/                  # Build, verificação e servidor de desenvolvimento
  ui/                      # Primitivas CSS e ligação de checkout neutras
docs/
  deploy.md
  novos-produtos.md
tests/
```

Cada app possui seu próprio `config.js`, `site.json`, HTML, CSS, JavaScript e assets. `packages/ui` não possui dados comerciais. O primeiro app mantém sua implementação original e não depende das primitivas visuais novas. Os apps da Coleção Afinal utilizam as primitivas; o build copia o módulo compartilhado para sua própria saída. Nenhum app importa outro app.

## Ferramentas

Node.js 22 ou superior e pnpm 11.19.0, indicado em `packageManager`. Use a versão fixada via Corepack, se disponível, ou a instalação oficial do pnpm. O workspace não baixa bibliotecas de produção: as dependências são links locais.

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm test
pnpm build:experiencia
pnpm build:industria
pnpm build:ia
```

Cada comando individual gera **somente** o `dist/` da aplicação selecionada. `pnpm build` gera os três. Não há validação de credenciais, checkout ou assets de outro produto durante um build individual.

```sh
pnpm dev:experiencia  # Porta 8100, recompila alterações
pnpm dev:industria   # Porta 8101, recompila alterações
pnpm dev:ia          # Porta 8102, recompila alterações
# Porta alternativa:
pnpm --filter @dobraverse/industria-40 dev --port 8201
```

Os servidores locais servem apenas `dist/`, sem listagem de diretórios. Reinicie o processo ao modificar as ferramentas de servidor/build. A página precisa ser recarregada para ver as mudanças; não há hot reload.

### Testes no navegador

`pnpm test:browser` é um runner opcional que exige Playwright e Chromium instalados no ambiente de testes. Eles não são dependências das landing pages. Pode-se provisionar Playwright fora do checkout e informar `PLAYWRIGHT_MODULE_PATH` com o caminho absoluto do módulo. Use `CHROMIUM_PATH` para um Chromium já instalado. Na ausência desse caminho, o runner usa o navegador gerenciado por Playwright.

```sh
CHROMIUM_PATH=/usr/bin/chromium pnpm test:browser
# Somente a nova aplicação de IA:
BROWSER_APPS=ia CHROMIUM_PATH=/usr/bin/chromium pnpm test:browser
```

Opcionalmente use `SCREENSHOT_DIR` para salvar screenshots fora do repositório. O filtro `BROWSER_APPS` aceita `experiencia`, `industria` e `ia`, separados por vírgula; sem filtro, verifica todos. O runner inicia e encerra seus próprios servidores em portas disponíveis. Verifica 320, 390, 768 e 1440 pixels, imagens, FAQ, isolamento comercial, checkout, configuração de capa/prévias/sumário, UTMs da IA e movimento reduzido. Os dados de teste são temporários e não são salvos nos produtos.

## Produtos e pendências

### Experiência à Tecnologia

Código e assets originais em `apps/experiencia-tecnologia`. Checkout, preço, autoria e contato mantidos exatamente como estavam. Consulte o README do app para a configuração.

### Afinal, o que é Indústria 4.0?

Configuração independente em `apps/industria-40/config.js`. As atualizações recentes do próprio repositório adicionaram a capa oficial, quatro prévias, banners, kit criativo e uma oferta configurada. Esses arquivos e dados comerciais foram preservados nesta entrega. Os 12 capítulos continuam organizados em quatro grupos temáticos. Consulte a configuração desse produto antes de publicar; o checkout ainda possui placeholder.

A suíte completa detecta um problema anterior à app IA: o SVG `.hero-arcs-bg` ultrapassa a borda em 10 pixels nas telas de 320 e 390 pixels. A regra vem do commit `029fea0`; esta entrega não modifica a página anterior.

Para Open Graph com imagem, preencha `image` em `site.json` com o caminho da capa oficial. Antes da publicação, informe `SITE_URL` no build para produzir URL canônica, `og:url` e imagem absoluta. Domínios não são presumidos.

### Afinal, vale a pena estudar Inteligência Artificial?

Volume 03, integrado em `apps/inteligencia-artificial`, com identidade grafite/prata. Usa a capa original extraída do PDF, três prévias reais, os 12 capítulos confirmados e sete ferramentas práticas. O PDF completo permanece fora da pasta pública. O briefing e o PDF confirmam os personagens fictícios e o caráter reflexivo do conteúdo.

`config.js` centraliza nome, checkout Kiwify, preço, capa, autoria, contato e links. Checkout e preço permanecem com placeholders; compra desativada acessivelmente até configurar a URL real. Não há backend nem rastreadores. UTMs são encaminhadas por uma lista restrita, de modo opcional; evento local de clique não é compra.

A arte Open Graph está em `assets/og-ia.png`, 1200×630. Este app declara `socialImage` e `seoFiles` em `site.json`: com `SITE_URL` real, o build gera canonical, OG/Twitter completos, robots e sitemap. Sem domínio, não inventa URLs. As extensões de SEO são opcionais e não mudam os metadados dos apps anteriores. Veja o README específico para configuração e pendências.

## Compatibilidade com a primeira publicação

Os arquivos estáticos originais na raiz continuam **sem alterações**, como uma entrada de compatibilidade durante a migração. Eles não são a fonte para novos produtos. As fontes ativas passam a ser `apps/`. Não há redirecionamento da página original nem alteração de links comerciais.

Um deploy já configurado para publicar arquivos estáticos da raiz pode continuar usando esses arquivos. Contudo, a presença de `package.json` pode mudar a detecção automática de alguns provedores: confirme os parâmetros do deploy existente antes de ativar a nova configuração. Não removemos a entrada legada e não modificamos nenhum domínio ou servidor remoto. Ao migrar o deploy, publique o `dist/` correspondente, preservando o domínio e o checkout.

Os testes de migração comparam a primeira aplicação com os arquivos legados byte a byte. Depois de migrar o deploy, a remoção da compatibilidade deve ser uma etapa explícita. Enquanto ela existir, mudanças intencionais no primeiro app exigem atualizar também essa entrada ou ajustar os testes/documentar a decisão.

## Decisões de arquitetura

- pnpm Workspaces para tarefas e dependências locais.
- Sem mudança de framework: o projeto original não usa framework.
- Sem Turborepo: três builds que apenas copiam arquivos não precisam de cache ou grafo adicional. Pode ser adotado se as tarefas crescerem.
- Sem conversão para TypeScript: o código original e as páginas continuam JavaScript nativo. TypeScript pode entrar em ferramentas ou componentes que realmente o exijam.
- `.editorconfig` compartilha convenções de formatação. `pnpm check` valida sintaxe JavaScript, JSON e estrutura HTML básica; não é um linter de estilo completo.
- Compartilhamento limitado a layout/interação acessível e infraestrutura. Não há CMS, catálogo automático ou novos volumes implementados.

Veja [deploy individual](docs/deploy.md) e [como adicionar um produto](docs/novos-produtos.md).
