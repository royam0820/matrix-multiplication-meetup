#!/usr/bin/env python3
"""
Démo 5 — La boucle génération / vérification.

Un LLM propose une preuve Lean ; un vérificateur indépendant (Lean) dit oui ou non ;
les erreurs repartent vers le LLM. Le point du Meetup : le LLM n'est jamais cru,
il est *corrigé par un juge* qui ne sait rien de lui.

Deux modes :
  --checker none   simule la boucle sans Lean installé (démo de la mécanique)
  --checker lean   utilise `lean` ou `lake env lean` sur le fichier écrit

Modèle : endpoint OpenAI-compatible (DeepSeek par défaut, la clé est déjà en env).
Aucune clé n'est écrite dans ce fichier.

Usage :
    python agents/lean_prover.py --problem "∀ a b : ℝ, (a+b)^2 = a^2 + 2*a*b + b^2"
    python agents/lean_prover.py --max-iters 3 --checker lean
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

DEFAULT_BASE_URL = os.environ.get("LEAN_PROVER_BASE_URL", "https://api.deepseek.com/v1")
DEFAULT_MODEL = os.environ.get("LEAN_PROVER_MODEL", "deepseek-chat")

SYSTEM = """Tu es un assistant de formalisation en Lean 4 + Mathlib.
Tu réponds UNIQUEMENT par un bloc de code Lean complet et compilable.
Pas d'explication, pas de markdown autour, pas de commentaire sur ta démarche.
Le fichier doit commencer par `import Mathlib`.
Si le vérificateur renvoie des erreurs, corrige-les et renvoie le fichier complet."""

PROBLEM_DEFAULT = "Pour tous réels a et b : (a + b)^2 = a^2 + 2*a*b + b^2"

SEED = """import Mathlib

theorem carre_somme (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by
  ring
"""


def call_llm(messages: list[dict]) -> str:
    """Appel HTTP minimal, sans dépendance au SDK openai."""
    import urllib.request

    key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Aucune clé API dans l'environnement (DEEPSEEK_API_KEY).")
    body = json.dumps(
        {"model": DEFAULT_MODEL, "messages": messages, "temperature": 0.1}
    ).encode()
    req = urllib.request.Request(
        f"{DEFAULT_BASE_URL}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]


def extract_code(text: str) -> str:
    m = re.search(r"```(?:lean4?)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip() + "\n"


def check_lean(code: str) -> tuple[bool, str]:
    """Écrit le code dans un fichier temporaire et tente de le compiler."""
    lean = shutil.which("lean")
    if not lean:
        return False, "⚠️  `lean` introuvable dans le PATH — utilisez --checker none."

    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run(
            [lean, path], capture_output=True, text=True, timeout=300
        )
        ok = proc.returncode == 0
        return ok, (proc.stdout + proc.stderr).strip()[:4000]
    except subprocess.TimeoutExpired:
        return False, "Timeout du vérificateur (300 s)."
    finally:
        os.unlink(path)


def fake_check(code: str) -> tuple[bool, str]:
    """Simulateur de vérificateur : accepte si `sorry` absent et `ring` présent."""
    has_sorry = "sorry" in code
    has_tactic = any(t in code for t in ("ring", "norm_num", "omega", "simp"))
    if has_sorry:
        return False, "error: declaration uses 'sorry'"
    if not has_tactic:
        return False, "error: unsolved goals (aucune tactique de clôture)"
    return True, "✔ (simulation) aucune erreur"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", default=PROBLEM_DEFAULT)
    ap.add_argument("--max-iters", type=int, default=3)
    ap.add_argument("--checker", choices=["none", "lean"], default="none")
    ap.add_argument("--seed", action="store_true", help="partir du fichier de départ")
    args = ap.parse_args()

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Formalise et prouve en Lean 4 : {args.problem}"},
    ]

    code = SEED if args.seed else ""
    for it in range(1, args.max_iters + 1):
        print(f"\n──────── itération {it}/{args.max_iters} ────────")
        if it == 1 and not code:
            raw = call_llm(messages)
            code = extract_code(raw)
            messages.append({"role": "assistant", "content": raw})
        print(code)

        ok, feedback = (check_lean if args.checker == "lean" else fake_check)(code)
        print(f"\nVérificateur : {'✔ VALIDÉ' if ok else '✘ REJETÉ'}")
        if feedback:
            print(feedback[:1500])
        if ok:
            print("\nLa boucle s'arrête : le vérificateur a accepté la preuve.")
            print("Rappel : il a validé la LOGIQUE, pas l'adéquation au problème réel.")
            return

        messages.append({"role": "user", "content": f"Le vérificateur Lean renvoie :\n{feedback}\nCorrige."})
        raw = call_llm(messages)
        code = extract_code(raw)
        messages.append({"role": "assistant", "content": raw})

    print(f"\nPas de preuve acceptée en {args.max_iters} itérations — c'est un résultat en soi.")
    sys.exit(0)


if __name__ == "__main__":
    main()
