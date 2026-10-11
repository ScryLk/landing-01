# Adicionar outro e-book

1. Crie `apps/<slug>/` com `index.html`, `styles.css`, `app.js`, `config.js`, `assets/`, `site.json` e `package.json`.
2. Use um nome de pacote único, como `@dobraverse/<slug>`. Declare `@dobraverse/config: workspace:*` nas dependências de desenvolvimento. Declare `@dobraverse/ui: workspace:*` apenas se usar suas primitivas.
3. Defina os scripts `build: dobraverse-build`, `check: dobraverse-check`, `dev: dobraverse-serve --watch --port <porta>` e `preview: dobraverse-serve --port <porta>`.
4. Em `site.json`, informe `title`, `description`, `image` e `sharedUi`. Com `sharedUi: true`, o build concatena as primitivas CSS antes do CSS do app e copia `commerce.js` para `shared/commerce.js` na saída.
5. Configure uma identidade própria e conteúdo confirmado. Dados comerciais permanecem no `config.js` daquele app. Não copie preços, links ou autoria de outro produto.
6. Use imagens reais e otimizadas em `assets/`. Não coloque o PDF completo no diretório de publicação.
7. Atualize o lockfile com `pnpm install`, verifique a aplicação e gere `pnpm --filter @dobraverse/<slug> build`.
8. Configure um deploy/URL próprios apontando apenas para `apps/<slug>/dist`.

Para o checkout compartilhado, importe `bindCheckout` de `./shared/commerce.js` no código do app e forneça explicitamente URL, hosts permitidos, ID do status e mensagens da plataforma. O módulo não contém dados de nenhum livro.

Para manter a autonomia, nunca importe `apps/outro-produto/*`. Apenas os pacotes compartilhados podem ser dependências. O código publicado é autocontido: não aponta para `packages/` nem depende de outro site em execução.

Não há gerador de sites, CMS ou páginas futuras neste repositório. Copie somente a estrutura técnica e crie o conteúdo e a identidade de cada novo produto.
