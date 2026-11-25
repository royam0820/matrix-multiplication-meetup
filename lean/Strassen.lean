import Mathlib

/-!
# Identités de Strassen (2×2)

Pour  A = [[a, b], [c, d]]  et  B = [[e, f], [g, h]] :

    M1 = (a+d)(e+h)    M2 = (c+d)e      M3 = a(f-h)
    M4 = d(g-e)        M5 = (a+b)h      M6 = (c-a)(e+f)
    M7 = (b-d)(g+h)

    c₁₁ = M1 + M4 - M5 + M7 = a·e + b·g
    etc.

`ring` vérifie chaque identité dans l'anneau des polynômes
ℤ[a,b,c,d,e,f,g,h] : la preuve vaut pour tout anneau commutatif.
-/
set_option linter.unusedVariables false

theorem strassen_c11 {R : Type*} [CommRing R] (a b c d e f g h : R) :
    (a + d) * (e + h) + d * (g - e) - (a + b) * h + (b - d) * (g + h)
    = a * e + b * g := by
  ring

theorem strassen_c12 {R : Type*} [CommRing R] (a b c d e f g h : R) :
    a * (f - h) + (a + b) * h = a * f + b * h := by
  ring

theorem strassen_c21 {R : Type*} [CommRing R] (a b c d e f g h : R) :
    (c + d) * e + d * (g - e) = c * e + d * g := by
  ring

theorem strassen_c22 {R : Type*} [CommRing R] (a b c d e f g h : R) :
    (a + d) * (e + h) - (c + d) * e + a * (f - h) + (c - a) * (e + f)
    = c * f + d * h := by
  ring
