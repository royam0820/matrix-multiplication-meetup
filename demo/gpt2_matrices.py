#!/usr/bin/env python3
"""
Démo 1 — Où se cachent les matrices dans un LLM ?

On charge GPT-2 small (124 M), on fait un forward sur "The city of Paris",
et on affiche les formes des matrices à chaque Linear/Conv1D (attention + FFN).
Le but : montrer qu'une phrase de 4 tokens déclenche des millions de
multiplications matricielles — et que le cœur du LLM, c'est du GEMM pur.

Usage :
    python demo/gpt2_matrices.py              # télécharge si absent (~500 Mo)
    python demo/gpt2_matrices.py --tiny       # modèle aléatoire petit (démo hors-ligne)
    python demo/gpt2_matrices.py --no-cache   # force re-téléchargement
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2Config

# --------------------------------------------------------------------- config
PROMPT = "The city of Paris"
MODEL_ID = "gpt2"  # 124 M paramètres
DEVICE = "cpu"  # M4 ou CPU VPS — pas de GPU distant

# --------------------------------------------------------------------- hooks


class HookCollector:
    def __init__(self):
        self.hooks = []
        self.records = []  # list of (module_name, in_shape, out_shape, module_type)

    def clear(self):
        self.records.clear()

    def __call__(self, module, inp, out):
        x = inp[0] if isinstance(inp, tuple) else inp
        cname = module.__class__.__name__
        if cname == "Linear":
            mtype = "Linear"
        elif cname == "Conv1D":
            mtype = "Conv1D"
        else:
            mtype = cname
        self.records.append(
            (
                cname,
                tuple(x.shape),
                tuple(out.shape if not isinstance(out, tuple) else out[0].shape),
                mtype,
            )
        )

    def remove(self):
        for h in self.hooks:
            h.remove()
        self.hooks.clear()


def install_hooks(model: nn.Module, collector: HookCollector):
    for name, mod in model.named_modules():
        cname = mod.__class__.__name__
        if cname in ("Linear", "Conv1D"):
            h = mod.register_forward_hook(collector)
            collector.hooks.append(h)


def flops_gemm(a: int, b: int, c: int) -> int:
    return 2 * a * b * c


def report(records: list) -> None:
    print("=" * 78)
    print(f"  MATRICES DANS GPT-2 SMALL — prompt : '{PROMPT}'")
    print("=" * 78)
    print(f"{'#':>3} {'module':<30} {'input':>22} {'output':>22} {'GFLOPs':>10}")
    total = 0
    for i, (cls, ins, outs, mtype) in enumerate(records, 1):
        if mtype not in ("Linear", "Conv1D"):
            continue
        batch_seq = ins[0] * ins[1] if len(ins) >= 2 else 1
        in_f = ins[-1]
        out_f = outs[-1]
        gf = flops_gemm(batch_seq, in_f, out_f) / 1e9
        total += gf
        short = cls.replace("GPT2MLP", "FFN").replace("GPT2Attention", "Attn")
        print(f"{i:>3} {short:<30} {str(ins):>22} {str(outs):>22} {gf:>9.3f}")
    print("-" * 78)
    print(f"{'TOTAL':>3} {'':<30} {'':>22} {'':>22} {total:>9.3f} GFLOPs")
    print()

    by_type = {}
    for cls, ins, outs, mtype in records:
        if mtype not in ("Linear", "Conv1D"):
            continue
        short = cls.replace("GPT2MLP", "FFN").replace("GPT2Attention", "Attn")
        by_type.setdefault(short, {"count": 0, "gflops": 0})
        batch_seq = ins[0] * ins[1] if len(ins) >= 2 else 1
        in_f, out_f = ins[-1], outs[-1]
        by_type[short]["count"] += 1
        by_type[short]["gflops"] += flops_gemm(batch_seq, in_f, out_f) / 1e9
    print("  Par type de couche :")
    for k, v in by_type.items():
        print(f"    {k:<12} : {v['count']:>2} appels  ->  {v['gflops']:.3f} GFLOPs")
    print()


def load_real_model(no_cache: bool = False):
    print(f"  Chargement de {MODEL_ID}...")
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=not no_cache)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        local_files_only=not no_cache,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    print(f"  Chargé en {time.time() - t0:.1f}s  ({sum(p.numel() for p in model.parameters()):,} paramètres)")
    return tok, model


def load_tiny_model():
    cfg = GPT2Config(
        vocab_size=50257,
        n_positions=128,
        n_embd=256,
        n_layer=4,
        n_head=4,
        n_inner=1024,
    )
    model = AutoModelForCausalLM.from_config(cfg)
    model.eval()
    from transformers import GPT2TokenizerFast

    tok = GPT2TokenizerFast.from_pretrained("gpt2")
    print(f"  Modèle aléatoire tiny : {sum(p.numel() for p in model.parameters()):,} paramètres")
    return tok, model


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiny", action="store_true", help="modèle aléatoire petit (pas de téléchargement)")
    ap.add_argument("--no-cache", action="store_true", help="forcer le téléchargement")
    args = ap.parse_args()

    if args.tiny:
        tok, model = load_tiny_model()
    else:
        try:
            tok, model = load_real_model(args.no_cache)
        except Exception as e:
            print(f"  ⚠️  Échec chargement GPT-2 : {e}")
            print("  Basculement sur --tiny...")
            tok, model = load_tiny_model()

    inputs = tok(PROMPT, return_tensors="pt")
    print(f"  Tokens : {inputs['input_ids'].shape[1]}  (longueur séquence)")

    collector = HookCollector()
    install_hooks(model, collector)

    with torch.no_grad():
        _ = model(**inputs)

    report(collector.records)
    collector.remove()

    print("  Point pédagogique :")
    print("    • Chaque Linear/Conv1D est une multiplication matricielle (GEMM).")
    print("    • L'attention = Q,K,V projections (c_attn) + matmul attention + sortie (c_proj).")
    print("    • Le FFN = deux GEMM (c_fc up + c_proj down) avec GELU entre les deux.")
    print("    • Un LLM, c'est 95 % de GEMM. Améliorer le GEMM, c'est améliorer l'IA.")


if __name__ == "__main__":
    main()