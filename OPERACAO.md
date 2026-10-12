# Manual de Operação e Governança: Landing Pages de E-books

Este documento centraliza as instruções operacionais para manutenção, atualização, rollback e expansão da infraestrutura de hospedagem de e-books na VPS.

---

## 1. Arquitetura da Infraestrutura

- **Servidor Web:** Nginx (contêiner Docker `catana_web` gerenciado pelo Docker Compose em `/var/www/catana`).
- **Camada HTTPS/TLS:** Let's Encrypt gerenciado pelo contêiner `catana_certbot` com renovação automática.
- **Portas:** 80 (HTTP com redirect 301 para HTTPS) e 443 (HTTPS com HTTP/2, SSL moderno e compressão Gzip).
- **Diretório de Fontes Git (privado):** `/srv/ebook-sources/`
- **Diretório Público Web:** `/var/www/ebooks/`
- **Políticas de Cache:**
  - `index.html` e `config.js`: `Cache-Control: no-cache, must-revalidate` (sempre revalidado).
  - Assets visuais (`.css`, `.js`, `.webp`, `.svg`): `Cache-Control: public, max-age=604800, must-revalidate`.
  - Arquivos sensíveis (`.git`, `.env`, `README.md`): Bloqueados com HTTP 404.
  - Listagem de diretórios (`autoindex`): Desativada (`off`).

---

## 2. Estrutura de Arquivos e Isolamento

```
/srv/ebook-sources/
├── landing-01/                  # Clone da branch main do Git (fora do acesso web)
├── deploy-ebook.sh              # Script unificado de deploy, rollback e status
└── OPERACAO.md                  # Este manual operacional

/var/www/ebooks/
├── shared/
│   └── experiencia-tecnologia/
│       └── config.js            # Configuração comercial persistente de produção
├── releases/
│   └── experiencia-tecnologia/
│       ├── 20261009_105919/     # Versões imutáveis anteriores
│       └── 20261009_110547/     # Versão em produção
└── experiencia-tecnologia -> releases/experiencia-tecnologia/20261009_110547
```

---

## 3. Comandos do Script de Publicação (`deploy-ebook.sh`)

O script `/srv/ebook-sources/deploy-ebook.sh` garante:
- Atualização limpa via `git fetch && git merge --ff-only` (sem `git reset --hard`).
- Validação de integridade e sintaxe JavaScript.
- Criação de pasta isolada contendo apenas arquivos permitidos (sem `.git`, `.env` ou `README.md`).
- Preservação das configurações de produção salvas em `shared/<slug>/config.js`.
- Troca atômica do symlink via `rename` no Linux (zero downtime).
- Retenção das últimas 5 versões para rollback instantâneo.

### Ver status da versão ativa:
```bash
/srv/ebook-sources/deploy-ebook.sh status experiencia-tecnologia
```

### Publicar nova versão:
```bash
/srv/ebook-sources/deploy-ebook.sh deploy experiencia-tecnologia
```

### Reverter para a versão anterior (Rollback):
```bash
/srv/ebook-sources/deploy-ebook.sh rollback experiencia-tecnologia
```

---

## 4. Como Alterar o Link de Checkout e Informações Comerciais

Para configurar o link de compra (Kiwify, Hotmart, etc.) ou atualizar preço, autor ou contato sem risco de sobrescrita pelo Git:

1. Edite o arquivo de produção:
   ```bash
   nano /var/www/ebooks/shared/experiencia-tecnologia/config.js
   ```
2. Altere o valor de `CHECKOUT_URL` para a URL completa com HTTPS:
   ```javascript
   window.BOOK_CONFIG = Object.freeze({
     CHECKOUT_URL: "https://pay.kiwify.com.br/SEU_CODIGO",
     price: "R$ 47,00",
     author: "Lucas",
     contactEmail: "contato@seudominio.com.br",
     ...
   });
   ```
3. Aplique a alteração executando o deploy:
   ```bash
   /srv/ebook-sources/deploy-ebook.sh deploy experiencia-tecnologia
   ```

---

## 5. Como Adicionar Outro E-book à Mesma Estrutura

Para lançar uma nova landing page (ex.: `outro-ebook`):

1. **Clonar o novo repositório em `/srv/ebook-sources/`:**
   ```bash
   git clone https://github.com/ScryLk/outro-ebook.git /srv/ebook-sources/outro-ebook
   ```

2. **Adicionar o bloco de rotas no Nginx (`/var/www/catana/nginx/nginx.conf`):**
   Logo acima de `# Frontend React SPA`, insira:
   ```nginx
   # E-book: Outro E-book
   location = /outro-ebook {
       return 301 /outro-ebook/;
   }

   location ^~ /outro-ebook/ {
       root /var/www/ebooks;
       index index.html;
       autoindex off;
       try_files $uri $uri/ =404;

       location ~* /(?:\.git|\.env|README\.md) {
           return 404;
       }

       location ~* /outro-ebook/(?:|index\.html|config\.js)$ {
           root /var/www/ebooks;
           add_header Cache-Control "no-cache, must-revalidate" always;
           add_header X-Content-Type-Options "nosniff" always;
           add_header X-Frame-Options "SAMEORIGIN" always;
       }

       location ~* /outro-ebook/.*\.(?:css|js|svg|webp|png|jpe?g|ico)$ {
           root /var/www/ebooks;
           expires 7d;
           add_header Cache-Control "public, max-age=604800, must-revalidate" always;
           add_header X-Content-Type-Options "nosniff" always;
           access_log off;
       }
   }
   ```

3. **Validar e recarregar o Nginx:**
   ```bash
   docker exec catana_web nginx -t
   docker exec catana_web nginx -s reload
   ```

4. **Executar o deploy do novo e-book:**
   ```bash
   /srv/ebook-sources/deploy-ebook.sh deploy outro-ebook
   ```

A nova página estará imediatamente disponível em `https://[DOMÍNIO]/outro-ebook/`.

---

## 6. Arquitetura de Subdomínios (`ebook.dobraverse.io`, `*.dobraverse.io`)

Para permitir múltiplos e-books onde cada um responde pelo seu próprio subdomínio exclusivo (ex.: `https://ebook.dobraverse.io/` ou `https://outro-ebook.dobraverse.io/`):

### 1. Configuração de DNS na Hostinger (Zona DNS de dobraverse.io):
Para cobrir todos os subdomínios de uma vez só (Wildcard):
* **Tipo:** `A`
* **Nome:** `*`
* **Aponta para:** `179.236.238.62`
* **TTL:** `300`

Ou, se preferir criar individualmente por e-book:
* **Tipo:** `A`
* **Nome:** `ebook` (ou o nome do novo e-book)
* **Aponta para:** `179.236.238.62`
* **TTL:** `300`

### 2. Ativação Automática de SSL e Nginx para o Subdomínio:
Execute o script passando o subdomínio e a pasta do e-book:
```bash
/srv/ebook-sources/setup-domain-ssl.sh ebook.dobraverse.io experiencia-tecnologia
```

Para um futuro segundo e-book (`outro-ebook`):
```bash
/srv/ebook-sources/setup-domain-ssl.sh outro-ebook.dobraverse.io outro-ebook
```

O script:
1. Valida se o DNS do subdomínio já aponta para a VPS (`179.236.238.62`).
2. Emite o certificado SSL oficial da Let's Encrypt via Certbot.
3. Cria o bloco VirtualHost no Nginx apontando para `/var/www/ebooks/<slug>`.
4. Recarrega o Nginx com zero downtime.

---

## 7. Estrutura em Repositório Único (Monorepo)

Você pode hospedar todas as landing pages de e-books dentro de um **único repositório no GitHub** (ex.: `landing-01` ou renomeado para `ebooks`).

### Organização de Pastas no Repositório:
```text
landing-01/
├── experiencia-tecnologia/       # Landing page do primeiro e-book
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── config.js
│   └── assets/
├── outro-ebook/                  # Landing page do segundo e-book
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── config.js
│   └── assets/
└── README.md
```

### Como o Deploy Funciona no Monorepo:
O script `/srv/ebook-sources/deploy-ebook.sh` já está preparado com **detecção automática inteligente**:
1. Se existir a pasta `landing-01/<slug>/`, ele faz `git pull` na raiz e publica a partir dessa subpasta.
2. Se o e-book ainda estiver na raiz do repositório (estado inicial legado), ele continua funcionando normalmente sem quebrar nada.
3. Para cada e-book, as configurações persistentes continuam salvas e isoladas em `/var/www/ebooks/shared/<slug>/config.js`.

### Produtos Ativos no Monorepo:

| E-book | Subdomínio Oficial | Pasta no Repositório | Pasta Publicada |
| :--- | :--- | :--- | :--- |
| **Da sua experiência à tecnologia** | `https://experiencia-tecnologia.dobraverse.io/` | `apps/experiencia-tecnologia` | `/var/www/ebooks/experiencia-tecnologia` |
| **Afinal, o que é Indústria 4.0?** | `https://industria.dobraverse.io/` | `apps/industria-40` | `/var/www/ebooks/industria-40` |

### Comandos de Deploy por Produto:
```bash
# Atualizar Indústria 4.0:
/srv/ebook-sources/deploy-ebook.sh deploy industria-40

# Atualizar Experiência à Tecnologia:
/srv/ebook-sources/deploy-ebook.sh deploy experiencia-tecnologia
```

### Configurações Comerciais Independentes (Produção):
* Indústria 4.0: `/var/www/ebooks/shared/industria-40/config.js`
* Experiência à Tecnologia: `/var/www/ebooks/shared/experiencia-tecnologia/config.js`



