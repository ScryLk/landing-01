# Dobraverse · Landing pages

Monorepo estático para produtos digitais independentes. HTML, CSS e JavaScript nativos; sem backend, banco de dados, autenticação ou pagamento interno.

## Estrutura

```text
apps/
  experiencia-tecnologia/   # Primeira página, preservada
  industria-40/            # Coleção Afinal, identidade laranja
packages/
  config/                  # Build, verificação e servidor de desenvolvimento
  ui/                      # Primitivas CSS e ligação de checkout neutras
docs/
  deploy.md
  novos-produtos.md
tests/
```

Cada app possui seu próprio `config.js`, `site.json`, HTML, CSS, JavaScript e assets. `packages/ui` não possui dados comerciais. O primeiro app mantém sua implementação original e não depende das primitivas visuais novas. O segundo utiliza as primitivas; o build copia o módulo compartilhado para sua própria saída. Nenhum app importa outro app.

## Ferramentas

Node.js 22 ou superior e pnpm 11.19.0, indicado em `packageManager`. Use a versão fixada via Corepack, se disponível, ou a instalação oficial do pnpm. O workspace não baixa bibliotecas de produção: as dependências são links locais.

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm test
pnpm build:experiencia
pnpm build:industria
```

Cada comando individual gera **somente** o `dist/` da aplicação selecionada. `pnpm build` gera ambos. Não há validação de credenciais, checkout ou assets de outro produto durante um build individual.

```sh
pnpm dev:experiencia  # Porta 8100, recompila alterações
pnpm dev:industria   # Porta 8101, recompila alterações
# Porta alternativa:
pnpm --filter @dobraverse/industria-40 dev --port 8201
```

Os servidores locais servem apenas `dist/`, sem listagem de diretórios. Reinicie o processo ao modificar as ferramentas de servidor/build. A página precisa ser recarregada para ver as mudanças; não há hot reload.

### Testes no navegador

`pnpm test:browser` é um runner opcional que exige Playwright e Chromium instalados no ambiente de testes. Eles não são dependências das landing pages. Pode-se provisionar Playwright fora do checkout e informar `PLAYWRIGHT_MODULE_PATH` com o caminho absoluto do módulo. Use `CHROMIUM_PATH` para um Chromium já instalado. Na ausência desse caminho, o runner usa o navegador gerenciado por Playwright.

```sh
CHROMIUM_PATH=/usr/bin/chromium pnpm test:browser
```

Opcionalmente use `SCREENSHOT_DIR` para salvar screenshots fora do repositório. O runner inicia e encerra seus próprios servidores em portas disponíveis. Verifica 320, 390, 768 e 1440 pixels, imagens, FAQ, isolamento comercial, checkout, configuração de capa/prévias/sumário e movimento reduzido. Os dados de teste são temporários e não são salvos nos produtos.

## Produtos e pendências

### Experiência à Tecnologia

Código e assets originais em `apps/experiencia-tecnologia`. Checkout, preço, autoria e contato mantidos exatamente como estavam. Consulte o README do app para a configuração.

### Afinal, o que é Indústria 4.0?

Configuração independente em `apps/industria-40/config.js`. Checkout exclusivo da Kiwify, sem links inventados. Preço e informações não fornecidas permanecem em branco. Os links comerciais são indisponíveis enquanto faltar um checkout HTTPS válido da Kiwify.

**Materiais ainda não fornecidos:** capa oficial laranja e imagens reais de páginas internas. Os 12 títulos de capítulos foram fornecidos pelo usuário e estão organizados em quatro grupos temáticos. A composição tipográfica está claramente identificada como editorial, não como capa oficial. Nenhuma página interna ou capítulo foi inventado. Preencha `cover` e `previewImages` com os materiais reais. O sumário só aparece quando existem 12 números únicos, de 1 a 12, com títulos preenchidos. Confirme o formato do arquivo antes da publicação. A página não deve ser anunciada como comercialmente finalizada antes dessas confirmações.

Para Open Graph com imagem, preencha `image` em `site.json` com o caminho da capa oficial. Antes da publicação, informe `SITE_URL` no build para produzir URL canônica, `og:url` e imagem absoluta. Domínios não são presumidos.

## Compatibilidade com a primeira publicação

Os arquivos estáticos originais na raiz continuam **sem alterações**, como uma entrada de compatibilidade durante a migração. Eles não são a fonte para novos produtos. As fontes ativas passam a ser `apps/`. Não há redirecionamento da página original nem alteração de links comerciais.

Um deploy já configurado para publicar arquivos estáticos da raiz pode continuar usando esses arquivos. Contudo, a presença de `package.json` pode mudar a detecção automática de alguns provedores: confirme os parâmetros do deploy existente antes de ativar a nova configuração. Não removemos a entrada legada e não modificamos nenhum domínio ou servidor remoto. Ao migrar o deploy, publique o `dist/` correspondente, preservando o domínio e o checkout.

Os testes de migração comparam a primeira aplicação com os arquivos legados byte a byte. Depois de migrar o deploy, a remoção da compatibilidade deve ser uma etapa explícita. Enquanto ela existir, mudanças intencionais no primeiro app exigem atualizar também essa entrada ou ajustar os testes/documentar a decisão.

## Decisões de arquitetura

- pnpm Workspaces para tarefas e dependências locais.
- Sem mudança de framework: o projeto original não usa framework.
- Sem Turborepo: dois builds que apenas copiam arquivos não precisam de cache ou grafo adicional. Pode ser adotado se as tarefas crescerem.
- Sem conversão para TypeScript: o código original e as páginas continuam JavaScript nativo. TypeScript pode entrar em ferramentas ou componentes que realmente o exijam.
- `.editorconfig` compartilha convenções de formatação. `pnpm check` valida sintaxe JavaScript, JSON e estrutura HTML básica; não é um linter de estilo completo.
- Compartilhamento limitado a layout/interação acessível e infraestrutura. Não há CMS, catálogo automático ou novos volumes implementados.

Veja [deploy individual](docs/deploy.md) e [como adicionar um produto](docs/novos-produtos.md).
