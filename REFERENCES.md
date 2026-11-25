# REFERENCES — sources primaires

Toutes les affirmations du kit doivent pouvoir être rattachées à une ligne ci-dessous.
Vérifié le 25 novembre 2026.

## La découverte

**1. Borne supérieure (2 octobre 2026)**
OpenAI, *An Upper Bound of 9/4 for the Matrix Multiplication Exponent*.
- PDF : https://github.com/openai/math/blob/main/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/paper.pdf
- Contenu : un algorithme dont l'exposant est ≤ 2,25 (sur ℂ).
- Ce que ça ne dit pas : rien sur l'optimalité.

**2. Borne inférieure (24 novembre 2026)**
OpenAI, *The matrix multiplication exponent is nine fourths*.
- PDF : https://github.com/openai/math/blob/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/paper.pdf
- README du manuscrit : https://github.com/openai/math/tree/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026
- Revendication exacte : « l'exposant de la multiplication matricielle carrée est 9/4 sur tout corps » ;
  pour tout n ≥ 2, au moins ⌈n^(9/4)/2⌉ portes de multiplication **non scalaire** (ou division)
  sont nécessaires dans le modèle des circuits arithmétiques formels.
- Rang de bord géométrique ≥ n^(9/4), rang asymptotique = n^(9/4).

**3. Formalisation Lean associée**
- Bibliothèque : https://github.com/openai/math/tree/main/lean
- Théorème `square_exponent` : `formalOmega F 1 1 1 = 9/4`
  → `lean/OAI/LinearAlgebra/SpectralBooks/ExactExponent.lean`
- Périmètre : `lean/docs/107.md` — circuits **sans division**, identités polynomiales formelles.
- ⚠️ Formalisation **partielle** : le README du dépôt indique explicitement que tout n'est pas formalisé.

**4. Contexte et vérification indépendante**
- Historique des versions du dépôt : https://github.com/openai/math/blob/main/history.md
- Table des records (Wikipedia, consultée le 25/11/2026) : meilleure borne publiée avant octobre = **2,371177**.
- Le manuscrit d'octobre s'appuie sur arXiv 2610.28627 ; le manuscrit de novembre cite 2611.09716.
- ⚠️ Aucune vérification par les pairs au 25/11/2026. Aucune reproduction indépendante connue de la borne inférieure.

## Travaux antérieurs (à citer en démo)

**Strassen (1969)** — *Gaussian elimination is not optimal*, Numerische Mathematik 13, 354–356.
- 7 multiplications pour 2×2 → exposant log₂7 ≈ 2,8074.

**Winograd (1971)** — rang du tenseur de multiplication 2×2 = 7 (pas de décomposition à 6 termes).
- Référence moderne : Landsberg, *Geometry and Complexity Theory*, ch. 4.

**AlphaTensor (DeepMind, 2022)** — Fawzi et al., *Discovering faster matrix multiplication algorithms with reinforcement learning*, Nature 610, 47–53.
- Code et factorisations : https://github.com/google-deepmind/alphatensor
- Notebook Colab d'exploration fourni par DeepMind dans ce dépôt.
- Résultats : 3×3 en 23 multiplications, 4×4 en 47, 5×5 en 76.

**AlphaEvolve (DeepMind, 2025)** — agent de programmation évolutionnaire (Gemini).
- https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- Contexte : la borne de 2,371177 (août 2026) est présentée comme assistée par AlphaEvolve.

## Outils

- Lean 4 : https://lean-lang.org/ · Web editor : https://live.lean-lang.org/
- Mathlib : https://leanprover-community.github.io/
- GPT-2 small : https://huggingface.co/openai-community/gpt2 (124 M paramètres)

## Chiffres utilisés dans les slides (recalculables)

| Affirmation | Vérification |
|---|---|
| 8 → 7 multiplications pour 2×2 | `demo/strassen.py --count` |
| log₂7 = 2,807355 | idem |
| n^(9/4) à n = 10⁹ = 1,78×10²⁰ | `demo/complexity.py` |
| gain 9/4 vs 2,371177 à n = 10⁹ : ×12,3 | idem |
| ⌈2^(9/4)/2⌉ = 3 (borne faible à n = 2, rang réel 7) | idem |
| GPT-2 small : 49 GEMM, ~1 GFLOP pour 4 tokens | `demo/gpt2_matrices.py` |
