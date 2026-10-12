#!/usr/bin/env python3
"""
Gerador de Imagens em Alta Resolução do Kit Gráfico Publicitário
Coleção Afinal — Volume 02: Afinal, o que é Indústria 4.0?
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = '/Users/lucas/Documents/ebooks/apps/industria-40'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
KIT_DIR = os.path.join(BASE_DIR, 'kit-publicitario')

COVER_PATH = os.path.join(ASSETS_DIR, 'capa.png')
PAGE2_PATH = os.path.join(ASSETS_DIR, 'pagina_2.png')
PAGE3_PATH = os.path.join(ASSETS_DIR, 'pagina_3.png')
PAGE8_PATH = os.path.join(ASSETS_DIR, 'pagina_8.png')

FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

ORANGE = (255, 138, 0)
ORANGE_DARK = (217, 110, 0)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
OFFWHITE = (247, 246, 242)
GRAY_LINE = (60, 60, 60)
GRAY_TEXT = (148, 163, 184)
CARD_BG = (25, 29, 38)

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_gear(draw, cx, cy, r_outer, r_inner, teeth=16, color=INK, center_hole_color=ORANGE):
    points = []
    for i in range(teeth * 2):
        angle = i * math.pi / teeth
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color)
    if center_hole_color:
        hole_r = r_inner * 0.45
        draw.ellipse([cx - hole_r, cy - hole_r, cx + hole_r, cy + hole_r], fill=center_hole_color)

def draw_concentric_arcs(draw, cx, cy, r_max, step=18, width=3, color=INK):
    for r in range(40, r_max, step):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)

def draw_dot_matrix(draw, x_start, y_start, rows=3, cols=4, gap=16, dot_r=4, color=WHITE):
    for r in range(rows):
        for c in range(cols):
            cx = x_start + c * gap
            cy = y_start + r * gap
            draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color)

def load_cover(target_width):
    if os.path.exists(COVER_PATH):
        cov = Image.open(COVER_PATH).convert('RGBA')
        w, h = cov.size
        target_height = int(target_width * (h / w))
        return cov.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return None

def load_page(page_path, target_width):
    if os.path.exists(page_path):
        p = Image.open(page_path).convert('RGBA')
        w, h = p.size
        target_height = int(target_width * (h / w))
        return p.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return None

print("Iniciando geração dos gráficos...")

# -------------------------------------------------------------
# GRUPO 01: IDENTIDADE E THUMBNAIL (1080 x 1080)
# -------------------------------------------------------------
print("Gerando Grupo 01...")
g1_dir = os.path.join(KIT_DIR, '01-identidade-e-thumbnail')

# Peça 01A: Thumbnail Kiwify com Mockup
t1 = Image.new('RGB', (1080, 1080), ORANGE)
d1 = ImageDraw.Draw(t1)
draw_concentric_arcs(d1, 950, 150, 400, step=22, width=4, color=INK)
draw_gear(d1, 150, 950, 260, 200, teeth=18, color=INK, center_hole_color=ORANGE)
draw_dot_matrix(d1, 80, 80, rows=3, cols=4, gap=22, dot_r=5, color=WHITE)

d1.text((80, 170), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 26), fill=INK)
d1.text((80, 205), "TECNOLOGIA · VOL. 02", font=get_font(FONT_REGULAR, 20), fill=INK)

cov = load_cover(460)
if cov:
    # Sombra dura brutalista
    shadow = Image.new('RGBA', cov.size, INK)
    t1.paste(shadow, (330 + 18, 300 + 18))
    t1.paste(cov, (330, 300), cov)

# Badge Kiwify
d1.rectangle([80, 940, 1000, 1010], fill=INK)
d1.text((100, 960), "EDIÇÃO DIGITAL · ACESSO IMEDIATO NA KIWIFY", font=get_font(FONT_BOLD, 22), fill=WHITE)
d1.text((950, 955), "↗", font=get_font(FONT_BOLD, 32), fill=ORANGE)
t1.save(os.path.join(g1_dir, 'peca-01-thumbnail-kiwify-com-mockup-1080x1080.png'), 'PNG')

# Peça 01B: Thumbnail Apenas Capa
t2 = Image.new('RGB', (1080, 1080), OFFWHITE)
d2 = ImageDraw.Draw(t2)
d2.rectangle([0, 0, 1080, 30], fill=ORANGE)
d2.rectangle([0, 1050, 1080, 1080], fill=ORANGE)
cov_full = load_cover(650)
if cov_full:
    shadow = Image.new('RGBA', cov_full.size, (17, 17, 17, 180))
    t2.paste(shadow, (215 + 14, 80 + 14))
    t2.paste(cov_full, (215, 80), cov_full)
t2.save(os.path.join(g1_dir, 'peca-01-thumbnail-kiwify-apenas-capa-1080x1080.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 02: MOCKUPS DO PRODUTO (1080 x 1080)
# -------------------------------------------------------------
print("Gerando Grupo 02...")
g2_dir = os.path.join(KIT_DIR, '02-mockups-do-produto')

# Mockup 1: Perspectiva 3D Discreta
m1 = Image.new('RGB', (1080, 1080), OFFWHITE)
dm1 = ImageDraw.Draw(m1)
draw_concentric_arcs(dm1, 150, 150, 250, step=20, width=2, color=(220, 220, 215))
draw_dot_matrix(dm1, 850, 80, rows=3, cols=4, gap=20, dot_r=4, color=ORANGE)

dm1.text((80, 80), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=INK)
dm1.text((80, 115), "MOCKUP EDITORIAL 3D // TECNOLOGIA · VOL. 02", font=get_font(FONT_REGULAR, 18), fill=GRAY_LINE)

cov_3d = load_cover(520)
if cov_3d:
    # Sombra difusa
    sh = Image.new('RGBA', (560, int(520 * 1.41) + 40), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.rectangle([20, 20, 540, int(520 * 1.41) + 20], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    m1.paste(sh, (270, 220), sh)
    m1.paste(cov_3d, (280, 220), cov_3d)

dm1.rectangle([80, 950, 1000, 952], fill=INK)
dm1.text((80, 970), "FORMATO DIGITAL EM PDF · COMPATÍVEL COM COMPUTADOR, TABLET E CELULAR", font=get_font(FONT_BOLD, 18), fill=INK)
m1.save(os.path.join(g2_dir, 'peca-02-mockup-perspectiva-3d-1080x1080.png'), 'PNG')

# Mockup 2: Tablet Editorial
m2 = Image.new('RGB', (1080, 1080), INK)
dm2 = ImageDraw.Draw(m2)
draw_concentric_arcs(dm2, 950, 950, 380, step=22, width=2, color=GRAY_LINE)
dm2.text((80, 80), "LEITURA DIGITAL ACESSÍVEL", font=get_font(FONT_BOLD, 22), fill=ORANGE)
dm2.text((80, 115), "Layout responsivo e visualização perfeita em qualquer dispositivo", font=get_font(FONT_REGULAR, 18), fill=WHITE)

# Tablet Bezel
tablet_w, tablet_h = 580, 780
tx, ty = (1080 - tablet_w)//2, 200
dm2.rectangle([tx-10, ty-10, tx+tablet_w+10, ty+tablet_h+10], fill=(45, 52, 64), outline=(70, 80, 98), width=3)
dm2.rectangle([tx, ty, tx+tablet_w, ty+tablet_h], fill=(0, 0, 0))
# Camera dot
dm2.ellipse([tx + tablet_w//2 - 4, ty + 12, tx + tablet_w//2 + 4, ty + 20], fill=(80, 80, 80))

cov_tab = load_cover(520)
if cov_tab:
    m2.paste(cov_tab, (tx + (tablet_w - 520)//2, ty + 40), cov_tab)
m2.save(os.path.join(g2_dir, 'peca-02-mockup-tablet-editorial-1080x1080.png'), 'PNG')

# Mockup 3: Livro com Páginas Internas Reais
m3 = Image.new('RGB', (1080, 1080), OFFWHITE)
dm3 = ImageDraw.Draw(m3)
dm3.text((80, 70), "POR DENTRO DA PUBLICAÇÃO", font=get_font(FONT_BOLD, 24), fill=INK)
dm3.text((80, 105), "Páginas reais: estudos de caso na Horizonte Componentes e infográficos práticos", font=get_font(FONT_REGULAR, 18), fill=GRAY_LINE)

p3 = load_page(PAGE3_PATH, 340) # Diagrama da fábrica
p8 = load_page(PAGE8_PATH, 340) # Linha do tempo 4 revoluções
cov_m3 = load_cover(400)

if p8:
    m3.paste(p8, (580, 200), p8)
    dm3.rectangle([580, 200, 580 + p8.size[0], 200 + p8.size[1]], outline=GRAY_LINE, width=1)
if p3:
    m3.paste(p3, (420, 300), p3)
    dm3.rectangle([420, 300, 420 + p3.size[0], 300 + p3.size[1]], outline=GRAY_LINE, width=1)
if cov_m3:
    shadow = Image.new('RGBA', cov_m3.size, (17, 17, 17, 220))
    m3.paste(shadow, (120 + 16, 250 + 16))
    m3.paste(cov_m3, (120, 250), cov_m3)

dm3.rectangle([80, 940, 1000, 1010], fill=ORANGE)
dm3.text((100, 962), "12 CAPÍTULOS · ROTEIRO DE 30 DIAS · 5 ESTUDOS DE CASO", font=get_font(FONT_BOLD, 22), fill=INK)
m3.save(os.path.join(g2_dir, 'peca-02-mockup-livro-com-paginas-reais-1080x1080.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 03: CRIATIVOS DE ANÚNCIOS
# -------------------------------------------------------------
print("Gerando Grupo 03...")
g3_dir = os.path.join(KIT_DIR, '03-criativos-de-anuncios')

# Peça 03A: Curiosidade 1080 x 1080
a3_sq = Image.new('RGB', (1080, 1080), INK)
da3_sq = ImageDraw.Draw(a3_sq)
draw_concentric_arcs(da3_sq, 900, 200, 360, step=22, width=3, color=ORANGE)
draw_gear(da3_sq, 160, 920, 240, 180, teeth=18, color=GRAY_LINE, center_hole_color=INK)
da3_sq.text((80, 80), "COLEÇÃO AFINAL · VOL. 02", font=get_font(FONT_BOLD, 22), fill=ORANGE)

da3_sq.text((80, 160), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=10)
da3_sq.text((80, 310), "Muito além dos robôs: entenda como dados e sistemas\ntransformam o chão de fábrica na prática.", font=get_font(FONT_REGULAR, 24), fill=GRAY_TEXT, spacing=8)

cov_a3 = load_cover(360)
if cov_a3:
    a3_sq.paste(cov_a3, (620, 420), cov_a3)
    da3_sq.rectangle([620, 420, 620+cov_a3.size[0], 420+cov_a3.size[1]], outline=ORANGE, width=2)

da3_sq.rectangle([80, 880, 520, 960], fill=ORANGE)
da3_sq.text((120, 905), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 28), fill=INK)
a3_sq.save(os.path.join(g3_dir, 'peca-03-curiosidade-1080x1080.png'), 'PNG')

# Peça 03B: Curiosidade 1080 x 1350
a3_feed = Image.new('RGB', (1080, 1350), INK)
da3_f = ImageDraw.Draw(a3_feed)
draw_concentric_arcs(da3_f, 950, 250, 420, step=24, width=3, color=ORANGE)
draw_gear(da3_f, 150, 1200, 280, 210, teeth=18, color=GRAY_LINE, center_hole_color=INK)
draw_dot_matrix(da3_f, 80, 80, rows=3, cols=4, gap=22, dot_r=5, color=WHITE)

da3_f.text((80, 180), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 02", font=get_font(FONT_BOLD, 24), fill=ORANGE)
da3_f.text((80, 240), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 62), fill=WHITE, spacing=12)
da3_f.text((80, 400), "Muito além dos robôs.", font=get_font(FONT_BOLD, 32), fill=ORANGE)
da3_f.text((80, 450), "Entenda como máquinas, pessoas e dados estão\ntransformando a produção sem promessas irreais.", font=get_font(FONT_REGULAR, 24), fill=GRAY_TEXT, spacing=8)

cov_a3_f = load_cover(460)
if cov_a3_f:
    a3_feed.paste(cov_a3_f, (310, 560), cov_a3_f)
    da3_f.rectangle([310, 560, 310+cov_a3_f.size[0], 560+cov_a3_f.size[1]], outline=ORANGE, width=2)

da3_f.rectangle([80, 1210, 1000, 1290], fill=ORANGE)
da3_f.text((430, 1235), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 30), fill=INK)
a3_feed.save(os.path.join(g3_dir, 'peca-03-curiosidade-1080x1350.png'), 'PNG')

# Peça 03C: Curiosidade 1080 x 1920 (Stories)
a3_st = Image.new('RGB', (1080, 1920), INK)
da3_s = ImageDraw.Draw(a3_st)
draw_concentric_arcs(da3_s, 540, 960, 500, step=26, width=3, color=ORANGE)
draw_gear(da3_s, 200, 1750, 300, 220, teeth=20, color=GRAY_LINE, center_hole_color=INK)

# Safe area topo
da3_s.text((100, 260), "COLEÇÃO AFINAL · VOL. 02", font=get_font(FONT_BOLD, 24), fill=ORANGE)
da3_s.text((100, 320), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 64), fill=WHITE, spacing=12)
da3_s.text((100, 480), "Muito além dos robôs.", font=get_font(FONT_BOLD, 34), fill=ORANGE)

cov_a3_s = load_cover(520)
if cov_a3_s:
    a3_st.paste(cov_a3_s, (280, 650), cov_a3_s)
    da3_s.rectangle([280, 650, 280+cov_a3_s.size[0], 650+cov_a3_s.size[1]], outline=ORANGE, width=3)

# Safe area base
da3_s.rectangle([100, 1540, 980, 1630], fill=ORANGE)
da3_s.text((390, 1570), "TOQUE PARA SABER MAIS ↗", font=get_font(FONT_BOLD, 26), fill=INK)
a3_st.save(os.path.join(g3_dir, 'peca-03-curiosidade-1080x1920.png'), 'PNG')

# Peça 04: Transformação 1080 x 1350
a4 = Image.new('RGB', (1080, 1350), ORANGE)
da4 = ImageDraw.Draw(a4)
draw_concentric_arcs(da4, 950, 200, 420, step=24, width=4, color=INK)
draw_gear(da4, 180, 1200, 280, 210, teeth=18, color=INK, center_hole_color=ORANGE)
draw_dot_matrix(da4, 80, 80, rows=3, cols=4, gap=22, dot_r=5, color=WHITE)

da4.text((80, 170), "COLEÇÃO AFINAL // TRANSFORMAÇÃO", font=get_font(FONT_BOLD, 24), fill=INK)
da4.text((80, 230), "A INDÚSTRIA\nESTÁ MUDANDO.", font=get_font(FONT_BOLD, 64), fill=INK, spacing=10)
da4.text((80, 380), "Entenda como.", font=get_font(FONT_BOLD, 40), fill=WHITE)
da4.text((80, 440), "Conectividade, dados e pessoas transformando\no processo produtivo do chão de fábrica.", font=get_font(FONT_REGULAR, 24), fill=INK, spacing=8)

cov_a4 = load_cover(460)
if cov_a4:
    shadow = Image.new('RGBA', cov_a4.size, INK)
    a4.paste(shadow, (310 + 16, 560 + 16))
    a4.paste(cov_a4, (310, 560), cov_a4)

da4.rectangle([80, 1220, 1000, 1290], fill=INK)
da4.text((380, 1245), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)
a4.save(os.path.join(g3_dir, 'peca-04-transformacao-1080x1350.png'), 'PNG')

# Peça 05: Para Profissionais 1080 x 1350
a5 = Image.new('RGB', (1080, 1350), OFFWHITE)
da5 = ImageDraw.Draw(a5)
draw_concentric_arcs(da5, 950, 200, 360, step=22, width=2, color=(220, 220, 215))
da5.rectangle([0, 0, 1080, 24], fill=ORANGE)

da5.text((80, 80), "PARA QUEM VIVE O CHÃO DE FÁBRICA", font=get_font(FONT_BOLD, 22), fill=ORANGE_DARK)
da5.text((80, 140), "VOCÊ TRABALHA\nNA INDÚSTRIA.\nMAS ENTENDE A TECNOLOGIA\nPOR TRÁS DELA?", font=get_font(FONT_BOLD, 46), fill=INK, spacing=10)
da5.text((80, 360), "Conheça a Indústria 4.0 de forma prática, sem jargões\ne com os desafios reais de quem produz.", font=get_font(FONT_REGULAR, 24), fill=GRAY_LINE, spacing=6)

cov_a5 = load_cover(440)
if cov_a5:
    shadow = Image.new('RGBA', cov_a5.size, (17, 17, 17, 160))
    a5.paste(shadow, (320 + 14, 470 + 14))
    a5.paste(cov_a5, (320, 470), cov_a5)

# 3 Perfis
da5.rectangle([80, 1100, 1000, 1160], fill=WHITE, outline=INK, width=2)
da5.text((100, 1120), "OPERADORES · TÉCNICOS · GESTORES · ESTUDANTES", font=get_font(FONT_BOLD, 20), fill=INK)

da5.rectangle([80, 1200, 1000, 1280], fill=INK)
da5.text((380, 1225), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)
a5.save(os.path.join(g3_dir, 'peca-05-profissionais-1080x1350.png'), 'PNG')

# Peça 06: Anúncio Educacional 1080 x 1350
a6 = Image.new('RGB', (1080, 1350), INK)
da6 = ImageDraw.Draw(a6)
da6.text((80, 80), "SISTEMA INTEGRADO // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=ORANGE)
da6.text((80, 140), "SENSORES. DADOS.\nAUTOMAÇÃO.\nINTELIGÊNCIA ARTIFICIAL.", font=get_font(FONT_BOLD, 50), fill=WHITE, spacing=10)
da6.text((80, 320), "Entenda como tudo isso se conecta.", font=get_font(FONT_BOLD, 28), fill=ORANGE)

# 4 Quadrantes
coords = [
    (80, 400, "01 / SENSORES", "Percebem o estado da máquina"),
    (560, 400, "02 / DADOS", "Circulam informação estruturada"),
    (80, 550, "03 / AUTOMAÇÃO", "Executam rotinas programadas"),
    (560, 550, "04 / DECISÃO", "Pessoas decidem com clareza")
]
for x, y, title, desc in coords:
    da6.rectangle([x, y, x+440, y+120], fill=CARD_BG, outline=GRAY_LINE, width=1)
    da6.text((x+20, y+25), title, font=get_font(FONT_BOLD, 20), fill=ORANGE)
    da6.text((x+20, y+65), desc, font=get_font(FONT_REGULAR, 17), fill=GRAY_TEXT)

cov_a6 = load_cover(360)
if cov_a6:
    a6.paste(cov_a6, (360, 720), cov_a6)
    da6.rectangle([360, 720, 360+cov_a6.size[0], 720+cov_a6.size[1]], outline=ORANGE, width=2)

da6.rectangle([80, 1220, 1000, 1290], fill=ORANGE)
da6.text((430, 1245), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 28), fill=INK)
a6.save(os.path.join(g3_dir, 'peca-06-educacional-sensores-dados-1080x1350.png'), 'PNG')

# Peça 07: Anúncio de Produto 1080 x 1350
a7 = Image.new('RGB', (1080, 1350), WHITE)
da7 = ImageDraw.Draw(a7)
draw_concentric_arcs(da7, 950, 200, 380, step=22, width=3, color=ORANGE)
da7.rectangle([0, 0, 1080, 24], fill=INK)

da7.text((80, 80), "PUBLICAÇÃO DIGITAL OFICIAL", font=get_font(FONT_BOLD, 22), fill=GRAY_LINE)
da7.text((80, 140), "CONHEÇA O E-BOOK.", font=get_font(FONT_BOLD, 60), fill=INK)
da7.text((80, 220), "Afinal, o que é Indústria 4.0?", font=get_font(FONT_BOLD, 32), fill=ORANGE_DARK)
da7.text((80, 275), "Um guia prático para compreender as tecnologias\ndas fábricas modernas.", font=get_font(FONT_REGULAR, 24), fill=GRAY_LINE, spacing=6)

cov_a7 = load_cover(500)
if cov_a7:
    shadow = Image.new('RGBA', cov_a7.size, INK)
    a7.paste(shadow, (290 + 16, 380 + 16))
    a7.paste(cov_a7, (290, 380), cov_a7)

da7.rectangle([80, 1180, 1000, 1260], fill=INK)
da7.text((440, 1205), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 30), fill=WHITE)
a7.save(os.path.join(g3_dir, 'peca-07-anuncio-produto-saiba-mais-1080x1350.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 04: POSTS EDUCATIVOS (1080 x 1080)
# -------------------------------------------------------------
print("Gerando Grupo 04...")
g4_dir = os.path.join(KIT_DIR, '04-posts-educativos')

# Post A: Não é apenas robótica
pA = Image.new('RGB', (1080, 1080), INK)
dpA = ImageDraw.Draw(pA)
draw_concentric_arcs(dpA, 900, 150, 350, step=22, width=3, color=ORANGE)
draw_gear(dpA, 150, 920, 220, 160, teeth=16, color=GRAY_LINE, center_hole_color=INK)
dpA.text((80, 80), "CONCEITO // COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 22), fill=ORANGE)
dpA.text((80, 150), "INDÚSTRIA 4.0\nNÃO É APENAS\nROBÓTICA.", font=get_font(FONT_BOLD, 58), fill=WHITE, spacing=10)
dpA.text((80, 360), "Uma fábrica pode ter braços robóticos e ainda assim operar\ncomo ilhas isoladas. A verdadeira transformação acontece quando\na informação circula entre máquinas, pessoas e sistemas.", font=get_font(FONT_REGULAR, 22), fill=GRAY_TEXT, spacing=8)

dpA.rectangle([80, 520, 1000, 720], fill=CARD_BG, outline=GRAY_LINE, width=1)
dpA.text((120, 560), "Robô tradicional = executa uma tarefa sem conversar.", font=get_font(FONT_BOLD, 22), fill=WHITE)
dpA.text((120, 620), "Fábrica 4.0 = máquinas e pessoas trocam dados em tempo real.", font=get_font(FONT_BOLD, 22), fill=ORANGE)

dpA.text((80, 820), "Leia a análise completa no e-book Afinal, o que é Indústria 4.0?", font=get_font(FONT_BOLD, 22), fill=WHITE)
dpA.rectangle([80, 880, 480, 960], fill=ORANGE)
dpA.text((120, 905), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 26), fill=INK)
pA.save(os.path.join(g4_dir, 'peca-11-post-a-nao-e-apenas-robotica-1080x1080.png'), 'PNG')

# Post B: Como uma máquina envia dados
pB = Image.new('RGB', (1080, 1080), ORANGE)
dpB = ImageDraw.Draw(pB)
draw_concentric_arcs(dpB, 950, 950, 400, step=22, width=4, color=INK)
draw_dot_matrix(dpB, 80, 80, rows=3, cols=4, gap=22, dot_r=5, color=WHITE)
dpB.text((80, 170), "TELEMETRIA INDUSTRIAL", font=get_font(FONT_BOLD, 22), fill=INK)
dpB.text((80, 230), "COMO UMA MÁQUINA\nCONSEGUE ENVIAR\nINFORMAÇÕES?", font=get_font(FONT_BOLD, 54), fill=INK, spacing=10)
dpB.text((80, 420), "A jornada do dado do sensor à tomada de decisão:", font=get_font(FONT_BOLD, 24), fill=WHITE)

flow = ["1. Sensor mede grandeza física", "2. Módulo converte em sinal digital", "3. Rede industrial transmite o dado", "4. Painel exibe alerta para a equipe"]
for i, step in enumerate(flow):
    sy = 480 + i * 80
    dpB.rectangle([80, sy, 1000, sy + 60], fill=INK)
    dpB.text((110, sy + 18), step, font=get_font(FONT_BOLD, 20), fill=WHITE)

dpB.text((80, 850), "Capítulo 5: Sensores, IIoT e monitoramento na prática.", font=get_font(FONT_BOLD, 22), fill=INK)
dpB.rectangle([80, 900, 480, 980], fill=WHITE)
dpB.text((120, 925), "CONHEÇA O LIVRO ↗", font=get_font(FONT_BOLD, 24), fill=INK)
pB.save(os.path.join(g4_dir, 'peca-11-post-b-como-maquina-envia-dados-1080x1080.png'), 'PNG')

# Post C: Importância dos dados
pC = Image.new('RGB', (1080, 1080), OFFWHITE)
dpC = ImageDraw.Draw(pC)
dpC.rectangle([0, 0, 1080, 24], fill=ORANGE)
dpC.text((80, 80), "GESTÃO E ESTRATÉGIA // CAPÍTULO 7", font=get_font(FONT_BOLD, 22), fill=ORANGE_DARK)
dpC.text((80, 140), "POR QUE OS DADOS\nSÃO TÃO IMPORTANTES\nNAS FÁBRICAS?", font=get_font(FONT_BOLD, 50), fill=INK, spacing=10)
dpC.text((80, 320), "Porque sem dados confiáveis, as decisões de produção\ncontinuam sendo tomadas por impressões e palpites.", font=get_font(FONT_REGULAR, 24), fill=GRAY_LINE, spacing=6)

# Tabela simplificada
dpC.rectangle([80, 420, 1000, 720], fill=WHITE, outline=INK, width=2)
dpC.rectangle([80, 420, 1000, 480], fill=INK)
dpC.text((110, 440), "DADO BRUTO  →  INFORMAÇÃO  →  INDICADOR (OEE)", font=get_font(FONT_BOLD, 20), fill=WHITE)
dpC.text((110, 520), "• 'Máquina 3 parou às 10h12' = Dado isolado", font=get_font(FONT_REGULAR, 20), fill=INK)
dpC.text((110, 580), "• '14h de parada por falta de material' = Informação contextualizada", font=get_font(FONT_REGULAR, 20), fill=INK)
dpC.text((110, 640), "• Decisão consciente entre Compras e PCP = Ação fundamentada", font=get_font(FONT_BOLD, 20), fill=ORANGE_DARK)

dpC.text((80, 800), "Aprenda a montar indicadores e checklists reais.", font=get_font(FONT_BOLD, 24), fill=INK)
dpC.rectangle([80, 860, 480, 940], fill=INK)
dpC.text((120, 885), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 26), fill=WHITE)
pC.save(os.path.join(g4_dir, 'peca-11-post-c-importancia-dos-dados-1080x1080.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 05: STORIES (1080 x 1920)
# -------------------------------------------------------------
print("Gerando Grupo 05...")
g5_dir = os.path.join(KIT_DIR, '05-stories')

# Story 1: Curiosidade
s1 = Image.new('RGB', (1080, 1920), INK)
ds1 = ImageDraw.Draw(s1)
draw_concentric_arcs(ds1, 540, 960, 450, step=26, width=3, color=GRAY_LINE)
ds1.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=ORANGE)
ds1.text((100, 320), "1 / 3", font=get_font(FONT_BOLD, 20), fill=GRAY_TEXT)
ds1.text((100, 600), "TODO MUNDO FALA EM\nINDÚSTRIA 4.0...", font=get_font(FONT_BOLD, 64), fill=WHITE, spacing=14)
ds1.text((100, 780), "Mas você sabe o que isso significa de verdade?", font=get_font(FONT_REGULAR, 30), fill=ORANGE)
draw_dot_matrix(ds1, 100, 1200, rows=4, cols=6, gap=26, dot_r=5, color=WHITE)
ds1.text((100, 1600), "TOQUE PARA CONTINUAR →", font=get_font(FONT_BOLD, 24), fill=GRAY_TEXT)
s1.save(os.path.join(g5_dir, 'peca-12-story-1-curiosidade-1080x1920.png'), 'PNG')

# Story 2: Descoberta
s2 = Image.new('RGB', (1080, 1920), ORANGE)
ds2 = ImageDraw.Draw(s2)
draw_concentric_arcs(ds2, 540, 960, 450, step=26, width=4, color=INK)
draw_gear(ds2, 180, 1750, 300, 220, teeth=18, color=INK, center_hole_color=ORANGE)
ds2.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=INK)
ds2.text((100, 320), "2 / 3", font=get_font(FONT_BOLD, 20), fill=WHITE)
ds2.text((100, 600), "MAS O QUE REALMENTE\nMUDA DENTRO DE\nUMA FÁBRICA?", font=get_font(FONT_BOLD, 60), fill=INK, spacing=14)
ds2.text((100, 840), "Não é encher o galpão de robôs.\nÉ fazer a informação circular entre\nmáquinas, sistemas e pessoas.", font=get_font(FONT_BOLD, 30), fill=WHITE, spacing=10)
ds2.text((100, 1600), "VEJA O GUIA COMPLETO →", font=get_font(FONT_BOLD, 24), fill=INK)
s2.save(os.path.join(g5_dir, 'peca-12-story-2-descoberta-1080x1920.png'), 'PNG')

# Story 3: Produto & CTA
s3 = Image.new('RGB', (1080, 1920), INK)
ds3 = ImageDraw.Draw(s3)
draw_concentric_arcs(ds3, 540, 850, 400, step=24, width=3, color=ORANGE)
ds3.text((100, 260), "COLEÇÃO AFINAL", font=get_font(FONT_BOLD, 24), fill=ORANGE)
ds3.text((100, 320), "3 / 3", font=get_font(FONT_BOLD, 20), fill=GRAY_TEXT)
ds3.text((100, 400), "DESCUBRA NO E-BOOK\nAFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 54), fill=WHITE, spacing=12)

cov_s3 = load_cover(480)
if cov_s3:
    s3.paste(cov_s3, (300, 680), cov_s3)
    ds3.rectangle([300, 680, 300+cov_s3.size[0], 680+cov_s3.size[1]], outline=ORANGE, width=3)

# CTA sticker safe
ds3.rectangle([100, 1540, 980, 1630], fill=ORANGE)
ds3.text((430, 1570), "SAIBA MAIS ↗", font=get_font(FONT_BOLD, 30), fill=INK)
ds3.text((340, 1650), "LINK DISPONÍVEL NA BIO E NO ANÚNCIO", font=get_font(FONT_BOLD, 18), fill=GRAY_TEXT)
s3.save(os.path.join(g5_dir, 'peca-12-story-3-produto-1080x1920.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 06: BANNERS PARA LANDING PAGE
# -------------------------------------------------------------
print("Gerando Grupo 06...")
g6_dir = os.path.join(KIT_DIR, '06-banners-landing-page')

# Peça 08A: Banner LP Desktop 1600 x 900
b8 = Image.new('RGB', (1600, 900), ORANGE)
db8 = ImageDraw.Draw(b8)
draw_concentric_arcs(db8, 1400, 200, 450, step=24, width=4, color=INK)
draw_gear(db8, 200, 850, 260, 190, teeth=18, color=INK, center_hole_color=ORANGE)

# Área esquerda para HTML (respiro)
db8.text((120, 120), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 02", font=get_font(FONT_BOLD, 22), fill=INK)
db8.text((120, 180), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 68), fill=INK, spacing=12)
db8.text((120, 350), "Entenda como máquinas, pessoas e dados estão\ntransformando o chão de fábrica.", font=get_font(FONT_REGULAR, 26), fill=WHITE, spacing=8)

# Botão reservado
db8.rectangle([120, 460, 460, 530], fill=INK)
db8.text((160, 482), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 24), fill=WHITE)

cov_b8 = load_cover(460)
if cov_b8:
    shadow = Image.new('RGBA', cov_b8.size, INK)
    b8.paste(shadow, (1020 + 16, 160 + 16))
    b8.paste(cov_b8, (1020, 160), cov_b8)
b8.save(os.path.join(g6_dir, 'peca-08-banner-lp-desktop-1600x900.png'), 'PNG')

# Peça 08B: Banner LP Mobile 1080 x 1350
b8_m = Image.new('RGB', (1080, 1350), ORANGE)
db8_m = ImageDraw.Draw(b8_m)
draw_concentric_arcs(db8_m, 950, 200, 380, step=22, width=3, color=INK)
db8_m.text((80, 120), "COLEÇÃO AFINAL // VOL. 02", font=get_font(FONT_BOLD, 24), fill=INK)
db8_m.text((80, 180), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 58), fill=INK, spacing=10)
db8_m.text((80, 330), "Máquinas, pessoas e dados no chão de fábrica.", font=get_font(FONT_REGULAR, 24), fill=WHITE)

cov_b8_m = load_cover(460)
if cov_b8_m:
    shadow = Image.new('RGBA', cov_b8_m.size, INK)
    b8_m.paste(shadow, (310 + 14, 420 + 14))
    b8_m.paste(cov_b8_m, (310, 420), cov_b8_m)

db8_m.rectangle([80, 1180, 1000, 1260], fill=INK)
db8_m.text((380, 1205), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)
b8_m.save(os.path.join(g6_dir, 'peca-08-banner-lp-mobile-1080x1350.png'), 'PNG')

# Peça 09A: Banner Promocional Laranja 1920 x 1080
b9_ora = Image.new('RGB', (1920, 1080), ORANGE)
db9_o = ImageDraw.Draw(b9_ora)
draw_concentric_arcs(db9_o, 1700, 250, 500, step=26, width=4, color=INK)
draw_gear(db9_o, 200, 950, 300, 220, teeth=20, color=INK, center_hole_color=ORANGE)

db9_o.text((140, 160), "COLEÇÃO AFINAL // LANÇAMENTO OFICIAL", font=get_font(FONT_BOLD, 26), fill=INK)
db9_o.text((140, 230), "O FUTURO DA INDÚSTRIA\nCOMEÇA PELO CONHECIMENTO.", font=get_font(FONT_BOLD, 68), fill=INK, spacing=12)
db9_o.text((140, 410), "Descubra como máquinas, pessoas e dados estão\ntransformando a produção.", font=get_font(FONT_REGULAR, 30), fill=WHITE, spacing=10)

db9_o.rectangle([140, 560, 540, 640], fill=INK)
db9_o.text((180, 585), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=WHITE)

cov_b9 = load_cover(520)
if cov_b9:
    shadow = Image.new('RGBA', cov_b9.size, INK)
    b9_ora.paste(shadow, (1260 + 18, 180 + 18))
    b9_ora.paste(cov_b9, (1260, 180), cov_b9)
b9_ora.save(os.path.join(g6_dir, 'peca-09-banner-promocional-laranja-1920x1080.png'), 'PNG')

# Peça 09B: Banner Promocional Preto 1920 x 1080
b9_blk = Image.new('RGB', (1920, 1080), INK)
db9_b = ImageDraw.Draw(b9_blk)
draw_concentric_arcs(db9_b, 1700, 250, 500, step=26, width=3, color=ORANGE)
draw_gear(db9_b, 200, 950, 300, 220, teeth=20, color=GRAY_LINE, center_hole_color=INK)

db9_b.text((140, 160), "COLEÇÃO AFINAL // LANÇAMENTO OFICIAL", font=get_font(FONT_BOLD, 26), fill=ORANGE)
db9_b.text((140, 230), "O FUTURO DA INDÚSTRIA\nCOMEÇA PELO CONHECIMENTO.", font=get_font(FONT_BOLD, 68), fill=WHITE, spacing=12)
db9_b.text((140, 410), "Descubra como máquinas, pessoas e dados estão\ntransformando a produção.", font=get_font(FONT_REGULAR, 30), fill=GRAY_TEXT, spacing=10)

db9_b.rectangle([140, 560, 540, 640], fill=ORANGE)
db9_b.text((180, 585), "CONHEÇA O E-BOOK ↗", font=get_font(FONT_BOLD, 28), fill=INK)

if cov_b9:
    b9_blk.paste(cov_b9, (1260, 180), cov_b9)
    db9_b.rectangle([1260, 180, 1260+cov_b9.size[0], 180+cov_b9.size[1]], outline=ORANGE, width=2)
b9_blk.save(os.path.join(g6_dir, 'peca-09-banner-promocional-preto-1920x1080.png'), 'PNG')

# -------------------------------------------------------------
# GRUPO 07: COMPARTILHAMENTO E OPEN GRAPH (1200 x 630)
# -------------------------------------------------------------
print("Gerando Grupo 07...")
g7_dir = os.path.join(KIT_DIR, '07-compartilhamento-open-graph')

og = Image.new('RGB', (1200, 630), WHITE)
dog = ImageDraw.Draw(og)
dog.rectangle([0, 0, 12, 630], fill=ORANGE)
draw_concentric_arcs(dog, 1100, 150, 300, step=20, width=2, color=ORANGE)

dog.text((80, 80), "COLEÇÃO AFINAL // TECNOLOGIA · VOL. 02", font=get_font(FONT_BOLD, 18), fill=GRAY_LINE)
dog.text((80, 130), "AFINAL, O QUE É\nINDÚSTRIA 4.0?", font=get_font(FONT_BOLD, 52), fill=INK, spacing=8)
dog.text((80, 270), "Entenda como máquinas, pessoas e dados estão\ntransformando o chão de fábrica.", font=get_font(FONT_REGULAR, 22), fill=GRAY_LINE, spacing=6)

# Badge
dog.rectangle([80, 380, 420, 430], fill=INK)
dog.text((100, 396), "E-BOOK EM PDF · GUIA PRÁTICO ↗", font=get_font(FONT_BOLD, 18), fill=WHITE)

cov_og = load_cover(360)
if cov_og:
    shadow = Image.new('RGBA', cov_og.size, INK)
    og.paste(shadow, (760 + 12, 70 + 12))
    og.paste(cov_og, (760, 70), cov_og)
og.save(os.path.join(g7_dir, 'peca-10-compartilhamento-og-1200x630.png'), 'PNG')

print("TODAS AS 21 ARTES FORAM GERADAS COM SUCESSO!")
