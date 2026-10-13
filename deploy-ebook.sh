#!/usr/bin/env bash
set -euo pipefail

# Deploy & Rollback Automation for Dobraverse Monorepo Landing Pages
# Suporta builds independentes com pnpm workspaces e releases atomicas.

BASE_SOURCES="/srv/ebook-sources"
REPO_DIR="${BASE_SOURCES}/landing-01"
BASE_WWW="/var/www/ebooks"

usage() {
    echo "Uso: $0 {deploy|rollback|status} <slug-do-ebook>"
    echo "Exemplos:"
    echo "  $0 deploy industria-40"
    echo "  $0 deploy experiencia-tecnologia"
    exit 1
}

if [ $# -lt 2 ]; then
    usage
fi

ACTION="$1"
INPUT_SLUG="$2"

case "$INPUT_SLUG" in
    portal)
        APP_NAME="portal"
        PUB_SLUG="portal"
        SITE_URL="https://dobraverse.io/"
        BUILD_CMD="pnpm build:portal"
        ;;
    industria|industria-40)
        APP_NAME="industria-40"
        PUB_SLUG="industria-40"
        SITE_URL="https://industria.dobraverse.io/"
        BUILD_CMD="pnpm build:industria"
        ;;
    experiencia|experiencia-tecnologia)
        APP_NAME="experiencia-tecnologia"
        PUB_SLUG="experiencia-tecnologia"
        SITE_URL="https://experiencia-tecnologia.dobraverse.io/"
        BUILD_CMD="pnpm build:experiencia"
        ;;
    ia|inteligencia-artificial)
        APP_NAME="inteligencia-artificial"
        PUB_SLUG="inteligencia-artificial"
        SITE_URL="https://ia.dobraverse.io/"
        BUILD_CMD="pnpm build:ia"
        ;;
    *)
        APP_NAME="$INPUT_SLUG"
        PUB_SLUG="$INPUT_SLUG"
        SITE_URL="https://${INPUT_SLUG}.dobraverse.io/"
        BUILD_CMD="pnpm --filter @dobraverse/${INPUT_SLUG} build"
        ;;
esac

APP_DIR="${REPO_DIR}/apps/${APP_NAME}"
DIST_DIR="${APP_DIR}/dist"
SHARED_DIR="${BASE_WWW}/shared/${PUB_SLUG}"
RELEASES_DIR="${BASE_WWW}/releases/${PUB_SLUG}"
CURRENT_LINK="${BASE_WWW}/${PUB_SLUG}"

do_deploy() {
    echo "=== [DEPLOY] Iniciando publicacao de: $APP_NAME (Slug: $PUB_SLUG) ==="
    echo "-> URL do site: $SITE_URL"

    if [ ! -d "$REPO_DIR/.git" ]; then
        echo "ERRO: Repositorio nao encontrado em $REPO_DIR"
        exit 1
    fi

    if [ ! -d "$APP_DIR" ]; then
        echo "ERRO: Diretorio da aplicacao nao encontrado: $APP_DIR"
        exit 1
    fi

    # 1. Atualizar branch main
    echo "-> Atualizando repositorio Git (main)..."
    cd "$REPO_DIR"
    git fetch origin main
    git checkout main
    git merge --ff-only origin/main

    # 2. Instalar dependencias do workspace
    echo "-> Verificando dependencias do workspace com pnpm..."
    pnpm install --frozen-lockfile

    # 3. Executar check de sintaxe se existir
    echo "-> Executando checagem de integridade..."
    node --check "${APP_DIR}/app.js"
    node --check "${APP_DIR}/config.js"

    # 4. Executar build estatico individual com SITE_URL
    echo "-> Executando build estatico..."
    SITE_URL="$SITE_URL" $BUILD_CMD

    if [ ! -d "$DIST_DIR" ] || [ ! -f "$DIST_DIR/index.html" ]; then
        echo "ERRO: O build nao gerou os arquivos esperados em $DIST_DIR"
        exit 1
    fi

    # 5. Criar diretorio da nova versao
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    TARGET_DIR="${RELEASES_DIR}/${TIMESTAMP}"
    mkdir -p "$TARGET_DIR" "$SHARED_DIR"

    # 6. Copiar arquivos do dist gerado
    echo "-> Copiando dist gerado para $TARGET_DIR..."
    cp -r "${DIST_DIR}/." "$TARGET_DIR/"

    # Preservar config de producao se existir no shared
    if [ -f "$SHARED_DIR/config.js" ]; then
        echo "-> Aplicando config.js personalizado de producao..."
        cp "$SHARED_DIR/config.js" "$TARGET_DIR/config.js"
    else
        echo "-> Inicializando $SHARED_DIR/config.js a partir do repositorio..."
        cp "$TARGET_DIR/config.js" "$SHARED_DIR/config.js"
    fi

    # 7. Sanitizacao de seguranca
    rm -rf "$TARGET_DIR/.git" "$TARGET_DIR/README.md" "$TARGET_DIR/"*.pdf "$TARGET_DIR/"*.env

    # 8. Permissoes minimas de leitura publica
    find "$TARGET_DIR" -type d -exec chmod 755 {} +
    find "$TARGET_DIR" -type f -exec chmod 644 {} +

    # 9. Troca atomica do symlink
    echo "-> Ativando nova versao atomicamente..."
    mkdir -p "$BASE_WWW"
    ln -sfn "releases/${PUB_SLUG}/${TIMESTAMP}" "${BASE_WWW}/${PUB_SLUG}.tmp"
    mv -Tf "${BASE_WWW}/${PUB_SLUG}.tmp" "$CURRENT_LINK"

    # 10. Limpeza de versoes antigas (manter ultimas 5)
    echo "-> Mantendo ultimas 5 versoes..."
    cd "$RELEASES_DIR"
    ls -1dt 20* 2>/dev/null | tail -n +6 | xargs -r rm -rf

    echo "=== [DEPLOY CONCLUIDO] $PUB_SLUG ativo na versao $TIMESTAMP ==="
}

do_rollback() {
    echo "=== [ROLLBACK] Revertendo versao de: $PUB_SLUG ==="
    if [ ! -d "$RELEASES_DIR" ]; then
        echo "ERRO: Diretorio de releases nao existe."
        exit 1
    fi

    CURRENT_TARGET=$(readlink "$CURRENT_LINK" || true)
    CURRENT_NAME=$(basename "$CURRENT_TARGET")

    PREV_VERSION=""
    while IFS= read -r rel_path; do
        b=$(basename "$rel_path")
        if [ "$b" != "$CURRENT_NAME" ]; then
            PREV_VERSION="$b"
            break
        fi
    done < <(ls -1dt "$RELEASES_DIR"/20* 2>/dev/null)

    if [ -z "$PREV_VERSION" ]; then
        echo "ERRO: Nenhuma versao anterior encontrada para rollback."
        exit 1
    fi

    echo "-> Revertendo de $CURRENT_NAME para $PREV_VERSION..."
    ln -sfn "releases/${PUB_SLUG}/${PREV_VERSION}" "${BASE_WWW}/${PUB_SLUG}.tmp"
    mv -Tf "${BASE_WWW}/${PUB_SLUG}.tmp" "$CURRENT_LINK"

    echo "=== [ROLLBACK CONCLUIDO] $PUB_SLUG ativo na versao $PREV_VERSION ==="
}

do_status() {
    echo "=== [STATUS] E-book: $PUB_SLUG (App: $APP_NAME) ==="
    if [ -L "$CURRENT_LINK" ]; then
        TARGET=$(readlink "$CURRENT_LINK")
        echo "Symlink atual: $CURRENT_LINK -> $TARGET"
        if [ -d "${BASE_WWW}/$TARGET" ]; then
            echo "Arquivos publicados em $TARGET:"
            ls -la "${BASE_WWW}/$TARGET"
        else
            echo "AVISO: Alvo do symlink nao existe!"
        fi
    else
        echo "Nenhum symlink ativo em $CURRENT_LINK"
    fi

    if [ -d "$RELEASES_DIR" ]; then
        echo "Historico de releases:"
        ls -1dt "$RELEASES_DIR"/20* 2>/dev/null || echo "Nenhuma release."
    fi
}

case "$ACTION" in
    deploy)
        do_deploy
        ;;
    rollback)
        do_rollback
        ;;
    status)
        do_status
        ;;
    *)
        usage
        ;;
esac
