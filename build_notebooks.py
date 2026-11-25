#!/usr/bin/env python3
"""
Génère les 4 notebooks du Meetup à partir du code déjà testé dans demo/.
Chaque cellule de code est importée du module correspondant : pas de copier-coller,
donc pas de dérive entre le script et le notebook.

Usage : python build_notebooks.py
"""
from __future__ import annotations

import os

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
NB_DIR = os.path.join(HERE, "notebooks")
os.makedirs(NB_DIR, exist_ok=True)


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text: str):
    return nbf.v4.new_code_cell(text.strip())


def write(name: str, cells) -> None:
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    nb.metadata["language_info"] = {"name": "python"}
    path = os.path.join(NB_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"  écrit {path}")


# ---------------------------------------------------------------- notebook 1
def nb_matrices_in_llm():
    write(
        "01_matrices_in_llm.ipynb",
        [
            md("""
# 1 — Où se cachent les matrices dans un LLM ?

Objectif : montrer que derrière une phrase de 4 tokens, GPT-2 small (124 M de
paramètres) exécute une cinquantaine de produits matriciels et ~1 GFLOP.

On installe un *hook* PyTorch sur chaque couche linéaire, on lance un forward,
et on lit les formes d'entrée/sortie. Rien de magique : ce sont les mêmes GEMM
que ceux que Strassen et AlphaTensor cherchent à accélérer.
"""),
            code("""
import sys, torch, torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

PROMPT = "The city of Paris"
tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2").eval()
print("paramètres :", f"{sum(p.numel() for p in model.parameters()):,}")
"""),
            code("""
records = []

def hook(module, inp, out):
    x = inp[0]
    records.append((module.__class__.__name__, tuple(x.shape), tuple(out.shape)))

for _, mod in model.named_modules():
    if mod.__class__.__name__ in ("Linear", "Conv1D"):
        mod.register_forward_hook(hook)

inputs = tok(PROMPT, return_tensors="pt")
with torch.no_grad():
    model(**inputs)

print("tokens :", inputs["input_ids"].shape[1], "| couches linéaires :", len(records))
"""),
            code("""
total = 0
for i, (cls, ins, outs) in enumerate(records[:8], 1):
    flops = 2 * ins[0] * ins[1] * ins[-1] * outs[-1]
    total += flops
    print(f"{i:>2} {cls:<8} {str(ins):<18} -> {str(outs):<18} {flops/1e6:8.2f} MFLOPs")
print("...")
print("total affiché pour 8 couches :", f"{total/1e9:.3f} GFLOPs")
"""),
            md("""
## Ce qu'il faut retenir

- GPT-2 small a **12 blocs**, chacun avec 4 GEMM (attention QKV, projection de sortie,
  FFN up, FFN down) → 48 GEMM par token, plus la tête de sortie.
- Un LLM de 124 M de paramètres fait ~1 GFLOP pour 4 tokens. Un modèle de 400 G
  de paramètres (GPT-4 classe) en fait des milliers.
- **Toute** l'industrie de l'accélération IA est une industrie de multiplication
  matricielle. D'où l'intérêt d'un exposant plus petit que 3.
"""),
        ],
    )


# ---------------------------------------------------------------- notebook 2
def nb_strassen():
    write(
        "02_strassen.ipynb",
        [
            md("""
# 2 — Le tour de magie de Strassen (1969)

Deux matrices 2×2 demandent 8 multiplications scalaires avec la méthode scolaire.
Strassen en trouve 7. Appliqué récursivement, cela donne l'exposant log₂7 ≈ 2,807.

Puis on chronomètre : et on constate que Strassen est **plus lent** que NumPy.
"""),
            code("""
import sys
sys.path.insert(0, "../demo")
from strassen import (
    naive_products, strassen_products, strassen_additions,
    _strassen, _strassen_blas, _median_time,
)
import numpy as np, math

for k in range(1, 8):
    n = 2**k
    print(f"n={n:>4}  scolaire={naive_products(n):>12,}  strassen={strassen_products(n):>12,}")
"""),
            code("""
# Vérification exacte sur entiers
rng = np.random.default_rng(0)
A = rng.integers(-9, 9, (4, 4)).astype(np.int64)
B = rng.integers(-9, 9, (4, 4)).astype(np.int64)
C = _strassen(A, B, 1, [0])
print("égalité exacte :", np.array_equal(C, A @ B))
"""),
            code("""
# Le chrono qui contredit la théorie
for n in (256, 512, 1024):
    A = rng.standard_normal((n, n)); B = rng.standard_normal((n, n))
    t1 = _median_time(lambda: A @ B)
    t2 = _median_time(lambda: _strassen_blas(A, B, 256))
    print(f"n={n:>5}  BLAS {t1*1e3:7.1f} ms   Strassen {t2*1e3:7.1f} ms   x{t2/t1:.2f}")
"""),
            md("""
## Pourquoi cet écart ?

| Cause | Effet |
|---|---|
| Copies de blocs | 7 allocations par niveau de récursion |
| Localité cache | Strassen saute entre 7 sous-blocs → cache froid |
| Vectorisation | BLAS fait 8 multiplications par cycle, Strassen non |
| Constante | `T(n) = C·n^2.807` avec C très grand |

Un exposant est une **pente asymptotique**. À n = 1000, on est encore dans la
partie dominée par la constante.
"""),
        ],
    )


# ---------------------------------------------------------------- notebook 3
def nb_alphatensor():
    write(
        "03_alphatensor.ipynb",
        [
            md("""
# 3 — AlphaTensor : un algorithme = une décomposition de tenseur

On construit le tenseur de la multiplication 2×2 (4×4×4), on vérifie que la
décomposition scolaire (8 termes de rang 1) et celle de Strassen (7 termes)
reconstruisent bien ce tenseur.

C'est exactement le problème que résout AlphaTensor : trouver une décomposition
à *r* termes, avec *r* le plus petit possible, pour des tailles plus grandes.
"""),
            code("""
import sys
sys.path.insert(0, "../demo")
import numpy as np
from tensor_rank import (
    build_tensor, classical_terms, strassen_terms, reconstruct, operational_check,
)

T = build_tensor()
print("forme du tenseur :", T.shape)
print("termes non nuls  :", int(T.sum()))
"""),
            code("""
for name, terms in (("scolaire", classical_terms()), ("Strassen", strassen_terms())):
    Tm = reconstruct(terms)
    print(f"{name:<9} : {len(terms)} termes | reconstruit={np.array_equal(Tm, T)} | "
          f"matrices={operational_check(terms)}")
"""),
            md("""
## Ce que fait l'agent AlphaTensor

| Élément | Traduction |
|---|---|
| État | tenseur résiduel |
| Action | soustraire un terme de rang 1 (coefficients entiers) |
| Récompense | atteindre le tenseur nul en peu d'étapes |
| Résultat | algorithme de multiplication inédit |

Résultats publiés (2022) : 3×3 en **23** multiplications (au lieu de 27),
4×4 en 47 (au lieu de 64), 5×5 en 76 (au lieu de 125). Certains ont ensuite
été améliorés par des humains — la boucle est itérative.

## Pourquoi 2×2 ne suffit plus

Le rang du tenseur 2×2 est exactement **7** (démontré). Il n'existe pas de
décomposition à 6 termes. La recherche doit donc porter sur des tailles plus
grandes, ou sur des **puissances** de tenseurs — c'est là qu'apparaît ω.
"""),
        ],
    )


# ---------------------------------------------------------------- notebook 4
def nb_complexity():
    write(
        "04_complexity.ipynb",
        [
            md("""
# 4 — Comprendre la portée du 9/4

Trois chiffres : 3 (scolaire), 2,807 (Strassen), 2,25 (9/4).
Ce notebook chiffre ce que cela change, et pourquoi votre GPU ne verra
aucune différence.
"""),
            code("""
import math
EXPO = {"scolaire": 3.0, "Strassen": math.log2(7),
        "record 2026": 2.371177, "9/4": 2.25}
for n in (1e3, 1e6, 1e9):
    print(f"n={n:.0e}")
    for k, w in EXPO.items():
        print(f"   {k:<12} n^{w:.4f} = {n**w:.3e}")
"""),
            code("""
# Gain du 9/4 sur le record précédent
for n in (1e3, 1e6, 1e9, 1e12):
    print(f"n={n:>6.0e}  gain = x{n**(2.371177-2.25):.2f}")
"""),
            code("""
# Croisement galactique : quand un meilleur exposant devient plus rapide
for w, label in ((math.log2(7), "Strassen"), (2.25, "9/4")):
    for ratio in (10, 100, 1000):
        print(f"{label:<9} C/C0={ratio:>5} -> n* ~ {ratio**(1/(3-w)):.3e}")
"""),
            md("""
## Le piège à éviter en présentant

- **Ne pas** dire « l'IA a rendu les GPU 10× plus rapides » : faux.
- **Dire** : « la borne théorique descend ; l'ingénierie, elle, est bloquée par
  les constantes et la mémoire ».
- La borne inférieure du 24 novembre est une **revendication non vérifiée**.
  Le manuscrit d'octobre donnait un algorithme ; celui de novembre dit qu'on ne
  peut pas faire mieux. Les deux ne sont pas du même ordre de difficulté.
"""),
        ],
    )


if __name__ == "__main__":
    print("Génération des notebooks :")
    nb_matrices_in_llm()
    nb_strassen()
    nb_alphatensor()
    nb_complexity()
    print("Fait.")
