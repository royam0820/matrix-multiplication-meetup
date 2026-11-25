/- Version matricielle, coefficient par coefficient (2×2).

Principe : on ne prouve pas « la matrice entière est égale », on prouve chaque
coefficient. L'idiome est :
    simp [Matrix.mul_apply, Fin.sum_univ_two]
qui développe (A * B) i j en une somme de deux termes, puis `ring` referme.

STATUT : NON COMPILÉ ICI (pas de toolchain Lean sur le VPS).
À tester dans le Lean 4 Web Editor avant le Meetup. Si `Fin.sum_univ_two`
n'est pas reconnu, essayer `Matrix.mul_apply` seul puis `fin_cases` + `simp`.
-/

import Mathlib
open Matrix

variable {R : Type*} [CommRing R]

/-- c₁₁ = M1 + M4 − M5 + M7 -/
theorem strassen_c11_matrix (A B : Matrix (Fin 2) (Fin 2) R) :
    (A * B) 0 0
      = (A 0 0 + A 1 1) * (B 0 0 + B 1 1)
        + A 1 1 * (B 1 0 - B 0 0)
        - (A 0 0 + A 0 1) * B 1 1
        + (A 0 1 - A 1 1) * (B 1 0 + B 1 1) := by
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  ring

/-- c₁₂ = M3 + M5 -/
theorem strassen_c12_matrix (A B : Matrix (Fin 2) (Fin 2) R) :
    (A * B) 0 1
      = A 0 0 * (B 0 1 - B 1 1) + (A 0 0 + A 0 1) * B 1 1 := by
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  ring

/-- c₂₁ = M2 + M4 -/
theorem strassen_c21_matrix (A B : Matrix (Fin 2) (Fin 2) R) :
    (A * B) 1 0
      = (A 1 0 + A 1 1) * B 0 0 + A 1 1 * (B 1 0 - B 0 0) := by
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  ring

/-- c₂₂ = M1 − M2 + M3 + M6 -/
theorem strassen_c22_matrix (A B : Matrix (Fin 2) (Fin 2) R) :
    (A * B) 1 1
      = (A 0 0 + A 1 1) * (B 0 0 + B 1 1)
        - (A 1 0 + A 1 1) * B 0 0
        + A 0 0 * (B 0 1 - B 1 1)
        + (A 1 0 - A 0 0) * (B 0 0 + B 0 1) := by
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  ring
