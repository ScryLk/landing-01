#!/usr/bin/env bash
set -euo pipefail

# Provisionamento automatico de SSL e VirtualHost HTTPS para subdominios
DOMAIN="${1:-experiencia-tecnologia.dobraverse.io}"
SLUG="${2:-experiencia-tecnologia}"
VPS_IP="179.236.238.62"
EMAIL="lucaskepler991@outlook.com"

echo "=== Verificando DNS de $DOMAIN ==="
CURRENT_IP=$(getent ahosts "$DOMAIN" | awk '{print $1}' | head -n 1 || true)

if [ "$CURRENT_IP" != "$VPS_IP" ]; then
    echo "ATENCAO: $DOMAIN ainda aponta para '$CURRENT_IP' (esperado: $VPS_IP)."
    echo ""
    echo "Para ativar este subdominio na Hostinger (Zona DNS de dobraverse.io):"
    echo "  Tipo: A"
    echo "  Nome: ${DOMAIN%%.dobraverse.io}  (ou use * para cobrir todos os subdominios)"
    echo "  Aponta para: $VPS_IP"
    echo "  TTL: 300"
    echo ""
    echo "Apos salvar e aguardar a propagacao, execute novamente:"
    echo "  /srv/ebook-sources/setup-domain-ssl.sh $DOMAIN $SLUG"
    exit 1
fi

echo "DNS validado com sucesso: $DOMAIN -> $VPS_IP"
echo "=== Solicitando Certificado SSL Let's Encrypt para $DOMAIN ==="

docker exec catana_certbot certbot certonly --webroot -w /var/www/certbot \
    -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

echo "=== Gravando Bloco VirtualHost HTTPS no Nginx para $DOMAIN ==="
python3 - "$DOMAIN" "$SLUG" << 'PYEOF'
import sys

domain = sys.argv[1]
slug = sys.argv[2]

with open('/var/www/catana/nginx/nginx.conf', 'r') as f:
    conf = f.read()

vhost_block = f"""
# Servidor HTTPS para {domain} (E-book: {slug})
server {{
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name {domain};

    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384";
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/xml+rss application/atom+xml image/svg+xml;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    location / {{
        root /var/www/ebooks/{slug};
        index index.html;
        autoindex off;
        try_files $uri $uri/ =404;

        location ~* /(?:\\.git|\\.env|README\\.md) {{
            return 404;
        }}

        location ~* (?:|index\\.html|config\\.js)$ {{
            root /var/www/ebooks/{slug};
            add_header Cache-Control "no-cache, must-revalidate" always;
            add_header X-Content-Type-Options "nosniff" always;
            add_header X-Frame-Options "SAMEORIGIN" always;
        }}

        location ~* \\.(?:css|js|svg|webp|png|jpe?g|ico)$ {{
            root /var/www/ebooks/{slug};
            expires 7d;
            add_header Cache-Control "public, max-age=604800, must-revalidate" always;
            add_header X-Content-Type-Options "nosniff" always;
            access_log off;
        }}
    }}
}}
"""

if f"server_name {domain};" not in conf:
    with open('/var/www/catana/nginx/nginx.conf', 'a') as f:
        f.write(vhost_block)
    print(f"Bloco HTTPS para {domain} adicionado com sucesso!")
else:
    print(f"Bloco HTTPS para {domain} ja configurado.")
PYEOF

docker exec catana_web nginx -t
docker exec catana_web nginx -s reload

echo "=== CONCLUIDO! Landing page ativa com HTTPS em: https://$DOMAIN/ ==="
