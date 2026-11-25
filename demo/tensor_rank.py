#!/usr/bin/env python3
"""
Démo 3 — Un algorithme de multiplication EST une décomposition de tenseur.

C'est le pont conceptuel de tout le Meetup :
    multiplier deux matrices  =  contracter un tenseur fixe avec (vec A, vec B)
    trouver un algorithme     =  écrire ce tenseur comme somme de termes de rang 1
    le nombre de termes       =  le nombre de multiplications scalaires

On construit le tenseur de multiplication 2×2, on vérifie la décomposition
scolaire (8 termes) et celle de Strassen (7 termes), puis on montre ce que
l'IA cherche : une décomposition à 6 termes — qui n'existe pas. Le rang exact
du tenseur de multiplication 2×2 est 7 (Winograd/Landsberg) ; c'est ce qui
condamne la piste « battre Strassen sur 2×2 » et pousse la recherche vers
les puissances de tenseurs et le rang asymptotique (d'où ω).

Convention d'indices :
    C[i,j] = Σ_{k,l} A[i,k] · B[l,j] · δ(k,l)
    vec A → 4 coordonnées (i,k), vec B → 4 coordonnées (l,j), vec C → 4 (i,j)
    T[(i,k),(l,j),(i,j)] = 1 si k == l, 0 sinon

Usage :
    python demo/tensor_rank.py
    python demo/tensor_rank.py --json out/decomposition_strassen.json
"""
from __future__ import annotations

import argparse
import itertools
import json

import numpy as np

N = 2
D = N * N  # 4 coordonnées par côté


def idx(i: int, k: int) -> int:
    return i * N + k


def build_tensor() -> np.ndarray:
    """T[p, q, r] du produit matriciel 2×2."""
    T = np.zeros((D, D, D), dtype=np.int64)
    for i, k, l, j in itertools.product(range(N), repeat=4):
        if k == l:  # le contrat : A[i,k] · B[k,j]
            T[idx(i, k), idx(l, j), idx(i, j)] = 1
    return T


def classical_terms() -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """8 produits scolaires : un terme par (i, k, j)."""
    terms = []
    for i, k, j in itertools.product(range(N), repeat=3):
        u = np.zeros(D, dtype=np.int64)
        v = np.zeros(D, dtype=np.int64)
        w = np.zeros(D, dtype=np.int64)
        u[idx(i, k)] = 1
        v[idx(k, j)] = 1
        w[idx(i, j)] = 1
        terms.append((u, v, w))
    return terms


def strassen_terms() -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """7 produits de Strassen, écrits comme termes de rang 1.

    M1 = (a11+a22)(b11+b22)   M2 = (a21+a22)b11      M3 = a11(b12-b22)
    M4 = a22(b21-b11)         M5 = (a11+a12)b22      M6 = (a21-a11)(b11+b12)
    M7 = (a12-a22)(b21+b22)
    c11 = M1+M4-M5+M7   c12 = M3+M5   c21 = M2+M4   c22 = M1-M2+M3+M6
    """
    # Ordre des coordonnées : (1,1)=0, (1,2)=1, (2,1)=2, (2,2)=3
    A_FORMS = {  # u_r : combinaison linéaire des a_ij
        1: {0: 1, 3: 1},              # a11 + a22
        2: {2: 1, 3: 1},              # a21 + a22
        3: {0: 1},                    # a11
        4: {3: 1},                    # a22
        5: {0: 1, 1: 1},              # a11 + a12
        6: {2: 1, 0: -1},             # a21 - a11
        7: {1: 1, 3: -1},             # a12 - a22
    }
    B_FORMS = {  # v_r
        1: {0: 1, 3: 1},              # b11 + b22
        2: {0: 1},                    # b11
        3: {1: 1, 3: -1},             # b12 - b22
        4: {2: 1, 0: -1},             # b21 - b11
        5: {3: 1},                    # b22
        6: {0: 1, 1: 1},              # b11 + b12
        7: {2: 1, 3: 1},              # b21 + b22
    }
    C_FORMS = {  # w_r : où va chaque produit dans C
        1: {0: 1, 3: 1},              # c11 + c22
        2: {2: 1, 3: -1},             # c21 - c22
        3: {1: 1, 3: 1},              # c12 + c22
        4: {0: 1, 2: 1},              # c11 + c21
        5: {0: -1, 1: 1},             # -c11 + c12
        6: {3: 1},                    # c22
        7: {0: 1},                    # c11
    }

    def vec(form: dict[int, int]) -> np.ndarray:
        out = np.zeros(D, dtype=np.int64)
        for pos, coeff in form.items():
            # position dans l'ordre (1,1),(1,2),(2,1),(2,2) = même ordre que idx()
            out[pos] = coeff
        return out

    return [(vec(A_FORMS[r]), vec(B_FORMS[r]), vec(C_FORMS[r])) for r in range(1, 8)]


def reconstruct(terms) -> np.ndarray:
    T = np.zeros((D, D, D), dtype=np.int64)
    for u, v, w in terms:
        T += np.einsum("p,q,r->pqr", u, v, w)
    return T


def operational_check(terms) -> bool:
    """Vérifie sur des matrices concrètes que Σ (u·vecA)(v·vecB) w = A@B."""
    rng = np.random.default_rng(7)
    A = rng.integers(-9, 9, (N, N)).astype(np.int64)
    B = rng.integers(-9, 9, (N, N)).astype(np.int64)
    va, vb = A.reshape(-1), B.reshape(-1)  # ordre ligne-major = idx(i,k)
    C = np.zeros(D, dtype=np.int64)
    for u, v, w in terms:
        C += (u @ va) * (v @ vb) * w
    return np.array_equal(C.reshape(N, N), A @ B)


def show(terms) -> None:
    print(f"  {len(terms)} termes de rang 1 :")
    for r, (u, v, w) in enumerate(terms, 1):
        print(f"    T{r}: u={np.array2string(u, separator=',')}  "
              f"v={np.array2string(v, separator=',')}  "
              f"w={np.array2string(w, separator=',')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    T = build_tensor()
    print("=" * 68)
    print("  LE TENSEUR DE LA MULTIPLICATION 2x2")
    print("=" * 68)
    print(f"  Forme : {T.shape},  {T.sum()} coefficients non nuls, "
          f"max = {T.max()}")
    print("  Chaque algorithme = une façon d'écrire T comme somme de u⊗v⊗w.")
    print()

    for name, terms in (("scolaire", classical_terms()), ("Strassen", strassen_terms())):
        print("=" * 68)
        print(f"  DECOMPOSITION — {name}")
        print("=" * 68)
        Tm = reconstruct(terms)
        print(f"  T reconstruit identique : {np.array_equal(Tm, T)}")
        print(f"  Verifie sur matrices entieres aleatoires : {operational_check(terms)}")
        show(terms)
        print()

    print("=" * 68)
    print("  CE QUE CHERCHE UNE IA (AlphaTensor, 2022)")
    print("=" * 68)
    print("  Espace de recherche : suites (u_r, v_r, w_r) de petite taille,")
    print("  à coefficients entiers. L'agent retire un terme à chaque étape ;")
    print("  l'objectif est d'atteindre le tenseur nul en un minimum d'étapes.")
    print()
    print("  Sur 2x2, le rang est 7 — démontré. Pas de 6 : la recherche est close.")
    print("  AlphaTensor a donc cherché plus grand : 3x3 (23 multiplications au lieu")
    print("  de 27), 4x4 (47 au lieu de 64), et 5x5 (76 au lieu de 125) — c'est-à-dire")
    print("  de nouveaux algorithmes, vérifiés formellement, que personne n'avait écrits.")
    print()
    print("  Le lien avec ω : on ne compose pas des algorithmes, on compose des")
    print("  PUISSANCES de tenseurs. Si le rang asymptotique de T^⊗k croît comme")
    print("  n^{ωk}, alors l'exposant ω est défini par cette croissance — et c'est")
    print("  ce nombre que le 9/4 prétend avoir épinglé.")
    print()

    if args.json:
        payload = [
            {"u": u.tolist(), "v": v.tolist(), "w": w.tolist()}
            for u, v, w in strassen_terms()
        ]
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"tensor_shape": [D, D, D], "rank": len(payload), "terms": payload},
                      f, indent=2)
        print(f"  Décomposition écrite dans {args.json}")


if __name__ == "__main__":
    main()
