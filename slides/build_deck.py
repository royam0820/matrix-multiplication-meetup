#!/usr/bin/env python3
"""Deck Meetup « la révolution du 9/4 » — charte Code Academy 123 (v2026-11-01).

Aucune note de présentateur (Keynote les ignore).
Le déroulé oral est dans DEMO_LIVE_NOTES.md.
"""
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

NAVY = RGBColor(0x0D, 0x1B, 0x2A)
NAVY_PANEL = RGBColor(0x1B, 0x2D, 0x42)
NAVY_CARD = RGBColor(0x25, 0x32, 0x3F)
CREAM = RGBColor(0xF8, 0xF4, 0xEE)
GOLD = RGBColor(0xC9, 0xA8, 0x4C)
ORANGE = RGBColor(0xE8, 0x62, 0x1A)
TEAL = RGBColor(0x1D, 0x7A, 0x8A)
RED = RGBColor(0x8A, 0x20, 0x20)
GREY = RGBColor(0xD6, 0xDD, 0xE6)
FOOT = RGBColor(0x8F, 0xA1, 0xB3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

TITLE_FONT = "Cambria"
BODY_FONT = "Calibri"
CODE_FONT = "Courier New"
FOOTER_TEXT = "Code Academy 123 • www.codeacademy123.com • 06 02 88 10 31"
W, H = 13.333, 7.5
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(os.path.dirname(HERE), "figs")

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]


# ---------- primitives ----------
def slide(bg_color=CREAM):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg_color
    return s


def rect(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE, line=None, lw=1):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    return sh


def text(s, x, y, w, h, runs, size=16, color=WHITE, bold=False, italic=False,
         font=BODY_FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0,
         space_after=6):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)
    if isinstance(runs, str):
        runs = [(runs, {})]
    first = True
    for content, opts in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = opts.get("align", align)
        p.line_spacing = opts.get("spacing", spacing)
        p.space_after = Pt(opts.get("space_after", space_after))
        r = p.add_run()
        r.text = content
        f = r.font
        f.name = opts.get("font", font)
        f.size = Pt(opts.get("size", size))
        f.bold = opts.get("bold", bold)
        f.italic = opts.get("italic", italic)
        f.color.rgb = opts.get("color", color)
    return tb


def footer(s):
    text(s, 0, 7.06, W, 0.3, FOOTER_TEXT, size=10, color=FOOT, align=PP_ALIGN.CENTER)


def header(s, title, kicker=None, title_size=28):
    rect(s, 0, 0, W, 1.32, NAVY)
    rect(s, 0, 0, 0.085, 1.32, GOLD)
    if kicker:
        text(s, 0.5, 0.10, 11.5, 0.3, kicker.upper(), size=11, color=GOLD, bold=True)
        text(s, 0.5, 0.40, 12.2, 0.8, title, size=title_size, color=WHITE, font=TITLE_FONT, bold=True)
    else:
        text(s, 0.5, 0.22, 12.2, 0.9, title, size=title_size, color=WHITE, font=TITLE_FONT,
             bold=True, anchor=MSO_ANCHOR.MIDDLE)
    footer(s)


def key_message(s, msg, y=5.96, color=GOLD, text_color=NAVY, size=16):
    rect(s, 0.45, y, 12.43, 0.72, color)
    text(s, 0.6, y + 0.04, 12.1, 0.66, msg, size=size, color=text_color, bold=True,
         font=TITLE_FONT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def card(s, x, y, w, h, title_txt, body, accent=GOLD, title_size=17, body_size=14,
         fill=NAVY_PANEL, body_color=GREY):
    rect(s, x, y, w, 0.07, accent)
    rect(s, x, y + 0.07, w, h - 0.07, fill)
    text(s, x + 0.22, y + 0.2, w - 0.44, 0.45, title_txt, size=title_size, color=WHITE,
         bold=True, font=TITLE_FONT)
    text(s, x + 0.22, y + 0.72, w - 0.44, h - 0.85, body, size=body_size, color=body_color,
         spacing=1.05)


def bullets(s, x, y, w, items, size=15, gap=0.48, dot=GOLD):
    for i, item in enumerate(items):
        yy = y + i * gap
        rect(s, x, yy + 0.11, 0.11, 0.11, dot, shape=MSO_SHAPE.OVAL)
        text(s, x + 0.26, yy - 0.02, w - 0.26, gap, item, size=size, color=NAVY_CARD, spacing=1.02)


def stat(s, x, y, w, h, number, label, source=None, num_size=42, num_color=GOLD):
    rect(s, x, y, w, 0.07, GOLD)
    rect(s, x, y + 0.07, w, h - 0.07, NAVY_PANEL)
    text(s, x, y + 0.28, w, h * 0.45, number, size=num_size, color=num_color, bold=True,
         font=TITLE_FONT, align=PP_ALIGN.CENTER)
    text(s, x + 0.3, y + h * 0.52, w - 0.6, h * 0.4, label, size=12.5, color=WHITE,
         align=PP_ALIGN.CENTER, spacing=1.05)
    if source:
        text(s, x + 0.15, y + h - 0.4, w - 0.3, 0.32, source, size=9, color=FOOT,
             italic=True, align=PP_ALIGN.CENTER)


def code_block(s, x, y, w, h, code, ok=False):
    rect(s, x, y, w, h, NAVY_PANEL)
    rect(s, x, y, 0.06, h, GOLD if ok else RED)
    tb = s.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.12), Inches(w - 0.35), Inches(h - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(code.strip("\n").split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = line if line else " "
        r.font.name = CODE_FONT
        r.font.size = Pt(12)
        r.font.color.rgb = WHITE


def image(s, path, x, y, w=None, h=None):
    kw = {}
    if w:
        kw["width"] = Inches(w)
    if h:
        kw["height"] = Inches(h)
    s.shapes.add_picture(path, Inches(x), Inches(y), **kw)


def cover(title_lines, subtitle, badge):
    s = slide(NAVY)
    rect(s, 8.6, 0, 0.03, H, GOLD)
    rect(s, 0.62, 0.55, 4.2, 0.5, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, 0.62, 0.6, 4.2, 0.4, badge, size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.62, 1.5, 7.8, 2.7, "\n".join(title_lines), size=40, color=WHITE, bold=True,
         font=TITLE_FONT, spacing=1.03)
    text(s, 0.62, 4.2, 7.5, 1.0, subtitle, size=16, color=GOLD, italic=True, spacing=1.12)
    rect(s, 0.45, 5.45, 7.7, 0.015, GOLD)
    text(s, 0.62, 5.62, 7.4, 1.1, [("Anne-Marie Roy", {"size": 19, "color": WHITE, "underline": True,
                                                        "font": TITLE_FONT}),
                                    ("Fondatrice · Code Academy 123", {"size": 12.5, "color": GOLD})])
    # visuel : grille 8 → 7 points
    for r in range(4):
        for c in range(4):
            used = not (r == 3 and c == 3)
            rect(s, 9.3 + c * 0.8, 1.9 + r * 0.8, 0.12, 0.12,
                 GOLD if used else NAVY_CARD, shape=MSO_SHAPE.OVAL)
    text(s, 8.9, 5.42, 4.0, 0.9, "8 multiplications → 7\npuis 2,25 comme exposant", size=12.5,
         color=GOLD, italic=True, align=PP_ALIGN.CENTER)
    return s


def close_slide():
    s = slide(NAVY)
    rect(s, 0.62, 0.6, 3.2, 0.5, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, 0.62, 0.65, 3.2, 0.4, "MERCI !", size=13, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.62, 1.9, 7.4, 1.4, "Questions ?", size=52, color=WHITE, bold=True, font=TITLE_FONT)
    rect(s, 0.48, 3.3, 4.0, 0.02, GOLD)
    text(s, 0.62, 3.55, 11.8, 1.4,
         "Tout est reproductible : quatre notebooks, les scripts de démonstration,\n"
         "le simulateur et les fichiers Lean sont dans le dépôt du Meetup.",
         size=18, color=GREY, spacing=1.25)
    text(s, 0.62, 5.6, 7.0, 0.5, "Anne-Marie Roy · Code Academy 123", size=14, color=GOLD)
    return s


def backup_divider():
    s = slide(NAVY)
    text(s, 0, 2.7, W, 1.0, "BACKUP", size=54, color=WHITE, bold=True, font=TITLE_FONT,
         align=PP_ALIGN.CENTER)
    rect(s, 6.1, 3.9, 1.1, 0.03, GOLD)
    text(s, 0, 4.2, W, 0.6, "Les slides suivantes ne sont montrées que sur demande.",
         size=15, color=GOLD, italic=True, align=PP_ALIGN.CENTER)
    return s


# ================================================================ 1. couverture
cover(["Quand l'IA réinvente", "ses propres mathématiques"],
      "La révolution du 9/4 : de la multiplication matricielle à la découverte algorithmique,\n"
      "puis à la preuve formelle.",
      "MEETUP · 2026 · 2 HEURES")

# ================================================================ 2. trois verbes
s = slide(NAVY)
text(s, 0, 0.85, W, 0.9, "Trois verbes, un seul fil", size=34, color=WHITE, bold=True,
     font=TITLE_FONT, align=PP_ALIGN.CENTER)
rect(s, 6.17, 1.85, 1.0, 0.03, GOLD)
card(s, 0.75, 2.35, 3.85, 2.9, "CALCULER", "Exécuter des algorithmes\nconçus par des humains.\n\n"
     "O(n³) : huit multiplications\npour deux matrices 2×2.", accent=GREY, body_size=15)
card(s, 4.74, 2.35, 3.85, 2.9, "DÉCOUVRIR", "Explorer un espace combinatoire\net proposer des "
     "algorithmes\nque personne n'a écrits.\n\nAlphaTensor, AlphaEvolve.", accent=TEAL, body_size=15)
card(s, 8.73, 2.35, 3.85, 2.9, "VÉRIFIER", "Soumettre la découverte\nà un juge indépendant "
     "du modèle.\n\nLean ne fait pas confiance :\nil recalcule.", accent=GOLD, body_size=15)
text(s, 0, 5.75, W, 0.5, "Calculer · Découvrir · Vérifier", size=20, color=GOLD, italic=True,
     align=PP_ALIGN.CENTER)

# ================================================================ 3. ce qui s'est passé
s = slide()
header(s, "Ce qui s'est passé, en deux dates", "LE POINT DE DÉPART")
card(s, 0.6, 1.6, 6.0, 2.5, "2 OCTOBRE 2026", "Une borne supérieure : ω ≤ 9/4.\n\n"
     "Un algorithme explicite, donc une méthode\nque l'on peut en principe exécuter.",
     accent=TEAL, body_size=14.5)
card(s, 6.86, 1.6, 6.0, 2.5, "24 NOVEMBRE 2026", "La borne inférieure revendiquée :\n"
     "ω = 9/4 exactement, sur tout corps.\n\nAu moins ⌈n^2,25 / 2⌉ portes non scalaires.",
     accent=GOLD, body_size=14.5)
bullets(s, 0.7, 4.4, 12.0, [
    "Les deux textes sont des prépublications du dépôt public openai/math.",
    "Aucune évaluation par les pairs au 25 novembre 2026 — et une borne inférieure, c'est beaucoup plus lourd qu'un algorithme.",
    "Une formalisation Lean existe, mais partielle : circuits sans division, identités polynomiales formelles.",
], size=14, gap=0.52)
key_message(s, "Le résultat peut être révisé. La méthode — générer puis vérifier — est déjà là.", size=15.5)

# ================================================================ 4. pourquoi ça vous concerne
s = slide()
header(s, "Pourquoi cela vous concerne directement", "LE LIEN AVEC L'IA")
bullets(s, 0.7, 1.7, 7.4, [
    "Un transformer, c'est 95 % de produits matriciels : projections QKV, projections de sortie, deux couches FFN par bloc.",
    "L'entraînement fait les mêmes produits, en plus grand, avec des gradients en plus.",
    "L'inférence les refait, token après token, à chaque requête.",
    "Toute l'économie du GPU est donc une économie de GEMM : le cœur de métier de cuBLAS et de ses équivalents.",
], size=15, gap=0.82)
card(s, 8.5, 1.75, 4.2, 3.5, "LA QUESTION DU SOIR",
     "Une IA peut-elle améliorer\nl'algorithme qui la fait\ntourner ?\n\nEt si oui, qui vérifie\nque l'amélioration est\nréellement correcte ?",
     accent=GOLD, body_size=15)
key_message(s, "Améliorer la multiplication matricielle, c'est améliorer toute l'IA — pas un modèle en particulier.")

# ================================================================ 5. GPT-2
s = slide()
header(s, "124 millions de paramètres, quatre mots", "DÉMO 1 — OÙ SONT LES MATRICES")
text(s, 0.6, 1.55, 12.2, 0.5, "Prompt : « The city of Paris » — GPT-2 small, 4 tokens après tokenisation.",
     size=15, color=NAVY_CARD, italic=True)
stat(s, 0.7, 2.35, 3.8, 2.05, "49", "produits matriciels\ndans un seul forward", num_size=44)
stat(s, 4.78, 2.35, 3.8, 2.05, "0,99", "GFLOP pour\nquatre tokens", num_size=44)
stat(s, 8.86, 2.35, 3.8, 2.05, "124,4 M", "paramètres, dont\nla moitié en matrices", num_size=40)
text(s, 0.6, 4.75, 12.2, 0.9,
     "12 blocs × 4 GEMM (QKV, sortie d'attention, FFN up, FFN down) + la tête de sortie.\n"
     "Un modèle frontière fait dix mille fois cela, par token.", size=14.5, color=NAVY_CARD, spacing=1.15)
key_message(s, "Derrière une phrase de quatre mots : des dizaines de millions de multiplications.", size=15.5)

# ================================================================ 6. scolaire
s = slide()
header(s, "La méthode scolaire : huit multiplications", "CALCULER")
text(s, 0.65, 1.62, 6.2, 0.5, "Deux matrices 2×2, quatre résultats à calculer :", size=15, color=NAVY_CARD)
code_block(s, 0.65, 2.2, 6.1, 2.25,
           "c11 = a11*b11 + a12*b21\n"
           "c12 = a11*b12 + a12*b22\n"
           "c21 = a21*b11 + a22*b21\n"
           "c22 = a21*b12 + a22*b22\n"
           "\n"
           "→ 8 multiplications, 4 additions")
bullets(s, 7.15, 2.15, 5.6, [
    "C'est l'algorithme enseigné partout, et celui que le matériel optimise.",
    "Pour n×n : n³ multiplications. À n = 1000, un milliard.",
    "Pendant 57 ans, on a cherché mieux — sans jamais trouver d'algorithme « pratique ».",
], size=14.5, gap=0.95)
key_message(s, "8 multiplications pour 2×2. C'est le point de départ, et la référence.", size=15.5)

# ================================================================ 7. Strassen
s = slide()
header(s, "Strassen, 1969 : sept multiplications", "CALCULER — LE TOUR DE MAGIE")
image(s, os.path.join(FIGS, "fig_strassen.png"), 0.45, 1.55, w=7.6)
text(s, 8.3, 1.65, 4.5, 4.2,
     [("L'idée", {"bold": True, "size": 17, "color": NAVY, "space_after": 6}),
      ("On réorganise les calculs : chaque produit devient une combinaison de a et de b.",
       {"size": 14, "color": NAVY_CARD}),
      ("M1 = (a11+a22)(b11+b22)", {"size": 13, "color": NAVY_CARD, "font": CODE_FONT}),
      ("M2 = (a21+a22)·b11", {"size": 13, "color": NAVY_CARD, "font": CODE_FONT}),
      ("…", {"size": 13, "color": NAVY_CARD, "font": CODE_FONT}),
      ("M7 = (a12−a22)(b21+b22)", {"size": 13, "color": NAVY_CARD, "font": CODE_FONT}),
      ("En échange : 18 additions et soustractions, gratuites en 1969.",
       {"size": 14, "color": NAVY_CARD})], spacing=1.15)
key_message(s, "Sept au lieu de huit : un gain de 12,5 %. Appliqué récursivement, cela change tout.")

# ================================================================ 8. log2 7
s = slide()
header(s, "log₂7 = 2,807 : la récursion fait le reste", "CALCULER — L'EXPOSANT")
text(s, 0.6, 1.6, 12.2, 0.5, "On découpe chaque matrice en quatre blocs et on applique le tour de magie à chaque niveau.",
     size=15, color=NAVY_CARD)
rows = [("2", "8", "7"), ("16", "4 096", "2 401"), ("64", "262 144", "117 649"),
        ("256", "16 777 216", "5 764 801"), ("1024", "1 073 741 824", "282 475 249")]
x0, y0 = 1.5, 2.3
w1, w2, w3 = 2.6, 3.4, 3.4
rect(s, x0, y0, w1 + w2 + w3, 0.5, NAVY)
for label, xx, ww in (("n", x0, w1), ("scolaire (n³)", x0 + w1, w2), ("Strassen", x0 + w1 + w2, w3)):
    text(s, xx, y0 + 0.05, ww, 0.4, label, size=13, color=GOLD, bold=True, align=PP_ALIGN.CENTER)
for i, (n, sc, st) in enumerate(rows):
    yy = y0 + 0.5 + i * 0.5
    rect(s, x0, yy, w1 + w2 + w3, 0.5, NAVY_PANEL if i % 2 == 0 else NAVY_CARD)
    text(s, x0, yy + 0.1, w1, 0.35, n, size=14, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, x0 + w1, yy + 0.1, w2, 0.35, sc, size=14, color=GREY, align=PP_ALIGN.CENTER)
    text(s, x0 + w1 + w2, yy + 0.1, w3, 0.35, st, size=14, color=GOLD, bold=True, align=PP_ALIGN.CENTER)
text(s, 1.5, 5.42, 10.5, 0.5, "À chaque doublement de taille, le nombre de multiplications est multiplié par 7, pas par 8.",
     size=15, color=NAVY_CARD)
key_message(s, "C'est tout : T(2n) = 7·T(n) donne n^2,807 au lieu de n³.", size=16)

# ================================================================ 9. plus lent
s = slide()
header(s, "Et pourtant, Strassen est plus lent", "CALCULER — LE RETOURNEMENT")
stat(s, 0.7, 1.7, 3.7, 2.2, "340 ms", "numpy / BLAS\nà n = 2048", num_size=38)
stat(s, 4.75, 1.7, 3.7, 2.2, "490 ms", "Strassen, blocs BLAS\nà n = 2048", num_size=38, num_color=ORANGE)
stat(s, 8.8, 1.7, 3.7, 2.2, "1,44×", "plus lent, avec\nmoins d'opérations", num_size=38, num_color=ORANGE)
bullets(s, 0.7, 4.25, 12.0, [
    "Copies de blocs, localité mémoire dégradée, surcoût des appels récursifs.",
    "BLAS exécute huit multiplications par cycle et optimise le cache ; Strassen non.",
    "La pente mesurée sur BLAS entre n = 256 et n = 2048 est n^2,90 — pas n³, pas n^2,25.",
], size=14, gap=0.55)
key_message(s, "Un exposant est une pente quand n tend vers l'infini. À n = 2000, on est encore dans le mur des constantes.", size=15)

# ================================================================ 10. tenseur
s = slide()
header(s, "Un algorithme est une décomposition de tenseur", "DÉCOUVRIR — LA BONNE REPRÉSENTATION")
image(s, os.path.join(FIGS, "fig_tensor.png"), 0.75, 1.62, h=4.15)
text(s, 6.4, 1.62, 6.4, 4.3,
     [("Le passage qui change tout", {"bold": True, "size": 17, "color": NAVY, "space_after": 8}),
      ("Multiplier deux matrices, c'est contracter un tenseur fixe T avec les deux vecteurs de coefficients.",
       {"size": 14.5, "color": NAVY_CARD}),
      ("T[(i,k),(l,j),(i,j)] = 1  si k = l", {"size": 13.5, "font": CODE_FONT, "color": NAVY}),
      ("Trouver un algorithme = écrire T comme somme de termes de rang 1. Le nombre de termes = le nombre de multiplications.",
       {"size": 14.5, "color": NAVY_CARD}),
      ("Scolaire : 8 termes. Strassen : 7 termes. La vérification est un calcul de trois lignes.",
       {"size": 14.5, "color": NAVY_CARD})], spacing=1.2)
key_message(s, "Un algorithme n'est plus un programme : c'est une factorisation que l'on peut vérifier.", size=15.5)

# ================================================================ 11. 8 puis 7
s = slide()
header(s, "Huit termes, puis sept — et la vérification est Triviale", "DÉCOUVRIR — PREUVE EXÉCUTABLE")
code_block(s, 0.6, 1.6, 6.3, 2.3,
           "T = build_tensor()        # 4×4×4, 8 coefficients\n"
           "Tm = reconstruct(strassen_terms())\n"
           "assert (Tm == T).all()    # True\n"
           "assert operational_check(strassen_terms())", ok=True)
bullets(s, 7.25, 1.72, 5.4, [
    "La décomposition de Strassen reconstruit exactement le tenseur du produit matriciel.",
    "Vérifié sur matrices entières : égalité exacte, aucune tolérance flottante.",
    "Le rang du tenseur 2×2 est 7, démontré : aucune décomposition à 6 termes n'existe.",
], size=14.5, gap=0.95)
text(s, 0.6, 4.25, 12.2, 1.4,
     "Conséquence pour la recherche : inutile d'essayer de battre Strassen sur 2×2.\n"
     "La découverte doit se déplacer vers des tailles plus grandes — c'est exactement ce qu'a fait AlphaTensor.",
     size=15, color=NAVY_CARD, spacing=1.2)
key_message(s, "L'algorithme est vérifié, pas supposé. C'est la première fois dans l'exposé.", size=15.5)

# ================================================================ 12. AlphaTensor
s = slide()
header(s, "AlphaTensor, 2022 : l'IA entre dans l'espace de recherche", "DÉCOUVRIR — L'AGENT")
stat(s, 0.7, 1.7, 3.7, 2.15, "23", "multiplications pour 3×3\n(au lieu de 27)", num_size=42)
stat(s, 4.75, 1.7, 3.7, 2.15, "47", "pour 4×4\n(au lieu de 64)", num_size=42)
stat(s, 8.8, 1.7, 3.7, 2.15, "76", "pour 5×5\n(au lieu de 125)", num_size=42)
bullets(s, 0.7, 4.2, 12.0, [
    "État : tenseur résiduel. Action : soustraire un terme de rang 1. Objectif : tenseur nul en un minimum d'étapes.",
    "L'agent explore un espace combinatoire ; la récompense est le nombre d'étapes économisées.",
    "Certains algorithmes trouvés ont ensuite été améliorés par des humains — la boucle est itérative, pas magique.",
], size=14, gap=0.55)
key_message(s, "3×3 en 23 multiplications : un algorithme que personne n'avait écrit, et que l'on peut exécuter.", size=15.5)

# ================================================================ 13. mur du rang
s = slide(NAVY)
text(s, 0.9, 1.75, 11.5, 1.6, "« Sur 2×2, le rang est 7.\nIl n'existe pas d'algorithme à 6 multiplications. »",
     size=32, color=WHITE, bold=True, font=TITLE_FONT, align=PP_ALIGN.CENTER, spacing=1.15)
rect(s, 6.17, 3.6, 1.0, 0.03, GOLD)
text(s, 1.4, 4.0, 10.5, 1.4,
     "Démontré (Winograd 1971, repris par Landsberg). Ce n'est pas une limite de l'IA :\n"
     "c'est une limite mathématique du problème lui-même.",
     size=17, color=GREY, align=PP_ALIGN.CENTER, spacing=1.25)
text(s, 1.4, 5.6, 10.5, 0.6, "D'où la nécessité de changer d'échelle : tenseurs plus grands, ou puissances de tenseurs.",
     size=15, color=GOLD, italic=True, align=PP_ALIGN.CENTER)

# ================================================================ 14. puissances
s = slide()
header(s, "Alors on compose les tenseurs — et ω apparaît", "DÉCOUVRIR — VERS L'EXPOSANT")
text(s, 0.65, 1.65, 6.0, 3.6,
     [("T^⊗k", {"size": 26, "bold": True, "color": GOLD, "font": CODE_FONT, "space_after": 8}),
      ("On multiplie le tenseur par lui-même k fois. Un algorithme pour T^⊗k donne un algorithme pour des matrices k fois plus grandes.",
       {"size": 14.5, "color": NAVY_CARD}),
      ("Si le rang croît comme n^(ωk), alors ω est l'exposant de la multiplication matricielle.",
       {"size": 14.5, "color": NAVY_CARD}),
      ("Toute la théorie consiste à majorer (puis, depuis novembre, à minorer) cette croissance.",
       {"size": 14.5, "color": NAVY_CARD})], spacing=1.2)
card(s, 7.0, 1.7, 5.7, 3.4, "CE QUE CHERCHENT LES MATHÉMATICIENS",
     "Pas une matrice plus rapide,\nmais une famille d'algorithmes\ndont le coût asymptotique\ndescend.\n\n"
     "D'où la différence entre\n« plus rapide » et « meilleur exposant ».",
     accent=TEAL, body_size=14.5)
key_message(s, "n^ω : un seul nombre résume 57 ans de recherche en algèbre algorithmique.", size=15.5)

# ================================================================ 15. frise
s = slide()
header(s, "Trois chiffres pour cinquante-six ans", "SITUER")
image(s, os.path.join(FIGS, "fig_timeline.png"), 2.24, 1.5, h=3.9)
text(s, 0.6, 5.52, 12.2, 0.35, "Sources : table des bornes publiées (Wikipedia, consultée le 25/11/2026) ; dépôt openai/math pour 2026.",
     size=10, color=FOOT, italic=True)
key_message(s, "2,807 en 1969 · 2,371177 en août 2026 · 2,25 revendiqué en octobre, plancher en novembre.", size=14.5)

# ================================================================ 16. n = 10^9
s = slide()
header(s, "À n = 10⁹, cela représente quoi ?", "MESURER")
stat(s, 0.7, 1.75, 3.7, 2.3, "1,78e20", "multiplications\navec ω = 2,25", num_size=34)
stat(s, 4.75, 1.75, 3.7, 2.3, "5,6 M×", "mieux que\nl'algorithme scolaire", num_size=36, num_color=TEAL)
stat(s, 8.8, 1.75, 3.7, 2.3, "×12", "mieux que le record\nde 2,371177", num_size=36, num_color=ORANGE)
text(s, 0.65, 4.5, 12.1, 1.2,
     "Mais aucun gain perceptible avant n ≈ 10⁶, et aucune implémentation connue de ces algorithmes\n"
     "à ces tailles : le croisement avec BLAS se situe dans une zone où l'on ne calcule pas.",
     size=14.5, color=NAVY_CARD, spacing=1.2)
key_message(s, "Ce n'est pas une accélération. C'est un déplacement de la frontière théorique.", size=16)

# ================================================================ 17. ce que ça ne fait pas
s = slide()
header(s, "Ce que cela ne fait pas", "LE CADRE HONNÊTE")
for i, item in enumerate([
    "Aucun gain mesurable sur votre GPU aujourd'hui : les constantes dominent encore.",
    "Aucun algorithme publié, exécutable, pour les tailles réelles (les preuves sont non constructives à ce stade).",
    "Aucune validation par les pairs : la borne inférieure du 24 novembre reste une revendication.",
]):
    yy = 1.8 + i * 1.0
    rect(s, 0.7, yy, 0.5, 0.5, RED, shape=MSO_SHAPE.OVAL)
    text(s, 0.7, yy + 0.04, 0.5, 0.42, "✕", size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.42, yy - 0.02, 11.2, 0.9, item, size=15, color=NAVY_CARD, spacing=1.1)
for i, item in enumerate([
    "Une borne théorique qui déplace ce que l'on croyait possible.",
    "Une démonstration que la recherche mathématique assistée par IA produit des objets vérifiables.",
]):
    yy = 4.95 + i * 0.75
    rect(s, 0.7, yy + 0.02, 0.5, 0.5, GOLD, shape=MSO_SHAPE.OVAL)
    text(s, 0.7, yy + 0.06, 0.5, 0.42, "✓", size=17, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.42, yy, 11.2, 0.7, item, size=15, color=NAVY_CARD, spacing=1.1)
key_message(s, "Ce n'est pas une annonce produit. C'est une annonce mathématique — et elle se juge comme telle.", size=15)

# ================================================================ 18. confiance
s = slide()
header(s, "Peut-on faire confiance à une preuve produite par une IA ?", "VÉRIFIER")
card(s, 0.7, 1.65, 5.85, 3.2, "LE MODÈLE GÉNÉRATIF",
     "Il propose une démonstration.\n\nIl peut se tromper, inventer\nun lemme, ou passer à côté\ndu cas limite.\n\nIl ne sait pas qu'il se trompe.",
     accent=TEAL, body_size=14.5)
card(s, 6.78, 1.65, 5.85, 3.2, "LE VÉRIFICATEUR",
     "Il ne lit pas la démonstration\ncomme un texte : il la rejoue.\n\nSi une règle d'inférence manque,\nil refuse. Sans opinion,\nsans confiance accordée.",
     accent=GOLD, body_size=14.5)
text(s, 0.7, 4.95, 12.0, 0.5, "Les deux n'ont aucune raison de partager la même erreur — c'est tout l'intérêt du dispositif.",
     size=15, color=NAVY_CARD, italic=True)
key_message(s, "La bonne question n'est pas « l'IA a-t-elle raison ? » mais « qu'est-ce qui peut la contredire ? »", size=15)

# ================================================================ 19. preuve
s = slide()
header(s, "Une preuve, en une seconde", "VÉRIFIER — DÉMO EN DIRECT")
code_block(s, 0.6, 1.6, 7.9, 2.6,
           "import Mathlib\n"
           "\n"
           "theorem carre_somme (a b : ℝ) :\n"
           "    (a + b)^2 = a^2 + 2*a*b + b^2 := by\n"
           "  ring", ok=True)
text(s, 8.75, 1.7, 4.0, 3.2,
     [("Lean : ✔", {"size": 22, "bold": True, "color": TEAL, "space_after": 10}),
      ("`ring` normalise les deux membres dans l'anneau des polynômes et constate qu'ils sont identiques.",
       {"size": 14, "color": NAVY_CARD}),
      ("Pas de « je pense que ». Un calcul, et une réponse.",
       {"size": 14, "color": NAVY_CARD})], spacing=1.2)
bullets(s, 0.7, 4.55, 12.0, [
    "Le même `ring` prouve les quatre identités de Strassen — celles de la slide 7.",
    "Ce sont de vraies preuves, pas des tests : elles valent pour tous les anneaux commutatifs.",
], size=14.5, gap=0.6)
key_message(s, "Une seconde pour vérifier ce qu'un humain mettrait une heure à recalculer.", size=15.5)

# ================================================================ 20. erreur
s = slide()
header(s, "Et une erreur, en une seconde", "VÉRIFIER — LA DÉMONSTRATION QUI ÉCHOUE")
code_block(s, 0.6, 1.6, 7.9, 2.4,
           "theorem carre_somme_faux (a b : ℝ) :\n"
           "    (a + b)^2 = a^2 + 3*a*b + b^2 := by\n"
           "  ring\n"
           "\n"
           "error: ring_nf failed to close the goal", ok=False)
text(s, 8.75, 1.7, 4.0, 3.0,
     [("Lean : ✘", {"size": 22, "bold": True, "color": RED, "space_after": 10}),
      ("Le vérificateur ne « corrige » pas : il constate que le but reste ouvert.",
       {"size": 14, "color": NAVY_CARD}),
      ("Un modèle génératif, lui, produirait volontiers une démonstration plausible.",
       {"size": 14, "color": NAVY_CARD})], spacing=1.2)
key_message(s, "Il refuse. Et il a raison : c'est exactement ce qu'on lui demande.", size=16)

# ================================================================ 21. spec gap
s = slide(NAVY)
text(s, 0.9, 1.5, 11.5, 1.2, "Le point que personne ne voit venir", size=34, color=WHITE,
     bold=True, font=TITLE_FONT, align=PP_ALIGN.CENTER)
rect(s, 6.17, 2.65, 1.0, 0.03, GOLD)
rect(s, 1.3, 3.0, 10.7, 1.7, NAVY_PANEL)
rect(s, 1.3, 3.0, 10.7, 0.07, GOLD)
text(s, 1.6, 3.2, 10.1, 1.4,
     "Lean vérifie que le théorème découle des axiomes.\n"
     "Il ne vérifie pas que le théorème formalisé correspond au problème qui vous intéresse.",
     size=19, color=WHITE, spacing=1.3)
text(s, 1.3, 5.05, 10.7, 1.0,
     "C'est le specification gap. On peut prouver parfaitement… la mauvaise chose.",
     size=18, color=GOLD, italic=True, align=PP_ALIGN.CENTER)

# ================================================================ 22. merci
close_slide()

# ================================================================ BACKUP
backup_divider()

# ---- B1 quiz
s = slide()
header(s, "Quiz — les quatre questions", "BACKUP")
qs = [("1. Multiplications scalaires pour deux matrices 2×2 (classique) ?", "8"),
      ("2. Quand n double, les multiplications de Strassen sont multipliées par…", "7"),
      ("3. Un meilleur exposant garantit-il une exécution plus rapide ?", "Non"),
      ("4. Une preuve Lean garantit-elle que l'énoncé correspond au problème réel ?", "Non")]
for i, (q, a) in enumerate(qs):
    yy = 1.6 + i * 1.05
    text(s, 0.65, yy, 10.3, 0.8, q, size=14.5, color=NAVY_CARD)
    rect(s, 11.15, yy + 0.02, 1.55, 0.6, GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, 11.15, yy + 0.08, 1.55, 0.45, a, size=15, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.65, 5.9, 12.0, 0.5, "Question 4 : c'est le specification gap — Lean valide la logique, pas l'adéquation au problème.",
     size=12.5, color=FOOT, italic=True)

# ---- B2 rang
s = slide()
header(s, "Pourquoi 7 et pas 6 ?", "BACKUP")
bullets(s, 0.7, 1.7, 12.0, [
    "Wongraf (1971) puis Landsberg démontrent que le rang du tenseur de multiplication 2×2 vaut exactement 7.",
    "Une décomposition à 6 termes de rang 1 est impossible — ce n'est pas une question de puissance de calcul.",
    "Le rang de bord vaut aussi 7 sur 2×2 : même en approximant, on ne descend pas.",
    "Conséquence : la recherche doit porter sur des tenseurs plus grands, ou sur des puissances de tenseurs (rang asymptotique).",
], size=14.5, gap=0.85)
key_message(s, "C'est une borne dure. Elle explique pourquoi AlphaTensor attaque 3×3, 4×4 et 5×5.", size=15)

# ---- B3 périmètre OpenAI
s = slide()
header(s, "Périmètre exact de la formalisation OpenAI", "BACKUP")
bullets(s, 0.7, 1.7, 12.0, [
    "Théorème `square_exponent` : formalOmega F 1 1 1 = 9/4, dans la bibliothèque lean/ du dépôt openai/math.",
    "Modèle formalisé : circuits arithmétiques sans division, identités polynomiales formelles sur un corps quelconque.",
    "Le dépôt indique lui-même que la formalisation est partielle : tout le manuscrit n'est pas formalisé.",
    "Aucune reproduction indépendante publique au 25 novembre 2026 ; aucune évaluation par les pairs.",
], size=14.5, gap=0.85)
key_message(s, "« Vérifié par Lean » ne veut pas dire « manuscrit entièrement formalisé ».", size=15)

# ---- B4 croisement
s = slide()
header(s, "Le croisement galactique, en formule", "BACKUP")
code_block(s, 0.7, 1.65, 7.5, 2.0,
           "T(n) = C · n^w        (algorithme)\n"
           "T₀(n) = C₀ · n³       (BLAS)\n"
           "\n"
           "n* = (C / C₀)^(1 / (3 − w))")
rows = [("Strassen, C/C₀ = 10", "n* ≈ 1,6·10⁵"), ("Strassen, C/C₀ = 100", "n* ≈ 2,4·10¹⁰"),
        ("9/4, C/C₀ = 100", "n* ≈ 4,6·10²"), ("9/4, C/C₀ = 1000", "n* ≈ 1,0·10⁴")]
for i, (k, v) in enumerate(rows):
    yy = 1.7 + i * 0.62
    text(s, 8.6, yy, 3.4, 0.5, k, size=13.5, color=NAVY_CARD)
    text(s, 11.6, yy, 1.5, 0.5, v, size=13.5, color=NAVY, bold=True)
text(s, 0.7, 4.15, 12.0, 1.2,
     "Les deux dernières lignes sont calculées à constante égale — ce que la théorie ne permet pas de supposer :\n"
     "les algorithmes sous-cubiques connus ont des constantes énormes, et une mauvaise localité mémoire.",
     size=13.5, color=NAVY_CARD, spacing=1.2)

# ---- B5 historique
s = slide()
header(s, "Historique des bornes supérieures publiées", "BACKUP")
hist = [("1969", "Strassen", "2,807"), ("1981", "Schönhage", "2,548"),
        ("1990", "Coppersmith–Winograd", "2,3755"), ("2010", "Stothers", "2,3737"),
        ("2014", "Le Gall", "2,3729"), ("2021", "Alman–Williams", "2,37286"),
        ("2026", "record publié (AlphaEvolve)", "2,371177"),
        ("2026", "OpenAI (revendiqué)", "2,25")]
for i, (year, who, val) in enumerate(hist):
    yy = 1.55 + i * 0.56
    bg = NAVY if i % 2 == 0 else NAVY_CARD
    rect(s, 0.7, yy, 12.0, 0.56, bg)
    text(s, 0.9, yy + 0.1, 1.4, 0.35, year, size=13.5, color=GOLD, bold=True)
    text(s, 2.4, yy + 0.1, 8.0, 0.35, who, size=13.5, color=WHITE)
    text(s, 10.6, yy + 0.1, 1.9, 0.35, val, size=13.5, color=GOLD, bold=True, align=PP_ALIGN.RIGHT)

# ---- B6 AlphaEvolve
s = slide()
header(s, "AlphaEvolve : la génération, avant la vérification", "BACKUP")
bullets(s, 0.7, 1.75, 12.0, [
    "Agent de programmation évolutionnaire bâti sur Gemini : il fait muter du code, l'évalue, garde les meilleurs.",
    "C'est cette famille d'approches qui porte la borne de 2,371177 publiée en août 2026.",
    "Différence avec le 9/4 : AlphaEvolve produit des algorithmes exécutables ; la revendication de novembre porte sur une borne inférieure, donc sur une preuve.",
    "Les deux illustrent le même déplacement : la machine ne calcule plus seulement, elle explore et démontre.",
], size=14.5, gap=0.9)
key_message(s, "Générer est devenu routinier. Vérifier reste le goulot d'étranglement.", size=15)

out = os.path.join(HERE, "deck_9_4_meetup.pptx")
prs.save(out)
print(f"{len(prs.slides.__iter__.__self__._sldIdLst)} slides → {out}")
