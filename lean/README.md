# Preuves Lean 4 pour le Meetup

## Fichiers

| Fichier | Contenu | Statut |
|---------|---------|--------|
| `BasicProofs.lean` | `(a+b)² = a²+2ab+b²` — démo `ring` | ✅ compilé |
| `Strassen.lean` | Identités scalaires de Strassen (c₁₁, c₁₂, c₂₁, c₂₂) — `ring` pur | ✅ compilé |
| `MatrixProofs.lean` | Version matricielle, coefficient par coefficient | ✅ compilé |

**Vérifié le 25 novembre 2026** avec Lean `4.37.0-rc1` et Mathlib (`cf28751`, 25/11/2026) :
les trois fichiers compilent sans erreur ni avertissement.

    lake env lean lean/BasicProofs.lean   # rc=0
    lake env lean lean/Strassen.lean      # rc=0
    lake env lean lean/MatrixProofs.lean  # rc=0

## Comment tester (zéro installation)

1. Ouvrez <https://lean4web-editor.vercel.app/>
2. Copiez-collez le contenu d'un fichier dans l'éditeur
3. Lean vérifie en temps réel — les coches vertes = succès

## Pour le Meetup (démo live)

1. **BasicProofs.lean** — montrez `(a+b)²` validé instantanément
2. **Introduisez une erreur** :
   ```lean
   theorem carre_somme_faux (a b : ℝ) : (a + b)^2 = a^2 + 3*a*b + b^2 := by ring
   ```
   → Lean affiche une erreur rouge : `ring_nf` ne peut pas fermer le but
3. **Strassen.lean** — montrez les 4 identités, toutes vertes
4. **Expliquez** : c'est exactement ce que fait la boucle LLM → Lean → correction

## Portée de la formalisation OpenAI (nov. 2026)

Le dépôt `openai/math/lean/` contient une formalisation **partielle** :
- Théorème `square_exponent` : `formalOmega F 1 1 1 = 9/4`
- Périmètre : circuits arithmétiques **sans division**, identités polynomiales formelles
- **Pas** : preuve complète du manuscrit papier, pas de borne inférieure sur tous les algorithmes

Voir `openai/math/lean/docs/107.md` (scope document) et `OAI/LinearAlgebra/SpectralBooks/ExactExponent.lean`.

## Liens

- Lean 4 Web Editor : https://lean4web-editor.vercel.app/
- Mathlib docs : https://leanprover-community.github.io/mathlib_docs/
- openai/math (GitHub) : https://github.com/openai/math/tree/main/lean