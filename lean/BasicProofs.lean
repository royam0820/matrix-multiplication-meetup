/-- Preuves Lean 4 / Mathlib de base pour la démo "Quand l'IA réinvente ses propres mathématiques".
Ces fichiers sont destinés à être ouverts dans le **Lean 4 Web Editor** (https://lean4web-editor.vercel.app/)
ou compilés localement avec `lake build` après avoir initialisé un projet Mathlib.

STATUT : **NON VÉRIFIÉS DANS CET ENVIRONNEMENT** (pas de toolchain Lean sur le VPS).
Testez dans le Web Editor AVANT le Meetup. -/

import Mathlib

/-- Identité élémentaire : (a + b)² = a² + 2ab + b².
    Le tactic `ring` normalise les deux côtés et vérifie l'égalité. -/
theorem carre_somme (a b : ℝ) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

/-- Même identité sur un anneau commutatif quelconque. -/
theorem carre_somme_anneau {R : Type*} [CommRing R] (a b : R) :
    (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring