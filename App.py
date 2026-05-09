import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data_utils import load_and_process

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PropVision · India Real Estate",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  { font-family:'Inter',sans-serif; }
.stApp                      { background:#07111f; color:#cdd9f0; }
section[data-testid="stSidebar"] { background:#0b1828 !important; border-right:1px solid rgba(96,165,250,0.1); }

/* Hero */
.hero {
    background:linear-gradient(135deg,#0c1c36 0%,#0e2347 60%,#091a30 100%);
    border:1px solid rgba(96,165,250,0.2); border-radius:20px;
    padding:36px 44px 28px; margin-bottom:24px;
}
.hero-title {
    font-family:'Playfair Display',serif; font-size:2.9rem; font-weight:700;
    background:linear-gradient(120deg,#60a5fa,#a78bfa,#34d399);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0 0 6px 0; line-height:1.15;
}
.hero-sub { color:rgba(186,210,250,0.55); font-size:0.96rem; font-weight:300; letter-spacing:0.4px; }

/* KPI */
.kpi-card {
    background:linear-gradient(145deg,rgba(255,255,255,0.055),rgba(255,255,255,0.02));
    border:1px solid rgba(96,165,250,0.22); border-radius:14px;
    padding:18px 14px; text-align:center;
}
.kpi-val { font-family:'Playfair Display',serif; font-size:1.8rem; color:#60a5fa; margin:4px 0; font-weight:700; }
.kpi-lbl { color:rgba(166,198,255,0.5); font-size:0.7rem; text-transform:uppercase; letter-spacing:1.1px; }

/* Section title */
.sec-title {
    font-family:'Playfair Display',serif; font-size:1.4rem; color:#93c5fd;
    border-left:3px solid #3b82f6; padding-left:12px; margin:28px 0 16px;
}

/* Generic card */
.card {
    background:rgba(255,255,255,0.04); border:1px solid rgba(96,165,250,0.14);
    border-radius:14px; padding:20px; margin:10px 0;
}

/* ── Verdict cards ── */
.verdict-good {
    background:linear-gradient(145deg,rgba(52,211,153,0.14),rgba(16,185,129,0.06));
    border:2px solid rgba(52,211,153,0.55); border-radius:18px; padding:28px 24px; text-align:center;
}
.verdict-moderate {
    background:linear-gradient(145deg,rgba(251,191,36,0.14),rgba(245,158,11,0.06));
    border:2px solid rgba(251,191,36,0.55); border-radius:18px; padding:28px 24px; text-align:center;
}
.verdict-risky {
    background:linear-gradient(145deg,rgba(239,68,68,0.14),rgba(220,38,38,0.06));
    border:2px solid rgba(239,68,68,0.55); border-radius:18px; padding:28px 24px; text-align:center;
}
.verdict-title  { font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:700; margin:10px 0 6px; }
.verdict-sub    { font-size:0.9rem; opacity:0.72; margin-top:4px; color:#e2eaf8; }

/* Score bar */
.score-bar-wrap {
    background:rgba(255,255,255,0.07); border-radius:30px; height:12px;
    margin:10px 0 4px; overflow:hidden; border:1px solid rgba(255,255,255,0.08);
}
.score-bar-fill { height:100%; border-radius:30px; }

/* Factor pills */
.factors-grid { display:flex; flex-wrap:wrap; gap:8px; margin:10px 0; }
.factor-pill  {
    display:inline-flex; align-items:center; gap:5px;
    padding:5px 13px; border-radius:20px;
    font-size:0.79rem; font-weight:500; letter-spacing:0.2px;
}
.pill-green  { background:rgba(52,211,153,0.14); border:1px solid rgba(52,211,153,0.45); color:#34d399; }
.pill-red    { background:rgba(239,68,68,0.14);  border:1px solid rgba(239,68,68,0.45);  color:#f87171; }
.pill-yellow { background:rgba(251,191,36,0.14); border:1px solid rgba(251,191,36,0.45); color:#fbbf24; }

/* Explanation box */
.explain-box {
    background:rgba(255,255,255,0.03); border:1px solid rgba(96,165,250,0.13);
    border-radius:12px; padding:16px 18px; margin:12px 0;
    font-size:0.87rem; line-height:1.7; color:#b8ccec;
}
.explain-box strong { color:#93c5fd; }
.explain-section-hdr {
    font-size:0.72rem; text-transform:uppercase; letter-spacing:1.1px;
    color:rgba(186,210,250,0.4); margin:12px 0 6px;
}

/* Why sentences */
.why-list { list-style:none; padding:0; margin:6px 0; }
.why-list li { padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.why-list li:last-child { border-bottom:none; }

/* Price big */
.price-big { font-family:'Playfair Display',serif; font-size:2.2rem; color:#34d399; font-weight:700; }

/* Button */
div.stButton > button {
    background:linear-gradient(135deg,#1d4ed8,#5b21b6); color:white; border:none;
    border-radius:10px; padding:0.65rem 1.5rem; font-weight:600; font-size:0.95rem;
    width:100%; transition:all 0.25s; letter-spacing:0.3px;
}
div.stButton > button:hover {
    background:linear-gradient(135deg,#1e40af,#4c1d95);
    box-shadow:0 6px 22px rgba(99,102,241,0.4); transform:translateY(-1px);
}

/* Streamlit overrides */
[data-testid="stMetric"]      { background:rgba(255,255,255,0.035); border-radius:10px; padding:10px 14px; border:1px solid rgba(96,165,250,0.12); }
[data-testid="stMetricLabel"] { color:rgba(166,198,255,0.6) !important; }
[data-testid="stMetricValue"] { color:#e2eaf8 !important; font-family:'Playfair Display',serif !important; }
.stTabs [data-baseweb="tab"]  { color:rgba(166,198,255,0.55); font-weight:500; }
.stTabs [aria-selected="true"]{ color:#60a5fa !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color:#3b82f6 !important; }
details summary { color:#93c5fd !important; }
[data-testid="stPlotlyChart"] { border-radius:12px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

# ── Plotly base layout ────────────────────────────────────────────────────────
PLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.025)",
    font=dict(color="#94a3b8", family="Inter", size=11),
    xaxis=dict(gridcolor="rgba(96,165,250,0.08)", showgrid=True, zeroline=False,
               tickfont=dict(color="#64748b"), title_font=dict(color="#94a3b8")),
    yaxis=dict(gridcolor="rgba(96,165,250,0.08)", showgrid=True, zeroline=False,
               tickfont=dict(color="#64748b"), title_font=dict(color="#94a3b8")),
    legend=dict(font=dict(color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
    coloraxis_colorbar=dict(tickfont=dict(color="#64748b"), title_font=dict(color="#94a3b8")),
)
CSEQ = ["#60a5fa","#34d399","#f472b6","#fb923c","#a78bfa","#facc15","#38bdf8","#4ade80"]

def sfig(fig, h=None):
    kw = dict(**PLY, margin=dict(t=48, b=32, l=24, r=24))
    fig.update_layout(**kw)
    if h:
        fig.update_layout(height=h)
    return fig

# ── City growth rates ─────────────────────────────────────────────────────────
CITY_GROWTH = {
    "Mumbai":0.090,"New Delhi":0.085,"Noida":0.085,"Gurgaon":0.085,
    "Bangalore":0.100,"Hyderabad":0.100,"Pune":0.090,"Chennai":0.080,
    "Ahmedabad":0.075,"Kolkata":0.070,"Surat":0.075,"Jaipur":0.080,
    "Lucknow":0.075,"Kochi":0.080,"Indore":0.075,"Bhubaneswar":0.080,
    "Vishakhapatnam":0.080,"Dehradun":0.080,"Haridwar":0.075,
    "Guwahati":0.075,"Trivandrum":0.075,"Mysore":0.075,
    "Coimbatore":0.075,"Vijayawada":0.075,"Mangalore":0.070,
    "Faridabad":0.075,"Amritsar":0.070,"Ludhiana":0.070,
    "Jodhpur":0.070,"Nagpur":0.075,"Bhopal":0.075,"Patna":0.070,
    "Ranchi":0.070,"Raipur":0.070,"Warangal":0.070,"Nashik":0.075,
}

# ── Helper: per-factor explanation sentences ──────────────────────────────────
def factor_why(name, score, value_index=None, bhk=None, age=None,
               growth_rate=None, availability=None):
    if name == "Value vs Market":
        vi = round(value_index, 2) if value_index else 1.0
        if score >= 7:
            return f"Property is priced <strong>{(vi-1)*100:.0f}% below</strong> the city median — excellent value for money."
        elif score >= 4:
            return f"Price is near city median (value index {vi:.2f}) — fair deal with moderate upside."
        else:
            return f"Property is priced <strong>above the city median</strong> — limited margin of safety."
    if name == "BHK Size":
        if score >= 7:
            return f"{bhk} BHK offers strong rental demand and broad resale appeal."
        elif score >= 4:
            return f"{bhk} BHK is decent; 3+ BHK units typically command better returns."
        else:
            return f"{bhk} BHK limits rental pool and may compress resale price."
    if name == "Infrastructure":
        if score >= 7:
            return "Excellent connectivity — high transport access, schools, and hospitals nearby."
        elif score >= 4:
            return "Moderate infrastructure; some amenities or connectivity gaps exist."
        else:
            return "Weak infrastructure — low transport access or fewer civic amenities."
    if name == "Property Age":
        yr = 2024 - age if age else 0
        if score >= 7:
            return f"Built in {yr} — relatively new construction, lower maintenance risk."
        elif score >= 4:
            return f"Moderate age ({age} years); maintenance costs may rise over time."
        else:
            return f"Older property ({age} years) — higher upkeep costs and depreciation risk."
    if name == "Availability":
        if availability == "Ready_to_Move":
            return "Ready-to-move — no construction risk, immediate possession and rental income."
        else:
            return "Under construction — delayed possession risk and no immediate rental income."
    if name == "City Growth":
        gr = growth_rate * 100 if growth_rate else 7.5
        if score >= 7:
            return f"City projected at <strong>{gr:.1f}% annual growth</strong> — strong appreciation outlook."
        elif score >= 4:
            return f"Moderate city growth at {gr:.1f}% per year — stable but not exceptional."
        else:
            return f"City growth rate is {gr:.1f}% — below-average appreciation expected."
    if name == "Security":
        if score >= 7:
            return "Secured community adds value, tenant trust, and resale premium."
        else:
            return "No security features — may deter premium tenants and buyers."
    if name == "Parking":
        if score >= 7:
            return "Dedicated parking is a strong selling point in urban markets."
        else:
            return "No parking — reduces appeal for car-owning buyers and tenants."
    return ""

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading 2,50,000 property records…"):
    df = load_and_process()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">PropVision AI</div>
  <div class="hero-sub">India Real Estate Investment Intelligence &nbsp;·&nbsp;
    2,50,000 Properties &nbsp;·&nbsp; 42 Cities &nbsp;·&nbsp; 20 States</div>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k = st.columns(6)
kpis = [
    ("2,50,000",                                "Properties"),
    (f"{df['City'].nunique()}",                 "Cities"),
    (f"{df['State'].nunique()}",                "States"),
    (f"₹{df['Price_in_Lakhs'].median():.0f}L",  "Median Price"),
    (f"{df['Good_Investment'].mean()*100:.1f}%", "Good Investments"),
    (f"₹{df['Price_per_SqFt'].median()/1000:.1f}K","Median ₹/SqFt"),
]
for col, (val, lbl) in zip(k, kpis):
    col.markdown(f'<div class="kpi-card"><div class="kpi-val">{val}</div>'
                 f'<div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🔮 Investment Analyzer",
    "📊 Price & Size Analysis",
    "🗺️ Location Intelligence",
    "🔗 Feature Relationships",
    "💼 Ownership & Amenities",
    "🔍 Property Explorer",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — INVESTMENT ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="sec-title">Property Investment Analyzer</div>', unsafe_allow_html=True)
    st.caption("Enter property details to receive a weighted investment verdict, factor-by-factor reasoning, and a 5-year price forecast.")

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        c1, c2 = st.columns(2)
        with c1: state = st.selectbox("State", sorted(df["State"].unique()))
        with c2:
            cities = sorted(df[df["State"] == state]["City"].unique())
            city   = st.selectbox("City", cities)

        c3, c4 = st.columns(2)
        with c3: prop_type = st.selectbox("Property Type", sorted(df["Property_Type"].unique()))
        with c4: bhk       = st.selectbox("BHK", [1, 2, 3, 4, 5], index=2)

        c5, c6 = st.columns(2)
        with c5: size  = st.number_input("Size (SqFt)",     500,  10000, 1500, 100)
        with c6: price = st.number_input("Price (₹ Lakhs)", 10.0, 1000.0, 120.0, 5.0)

        c7, c8 = st.columns(2)
        with c7: year_built   = st.number_input("Year Built", 1980, 2024, 2015)
        with c8: furnished    = st.selectbox("Furnished Status",
                                             ["Unfurnished", "Semi-furnished", "Furnished"])

        c9, c10 = st.columns(2)
        with c9:  transport    = st.selectbox("Public Transport", ["Low","Medium","High"], index=1)
        with c10: availability = st.selectbox("Availability",
                                              ["Ready_to_Move","Under_Construction"])

        c11, c12 = st.columns(2)
        with c11: schools   = st.slider("Nearby Schools",   0, 20, 5)
        with c12: hospitals = st.slider("Nearby Hospitals", 0, 15, 3)

        c13, c14 = st.columns(2)
        with c13: parking  = st.selectbox("Parking Space", ["Yes","No"])
        with c14: security = st.selectbox("Security",      ["Yes","No"])

        amenity_sel = st.multiselect("Amenities",
                                     ["Gym","Pool","Garden","Playground","Clubhouse"],
                                     default=["Gym","Pool"])

        analyze = st.button("🔮 Analyze Investment", use_container_width=True)

    with right:
        if analyze:
            # ── Sub-scores (all normalized 0–10) ──────────────────────────────
            age = 2024 - year_built

            ppsf             = (price * 100_000) / max(size, 1)
            city_med         = df[df["City"] == city]["Price_per_SqFt"].median()
            value_index      = city_med / max(ppsf, 1)
            value_score_raw  = min(max(value_index, 0.5), 1.5)
            value_score      = (value_score_raw - 0.5) / 1.0 * 10   # 0–10

            bhk_score          = min(bhk / 5 * 10, 10)
            age_score          = max(0, (10 - age) / 10 * 10)
            availability_score = 10 if availability == "Ready_to_Move" else 5

            transport_score  = {"Low":1,"Medium":5,"High":10}[transport]
            school_score     = min(schools  / 20 * 10, 10)
            hospital_score   = min(hospitals / 15 * 10, 10)
            parking_score    = 10 if parking  == "Yes" else 0
            security_score   = 10 if security == "Yes" else 0
            amenity_count    = len(amenity_sel)
            amenity_score    = amenity_count / 5 * 10

            infra_score = (
                transport_score  * 0.25 +
                school_score     * 0.20 +
                hospital_score   * 0.20 +
                amenity_score    * 0.15 +
                security_score   * 0.10 +
                parking_score    * 0.10
            )

            growth_rate  = CITY_GROWTH.get(city, 0.075)
            growth_score = min(growth_rate / 0.10 * 10, 10)

            # ── Weighted composite ────────────────────────────────────────────
            score = (
                0.25 * value_score        +
                0.15 * bhk_score          +
                0.20 * infra_score        +
                0.10 * age_score          +
                0.10 * availability_score +
                0.10 * growth_score       +
                0.05 * security_score     +
                0.05 * parking_score
            )
            confidence = min((score / 10) * 100, 95)

            # ── Verdict ───────────────────────────────────────────────────────
            if score >= 7:
                verdict     = "GOOD INVESTMENT"
                verdict_cls = "verdict-good"
                v_icon      = "✅"
                v_color     = "#34d399"
                bar_color   = "linear-gradient(90deg,#059669,#34d399)"
                v_tagline   = "Strong fundamentals across most factors — worth serious consideration."
                summary_txt = (f"This property scores <strong>{score:.1f}/10</strong>, indicating solid investment "
                               f"potential. Key strengths include competitive pricing relative to the {city} market, "
                               f"good infrastructure, and favourable city growth dynamics.")
            elif score >= 5:
                verdict     = "MODERATE INVESTMENT"
                verdict_cls = "verdict-moderate"
                v_icon      = "⚡"
                v_color     = "#fbbf24"
                bar_color   = "linear-gradient(90deg,#b45309,#fbbf24)"
                v_tagline   = "Acceptable returns likely — negotiate price or address weak factors."
                summary_txt = (f"Score of <strong>{score:.1f}/10</strong> signals a mixed picture. "
                               f"The property has some positive attributes but also identifiable risk factors "
                               f"that could limit long-term returns. Negotiating a lower price could improve the verdict.")
            else:
                verdict     = "RISKY INVESTMENT"
                verdict_cls = "verdict-risky"
                v_icon      = "⚠️"
                v_color     = "#f87171"
                bar_color   = "linear-gradient(90deg,#b91c1c,#f87171)"
                v_tagline   = "Multiple red flags detected — exercise caution or seek alternatives."
                summary_txt = (f"Score of <strong>{score:.1f}/10</strong> reveals significant weaknesses. "
                               f"The combination of weak factors makes this property a high-risk buy at the "
                               f"current price. Consider a lower offer or look for properties in better-growth cities.")

            # ── Verdict card ──────────────────────────────────────────────────
            bar_w = int(score / 10 * 100)
            st.markdown(f"""
            <div class="{verdict_cls}">
              <div style="font-size:2.8rem;line-height:1">{v_icon}</div>
              <div class="verdict-title" style="color:{v_color}">{verdict}</div>
              <div class="verdict-sub">{v_tagline}</div>
              <div style="margin:16px 0 4px;display:flex;justify-content:space-between;
                          font-size:0.8rem;color:rgba(220,235,255,0.5)">
                <span>Composite Investment Score</span>
                <span style="color:{v_color};font-weight:700;font-size:1rem">{score:.1f} / 10</span>
              </div>
              <div class="score-bar-wrap">
                <div class="score-bar-fill" style="width:{bar_w}%;background:{bar_color}"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:8px;
                          font-size:0.76rem;color:rgba(200,220,255,0.4)">
                <span>0 — Risky</span>
                <span>Analyst Confidence: <strong style="color:rgba(200,220,255,0.7)">{confidence:.0f}%</strong></span>
                <span>10 — Excellent</span>
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Factor data ───────────────────────────────────────────────────
            factor_data = [
                ("Value vs Market",   value_score,        0.25),
                ("Infrastructure",    infra_score,        0.20),
                ("BHK Size",          bhk_score,          0.15),
                ("City Growth",       growth_score,       0.10),
                ("Property Age",      age_score,          0.10),
                ("Availability",      availability_score, 0.10),
                ("Security",          security_score,     0.05),
                ("Parking",           parking_score,      0.05),
            ]

            # ── Why card with pills + sentences ──────────────────────────────
            pills_good = pills_mid = pills_bad = ""
            why_sentences_good = why_sentences_mid = why_sentences_bad = ""

            for fname, fscore, weight in factor_data:
                why = factor_why(fname, fscore,
                                 value_index=value_index, bhk=bhk, age=age,
                                 growth_rate=growth_rate, availability=availability)
                weight_lbl = f"{int(weight*100)}% weight"
                if fscore >= 7:
                    pills_good += f'<span class="factor-pill pill-green">✓ {fname}</span>'
                    why_sentences_good += f'<li><span style="color:#34d399;font-weight:600">✓ {fname}</span> <span style="color:rgba(186,210,250,0.4);font-size:0.75rem">({weight_lbl})</span><br><span style="color:#b8ccec">{why}</span></li>'
                elif fscore >= 4:
                    pills_mid  += f'<span class="factor-pill pill-yellow">~ {fname}</span>'
                    why_sentences_mid += f'<li><span style="color:#fbbf24;font-weight:600">~ {fname}</span> <span style="color:rgba(186,210,250,0.4);font-size:0.75rem">({weight_lbl})</span><br><span style="color:#b8ccec">{why}</span></li>'
                else:
                    pills_bad  += f'<span class="factor-pill pill-red">✗ {fname}</span>'
                    why_sentences_bad += f'<li><span style="color:#f87171;font-weight:600">✗ {fname}</span> <span style="color:rgba(186,210,250,0.4);font-size:0.75rem">({weight_lbl})</span><br><span style="color:#b8ccec">{why}</span></li>'

            st.markdown(f"""
            <div class="explain-box">
              <div style="font-size:0.92rem;font-weight:600;color:#93c5fd;margin-bottom:10px">
                📋 Why this verdict?
              </div>
              <div style="color:#b8ccec;font-size:0.86rem;margin-bottom:14px;line-height:1.7">
                {summary_txt}
              </div>

              <div class="explain-section-hdr">AT A GLANCE</div>
              <div class="factors-grid">
                {pills_good}{pills_mid}{pills_bad}
              </div>

              {"<div class='explain-section-hdr' style='margin-top:14px'>STRENGTHS</div><ul class='why-list'>" + why_sentences_good + "</ul>" if why_sentences_good else ""}
              {"<div class='explain-section-hdr' style='margin-top:10px'>NEUTRAL FACTORS</div><ul class='why-list'>" + why_sentences_mid + "</ul>" if why_sentences_mid else ""}
              {"<div class='explain-section-hdr' style='margin-top:10px'>WEAKNESSES</div><ul class='why-list'>" + why_sentences_bad + "</ul>" if why_sentences_bad else ""}
            </div>""", unsafe_allow_html=True)

            # ── Factor bar chart ──────────────────────────────────────────────
            fnames  = [f[0] for f in factor_data]
            fscores = [round(f[1], 1) for f in factor_data]
            fcolors = ["#34d399" if s >= 7 else "#fbbf24" if s >= 4 else "#f87171"
                       for s in fscores]

            fig_f = go.Figure(go.Bar(
                x=fscores, y=fnames, orientation="h",
                marker=dict(color=fcolors, line=dict(width=0)),
                text=[f"{s:.1f}" for s in fscores],
                textposition="outside",
                textfont=dict(color="#94a3b8", size=11),
                cliponaxis=False,
            ))
            fig_f.add_vline(x=7, line_dash="dot", line_color="rgba(52,211,153,0.35)",
                            annotation_text="Good ≥7", annotation_font_color="#34d399",
                            annotation_font_size=10, annotation_position="top right")
            fig_f.add_vline(x=5, line_dash="dot", line_color="rgba(251,191,36,0.35)",
                            annotation_text="Moderate ≥5", annotation_font_color="#fbbf24",
                            annotation_font_size=10, annotation_position="top right")
            fig_f.update_layout(**PLY)
            fig_f.update_layout(
                height=300,
                margin=dict(t=38, b=20, l=10, r=56),
                title=dict(text="Factor Score Breakdown  (0 – 10)", font=dict(size=12, color="#e2eaf8")),
                xaxis=dict(range=[0, 12.5], showgrid=True, gridcolor="rgba(96,165,250,0.08)",
                           tickfont=dict(color="#64748b")),
                yaxis=dict(showgrid=False, tickfont=dict(color="#cbd5e1", size=11)),
            )
            st.plotly_chart(fig_f, use_container_width=True)

            # ── 5-Year price forecast ─────────────────────────────────────────
            future_price = price * (1 + growth_rate) ** 5
            appreciation = future_price - price
            pct          = (appreciation / price) * 100

            st.markdown(f"""
            <div class="card">
              <div style="color:rgba(166,198,255,0.5);font-size:0.7rem;
                          text-transform:uppercase;letter-spacing:1.1px;margin-bottom:6px">
                5-Year Price Forecast
              </div>
              <div class="price-big">₹{future_price:.1f}L</div>
              <div style="color:#34d399;margin-top:6px;font-weight:500">
                +₹{appreciation:.1f}L &nbsp;·&nbsp; +{pct:.1f}% total return
              </div>
              <div style="color:rgba(166,198,255,0.4);font-size:0.82rem;margin-top:4px">
                City annual growth rate: {growth_rate*100:.1f}% &nbsp;·&nbsp; Compounded over 5 years
              </div>
            </div>""", unsafe_allow_html=True)

            # Year-by-year trajectory
            yrs_lbl   = ["Now"] + [f"Yr {i}" for i in range(1, 6)]
            yrs_price = [price] + [price * (1 + growth_rate) ** i for i in range(1, 6)]
            p_color   = "#34d399" if score >= 7 else "#fbbf24" if score >= 5 else "#f87171"
            rgb       = tuple(int(p_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

            fig_proj = go.Figure()
            fig_proj.add_trace(go.Scatter(
                x=yrs_lbl, y=yrs_price,
                mode="lines+markers+text",
                text=[f"₹{p:.0f}L" for p in yrs_price],
                textposition="top center",
                textfont=dict(size=10, color=p_color),
                fill="tozeroy", fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.08)",
                line=dict(color=p_color, width=2.5),
                marker=dict(size=8, color=p_color),
            ))
            fig_proj.update_layout(**PLY)
            fig_proj.update_layout(
                height=215, showlegend=False,
                margin=dict(t=40, b=20, l=20, r=20),
                title=dict(text="Price Trajectory (₹ Lakhs)", font=dict(size=12, color="#e2eaf8")),
            )
            st.plotly_chart(fig_proj, use_container_width=True)

            # ── Radar chart ───────────────────────────────────────────────────
            r_labels = ["Transport","Schools","Hospitals","Amenities","Security","Parking"]
            r_vals   = [transport_score, school_score, hospital_score,
                        amenity_score, security_score, parking_score]
            r_fill   = (f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.18)")

            fig_rad = go.Figure(go.Scatterpolar(
                r=r_vals + [r_vals[0]],
                theta=r_labels + [r_labels[0]],
                fill="toself", fillcolor=r_fill,
                line=dict(color=p_color, width=2.5),
                marker=dict(size=5, color=p_color),
            ))
            fig_rad.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(range=[0, 10], gridcolor="rgba(96,165,250,0.12)",
                                   tickfont=dict(color="#475569", size=9), color="#475569"),
                    angularaxis=dict(tickfont=dict(color="#94a3b8", size=10)),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", family="Inter"),
                height=270,
                margin=dict(t=36, b=20, l=40, r=40),
                title=dict(text="Infrastructure Profile", font=dict(size=12, color="#e2eaf8")),
            )
            st.plotly_chart(fig_rad, use_container_width=True)

            # ── Comparable properties ─────────────────────────────────────────
            comp = df[
                (df["City"]          == city) &
                (df["BHK"]           == bhk)  &
                (df["Property_Type"] == prop_type) &
                (df["Price_in_Lakhs"].between(price * 0.8, price * 1.2))
            ][["Locality","Price_in_Lakhs","Size_in_SqFt","Price_per_SqFt",
               "Good_Investment","Future_Price_5Yr"]].head(6)

            if not comp.empty:
                st.markdown(
                    '<div style="font-size:0.9rem;font-weight:600;color:#93c5fd;margin:16px 0 8px">'
                    '📋 Comparable Properties in Your City</div>',
                    unsafe_allow_html=True)
                st.dataframe(comp.reset_index(drop=True), use_container_width=True,
                    column_config={
                        "Good_Investment":  st.column_config.CheckboxColumn("Good?"),
                        "Price_in_Lakhs":   st.column_config.NumberColumn("Price (L)",    format="₹%.1f"),
                        "Future_Price_5Yr": st.column_config.NumberColumn("5yr (L)",      format="₹%.1f"),
                        "Price_per_SqFt":   st.column_config.NumberColumn("₹/SqFt",      format="₹%.0f"),
                    })
        else:
            st.markdown("""
            <div style="text-align:center;padding:90px 20px;opacity:0.35">
              <div style="font-size:4rem">🏡</div>
              <div style="font-size:1rem;margin-top:16px;line-height:1.75;color:#b8ccec">
                Fill in the property details<br>and click <strong>Analyze Investment</strong>
              </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PRICE & SIZE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-title">Price & Size Analysis</div>', unsafe_allow_html=True)

    with st.expander("⚙️ Filters", expanded=False):
        fa, fb, fc = st.columns(3)
        with fa: f_city1 = st.multiselect("City",          sorted(df["City"].unique()),          key="p_city")
        with fb: f_type1 = st.multiselect("Property Type", sorted(df["Property_Type"].unique()), key="p_type")
        with fc: f_pr    = st.slider("Price Range (Lakhs)", 10.0, 500.0, (10.0, 500.0),          key="p_pr")

    df1 = df.copy()
    if f_city1: df1 = df1[df1["City"].isin(f_city1)]
    if f_type1: df1 = df1[df1["Property_Type"].isin(f_type1)]
    df1     = df1[df1["Price_in_Lakhs"].between(*f_pr)]
    sample1 = df1.sample(min(50000, len(df1)), random_state=42)

    r1, r2 = st.columns(2)
    with r1:
        fig = px.histogram(sample1, x="Price_in_Lakhs", nbins=60,
                           title="Q1 · Distribution of Property Prices",
                           color_discrete_sequence=["#60a5fa"])
        fig.add_vline(x=df1["Price_in_Lakhs"].median(), line_dash="dash",
                      line_color="#fbbf24", annotation_text="Median",
                      annotation_font_color="#fbbf24")
        st.plotly_chart(sfig(fig, 340), use_container_width=True)
    with r2:
        fig = px.histogram(sample1, x="Size_in_SqFt", nbins=60,
                           title="Q2 · Distribution of Property Sizes",
                           color_discrete_sequence=["#a78bfa"])
        fig.add_vline(x=df1["Size_in_SqFt"].median(), line_dash="dash",
                      line_color="#fbbf24", annotation_text="Median",
                      annotation_font_color="#fbbf24")
        st.plotly_chart(sfig(fig, 340), use_container_width=True)

    r3, r4 = st.columns(2)
    with r3:
        fig = px.box(df1, x="Property_Type", y="Price_per_SqFt",
                     color="Property_Type", color_discrete_sequence=CSEQ,
                     title="Q3 · Price/SqFt by Property Type")
        fig.update_yaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)
    with r4:
        fig = px.scatter(sample1, x="Size_in_SqFt", y="Price_in_Lakhs",
                         color="Property_Type", opacity=0.4,
                         color_discrete_sequence=CSEQ,
                         title="Q4 · Property Size vs Price")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)

    st.markdown('<div class="sec-title" style="font-size:1.1rem">Q5 · Outlier Detection</div>', unsafe_allow_html=True)
    o1, o2 = st.columns(2)
    with o1:
        q1_p, q3_p = df1["Price_per_SqFt"].quantile([0.25, 0.75])
        out_p = df1[df1["Price_per_SqFt"] > q3_p + 1.5 * (q3_p - q1_p)]
        fig   = px.box(df1, x="Property_Type", y="Price_per_SqFt",
                       title=f"Outliers in Price/SqFt — {len(out_p):,} detected",
                       color="Property_Type", color_discrete_sequence=CSEQ, points="outliers")
        st.plotly_chart(sfig(fig, 320), use_container_width=True)
    with o2:
        q1_s, q3_s = df1["Size_in_SqFt"].quantile([0.25, 0.75])
        out_s = df1[df1["Size_in_SqFt"] > q3_s + 1.5 * (q3_s - q1_s)]
        fig   = px.box(df1, x="BHK", y="Size_in_SqFt",
                       title=f"Outliers in Size — {len(out_s):,} detected",
                       color="BHK", color_discrete_sequence=CSEQ, points="outliers")
        st.plotly_chart(sfig(fig, 320), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LOCATION INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec-title">Location-Based Analysis</div>', unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        s6 = df.groupby("State")["Price_per_SqFt"].mean().sort_values(ascending=True).reset_index()
        fig = px.bar(s6, y="State", x="Price_per_SqFt", orientation="h",
                     title="Q6 · Avg Price/SqFt by State",
                     color="Price_per_SqFt", color_continuous_scale="Blues")
        fig.update_xaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 430), use_container_width=True)
    with r2:
        s7 = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(20).reset_index()
        fig = px.bar(s7, x="City", y="Price_in_Lakhs",
                     title="Q7 · Top 20 Cities by Avg Property Price",
                     color="Price_in_Lakhs", color_continuous_scale="Blues")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(sfig(fig, 430), use_container_width=True)

    r3, r4 = st.columns(2)
    with r3:
        s8 = df.groupby("Locality")["Age_of_Property"].median().sort_values().head(20).reset_index()
        fig = px.bar(s8, x="Locality", y="Age_of_Property",
                     title="Q8 · Youngest 20 Localities by Median Age",
                     color="Age_of_Property", color_continuous_scale="YlOrRd")
        fig.update_xaxes(tickangle=55, tickfont=dict(size=9))
        st.plotly_chart(sfig(fig, 380), use_container_width=True)
    with r4:
        top_cities = df["City"].value_counts().head(12).index
        s9 = (df[df["City"].isin(top_cities)]
              .groupby(["City","BHK"]).size().reset_index(name="Count"))
        fig = px.bar(s9, x="City", y="Count", color="BHK", barmode="stack",
                     title="Q9 · BHK Distribution Across Top Cities",
                     color_discrete_sequence=CSEQ)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(sfig(fig, 380), use_container_width=True)

    top5_loc = (df.groupby("Locality")["Price_in_Lakhs"].mean()
                  .sort_values(ascending=False).head(5).index)
    s10 = (df[df["Locality"].isin(top5_loc)]
           .groupby(["Locality","BHK"])["Price_in_Lakhs"].mean().reset_index())
    fig = px.line(s10, x="BHK", y="Price_in_Lakhs", color="Locality",
                  markers=True,
                  title="Q10 · Price Trends for Top 5 Expensive Localities (by BHK)",
                  color_discrete_sequence=CSEQ)
    st.plotly_chart(sfig(fig, 360), use_container_width=True)

    st.markdown('<div class="sec-title" style="font-size:1.1rem">City Investment Map</div>',
                unsafe_allow_html=True)
    city_inv = df.groupby("City").agg(
        Good_Pct=("Good_Investment","mean"),
        Avg_Price=("Price_in_Lakhs","mean"),
        Count=("ID","count"),
    ).reset_index()
    city_inv["Good_Pct_Disp"] = (city_inv["Good_Pct"] * 100).round(1)
    fig = px.scatter(city_inv, x="Avg_Price", y="Good_Pct_Disp",
                     size="Count", color="Good_Pct_Disp", text="City",
                     title="City: Avg Price vs Good Investment %",
                     color_continuous_scale="Greens",
                     labels={"Good_Pct_Disp":"Good Invest %","Avg_Price":"Avg Price (Lakhs)"})
    fig.update_traces(textposition="top center", textfont=dict(size=9, color="#94a3b8"))
    st.plotly_chart(sfig(fig, 450), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FEATURE RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec-title">Feature Relationships & Correlations</div>',
                unsafe_allow_html=True)

    num_cols = ["BHK","Size_in_SqFt","Price_in_Lakhs","Price_per_SqFt",
                "Age_of_Property","Nearby_Schools","Nearby_Hospitals",
                "Infrastructure_Score","Value_Index","Future_Price_5Yr",
                "Good_Investment","Amenity_Count"]
    corr = df[num_cols].corr().round(3)
    fig  = px.imshow(corr, text_auto=".2f", title="Q11 · Correlation Heatmap",
                     color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
    fig.update_layout(**PLY, height=450, margin=dict(t=48, b=32, l=24, r=24))
    st.plotly_chart(fig, use_container_width=True)

    r2c, r3c = st.columns(2)
    with r2c:
        s12 = df.groupby("Nearby_Schools")["Price_per_SqFt"].mean().reset_index()
        fig  = px.bar(s12, x="Nearby_Schools", y="Price_per_SqFt",
                      title="Q12 · Nearby Schools vs Avg Price/SqFt",
                      color="Price_per_SqFt", color_continuous_scale="Blues")
        fig.update_xaxes(title="Number of Nearby Schools")
        fig.update_yaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)
    with r3c:
        s13 = df.groupby("Nearby_Hospitals")["Price_per_SqFt"].mean().reset_index()
        fig  = px.bar(s13, x="Nearby_Hospitals", y="Price_per_SqFt",
                      title="Q13 · Nearby Hospitals vs Avg Price/SqFt",
                      color="Price_per_SqFt", color_continuous_scale="Greens")
        fig.update_xaxes(title="Number of Nearby Hospitals")
        fig.update_yaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)

    r4c, r5c = st.columns(2)
    with r4c:
        fig = px.violin(df.sample(30000, random_state=1),
                        x="Furnished_Status", y="Price_in_Lakhs",
                        color="Furnished_Status", box=True,
                        title="Q14 · Price by Furnished Status",
                        color_discrete_sequence=CSEQ,
                        category_orders={"Furnished_Status":
                                         ["Unfurnished","Semi-furnished","Furnished"]})
        st.plotly_chart(sfig(fig, 360), use_container_width=True)
    with r5c:
        s15 = (df.groupby("Facing")["Price_per_SqFt"].mean()
                 .sort_values(ascending=False).reset_index())
        fig  = px.bar(s15, x="Facing", y="Price_per_SqFt",
                      title="Q15 · Price/SqFt by Facing Direction",
                      color="Price_per_SqFt", color_continuous_scale="Purples")
        fig.update_yaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — OWNERSHIP & AMENITIES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec-title">Ownership, Amenities & Investment Factors</div>',
                unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        s16 = df["Owner_Type"].value_counts().reset_index()
        fig  = px.pie(s16, names="Owner_Type", values="count",
                      title="Q16 · Properties by Owner Type",
                      color_discrete_sequence=CSEQ, hole=0.48)
        fig.update_layout(**PLY, height=360, margin=dict(t=48, b=32, l=24, r=24))
        st.plotly_chart(fig, use_container_width=True)
    with r2:
        s17 = df["Availability_Status"].value_counts().reset_index()
        fig  = px.pie(s17, names="Availability_Status", values="count",
                      title="Q17 · Availability Status",
                      color_discrete_sequence=["#34d399","#fbbf24"], hole=0.48)
        fig.update_layout(**PLY, height=360, margin=dict(t=48, b=32, l=24, r=24))
        st.plotly_chart(fig, use_container_width=True)

    r3, r4 = st.columns(2)
    with r3:
        s18     = df.groupby("Parking_Space")[["Price_in_Lakhs"]].mean().reset_index()
        pct_d18 = (s18.loc[s18["Parking_Space"]=="Yes","Price_in_Lakhs"].values[0] /
                   s18.loc[s18["Parking_Space"]=="No","Price_in_Lakhs"].values[0] - 1) * 100
        fig = px.bar(s18, x="Parking_Space", y="Price_in_Lakhs",
                     color="Parking_Space",
                     title=f"Q18 · Parking vs Avg Price  ({pct_d18:+.1f}% premium)",
                     color_discrete_sequence=["#60a5fa","#475569"])
        st.plotly_chart(sfig(fig, 360), use_container_width=True)
    with r4:
        s19 = df.groupby("Amenity_Count")["Price_per_SqFt"].mean().reset_index()
        fig  = px.bar(s19, x="Amenity_Count", y="Price_per_SqFt",
                      title="Q19 · Amenity Count vs Avg Price/SqFt",
                      color="Price_per_SqFt", color_continuous_scale="Viridis")
        fig.update_xaxes(title="Number of Amenities")
        fig.update_yaxes(title="₹ per SqFt")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)

    r5, r6 = st.columns(2)
    with r5:
        fig = px.box(df.sample(30000, random_state=2),
                     x="Public_Transport_Accessibility", y="Price_per_SqFt",
                     color="Public_Transport_Accessibility",
                     title="Q20 · Transport Accessibility vs Price/SqFt",
                     color_discrete_sequence=["#f87171","#fbbf24","#34d399"],
                     category_orders={"Public_Transport_Accessibility":["Low","Medium","High"]})
        st.plotly_chart(sfig(fig, 360), use_container_width=True)
    with r6:
        tinv       = df.groupby("Public_Transport_Accessibility")["Good_Investment"].mean().reset_index()
        tinv["Pct"]= tinv["Good_Investment"] * 100
        fig = px.bar(tinv, x="Public_Transport_Accessibility", y="Pct",
                     title="Q20 · Transport Level vs Good Investment %",
                     color="Pct", color_continuous_scale="Greens",
                     category_orders={"Public_Transport_Accessibility":["Low","Medium","High"]})
        fig.update_yaxes(title="Good Investment %")
        st.plotly_chart(sfig(fig, 360), use_container_width=True)

    st.markdown('<div class="sec-title" style="font-size:1.1rem">Individual Amenity Impact on Price/SqFt</div>',
                unsafe_allow_html=True)
    a_cols   = ["Has_Gym","Has_Pool","Has_Garden","Has_Playground","Has_Clubhouse"]
    a_labels = ["Gym","Pool","Garden","Playground","Clubhouse"]
    w_price  = [df[df[a]==1]["Price_per_SqFt"].mean() for a in a_cols]
    wo_price = [df[df[a]==0]["Price_per_SqFt"].mean() for a in a_cols]
    fig = go.Figure(data=[
        go.Bar(name="With Amenity",    x=a_labels, y=w_price,  marker_color="#60a5fa"),
        go.Bar(name="Without Amenity", x=a_labels, y=wo_price, marker_color="#475569"),
    ])
    fig.update_layout(**PLY)
    fig.update_layout(
        barmode="group", height=340,
        margin=dict(t=48, b=32, l=24, r=24),
        title=dict(text="Avg Price/SqFt With vs Without Each Amenity",
                   font=dict(size=14, color="#e2eaf8")),
        yaxis_title="₹ per SqFt",
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROPERTY EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec-title">Property Explorer</div>', unsafe_allow_html=True)

    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1: f_state_e = st.multiselect("State", sorted(df["State"].unique()), key="e_state")
    with ex2:
        cities_e = (sorted(df[df["State"].isin(f_state_e)]["City"].unique())
                    if f_state_e else sorted(df["City"].unique()))
        f_city_e = st.multiselect("City", cities_e, key="e_city")
    with ex3: f_type_e = st.multiselect("Property Type", sorted(df["Property_Type"].unique()), key="e_type")
    with ex4: f_bhk_e  = st.multiselect("BHK", sorted(df["BHK"].unique()), key="e_bhk")

    ex5, ex6, ex7 = st.columns(3)
    with ex5: pr_e = st.slider("Price (Lakhs)", 10.0, 500.0, (10.0, 300.0), key="e_pr")
    with ex6: sz_e = st.slider("Size (SqFt)",    500,  5000,  (500,  3000),  key="e_sz")
    with ex7:
        inv_only       = st.checkbox("Good Investments only", False, key="e_gi")
        availability_e = st.selectbox("Availability",
                                      ["All","Ready_to_Move","Under_Construction"], key="e_av")

    df_e = df.copy()
    if f_state_e:               df_e = df_e[df_e["State"].isin(f_state_e)]
    if f_city_e:                df_e = df_e[df_e["City"].isin(f_city_e)]
    if f_type_e:                df_e = df_e[df_e["Property_Type"].isin(f_type_e)]
    if f_bhk_e:                 df_e = df_e[df_e["BHK"].isin(f_bhk_e)]
    df_e = df_e[df_e["Price_in_Lakhs"].between(*pr_e)]
    df_e = df_e[df_e["Size_in_SqFt"].between(*sz_e)]
    if inv_only:                df_e = df_e[df_e["Good_Investment"] == 1]
    if availability_e != "All": df_e = df_e[df_e["Availability_Status"] == availability_e]

    st.markdown(f"**{len(df_e):,}** properties match your filters")

    show_cols = ["State","City","Locality","Property_Type","BHK","Size_in_SqFt",
                 "Price_in_Lakhs","Price_per_SqFt","Age_of_Property","Furnished_Status",
                 "Availability_Status","Infrastructure_Score","Good_Investment",
                 "Future_Price_5Yr","Appreciation_Pct"]

    st.dataframe(
        df_e[show_cols].sort_values("Good_Investment", ascending=False).head(500).reset_index(drop=True),
        use_container_width=True, height=440,
        column_config={
            "Good_Investment":      st.column_config.CheckboxColumn("Good Invest?"),
            "Price_in_Lakhs":       st.column_config.NumberColumn("Price (L)",     format="₹%.1f"),
            "Price_per_SqFt":       st.column_config.NumberColumn("₹/SqFt",       format="₹%.0f"),
            "Future_Price_5Yr":     st.column_config.NumberColumn("5yr Price (L)", format="₹%.1f"),
            "Infrastructure_Score": st.column_config.ProgressColumn(
                "Infra Score", min_value=0, max_value=10, format="%.1f"),
            "Appreciation_Pct":     st.column_config.NumberColumn("5yr Return %",  format="%.1f%%"),
        }
    )

    if not df_e.empty:
        st.markdown('<div class="sec-title" style="font-size:1.1rem">Summary Statistics</div>',
                    unsafe_allow_html=True)
        st.dataframe(
            df_e[["Price_in_Lakhs","Price_per_SqFt","Size_in_SqFt","BHK",
                  "Age_of_Property","Infrastructure_Score","Future_Price_5Yr"
                  ]].describe().round(2),
            use_container_width=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:rgba(148,163,184,0.3);font-size:0.78rem;padding:8px 0">'
    'PropVision AI &nbsp;·&nbsp; India Real Estate Investment Intelligence'
    ' &nbsp;·&nbsp; 2,50,000 Properties &nbsp;·&nbsp; Built with Streamlit'
    '</div>',
    unsafe_allow_html=True,
)
