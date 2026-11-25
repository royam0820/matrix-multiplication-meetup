# Quand l'IA réinvente ses propres mathématiques — la révolution du 9/4

Kit de démonstration pour le Meetup Fastai-FR.
**Fil rouge :** calculer → découvrir → vérifier.

> En octobre 2026, OpenAI publie une borne supérieure `ω ≤ 9/4` pour l'exposant de la
> multiplication matricielle. Le 24 novembre 2026, un second manuscrit revendique la
> borne inférieure correspondante : `ω = 9/4` exactement, sur tout corps.
> Ce kit ne rejoue pas les preuves : il montre **ce que l'on peut vérifier soi-même**,
> avec un laptop, en 30 secondes par démo.

---

## Ce que contient le kit

| Dossier | Contenu | Ce que ça démontre |
|---|---|---|
| `demo/strassen.py` | Strassen 1969, compteur d'opérations, chrono | calculer : 7 multiplications au lieu de 8 |
| `demo/tensor_rank.py` | tenseur de multiplication 2×2, décompositions rang 1 | découvrir : un algorithme = une décomposition de tenseur |
| `demo/complexity.py` | tableaux et courbes d'exposants | comprendre la portée réelle du 9/4 |
| `demo/gpt2_matrices.py` | hooks sur GPT-2 small | où sont les matrices dans un LLM |
| `app/simulateur.html` | simulateur + quiz, zéro installation | faire participer la salle |
| `app/streamlit_app.py` | même simulateur en Python | alternative si vous préférez Streamlit |
| `lean/` | preuves Lean 4 / Mathlib | vérifier : la preuve formelle comme juge |
| `agents/lean_prover.py` | boucle LLM → Lean → erreurs → correction | l'IA qui se fait corriger par un vérificateur |
| `notebooks/` | les 4 démos en notebooks | reproduction par les participants |
| `DEMO_LIVE_NOTES.md` | déroulé 2 h, minuté, avec plans B | le jour J |
| `REFERENCES.md` | sources primaires | ne pas citer de mémoire |

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Testé avec Python 3.13, numpy 2.4, torch 2.12, transformers 5.11, matplotlib 3.10.

## Ordre de passage (2 h)

```
1. gpt2_matrices.py    → « les matrices sont partout »            5 min
2. strassen.py         → « 7 au lieu de 8 »                       8 min
3. tensor_rank.py      → « un algorithme est un tenseur »        10 min
4. complexity.py       → « ce que 2.25 veut dire »                6 min
5. simulateur.html     → quiz + slider, la salle manipule         8 min
6. lean/ (live)        → « et si on vérifiait ? »                12 min
7. agents/lean_prover  → la boucle génération / vérification     10 min
```

Le reste du créneau : intro, transitions, questions.

## Les trois chiffres à retenir

- **8 → 7** : Strassen, 1969, une multiplication économisée sur huit.
- **2,807 → 2,371177** : 57 ans pour gagner 0,44 sur l'exposant (record publié avant octobre 2026).
- **2,25** : la valeur revendiquée par OpenAI, à la fois comme plafond (oct.) et comme plancher (nov.).

## Avertissement scientifique

Les deux manuscrits d'octobre et de novembre 2026 sont des **prépublications non
évaluées par les pairs**. Le manuscrit du 24 novembre est une revendication de borne
inférieure — un objet mathématiquement beaucoup plus lourd qu'un nouvel algorithme,
et sa vérification indépendante prendra du temps. La formalisation Lean associée est
partielle et de périmètre restreint (circuits arithmétiques sans division, identités
polynomiales formelles). Le kit présente donc les résultats comme **des affirmations
en cours de vérification**, pas comme des théorèmes établis.

C'est précisément l'intérêt du troisième verbe : *vérifier*.

## Licence et attribution

Code : MIT. Voir `ATTRIBUTION.md` pour les sources, les figures et les citations.

## Statut de vérification (25/11/2026)

| Élément | Statut |
|---|---|
| `demo/strassen.py` | ✅ exécuté, comptage exact, égalité entière vérifiée, chrono mesuré |
| `demo/tensor_rank.py` | ✅ exécuté, les deux décompositions reconstruisent le tenseur |
| `demo/complexity.py` | ✅ exécuté, `out/complexite.png` générée |
| `demo/gpt2_matrices.py` | ✅ exécuté, 49 GEMM mesurés sur GPT-2 small |
| `notebooks/01-04` | ✅ exécutés de bout en bout (nbclient) |
| `app/simulateur.html` | ✅ JS validé syntaxiquement — à ouvrir dans un navigateur pour le rendu |
| `app/streamlit_app.py` | ⚠️ non lancé (streamlit non installé ici) — code relu, dépendances dans `requirements.txt` |
| `lean/*.lean` | ⚠️ **non compilés** (pas de toolchain Lean sur le VPS) — énoncés vérifiés numériquement, à valider dans le Web Editor |
| `agents/lean_prover.py` | ⚠️ logique testable en `--checker none`, nécessite une clé API |

