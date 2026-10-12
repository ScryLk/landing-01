#!/usr/bin/env python3
"""
Gerador Completo do Kit Publicitário — Coleção Afinal: Volume 03
Afinal, vale a pena estudar Inteligência Artificial?
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = '/Users/lucas/Documents/ebooks/apps/estudar-ia'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
KIT_DIR = os.path.join(BASE_DIR, 'kit-publicitario')

COVER_PATH = os.path.join(ASSETS_DIR, 'capa.png')

FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

# PALETA OFICIAL VOLUME 03
GRAFITE = (37, 37, 37)       # #252525
INK = (17, 17, 17)           # #111111
GRAY_MID = (115, 115, 115)   # #737373
SILVER = (191, 195, 199)     # #BFC3C7
GRAY_LIGHT = (232, 232, 232) # #E8E8E8
OFFWHITE = (247, 246, 242)   # #F7F6F2
WHITE = (255, 255, 255)      # #FFFFFF
DARK_PANEL = (26, 29, 36)

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_dot_matrix(draw, x_start, y_start, rows=3, cols=4, gap=20, dot_r=4, color=WHITE):
    for r in range(rows):
        for c in range(cols):
            cx = x_start + c * gap
            cy = y_start + r * gap
            draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color)

def draw_concentric_arcs(draw, cx, cy, r_max, step=22, width=3, color=GRAY_MID):
    for r in range(40, r_max, step):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)

def draw_circuit_lines(draw, color=SILVER, width=3):
    points = [
        (880, 0), (880, 380),
        (820, 440), (820, 720),
        (740, 800), (740, 1350)
    ]
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    draw.ellipse([873, 180, 887, 194], fill=WHITE, outline=INK, width=2)
    draw.ellipse([813, 520, 827, 534], fill=WHITE, outline=INK, width=2)
    draw.ellipse([733, 900, 747, 914], fill=WHITE, outline=INK, width=2)
    draw.line([(0, 907), (1080, 907)], fill=color, width=width)

def load_cover(target_width):
    if os.path.exists(COVER_PATH):
        cov = Image.open(COVER_PATH).convert('RGBA')
        w, h = cov.size
        target_height = int(target_width * (h / w))
        return cov.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return None

print("=== INICIANDO PRODUÇÃO COMPLETA DO KIT PUBLICITÁRIO — VOL. 03 ===")

# ==============================================================
# 01 — THUMBNAILS (1080 x 1080)
# ==============================================================
dir_01 = os.path.join(KIT_DIR, '01-thumbnails')
print("Gerando 01 — Thumbnails...")

# Versão A: Capa Original Centralizada
tA = Image.new('RGB', (1080, 1080), OFFWHITE)
dtA = ImageDraw.Draw(tA)
dtA.rectangle([0, 0, 1080, 24], fill=GRAFITE)
dtA.rectangle([0, 1056, 1080, 1080], fill=GRAFITE)
cov_tA = load_cover(660)
if cov_tA:
    sh = Image.new('RGBA', cov_tA.size, (17, 17, 17, 180))
    tA.paste(sh, (210 + 14, 75 + 14))
    tA.paste(cov_tA, (210, 75), cov_tA)
tA.save(os.path.join(dir_01, 'peca-01-thumbnail-a-capa-centralizada-1080x1080.png'), 'PNG')

# Versão B: Mockup Perspectiva Discreta
tB = Image.new('RGB', (1080, 1080), GRAFITE)
dtB = ImageDraw.Draw(tB)
draw_concentric_arcs(dtB, 950, 150, 360, step=22, width=3, color=(60, 60, 60))
draw_dot_matrix(dtB, 80, 80, rows=3, cols=4, gap=20, dot_r=4, color=SILVER)
dtB.text((80, 160), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=SILVER)
dtB.text((80, 195), "TECNOLOGIA · VOL. 03", font=get_font(FONT_REGULAR, 19), fill=WHITE)
cov_tB = load_cover(460)
if cov_tB:
    sh = Image.new('RGBA', cov_tB.size, INK)
    tB.paste(sh, (310 + 16, 260 + 16))
    tB.paste(cov_tB, (310, 260), cov_tB)
    dtB.rectangle([310, 260, 310+cov_tB.size[0], 260+cov_tB.size[1]], outline=SILVER, width=2)
dtB.rectangle([80, 940, 1000, 1010], fill=INK, outline=SILVER, width=1)
dtB.text((105, 962), "EDIÇÃO DIGITAL EM PDF · ACESSO IMEDIATO NA KIWIFY", font=get_font(FONT_BOLD, 20), fill=WHITE)
dtB.text((950, 958), "↗", font=get_font(FONT_BOLD, 30), fill=SILVER)
tB.save(os.path.join(dir_01, 'peca-01-thumbnail-b-mockup-perspectiva-1080x1080.png'), 'PNG')

# Versão C: Capa + Formas Abstratas
tC = Image.new('RGB', (1080, 1080), GRAY_LIGHT)
dtC = ImageDraw.Draw(tC)
draw_concentric_arcs(dtC, 150, 950, 380, step=24, width=3, color=GRAY_MID)
draw_dot_matrix(dtC, 880, 80, rows=3, cols=4, gap=20, dot_r=4, color=INK)
dtC.text((80, 80), "COLEÇÃO AFINAL // VOL. 03", font=get_font(FONT_BOLD, 22), fill=GRAFITE)
dtC.text((80, 120), "AFINAL, VALE A PENA\nESTUDAR IA?", font=get_font(FONT_BOLD, 46), fill=INK, spacing=6)
cov_tC = load_cover(430)
if cov_tC:
    sh = Image.new('RGBA', cov_tC.size, (17, 17, 17, 160))
    tC.paste(sh, (560 + 12, 280 + 12))
    tC.paste(cov_tC, (560, 280), cov_tC)
    dtC.rectangle([560, 280, 560+cov_tC.size[0], 280+cov_tC.size[1]], outline=INK, width=2)
dtC.rectangle([80, 920, 500, 990], fill=INK)
dtC.text((110, 943), "PUBLICAÇÃO DIGITAL ↗", font=get_font(FONT_BOLD, 22), fill=WHITE)
tC.save(os.path.join(dir_01, 'peca-01-thumbnail-c-formas-geometricas-1080x1080.png'), 'PNG')


# ==============================================================
# 02 — MOCKUPS PREMIUM (1080 x 1080)
# ==============================================================
dir_02 = os.path.join(KIT_DIR, '02-mockups')
print("Gerando 02 — Mockups...")

# Mockup 1: Livro Perspectiva 3D
m1 = Image.new('RGB', (1080, 1080), OFFWHITE)
dm1 = ImageDraw.Draw(m1)
draw_concentric_arcs(dm1, 150, 150, 260, step=22, width=2, color=(215, 215, 210))
draw_dot_matrix(dm1, 880, 80, rows=3, cols=4, gap=20, dot_r=4, color=GRAY_MID)
dm1.text((80, 80), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=INK)
dm1.text((80, 115), "MOCKUP EDITORIAL 3D // TECNOLOGIA · VOL. 03", font=get_font(FONT_REGULAR, 18), fill=GRAY_MID)
cov_m1 = load_cover(510)
if cov_m1:
    sh = Image.new('RGBA', (550, int(510 * 1.41) + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([20, 20, 530, int(510*1.41)+20], fill=(0, 0, 0, 80))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    m1.paste(sh, (280, 220), sh)
    m1.paste(cov_m1, (290, 220), cov_m1)
dm1.rectangle([80, 960, 1000, 962], fill=INK)
dm1.text((80, 980), "FORMATO DIGITAL EM PDF · COMPATÍVEL COM COMPUTADOR, TABLET E CELULAR", font=get_font(FONT_BOLD, 18), fill=INK)
m1.save(os.path.join(dir_02, 'peca-02-mockup-1-livro-perspectiva-1080x1080.png'), 'PNG')

# Mockup 2: Tablet Editorial
m2 = Image.new('RGB', (1080, 1080), INK)
dm2 = ImageDraw.Draw(m2)
draw_concentric_arcs(dm2, 950, 950, 380, step=22, width=2, color=(55, 55, 55))
dm2.text((80, 80), "LEITURA DIGITAL ACESSÍVEL", font=get_font(FONT_BOLD, 22), fill=SILVER)
dm2.text((80, 115), "Diagramação elegante e leitura perfeita em tablets e telas retina", font=get_font(FONT_REGULAR, 18), fill=WHITE)
tw, th = 580, 780
tx, ty = (1080 - tw)//2, 200
dm2.rectangle([tx-10, ty-10, tx+tw+10, ty+th+10], fill=(45, 48, 56), outline=(80, 85, 95), width=3)
dm2.rectangle([tx, ty, tx+tw, ty+th], fill=(0, 0, 0))
dm2.ellipse([tx + tw//2 - 4, ty + 12, tx + tw//2 + 4, ty + 20], fill=(90, 90, 90))
cov_m2 = load_cover(520)
if cov_m2:
    m2.paste(cov_m2, (tx + (tw - 520)//2, ty + 40), cov_m2)
m2.save(os.path.join(dir_02, 'peca-02-mockup-2-tablet-editorial-1080x1080.png'), 'PNG')

# Mockup 3: Edição Digital Multitela
m3 = Image.new('RGB', (1080, 1080), GRAFITE)
dm3 = ImageDraw.Draw(m3)
draw_circuit_lines(dm3, color=(60, 60, 60), width=2)
dm3.text((80, 80), "CONTEÚDO DIGITAL COMPLETO", font=get_font(FONT_BOLD, 24), fill=SILVER)
dm3.text((80, 115), "12 capítulos de investigação, 7 ferramentas práticas e exercícios de decisão", font=get_font(FONT_REGULAR, 18), fill=WHITE)
cov_m3 = load_cover(460)
if cov_m3:
    sh = Image.new('RGBA', cov_m3.size, INK)
    m3.paste(sh, (310 + 16, 240 + 16))
    m3.paste(cov_m3, (310, 240), cov_m3)
    dm3.rectangle([310, 240, 310+cov_m3.size[0], 240+cov_m3.size[1]], outline=SILVER, width=2)
dm3.rectangle([80, 920, 1000, 990], fill=INK, outline=SILVER, width=1)
dm3.text((110, 942), "E-BOOK EM PDF · LEITURA INDEPENDENTE · SEM FÓRMULAS MÁGICAS", font=get_font(FONT_BOLD, 20), fill=WHITE)
m3.save(os.path.join(dir_02, 'peca-02-mockup-3-edicao-digital-multitela-1080x1080.png'), 'PNG')


# ==============================================================
# 03 — ANÚNCIOS PARA FEED
# ==============================================================
dir_03 = os.path.join(KIT_DIR, '03-anuncios-feed')
print("Gerando 03 — Anúncios Feed...")

# Peça 03: Reflexão 1080 x 1080 (Quadrado)
f03_sq = Image.new('RGB', (1080, 1080), INK)
df03_sq = ImageDraw.Draw(f03_sq)
draw_concentric_arcs(df03_sq, 920, 200, 360, step=22, width=3, color=(60, 60, 60))
df03_sq.text((80, 80), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 03", font=get_font(FONT_BOLD, 22), fill=SILVER)
df03_sq.text((80, 150), "VOCÊ ESTÁ ESTUDANDO\nPARA EVOLUIR?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=10)
df03_sq.text((80, 290), "OU APENAS PARA NÃO FICAR PARA TRÁS?", font=get_font(FONT_BOLD, 30), fill=SILVER)
df03_sq.text((80, 345), "Uma reflexão sobre inteligência artificial, mercado e formação.", font=get_font(FONT_REGULAR, 22), fill=GRAY_LIGHT)
cov_f03_sq = load_cover(360)
if cov_f03_sq:
    f03_sq.paste(cov_f03_sq, (620, 420), cov_f03_sq)
    df03_sq.rectangle([620, 420, 620+cov_f03_sq.size[0], 420+cov_f03_sq.size[1]], outline=SILVER, width=2)
df03_sq.rectangle([80, 880, 500, 960], fill=SILVER)
df03_sq.text((120, 905), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 26), fill=INK)
f03_sq.save(os.path.join(dir_03, 'peca-03-reflexao-feed-quadrado-1080x1080.png'), 'PNG')

# Peça 03: Reflexão 1080 x 1350 (Vertical)
# Copia o gerado na etapa 1 para manter coerência
os.system(f"cp '{os.path.join(KIT_DIR, 'proposta-a-editorial-tipografico-1080x1350.png')}' '{os.path.join(dir_03, 'peca-03-reflexao-feed-vertical-1080x1350.png')}'")

# Peça 04: Graduação ou Pós 1080 x 1350
os.system(f"cp '{os.path.join(KIT_DIR, 'proposta-b-caminhos-bifurcacoes-1080x1350.png')}' '{os.path.join(dir_03, 'peca-04-graduacao-pos-ou-outro-1080x1350.png')}'")

# Peça 05: O Conhecimento Muda? 1080 x 1350
f05 = Image.new('RGB', (1080, 1350), GRAFITE)
df05 = ImageDraw.Draw(f05)
draw_concentric_arcs(df05, 950, 200, 400, step=22, width=3, color=(60, 60, 60))
draw_dot_matrix(df05, 80, 80, rows=3, cols=4, gap=20, dot_r=4, color=SILVER)
df05.text((80, 175), "FUNDAMENTOS VS FERRAMENTAS // VOL. 03", font=get_font(FONT_BOLD, 22), fill=SILVER)
df05.text((80, 230), "A IA MUDA.\nO QUE VALE A PENA\nAPRENDER?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=10)
df05.text((80, 420), "Uma reflexão sobre ferramentas passageiras, fundamentos sólidos\ne o que continuará sendo essencial no mercado.", font=get_font(FONT_REGULAR, 23), fill=GRAY_LIGHT, spacing=6)

# Blocos de contraste visual
df05.rectangle([80, 520, 520, 640], fill=DARK_PANEL, outline=GRAY_MID, width=1)
df05.text((105, 545), "FERRAMENTAS PASSAGEIRAS", font=get_font(FONT_BOLD, 18), fill=SILVER)
df05.text((105, 575), "Mudam a cada semana.\nExigem adaptação contínua.", font=get_font(FONT_REGULAR, 17), fill=GRAY_LIGHT, spacing=4)

df05.rectangle([560, 520, 1000, 640], fill=DARK_PANEL, outline=SILVER, width=2)
df05.text((585, 545), "FUNDAMENTOS SÓLIDOS", font=get_font(FONT_BOLD, 18), fill=WHITE)
df05.text((585, 575), "Permanecem por décadas.\nSustentam seu raciocínio.", font=get_font(FONT_REGULAR, 17), fill=SILVER, spacing=4)

cov_f05 = load_cover(400)
if cov_f05:
    f05.paste(cov_f05, (340, 680), cov_f05)
    df05.rectangle([340, 680, 340+cov_f05.size[0], 680+cov_f05.size[1]], outline=SILVER, width=2)

df05.rectangle([80, 1220, 1000, 1295], fill=SILVER)
df05.text((430, 1243), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 28), fill=INK)
f05.save(os.path.join(dir_03, 'peca-05-o-conhecimento-muda-1080x1350.png'), 'PNG')

# Peça 06: Decisão Antes do Investimento 1080 x 1350
f06 = Image.new('RGB', (1080, 1350), OFFWHITE)
df06 = ImageDraw.Draw(f06)
df06.rectangle([0, 0, 1080, 24], fill=INK)
draw_dot_matrix(df06, 880, 80, rows=3, cols=4, gap=20, dot_r=4, color=GRAY_MID)
df06.text((80, 75), "AVALIAÇÃO DE CARREIRA // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=GRAFITE)
df06.text((80, 130), "ANTES DE INVESTIR\nEM UMA FORMAÇÃO,\nFAÇA AS PERGUNTAS CERTAS.", font=get_font(FONT_BOLD, 48), fill=INK, spacing=10)
df06.text((80, 320), "Inteligência artificial, graduação, pós-graduação e carreira.", font=get_font(FONT_BOLD, 26), fill=GRAY_MID)
df06.text((80, 365), "Sem promessas de retorno garantido. Um método para analisar\nseu momento profissional com lucidez.", font=get_font(FONT_REGULAR, 22), fill=GRAFITE, spacing=6)

cov_f06 = load_cover(430)
if cov_f06:
    sh = Image.new('RGBA', cov_f06.size, (17, 17, 17, 180))
    f06.paste(sh, (325 + 14, 480 + 14))
    f06.paste(cov_f06, (325, 480), cov_f06)
    df06.rectangle([325, 480, 325+cov_f06.size[0], 480+cov_f06.size[1]], outline=INK, width=2)

df06.rectangle([80, 1140, 1000, 1205], fill=WHITE, outline=INK, width=1)
df06.text((105, 1162), "INCLUI 7 FERRAMENTAS PRÁTICAS DE REFLEXÃO E ANÁLISE DE MERCADO", font=get_font(FONT_BOLD, 18), fill=INK)

df06.rectangle([80, 1225, 1000, 1300], fill=INK)
df06.text((380, 1248), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)
f06.save(os.path.join(dir_03, 'peca-06-decisao-antes-do-investimento-1080x1350.png'), 'PNG')

# Peça 07: Prompt Engineering 1080 x 1350
f07 = Image.new('RGB', (1080, 1350), INK)
df07 = ImageDraw.Draw(f07)
draw_circuit_lines(df07, color=(60, 60, 60), width=2)
df07.text((80, 80), "EVOLUÇÃO DAS COMPETÊNCIAS // CAPÍTULO 4", font=get_font(FONT_BOLD, 22), fill=SILVER)
df07.text((80, 140), "E SE A FERRAMENTA\nSIMPLIFICAR AQUILO QUE\nVOCÊ ESTÁ ESTUDANDO?", font=get_font(FONT_BOLD, 50), fill=WHITE, spacing=10)
df07.text((80, 330), "O que continuará sendo seu conhecimento?", font=get_font(FONT_BOLD, 30), fill=SILVER)
df07.text((80, 380), "A evolução dos prompts e das interfaces levanta uma questão central:\nquais habilidades humanas mantêm valor quando a IA faz o código?", font=get_font(FONT_REGULAR, 22), fill=GRAY_LIGHT, spacing=6)

cov_f07 = load_cover(410)
if cov_f07:
    f07.paste(cov_f07, (335, 520), cov_f07)
    df07.rectangle([335, 520, 335+cov_f07.size[0], 520+cov_f07.size[1]], outline=SILVER, width=2)

df07.rectangle([80, 1220, 1000, 1295], fill=SILVER)
df07.text((360, 1243), "EXPLORE ESSA REFLEXÃO ↗", font=get_font(FONT_BOLD, 28), fill=INK)
f07.save(os.path.join(dir_03, 'peca-07-prompt-engineering-1080x1350.png'), 'PNG')

# Peça 08: Apresentação do E-book 1080 x 1350
os.system(f"cp '{os.path.join(KIT_DIR, 'proposta-c-mockup-produto-1080x1350.png')}' '{os.path.join(dir_03, 'peca-08-apresentacao-do-ebook-1080x1350.png')}'")


# ==============================================================
# 04 — STORIES (1080 x 1920)
# ==============================================================
dir_04 = os.path.join(KIT_DIR, '04-stories')
print("Gerando 04 — Stories...")

# Peça 03 Stories
s03 = Image.new('RGB', (1080, 1920), GRAFITE)
ds03 = ImageDraw.Draw(s03)
draw_concentric_arcs(ds03, 540, 960, 480, step=26, width=3, color=(60, 60, 60))
ds03.text((100, 260), "COLEÇÃO AFINAL // VOL. 03", font=get_font(FONT_BOLD, 24), fill=SILVER)
ds03.text((100, 330), "VOCÊ ESTÁ ESTUDANDO\nPARA EVOLUIR?", font=get_font(FONT_BOLD, 56), fill=WHITE, spacing=12)
ds03.text((100, 480), "OU APENAS PARA NÃO\nFICAR PARA TRÁS?", font=get_font(FONT_BOLD, 42), fill=SILVER, spacing=10)
cov_s03 = load_cover(520)
if cov_s03:
    s03.paste(cov_s03, (280, 680), cov_s03)
    ds03.rectangle([280, 680, 280+cov_s03.size[0], 680+cov_s03.size[1]], outline=SILVER, width=3)
ds03.rectangle([100, 1540, 980, 1630], fill=SILVER)
ds03.text((370, 1570), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=INK)
s03.save(os.path.join(dir_04, 'peca-03-reflexao-stories-1080x1920.png'), 'PNG')

# Story 1: Identificação
s1 = Image.new('RGB', (1080, 1920), INK)
ds1 = ImageDraw.Draw(s1)
draw_concentric_arcs(ds1, 540, 960, 450, step=26, width=2, color=(50, 50, 50))
ds1.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=SILVER)
ds1.text((100, 320), "1 / 4", font=get_font(FONT_BOLD, 20), fill=GRAY_MID)
ds1.text((100, 640), "A INTELIGÊNCIA\nARTIFICIAL ESTÁ\nMUDANDO TUDO?", font=get_font(FONT_BOLD, 64), fill=WHITE, spacing=14)
ds1.text((100, 880), "Novos modelos, notícias diárias e uma sensação\nconstante de aceleração.", font=get_font(FONT_REGULAR, 30), fill=SILVER, spacing=10)
draw_dot_matrix(ds1, 100, 1200, rows=4, cols=6, gap=26, dot_r=5, color=WHITE)
ds1.text((100, 1600), "TOQUE PARA REFLETIR →", font=get_font(FONT_BOLD, 24), fill=GRAY_MID)
s1.save(os.path.join(dir_04, 'peca-13-story-1-identificacao-1080x1920.png'), 'PNG')

# Story 2: Provocação
s2 = Image.new('RGB', (1080, 1920), GRAFITE)
ds2 = ImageDraw.Draw(s2)
draw_concentric_arcs(ds2, 540, 960, 450, step=26, width=3, color=(60, 60, 60))
ds2.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=SILVER)
ds2.text((100, 320), "2 / 4", font=get_font(FONT_BOLD, 20), fill=GRAY_MID)
ds2.text((100, 620), "MAS VOCÊ SABE\nPOR QUE QUER\nESTUDÁ-LA?", font=get_font(FONT_BOLD, 64), fill=WHITE, spacing=14)
ds2.text((100, 870), "Para desenvolver novas competências com propósito\nou apenas para aliviar o medo de ficar desatualizado?", font=get_font(FONT_BOLD, 30), fill=SILVER, spacing=10)
ds2.text((100, 1600), "CONTINUAR →", font=get_font(FONT_BOLD, 24), fill=WHITE)
s2.save(os.path.join(dir_04, 'peca-13-story-2-provocacao-1080x1920.png'), 'PNG')

# Story 3: Reflexão
s3 = Image.new('RGB', (1080, 1920), GRAY_LIGHT)
ds3 = ImageDraw.Draw(s3)
ds3.text((100, 260), "COLEÇÃO AFINAL // DECISÃO", font=get_font(FONT_BOLD, 24), fill=GRAFITE)
ds3.text((100, 320), "3 / 4", font=get_font(FONT_BOLD, 20), fill=GRAY_MID)
ds3.text((100, 520), "GRADUAÇÃO, PÓS,\nCURSOS OU PROJETOS:", font=get_font(FONT_BOLD, 54), fill=INK, spacing=12)
ds3.text((100, 660), "Qual caminho faz sentido\npara o seu momento?", font=get_font(FONT_BOLD, 34), fill=GRAY_MID, spacing=8)
ds3.rectangle([100, 800, 980, 900], fill=WHITE, outline=INK, width=2)
ds3.text((140, 835), "01 / Graduação: fundamentos e formação de longo prazo", font=get_font(FONT_BOLD, 22), fill=INK)
ds3.rectangle([100, 940, 980, 1040], fill=WHITE, outline=INK, width=2)
ds3.text((140, 975), "02 / Pós-graduação: especialização e rede profissional", font=get_font(FONT_BOLD, 22), fill=INK)
ds3.rectangle([100, 1080, 980, 1180], fill=WHITE, outline=INK, width=2)
ds3.text((140, 1115), "03 / Cursos livres: ferramentas e experimentação rápida", font=get_font(FONT_BOLD, 22), fill=INK)
ds3.text((100, 1600), "VEJA O LIVRO COMPLETO →", font=get_font(FONT_BOLD, 24), fill=GRAFITE)
s3.save(os.path.join(dir_04, 'peca-13-story-3-reflexao-1080x1920.png'), 'PNG')

# Story 4: Produto & CTA
s4 = Image.new('RGB', (1080, 1920), INK)
ds4 = ImageDraw.Draw(s4)
draw_concentric_arcs(ds4, 540, 850, 420, step=24, width=3, color=(60, 60, 60))
ds4.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=SILVER)
ds4.text((100, 320), "4 / 4", font=get_font(FONT_BOLD, 20), fill=GRAY_MID)
ds4.text((100, 380), "AFINAL, VALE A PENA\nESTUDAR INTELIGÊNCIA\nARTIFICIAL?", font=get_font(FONT_BOLD, 52), fill=WHITE, spacing=10)
ds4.text((100, 560), "Conheça o novo e-book da Coleção Afinal.", font=get_font(FONT_REGULAR, 26), fill=SILVER)
cov_s4 = load_cover(500)
if cov_s4:
    s4.paste(cov_s4, (290, 650), cov_s4)
    ds4.rectangle([290, 650, 290+cov_s4.size[0], 650+cov_s4.size[1]], outline=SILVER, width=3)
ds4.rectangle([100, 1540, 980, 1630], fill=WHITE)
ds4.text((430, 1570), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 30), fill=INK)
ds4.text((340, 1650), "LINK DISPONÍVEL NA BIO E NO ANÚNCIO", font=get_font(FONT_BOLD, 18), fill=GRAY_MID)
s4.save(os.path.join(dir_04, 'peca-13-story-4-produto-1080x1920.png'), 'PNG')


# ==============================================================
# 05 — POSTS EDUCATIVOS (1080 x 1080)
# ==============================================================
dir_05 = os.path.join(KIT_DIR, '05-posts-educativos')
print("Gerando 05 — Posts Educativos...")

# Post A: Nova Formação
pA = Image.new('RGB', (1080, 1080), INK)
dpA = ImageDraw.Draw(pA)
draw_concentric_arcs(dpA, 900, 150, 350, step=22, width=3, color=(60, 60, 60))
dpA.text((80, 80), "FORMAÇÃO // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpA.text((80, 150), "TODA MUDANÇA\nEXIGE UMA NOVA\nFORMAÇÃO?", font=get_font(FONT_BOLD, 58), fill=WHITE, spacing=10)
dpA.text((80, 360), "A cada nova tecnologia, o mercado educacional cria uma enxurrada\nde cursos e certificações urgentes. Mas nem toda evolução exige\nrecomeçar do zero ou colecionar diplomas.", font=get_font(FONT_REGULAR, 23), fill=GRAY_LIGHT, spacing=8)
dpA.rectangle([80, 520, 1000, 720], fill=DARK_PANEL, outline=GRAY_MID, width=1)
dpA.text((120, 560), "Pergunta chave:", font=get_font(FONT_BOLD, 20), fill=SILVER)
dpA.text((120, 600), "Você precisa de um curso inteiro ou apenas de prática consciente\npara aplicar IA dentro da sua área de domínio atual?", font=get_font(FONT_BOLD, 24), fill=WHITE, spacing=6)
dpA.text((80, 820), "Capítulo 7: O valor da formação e a influência do marketing educacional.", font=get_font(FONT_BOLD, 20), fill=SILVER)
dpA.rectangle([80, 880, 480, 960], fill=SILVER)
dpA.text((120, 905), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 26), fill=INK)
pA.save(os.path.join(dir_05, 'peca-12-post-a-nova-formacao-1080x1080.png'), 'PNG')

# Post B: Ferramenta vs Área
pB = Image.new('RGB', (1080, 1080), GRAFITE)
dpB = ImageDraw.Draw(pB)
draw_dot_matrix(dpB, 80, 80, rows=3, cols=4, gap=22, dot_r=5, color=SILVER)
dpB.text((80, 170), "COMPETÊNCIAS // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpB.text((80, 230), "APRENDER UMA\nFERRAMENTA É O MESMO\nQUE DOMINAR UMA ÁREA?", font=get_font(FONT_BOLD, 52), fill=WHITE, spacing=10)
dpB.text((80, 420), "Saber gerar comandos ou usar um modelo não substitui\no conhecimento do negócio, a capacidade crítica e a visão estratégica.", font=get_font(FONT_REGULAR, 24), fill=GRAY_LIGHT, spacing=6)
dpB.rectangle([80, 530, 1000, 620], fill=INK, outline=SILVER, width=1)
dpB.text((110, 560), "Operador de ferramenta: substituto fácil.", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpB.rectangle([80, 640, 1000, 730], fill=INK, outline=WHITE, width=2)
dpB.text((110, 670), "Profissional de fundamentos: inteligência insubstituível.", font=get_font(FONT_BOLD, 22), fill=WHITE)
dpB.text((80, 820), "Capítulo 3: Fundamentos vs ferramentas passageiras.", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpB.rectangle([80, 880, 480, 960], fill=WHITE)
dpB.text((120, 905), "LEIA O LIVRO ↗", font=get_font(FONT_BOLD, 24), fill=INK)
pB.save(os.path.join(dir_05, 'peca-12-post-b-ferramenta-vs-area-1080x1080.png'), 'PNG')

# Post C: Pós-graduação
pC = Image.new('RGB', (1080, 1080), GRAY_LIGHT)
dpC = ImageDraw.Draw(pC)
dpC.rectangle([0, 0, 1080, 24], fill=INK)
dpC.text((80, 80), "INVESTIMENTO ACADÊMICO // VOL. 03", font=get_font(FONT_BOLD, 22), fill=GRAFITE)
dpC.text((80, 140), "UMA PÓS-GRADUAÇÃO\nRESOLVE QUAL PROBLEMA\nDA SUA CARREIRA?", font=get_font(FONT_BOLD, 50), fill=INK, spacing=10)
dpC.text((80, 320), "Antes de comprometer meses de dedicação e milhares de reais,\nresponda: o objetivo é aprofundar um nicho, validar credenciais\nou apenas uma tentativa de aplacar a ansiedade profissional?", font=get_font(FONT_REGULAR, 22), fill=GRAFITE, spacing=6)
dpC.rectangle([80, 440, 1000, 700], fill=WHITE, outline=INK, width=2)
dpC.text((110, 470), "CHECKLIST DE DECISÃO DO LIVRO:", font=get_font(FONT_BOLD, 20), fill=GRAFITE)
dpC.text((110, 520), "1. O currículo do curso foca em conceitos ou em tutoriais?", font=get_font(FONT_REGULAR, 20), fill=INK)
dpC.text((110, 570), "2. Essa titulação é exigida pelo mercado onde você atua?", font=get_font(FONT_REGULAR, 20), fill=INK)
dpC.text((110, 620), "3. Você terá tempo hábil para aplicar os aprendizados?", font=get_font(FONT_REGULAR, 20), fill=INK)
dpC.text((80, 780), "Capítulo 8: Quando uma pós-graduação realmente compensa.", font=get_font(FONT_BOLD, 22), fill=INK)
dpC.rectangle([80, 840, 480, 920], fill=INK)
dpC.text((120, 865), "CONHEÇA O GUIA ↗", font=get_font(FONT_BOLD, 24), fill=WHITE)
pC.save(os.path.join(dir_05, 'peca-12-post-c-pos-graduacao-problema-1080x1080.png'), 'PNG')

# Post D: Desenvolver ou Utilizar
pD = Image.new('RGB', (1080, 1080), INK)
dpD = ImageDraw.Draw(pD)
draw_concentric_arcs(dpD, 900, 900, 360, step=22, width=2, color=(60, 60, 60))
dpD.text((80, 80), "ROTAS TECNOLÓGICAS // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpD.text((80, 150), "VOCÊ QUER\nDESENVOLVER IA OU\nAPENAS UTILIZÁ-LA?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=10)
dpD.text((80, 340), "Existe uma grande diferença entre criar arquiteturas de modelos\ne aplicar IA para resolver problemas de um negócio.", font=get_font(FONT_REGULAR, 24), fill=GRAY_LIGHT, spacing=6)
dpD.rectangle([80, 450, 1000, 570], fill=DARK_PANEL, outline=GRAY_MID, width=1)
dpD.text((110, 480), "DESENVOLVER: Matemática, estatística, engenharia e algoritmos.", font=get_font(FONT_BOLD, 20), fill=SILVER)
dpD.text((110, 520), "APLICAR: Contexto de negócios, processos, produto e integração.", font=get_font(FONT_BOLD, 20), fill=WHITE)
dpD.text((80, 740), "Saber para onde você está olhando evita gastar anos no caminho errado.", font=get_font(FONT_BOLD, 22), fill=SILVER)
dpD.rectangle([80, 840, 480, 920], fill=SILVER)
dpD.text((120, 865), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 26), fill=INK)
pD.save(os.path.join(dir_05, 'peca-12-post-d-desenvolver-ou-utilizar-1080x1080.png'), 'PNG')


# ==============================================================
# 06 — BANNERS HORIZONTAIS (1920 x 1080)
# ==============================================================
dir_06 = os.path.join(KIT_DIR, '06-banners-horizontais')
print("Gerando 06 — Banners Horizontais...")

# Banner 10A: Grafite 1920 x 1080
bh_g = Image.new('RGB', (1920, 1080), GRAFITE)
dbh_g = ImageDraw.Draw(bh_g)
draw_concentric_arcs(dbh_g, 1700, 250, 520, step=26, width=3, color=(60, 60, 60))
draw_circuit_lines(dbh_g, color=(70, 70, 70), width=2)
dbh_g.text((140, 160), "COLEÇÃO AFINAL // LANÇAMENTO OFICIAL", font=get_font(FONT_BOLD, 24), fill=SILVER)
dbh_g.text((140, 220), "O FUTURO ESTÁ MUDANDO.", font=get_font(FONT_BOLD, 68), fill=WHITE)
dbh_g.text((140, 310), "Mas por que você está correndo atrás dele?", font=get_font(FONT_BOLD, 42), fill=SILVER)
dbh_g.text((140, 390), "Uma reflexão lúcida sobre inteligência artificial, formação acadêmica\ne as escolhas que realmente definem uma carreira.", font=get_font(FONT_REGULAR, 26), fill=GRAY_LIGHT, spacing=8)
cov_bh_g = load_cover(520)
if cov_bh_g:
    sh = Image.new('RGBA', cov_bh_g.size, INK)
    bh_g.paste(sh, (1260 + 16, 180 + 16))
    bh_g.paste(cov_bh_g, (1260, 180), cov_bh_g)
    dbh_g.rectangle([1260, 180, 1260+cov_bh_g.size[0], 180+cov_bh_g.size[1]], outline=SILVER, width=2)
dbh_g.rectangle([140, 540, 540, 620], fill=SILVER)
dbh_g.text((180, 565), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=INK)
bh_g.save(os.path.join(dir_06, 'peca-10-banner-horizontal-grafite-1920x1080.png'), 'PNG')

# Banner 10B: Prata / Cinza Claro 1920 x 1080
bh_s = Image.new('RGB', (1920, 1080), GRAY_LIGHT)
dbh_s = ImageDraw.Draw(bh_s)
draw_concentric_arcs(dbh_s, 1700, 250, 520, step=26, width=2, color=(180, 180, 180))
dbh_s.text((140, 160), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 03", font=get_font(FONT_BOLD, 24), fill=GRAFITE)
dbh_s.text((140, 220), "O FUTURO ESTÁ MUDANDO.", font=get_font(FONT_BOLD, 68), fill=INK)
dbh_s.text((140, 310), "Mas por que você está correndo atrás dele?", font=get_font(FONT_BOLD, 42), fill=GRAY_MID)
dbh_s.text((140, 390), "Aprenda a diferenciar fundamentos de ferramentas passageiras\ne decida seus próximos passos com consciência.", font=get_font(FONT_REGULAR, 26), fill=GRAFITE, spacing=8)
if cov_bh_g:
    sh = Image.new('RGBA', cov_bh_g.size, (17, 17, 17, 180))
    bh_s.paste(sh, (1260 + 16, 180 + 16))
    bh_s.paste(cov_bh_g, (1260, 180), cov_bh_g)
    dbh_s.rectangle([1260, 180, 1260+cov_bh_g.size[0], 180+cov_bh_g.size[1]], outline=INK, width=2)
dbh_s.rectangle([140, 540, 540, 620], fill=INK)
dbh_s.text((180, 565), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)
bh_s.save(os.path.join(dir_06, 'peca-10-banner-horizontal-prata-1920x1080.png'), 'PNG')


# ==============================================================
# 07 — LANDING PAGE (1600 x 900 & Mobile)
# ==============================================================
dir_07 = os.path.join(KIT_DIR, '07-landing-page')
print("Gerando 07 — Landing Page...")

# Peça 09A: Desktop 1600 x 900 (Fundo com respiro à esquerda)
lp_d = Image.new('RGB', (1600, 900), GRAFITE)
dlp_d = ImageDraw.Draw(lp_d)
draw_concentric_arcs(dlp_d, 1400, 200, 480, step=24, width=3, color=(60, 60, 60))
draw_circuit_lines(dlp_d, color=(65, 65, 65), width=2)
cov_lp = load_cover(460)
if cov_lp:
    sh = Image.new('RGBA', cov_lp.size, INK)
    lp_d.paste(sh, (1040 + 16, 140 + 16))
    lp_d.paste(cov_lp, (1040, 140), cov_lp)
    dlp_d.rectangle([1040, 140, 1040+cov_lp.size[0], 140+cov_lp.size[1]], outline=SILVER, width=2)
# Marca d'água sutil para identificar a área HTML
dlp_d.text((120, 120), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 03", font=get_font(FONT_BOLD, 20), fill=SILVER)
dlp_d.text((120, 180), "AFINAL, VALE A PENA\nESTUDAR INTELIGÊNCIA\nARTIFICIAL?", font=get_font(FONT_BOLD, 60), fill=WHITE, spacing=10)
dlp_d.text((120, 390), "Você está estudando para evoluir ou apenas para não ficar para trás?", font=get_font(FONT_REGULAR, 24), fill=SILVER)
dlp_d.rectangle([120, 480, 480, 550], fill=SILVER)
dlp_d.text((160, 502), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 22), fill=INK)
lp_d.save(os.path.join(dir_07, 'peca-09-banner-lp-desktop-1600x900.png'), 'PNG')

# Peça 09B: Mobile 1080 x 1350
lp_m = Image.new('RGB', (1080, 1350), GRAFITE)
dlp_m = ImageDraw.Draw(lp_m)
draw_concentric_arcs(dlp_m, 950, 200, 380, step=22, width=3, color=(60, 60, 60))
dlp_m.text((80, 120), "COLEÇÃO AFINAL // VOL. 03", font=get_font(FONT_BOLD, 22), fill=SILVER)
dlp_m.text((80, 175), "AFINAL, VALE A PENA\nESTUDAR IA?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=10)
dlp_m.text((80, 310), "Você está estudando para evoluir ou apenas para não ficar para trás?", font=get_font(FONT_REGULAR, 22), fill=SILVER)
if cov_lp:
    sh = Image.new('RGBA', cov_lp.size, INK)
    lp_m.paste(sh, (310 + 14, 400 + 14))
    lp_m.paste(cov_lp, (310, 400), cov_lp)
    dlp_m.rectangle([310, 400, 310+cov_lp.size[0], 400+cov_lp.size[1]], outline=SILVER, width=2)
dlp_m.rectangle([80, 1180, 1000, 1260], fill=SILVER)
dlp_m.text((380, 1205), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=INK)
lp_m.save(os.path.join(dir_07, 'peca-09-banner-lp-mobile-1080x1350.png'), 'PNG')


# ==============================================================
# 08 — OPEN GRAPH (1200 x 630)
# ==============================================================
dir_08 = os.path.join(KIT_DIR, '08-open-graph')
print("Gerando 08 — Open Graph...")

og = Image.new('RGB', (1200, 630), WHITE)
dog = ImageDraw.Draw(og)
dog.rectangle([0, 0, 14, 630], fill=GRAFITE)
draw_concentric_arcs(dog, 1100, 150, 300, step=20, width=2, color=SILVER)

dog.text((80, 80), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 03", font=get_font(FONT_BOLD, 18), fill=GRAY_MID)
dog.text((80, 130), "AFINAL, VALE A PENA\nESTUDAR IA?", font=get_font(FONT_BOLD, 52), fill=INK, spacing=8)
dog.text((80, 270), "Você está estudando para evoluir ou apenas para não ficar para trás?", font=get_font(FONT_REGULAR, 22), fill=GRAFITE)
dog.rectangle([80, 360, 440, 420], fill=INK)
dog.text((105, 380), "E-BOOK EM PDF · GUIA PRÁTICO ↗", font=get_font(FONT_BOLD, 18), fill=WHITE)

cov_og = load_cover(360)
if cov_og:
    sh = Image.new('RGBA', cov_og.size, INK)
    og.paste(sh, (760 + 12, 70 + 12))
    og.paste(cov_og, (760, 70), cov_og)
    dog.rectangle([760, 70, 760+cov_og.size[0], 70+cov_og.size[1]], outline=SILVER, width=1)
og.save(os.path.join(dir_08, 'peca-11-compartilhamento-og-1200x630.png'), 'PNG')

print("=== TODAS AS 21 ARTES DO VOLUME 03 FORAM GERADAS COM SUCESSO! ===")
