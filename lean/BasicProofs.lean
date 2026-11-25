import Mathlib

/-!
# Preuves de base — démo 5 du Meetup « la révolution du 9/4 »

Fichier vérifié avec Lean 4 + Mathlib (voir `lean/README.md`).

À ouvrir dans le Lean 4 Web Editor, ou compiler avec :

    lake env lean lean/BasicProofs.lean
-/

/-- Identité élémentaire : (a + b)² = a² + 2ab + b².
    Le tactic `ring` normalise les deux côtés et vérifie l'égalité. -/
theorem carre_somme (a b : ℝ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

/-- Même identité sur un anneau commutatif quelconque. -/
theorem carre_somme_anneau {R : Type*} [CommRing R] (a b : R) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring
