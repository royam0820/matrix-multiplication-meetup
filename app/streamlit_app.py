#!/usr/bin/env python3
"""
Simulateur Streamlit — alternative Python au simulateur.html.
Lancez avec : streamlit run app/streamlit_app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.set_page_config(page_title="Simulateur 9/4", layout="wide")

EXPO = {
    "Scolaire (n³)": 3.0,
    "Strassen 1969": math.log2(7),
    "Record public 2026": 2.371177,
    "9/4 (OpenAI oct. 2026)": 2.25,
}

COLORS = {
    "Scolaire (n³)": "#8FA1B3",
    "Strassen 1969": "#1D7A8A",
    "Record public 2026": "#E8621A",
    "9/4 (OpenAI oct. 2026)": "#C9A84C",
}

def fmt(x: float) -> str:
    if x < 1e6:
        return f"{x:,.0f}"
    return f"{x:.3e}"

def human(n: float) -> str:
    for unit, div in [("G", 1e9), ("M", 1e6), ("k", 1e3)]:
        if n >= div:
            return f"{n/div:.1f}{unit}"
    return str(int(n))

st.title("🔬 Simulateur — La révolution du 9/4")
st.caption("Comparer les complexités théoriques de la multiplication matricielle")

# Sidebar
with st.sidebar:
    st.header("Paramètres")
    exp = st.slider("Exposant de 10 (n = 10ˣ)", 3.0, 15.0, 9.0, 0.1)
    n = 10 ** exp
    st.write(f"n = 10^{exp:.1f} = {human(n)}")

    st.divider()
    st.subheader("Quiz")
    q1 = st.radio("1. Multiplications scalaires 2×2 (classique) ?", [4, 7, 8, 16], index=None)
    q2 = st.radio("2. Strassen : quand n double, multiplications × ?", ["×2", "×4", "×7", "×8"], index=None)
    q3 = st.radio("3. Meilleur exposant → plus rapide sur GPU ?", ["Oui", "Non"], index=None)
    q4 = st.radio("4. Preuve Lean = énoncé correspond au problème réel ?", ["Oui", "Non"], index=None)
    if st.button("Valider le quiz"):
        ans = {q1: 8, q2: "×7", q3: "Non", q4: "Non"}
        score = sum(1 for k, v in ans.items() if k == v)
        if score == 4:
            st.success("🎉 4/4 — Parfait !")
        else:
            st.error(f"{score}/4 — Relisez les explications.")
            if q1 != 8: st.write("• Classique 2×2 = 2³ = 8 multiplications.")
            if q2 != "×7": st.write("• Strassen récursif : T(2n) = 7·T(n).")
            if q3 != "Non": st.write("• Exposant = asymptotique ; constantes/BLAS dominent en pratique.")
            if q4 != "Non": st.write("• Lean vérifie la logique, pas l'adéquation au problème (spec gap).")

# Main area
st.subheader("Opérations scalaires théoriques (ordre de grandeur)")
n_float = float(n)
rows = []
for name, w in EXPO.items():
    val = n_float ** w
    gain = n_float ** 3 / val
    rows.append({"Algorithme": name, "Exposant w": f"{w:.4f}", "Opérations": fmt(val), "Gain vs scolaire": f"×{gain:.1f}"})

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

# Bar chart
fig = px.bar(df, x="Algorithme", y="Opérations", color="Algorithme",
             color_discrete_map=COLORS, log_y=True,
             title=f"Complexité en multiplications scalaires pour n = {human(n)}")
fig.update_layout(showlegend=False, yaxis_title="Opérations (échelle log)")
st.plotly_chart(fig, use_container_width=True)

# Crossover note
st.divider()
st.markdown("""
### 📐 Le croisement galactique

Un algorithme d'exposant *w* s'écrit `T(n) = C · nʷ`. Il bat BLAS (`C₀ · n³`) seulement au-delà de :

```
n* = (C / C₀) ^ (1 / (3 - w))
```

En pratique, pour un algorithme récursif en blocs, `C/C₀` est de **10 à 1000**.
""")
cross = pd.DataFrame([
    {"Algorithme": "Strassen (2,807)", "C/C₀": 10, "n*": 10**(1/(3-math.log2(7)))},
    {"Algorithme": "Strassen (2,807)", "C/C₀": 100, "n*": 100**(1/(3-math.log2(7)))},
    {"Algorithme": "Strassen (2,807)", "C/C₀": 1000, "n*": 1000**(1/(3-math.log2(7)))},
    {"Algorithme": "9/4 (2,25)", "C/C₀": 10, "n*": 10**(1/(3-2.25))},
    {"Algorithme": "9/4 (2,25)", "C/C₀": 100, "n*": 100**(1/(3-2.25))},
    {"Algorithme": "9/4 (2,25)", "C/C₀": 1000, "n*": 1000**(1/(3-2.25))},
])
cross["n*"] = cross["n*"].apply(lambda x: f"{x:.2e}")
st.dataframe(cross, use_container_width=True, hide_index=True)

st.caption("⚠️ Exposants théoriques — pas des mesures de vitesse réelle. À n = 10⁹, le 9/4 gagne un facteur 5,6 millions sur le scolaire, mais le croisement pratique reste hors de portée.")