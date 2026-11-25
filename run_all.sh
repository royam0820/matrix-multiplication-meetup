#!/usr/bin/env bash
# Tout lancer, dans l'ordre du Meetup. ~2 min hors téléchargement du modèle.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

echo "=== 1/4 — matrices dans GPT-2 ==========================================="
python3 demo/gpt2_matrices.py | tee out/gpt2.txt

echo "=== 2/4 — Strassen ====================================================="
python3 demo/strassen.py | tee out/strassen.txt

echo "=== 3/4 — tenseur / rang ==============================================="
python3 demo/tensor_rank.py | tee out/tensor.txt

echo "=== 4/4 — complexités =================================================="
python3 demo/complexity.py | tee out/complexity.txt

echo
echo "Notebooks :"
python3 build_notebooks.py
echo
echo "Simulateur : ouvrir app/simulateur.html dans un navigateur."
echo "Fait."
