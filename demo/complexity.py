#!/usr/bin/env python3
"""
Démo 4 — Comprendre la portée du 9/4 (et ses limites).

Trois idées, dans l'ordre :
  1. ce que change un exposant, chiffré, pour des tailles concrètes ;
  2. l'écart réel entre 2,371177 et 2,25 : dérisoire à petite taille,
     décisif à très grande taille ;
  3. le « croisement galactique » : pourquoi un meilleur exposant ne se
     traduit pas par un programme plus rapide aujourd'hui.

Sortie : out/complexite.csv, out/complexite.png

Usage :
    python demo/complexity.py
"""
from __future__ import annotations

import csv
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")

# Exposants, avec leur provenance
EXPO = {
    "scolaire (n^3)": 3.0,
    "Strassen 1969": math.log2(7),            # 2.807354922…
    "record public 2026": 2.371177,            # meilleure borne haute publiée avant oct.
    "9/4 (OpenAI oct. 2026)": 2.25,
}


def human(x: float) -> str:
    if x < 1e6:
        return f"{x:,.0f}"
    return f"{x:.3e}"


def table() -> list[dict]:
    rows = []
    ns = [10**k for k in (3, 6, 9, 12, 15)]
    print("=" * 84)
    print("  NOMBRE D'OPERATIONS SCALAIRES POUR DEUX MATRICES n x n")
    print("=" * 84)
    header = f"{'n':>6} " + " ".join(f"{name:>22}" for name in EXPO)
    print(header)
    for n in ns:
        line = f"{n:>6.0e} " + " ".join(f"{n**w:>22.3e}" for w in EXPO.values())
        print(line)
        rows.append({"n": n, **{name: n**w for name, w in EXPO.items()}})
    print()

    print("  Division par 2 du nombre d'operations, cela veut dire quoi ?")
    print("  A n = 10^9 : 1,78e20 multiplications (9/4) au lieu de 1,00e27 (scolaire).")
    print("  Ce n'est pas 5 % de mieux : c'est un facteur 5,6 millions.")
    print()

    # Gain du 9/4 sur le record précédent, en fonction de n
    print("  Gain 9/4 face au record 2,371177 :")
    for n in (1e3, 1e6, 1e9, 1e12):
        gain = n ** (2.371177 - 2.25)
        print(f"    n = {n:>6.0e} : x{gain:>8.2f}")
    print("  Aucun gain avant n ~ 10^6. Voilà pourquoi votre GPU ne va pas accélérer.")
    print()

    # Borne inférieure revendiquée
    print("  La borne inferieure revendiquee le 24 novembre 2026 :")
    print("    au moins ceil(n^(9/4) / 2) portes de multiplication NON scalaire,")
    print("    pour tout n >= 2, dans le modele des circuits arithmetiques formels.")
    for n in (2, 4, 8, 16):
        print(f"    n = {n:>2} : borne >= {math.ceil(n**2.25 / 2):>6,}"
              f"   (algorithmes connus : {n**3:>5,} avec le scolaire)")
    print("  A n = 2, la borne dit 3 ; le rang exact est 7. La force de l'enonce")
    print("  est asymptotique, pas numerique. C'est un point a dire clairement.")
    print()
    return rows


def crossover() -> None:
    print("=" * 84)
    print("  LE CROISEMENT GALACTIQUE")
    print("=" * 84)
    print("  Un algorithme d'exposant w s'ecrit  T(n) = C * n^w.")
    print("  Il bat BLAS (T = C0 * n^3) seulement au-dela de :")
    print("      n* = (C / C0)^(1 / (3 - w))")
    print()
    print("  En pratique, pour un algorithme recursif en blocs, C/C0 est de l'ordre")
    print("  de 10 a 1000 (copies, surcout d'appels, moins bonne localite cache).")
    for w, label in ((math.log2(7), "Strassen (2,807)"), (2.25, "9/4 (2,25)")):
        for ratio in (10, 100, 1000):
            n_star = ratio ** (1 / (3 - w))
            print(f"    {label:<18} C/C0 = {ratio:>5}  ->  n* ~ {n_star:>10.3e}")
    print()
    print("  Strassen est utilise en pratique... avec une coupure recursive a 128-512")
    print("  et seulement sur de tres gros produits. Le reste du temps, c'est BLAS.")
    print()


def plot() -> None:
    os.makedirs(OUT, exist_ok=True)
    ns = [10 ** (3 + 0.05 * k) for k in range(0, 241)]  # 1e3 → ~1e15
    plt.figure(figsize=(9, 5.2))
    styles = {
        "scolaire (n^3)": ("#8FA1B3", "--"),
        "Strassen 1969": ("#1D7A8A", "-"),
        "record public 2026": ("#E8621A", "-"),
        "9/4 (OpenAI oct. 2026)": ("#C9A84C", "-"),
    }
    for name, w in EXPO.items():
        color, ls = styles[name]
        plt.plot(ns, [n**w for n in ns], ls, color=color, lw=2.2,
                 label=f"{name}  (w = {w:.4f})" if w != 3 else f"{name}  (w = 3)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("taille n de la matrice (n x n)")
    plt.ylabel("multiplications scalaires")
    plt.title("Ce que change un exposant : n^3, n^2,807, n^2,371, n^2,25")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend(frameon=False, fontsize=9)
    plt.tight_layout()
    path = os.path.join(OUT, "complexite.png")
    plt.savefig(path, dpi=160)
    plt.close()
    print(f"  Figure ecrite dans {path}")


def main() -> None:
    rows = table()
    crossover()
    os.makedirs(OUT, exist_ok=True)
    csv_path = os.path.join(OUT, "complexite.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"  Tableau ecrit dans {csv_path}")
    plot()


if __name__ == "__main__":
    main()
