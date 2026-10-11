# Afinal, o que é Indústria 4.0?

Landing page independente da Coleção Afinal. Paleta laranja, preto e off-white; HTML/CSS/JS nativos, com primitivas compartilhadas no build. Fontes equivalentes locais evitam dependências de rede.

Na raiz do monorepo:

```sh
pnpm install --frozen-lockfile
pnpm --filter @dobraverse/industria-40 dev
pnpm --filter @dobraverse/industria-40 check
pnpm --filter @dobraverse/industria-40 build
```

Saída: `apps/industria-40/dist/`. Dentro deste app, `pnpm build` e `pnpm dev` também funcionam após instalar o workspace. Servir o fonte diretamente não é o workflow: o módulo UI e as primitivas CSS são incorporados no `dist/`.

## Editáveis

`config.js` controla exclusivamente este produto. `checkoutUrl` aceita apenas HTTPS em domínios Kiwify aprovados; o placeholder desativa a compra. `price`, `author` e `contactEmail` ficam vazios até serem confirmados. Links institucionais só aceitam HTTPS.

A capa oficial laranja e o PDF deste livro não foram fornecidos nesta conversa. A arte tipográfica é identificada como composição editorial. Não há páginas internas simuladas. Para inserir a capa, salve uma imagem otimizada em `assets/` e preencha `cover`. Depois preencha também `image` em `site.json` para Open Graph. Preencha `previewImages` apenas com páginas reais.

Os títulos dos 12 capítulos foram confirmados pelo usuário e inseridos em quatro grupos temáticos. `chapterGroups` aceita grupos com `{ title, chapters: [{ number, title }] }`. Para mostrar o sumário, forneça os 12 capítulos confirmados, numerados de 1 a 12, sem repetição. Os nomes dos capítulos seguem os títulos fornecidos; os grupos são uma organização editorial da página.

A oferta mostra a capa assim que seu arquivo oficial for configurado e carregado. O formato e as condições de acesso devem ser confirmados na Kiwify antes da publicação comercial. Não há políticas de garantia, prazo ou entrega presumidas.

Informe `SITE_URL` com o domínio real ao gerar o build. Veja `../../docs/deploy.md`.
