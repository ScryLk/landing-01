# Deploy independente

Publique apenas o `dist/` de cada aplicação. O repositório, `node_modules`, ferramentas, README, testes e PDFs completos ficam fora do diretório público.

| Aplicação | Diretório do app | Comando na raiz | Saída relativa à raiz |
| --- | --- | --- | --- |
| Portal Dobraverse (Apex) | `apps/portal` | `pnpm build:portal` | `apps/portal/dist` |
| Experiência à Tecnologia | `apps/experiencia-tecnologia` | `pnpm build:experiencia` | `apps/experiencia-tecnologia/dist` |
| Indústria 4.0 | `apps/industria-40` | `pnpm build:industria` | `apps/industria-40/dist` |
| Inteligência Artificial | `apps/inteligencia-artificial` | `pnpm build:ia` | `apps/inteligencia-artificial/dist` |

Instalação: `pnpm install --frozen-lockfile`. Não há dependências npm de produção. O workspace tem apenas links locais. Se o ambiente não permitir o diretório de dados padrão do pnpm, configure `XDG_DATA_HOME`/`XDG_CACHE_HOME` em caminhos graváveis e `--store-dir` local, sem mudar as dependências ou o lockfile.

## Metadados por domínio

Informe a URL real do produto ao executar seu build. Exemplo **ilustrativo**, não um domínio publicado:

```sh
SITE_URL=https://seu-dominio.example/experiencia-tecnologia/ pnpm build:experiencia
SITE_URL=https://outro-dominio.example/ pnpm build:industria
SITE_URL=https://seu-dominio.example/inteligencia-artificial/ pnpm build:ia
```

Sem `SITE_URL`, o build inclui título, descrição e locale Open Graph, mas não inventa canonical, URL pública ou imagem absoluta. Os metadados vêm de `site.json` de cada app. Mantenha título/descrição de `index.html` e `site.json` alinhados. `config.js` controla dados comerciais, não o domínio de hospedagem.

## VPS

Não foi realizado deploy na VPS nesta tarefa. O repositório contém `OPERACAO.md`, `deploy-ebook.sh` e `setup-domain-ssl.sh` de uma configuração anterior; foram preservados. Não há acesso SSH validado nesta tarefa, e o domínio do produto de IA ainda precisa ser confirmado.

1. Mantenha o checkout Git fora do diretório público.
2. Instale os workspaces e execute apenas o build do produto desejado.
3. Copie seu `dist/` para um diretório de release exclusivo do produto.
4. Valide arquivos e configuração do servidor web.
5. Troque a release ativa de forma atômica e mantenha a anterior para rollback.
6. Preserve domínios, regras, sites e certificados existentes.

Use o Nginx/Caddy existente. Não instale um segundo servidor disputando portas. Não exponha o checkout inteiro. Não execute o servidor de desenvolvimento em produção.

Para subpastas, configure uma regra dedicada, com remoção do prefixo ao resolver os arquivos, e redirecione a URL sem barra final para a URL com barra final. Todos os assets das páginas são relativos. Não use fallback de SPA.

Exemplo de **trecho** Caddy para incorporar a uma configuração existente, após adaptar a pasta real:

```caddyfile
redir /industria-40 /industria-40/ 308
handle_path /industria-40/* {
    root * /var/www/ebooks/industria-40/current
    file_server
}
```

Não substitua o bloco inteiro do domínio por esse trecho. Configure compressão quando suportada e HTTPS conforme a infraestrutura existente. Use cache com revalidação para HTML, `config.js` e assets sem nomes versionados.

Se a configuração comercial for mantida fora do Git na VPS, aplique o `config.js` aprovado na **nova release, antes** de trocar o link ativo. Não sobrescreva o código-fonte com segredos, não exponha PDFs e não copie dados de um produto para outro. Alternativamente, mantenha configurações comerciais públicas confirmadas no `config.js` do respectivo app e revise cada atualização.

## Vercel ou hospedagem estática equivalente

Configure um projeto de deploy por app, ligado ao mesmo repositório. Não remova projetos/domínios existentes.

Opção recomendada para este monorepo: diretório raiz do projeto de deploy = raiz do repositório; preset `Other`; instalação `pnpm install --frozen-lockfile`; build e saída conforme a tabela. Configure `SITE_URL` individualmente em cada projeto.

Se o provedor trabalhar com raiz do app, use `apps/<produto>`, instalação na raiz do workspace, build `pnpm build` dentro do app e saída `dist`. Habilite a inclusão de arquivos fora da raiz do app para acessar `packages/config` e, nos produtos da Coleção Afinal, `packages/ui`. Não faça um checkout isolado do app sem os pacotes compartilhados.

Para um deploy antigo que servia a raiz sem build, revise essas configurações antes de migrar. A entrada legada continua no Git para manter a compatibilidade; a remoção futura é uma etapa separada.

## Checklist de publicação

- Confirmar checkout e preço; nunca colocar valores fictícios.
- Confirmar autoria, contato, direitos dos assets e links institucionais aplicáveis.
- No novo e-book, inserir a capa oficial e prévias disponíveis; os 12 títulos do sumário já estão confirmados.
- Confirmar formato do arquivo e procedimentos de entrega na Kiwify.
- Executar check, testes relevantes e build individual.
- Validar HTTPS, URL com barra final, imagens, scripts e links no domínio real.
- Validar mobile, teclado e FAQ.
- Confirmar que os outros produtos e sites continuam funcionando.

Atualização e rollback devem usar releases separadas por produto. Não há webhook, GitHub Actions ou automação de produção configurada nesta tarefa.

## SEO e campanhas do volume de IA

O app de IA declara a composição oficial `assets/og-ia.png` (1200×630) e `seoFiles: true`. Com `SITE_URL` HTTPS confirmado, publica robots/sitemap e tags OG/Twitter com URLs absolutas. Se o produto estiver em uma subpasta, o robots.txt dessa subpasta não substitui o robots da raiz do domínio; inclua a referência do sitemap do produto no arquivo do domínio existente. Não sobrescreva a política de outros sites.

UTMs podem acompanhar o visitante até o checkout. Não há Meta Pixel, IDs fictícios, cookies, armazenamento local ou analytics instalados. A venda acontece na Kiwify; um evento de clique não representa uma compra. Configure mensuração futura somente com valores reais e privacidade adequada.

Para configurar este produto, consulte `apps/inteligencia-artificial/README.md`. Capa, prévias, capítulos e caderno foram conferidos no PDF. Permanecem pendentes checkout, preço, autoria pessoal, contato público, políticas comerciais e domínio de publicação. Nenhum servidor ou domínio foi alterado durante a implementação.

### Script de deploy já existente

`deploy-ebook.sh` já aceita novos slugs pelo caso genérico e encontra `apps/inteligencia-artificial`, com build via filtro do pnpm. Entretanto, esse caso pressupõe o subdomínio `<slug>.dobraverse.io`; isso não confirma DNS ou hospedagem do novo volume. Antes de executá-lo na VPS, confirme o domínio desejado e a configuração `SITE_URL` do script. Alternativamente, gere o build com `SITE_URL` explícito e publique seu `dist/` usando o processo de releases existente.

A configuração comercial persistente desse slug será `/var/www/ebooks/shared/inteligencia-artificial/config.js`, conforme o script existente. Não execute `setup-domain-ssl.sh` com os parâmetros padrão de outro produto. Nenhum desses scripts foi executado nesta tarefa.
