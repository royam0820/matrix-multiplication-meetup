#!/usr/bin/env python3
"""Figures du deck 9/4 — palette Code Academy 123."""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

NAVY = "#0D1B2A"
PANEL = "#1B2D42"
CREAM = "#F8F4EE"
GOLD = "#C9A84C"
TEAL = "#1D7A8A"
ORANGE = "#E8621A"
GREY = "#8FA1B3"
RED = "#8A2020"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("  ", path)


# ---------------------------------------------------------------- 1. Strassen
def fig_strassen():
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # Gauche : 8 produits scolaires
    ax.text(0.15, 4.75, "SCOLAIRE — 8 MULTIPLICATIONS", color=NAVY, fontsize=13, weight="bold")
    for k in range(8):
        i, j = divmod(k, 4)
        x = 0.25 + j * 0.82
        y = 3.55 - i * 0.85
        ax.add_patch(Rectangle((x, y), 0.7, 0.6, facecolor=GREY, edgecolor=NAVY, lw=1))
        ax.text(x + 0.35, y + 0.3, "a·b", ha="center", va="center", fontsize=11, color=NAVY)
    ax.text(0.15, 1.55, "8 = 2³ produits scalaires\npour deux matrices 2×2", color=PANEL, fontsize=11)

    # Droite : 7 combinaisons
    ax.text(5.3, 4.75, "STRASSEN — 7 MULTIPLICATIONS", color=GOLD, fontsize=13, weight="bold")
    for k in range(7):
        x = 5.4 + (k % 4) * 1.05
        y = 3.55 - (k // 4) * 1.0
        ax.add_patch(Rectangle((x, y), 0.9, 0.7, facecolor=PANEL, edgecolor=GOLD, lw=1.2))
        ax.text(x + 0.45, y + 0.35, f"M{k+1}", ha="center", va="center", fontsize=12,
                color="#FFFFFF", weight="bold")
    ax.text(5.3, 1.55, "7 = 2^log₂7  →  exposant 2,807\nchaque M est une combinaison\nde a et de b",
            color=PANEL, fontsize=11)

    ax.add_patch(FancyArrowPatch((4.55, 2.6), (5.05, 2.6), arrowstyle="->", color=GOLD, lw=2.5))
    ax.text(2.9, 0.45, "log₂7 = 2,807355", color=NAVY, fontsize=20, weight="bold")
    save(fig, "fig_strassen.png")


# ---------------------------------------------------------------- 2. tenseur
def fig_tensor():
    """Les 8 coefficients non nuls du tenseur 2×2, colorés par coefficient de C."""
    fig, ax = plt.subplots(figsize=(6.0, 4.8))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    A_ORDER = ["a11", "a12", "a21", "a22"]
    B_ORDER = ["b11", "b12", "b21", "b22"]
    # (ligne A, colonne B) -> coefficient de C
    cells = {
        ("a11", "b11"): "c11", ("a11", "b12"): "c12",
        ("a12", "b21"): "c11", ("a12", "b22"): "c12",
        ("a21", "b11"): "c21", ("a21", "b12"): "c22",
        ("a22", "b21"): "c21", ("a22", "b22"): "c22",
    }
    colors = {"c11": TEAL, "c12": GOLD, "c21": ORANGE, "c22": GREY}

    for r, a in enumerate(A_ORDER):
        for c, b in enumerate(B_ORDER):
            y = 3 - r
            if (a, b) in cells:
                key = cells[(a, b)]
                ax.add_patch(Rectangle((c - 0.44, y - 0.44), 0.88, 0.88,
                                       facecolor=colors[key], alpha=0.9,
                                       edgecolor=NAVY, lw=1.2))
                ax.text(c, y, key, ha="center", va="center", fontsize=11,
                        color=NAVY, weight="bold")
            else:
                ax.add_patch(Rectangle((c - 0.44, y - 0.44), 0.88, 0.88,
                                       facecolor="white", alpha=0.55,
                                       edgecolor=GREY, lw=0.8, ls=(0, (2, 3))))

    ax.set_xlim(-0.65, 3.65)
    ax.set_ylim(-0.65, 3.65)
    ax.set_xticks(range(4)); ax.set_yticks(range(4))
    ax.set_xticklabels(B_ORDER, fontsize=11, color=NAVY)
    ax.set_yticklabels(A_ORDER, fontsize=11, color=NAVY)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.set_xlabel("coefficients de B", color=PANEL, fontsize=11)
    ax.set_ylabel("coefficients de A", color=PANEL, fontsize=11)
    ax.set_title("Le tenseur 2×2 : 8 coefficients = 8 produits", color=NAVY,
                 fontsize=13, weight="bold", pad=12)
    save(fig, "fig_tensor.png")


# ---------------------------------------------------------------- 3. frise
def fig_timeline():
    """Frise en positions ordinales : les deux dates de 2026 seraient sinon collées."""
    fig, ax = plt.subplots(figsize=(10.6, 4.0))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(-0.6, 4.9)
    ax.set_ylim(2.16, 3.12)
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(axis="x", length=0, colors=NAVY, labelsize=11)

    pts = [
        (0, 3.0, "1969", "Strassen\n3 → 2,807", GOLD, 20),
        (1, 2.3755, "1990", "Coppersmith–Winograd\n2,3755", TEAL, 20),
        (2, 2.371177, "août 2026", "record publié\n2,371177", ORANGE, 20),
        (3, 2.25, "oct. / nov. 2026", "OpenAI\n9/4 = 2,25", GOLD, 20),
    ]
    for x, y, date, label, c, dy in pts:
        ax.plot([x], [y], "o", ms=14, color=c, markeredgecolor=NAVY, markeredgewidth=1.3, zorder=3)
        ax.text(x, 2.185, date, ha="center", va="bottom", fontsize=10.5, color=PANEL)
        ax.text(x, y + 0.035, label, ha="center", va="bottom", fontsize=10.5,
                color=NAVY, weight="bold" if "OpenAI" in label else "normal")

    ax.axhline(2.25, color=GOLD, lw=1.3, ls=(0, (6, 5)), alpha=0.75, zorder=1)
    ax.text(4.35, 2.256, "plancher\nrevendiqué", color=GOLD, fontsize=10, va="bottom", ha="center",
            weight="bold")
    ax.set_title("56 ans pour descendre de 3 à 2,25", color=NAVY, fontsize=15, weight="bold", pad=8)
    save(fig, "fig_timeline.png")


if __name__ == "__main__":
    print("Figures :")
    fig_strassen()
    fig_tensor()
    fig_timeline()
