#!/usr/bin/env python3
"""
Démo 2 — Le tour de magie de Strassen (1969).

Trois choses, dans cet ordre :
  1. compter les multiplications scalaires (théorie exacte, pas d'estimation) ;
  2. vérifier numériquement que l'algorithme est correct ;
  3. chronométrer — et constater qu'il est PLUS LENT que numpy.

Le point de la démo : un meilleur exposant n'est pas une vitesse.
Un exposant est une pente quand n → ∞ ; la constante et la localité mémoire
décident de la vitesse réelle.

Usage :
    python demo/strassen.py            # tout (~ 15 s)
    python demo/strassen.py --count    # comptage seul (instantané)
    python demo/strassen.py --bench    # chrono seul
"""
from __future__ import annotations

import os

# Reproducibilité : un seul thread BLAS, sinon les petits n sont noyés
# dans le coût de lancement du pool de threads (mesuré : 8 ms fixes).
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import math
import time

import numpy as np

# ---------------------------------------------------------------- comptage


def naive_products(n: int) -> int:
    """Multiplications scalaires de l'algorithme scolaire pour deux n×n."""
    return n**3


def strassen_products(n: int) -> int:
    """Multiplications scalaires de Strassen récursif (n = 2^k)."""
    if n == 1:
        return 1
    if n % 2:
        raise ValueError("Strassen récursif tel que présenté exige n pair")
    return 7 * strassen_products(n // 2)


def strassen_additions(n: int) -> int:
    """Additions/soustractions : 18 blocs de (n/2)² à chaque niveau."""
    if n == 1:
        return 0
    h = n // 2
    return 18 * h * h + 7 * strassen_additions(h)


def report_counts() -> None:
    print("=" * 68)
    print("  COMPTAGE EXACT DES MULTIPLICATIONS SCALAIRES")
    print("=" * 68)
    print(f"{'n':>6} {'scolaire n³':>16} {'Strassen':>14} {'gain':>8} {'exposant':>10}")
    for k in range(1, 11):
        n = 2**k
        s, c = strassen_products(n), naive_products(n)
        expo = math.log(s) / math.log(n) if n > 1 else float("nan")
        print(f"{n:>6} {c:>16,} {s:>14,} {c / s:>7.1f}x {expo:>10.4f}")
    print()
    print(f"  log2(7) = {math.log2(7):.6f}   ->   Strassen coute n^{math.log2(7):.4f}")
    print(f"  A n = 1024 : {strassen_products(1024):,} multiplications")
    print(f"               au lieu de {naive_products(1024):,}")
    print(f"  Additions ajoutees a n = 1024 : {strassen_additions(1024):,}")
    print("  -> On echange des multiplications (cheres en 1969) contre des additions.")
    print("  Le mecanisme, en une ligne : (2^k)^{log2 7} = 7^k.")
    print()


# ---------------------------------------------------------------- algèbre

Counter = list[int]


def _naive(A: np.ndarray, B: np.ndarray, counter: Counter) -> np.ndarray:
    n = A.shape[0]
    C = np.zeros((n, n), dtype=A.dtype)
    for i in range(n):
        for k in range(n):
            a = A[i, k]
            for j in range(n):
                counter[0] += 1
                C[i, j] += a * B[k, j]
    return C


def _strassen(A: np.ndarray, B: np.ndarray, cutoff: int, counter: Counter) -> np.ndarray:
    n = A.shape[0]
    if n <= cutoff:
        return _naive(A, B, counter)

    h = n // 2
    a11, a12, a21, a22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    b11, b12, b21, b22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]

    def S(X, Y):
        return _strassen(X, Y, cutoff, counter)

    m1 = S(a11 + a22, b11 + b22)
    m2 = S(a21 + a22, b11)
    m3 = S(a11, b12 - b22)
    m4 = S(a22, b21 - b11)
    m5 = S(a11 + a12, b22)
    m6 = S(a21 - a11, b11 + b12)
    m7 = S(a12 - a22, b21 + b22)

    C = np.empty((n, n), dtype=A.dtype)
    C[:h, :h] = m1 + m4 - m5 + m7
    C[:h, h:] = m3 + m5
    C[h:, :h] = m2 + m4
    C[h:, h:] = m1 - m2 + m3 + m6
    return C


def _strassen_blas(A: np.ndarray, B: np.ndarray, cutoff: int = 256) -> np.ndarray:
    """Version 'réelle' : les blocs sont multipliés par BLAS, pas à la main."""
    n = A.shape[0]
    if n <= cutoff:
        return A @ B
    h = n // 2
    a11, a12, a21, a22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    b11, b12, b21, b22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    m1 = _strassen_blas(a11 + a22, b11 + b22, cutoff)
    m2 = _strassen_blas(a21 + a22, b11, cutoff)
    m3 = _strassen_blas(a11, b12 - b22, cutoff)
    m4 = _strassen_blas(a22, b21 - b11, cutoff)
    m5 = _strassen_blas(a11 + a12, b22, cutoff)
    m6 = _strassen_blas(a21 - a11, b11 + b12, cutoff)
    m7 = _strassen_blas(a12 - a22, b21 + b22, cutoff)
    C = np.empty_like(A)
    C[:h, :h] = m1 + m4 - m5 + m7
    C[:h, h:] = m3 + m5
    C[h:, :h] = m2 + m4
    C[h:, h:] = m1 - m2 + m3 + m6
    return C


def verify_algebra() -> None:
    print("=" * 68)
    print("  VERIFICATION NUMERIQUE (entiers -> egalite exacte)")
    print("=" * 68)
    rng = np.random.default_rng(1234)
    ok = True
    for k in range(1, 7):  # n = 2 … 64 : récursion jusqu'au scalaire
        n = 2**k
        A = rng.integers(-50, 50, (n, n)).astype(np.int64)
        B = rng.integers(-50, 50, (n, n)).astype(np.int64)
        counter = [0]
        C = _strassen(A, B, 1, counter)
        same = np.array_equal(C, A @ B)
        ok &= same
        print(
            f"  n={n:>4} : exact={same!s:<5} multiplications comptees={counter[0]:>7,}"
            f" (theorie {strassen_products(n):>7,})"
        )
    for n in (128, 256):
        A = rng.integers(-50, 50, (n, n)).astype(np.int64)
        B = rng.integers(-50, 50, (n, n)).astype(np.int64)
        same = np.array_equal(_strassen(A, B, 64, [0]), A @ B)
        ok &= same
        print(f"  n={n:>4} : exact={same!s:<5} (recursion coupee a 64)")
    print(f"\n  Toutes les verifications passent : {ok}")
    if not ok:
        raise SystemExit(1)
    print("  Entiers -> aucune tolerance flottante : l'egalite est exacte.\n")


# ---------------------------------------------------------------- chrono


def _median_time(fn, repeats: int = 3) -> float:
    fn()  # chauffe : allocation, cache à froid
    ts = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return sorted(ts)[len(ts) // 2]


def bench() -> None:
    print("=" * 68)
    print("  CHRONO — et pourquoi Strassen perd en pratique")
    print("=" * 68)
    print(f"{'n':>6} {'numpy/BLAS':>12} {'Strassen(BLAS)':>16} {'rapport':>9} {'correct':>8}")
    rows = []
    rng = np.random.default_rng(0)
    for n in (256, 512, 1024, 2048):
        A = rng.standard_normal((n, n))
        B = rng.standard_normal((n, n))
        t_blas = _median_time(lambda: A @ B)
        t_str = _median_time(lambda: _strassen_blas(A, B, cutoff=256))
        correct = np.allclose(_strassen_blas(A, B, cutoff=256), A @ B)
        rows.append((n, t_blas, t_str))
        print(
            f"{n:>6} {t_blas * 1e3:>10.1f}ms {t_str * 1e3:>14.1f}ms"
            f" {t_str / t_blas:>8.2f}x {str(correct):>8}"
        )
    print()
    print("  Strassen fait MOINS de multiplications, et prend PLUS de temps.")
    print("  Raisons : copies de blocs, cache, et surtout BLAS qui execute")
    print("  8 multiplications vectorisees par cycle et optimise la localite.")
    print("  Un exposant est une pente quand n -> infini ; a n = 2000, on est loin.")
    print()

    if len(rows) >= 2:
        n1, t1, _ = rows[0]
        n2, t2, _ = rows[-1]
        pente = math.log(t2 / t1) / math.log(n2 / n1)
        print(f"  Pente empirique mesuree sur BLAS entre n={n1} et n={n2} : n^{pente:.2f}")
        print("  Proche de 3 en pratique (terminologie : 2.8-3.0 selon le cache).")
        print("  Aucun algorithme 'sous-cubique' ne bat BLAS a ces tailles.")
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--bench", action="store_true")
    args = ap.parse_args()
    if args.count:
        report_counts()
        return
    if args.bench:
        bench()
        return
    report_counts()
    verify_algebra()
    bench()


if __name__ == "__main__":
    main()
