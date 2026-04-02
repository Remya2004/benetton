import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

# ═══════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="United Colors of Benetton — SS27 Buying Portal",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# 2. BENETTON BRAND CSS — refined palette, better contrast
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Deep forest green — true Benetton, not neon */
.stApp { background-color: #1a3d2b !important; color: #FFFFFF !important; }

[data-testid="stSidebar"] { background-color: #122b1e !important; border-right: 1px solid rgba(255,255,255,0.12) !important; }
[data-testid="stSidebar"] * { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important; color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #FFFFFF !important; background-color: transparent !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background-color: rgba(255,255,255,0.15) !important; }
[data-testid="stSidebar"] input[type="number"] {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #FFFFFF !important; border-radius: 8px !important;
}

h1 { color: #FFFFFF !important; font-weight: 700 !important; font-size: 2.2rem !important; letter-spacing: -0.5px !important; }
h2 { color: #FFFFFF !important; font-weight: 600 !important; font-size: 1.3rem !important; }
h3 { color: rgba(255,255,255,0.9) !important; font-weight: 500 !important; }

/* Metric cards — deeper tonal bg */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important; padding: 16px 14px !important;
    min-height: 90px !important; overflow: visible !important;
}
[data-testid="stMetricLabel"] > div { white-space: normal !important; overflow: visible !important; }
[data-testid="stMetricLabel"] p { white-space: normal !important; word-break: break-word !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.75) !important; font-size: 12px !important; font-weight: 500 !important; letter-spacing: 0.3px !important; white-space: normal !important; overflow: visible !important; text-overflow: unset !important; word-break: break-word !important; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 20px !important; font-weight: 700 !important; white-space: normal !important; overflow: visible !important; text-overflow: unset !important; word-break: break-all !important; }
[data-testid="stMetricValue"] > div { white-space: normal !important; overflow: visible !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.2) !important; border-radius: 12px !important; padding: 4px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { background-color: transparent !important; color: rgba(255,255,255,0.75) !important; border-radius: 8px !important; font-weight: 500 !important; font-size: 13px !important; padding: 8px 18px !important; border: none !important; }
.stTabs [aria-selected="true"] { background-color: #FFFFFF !important; color: #1a3d2b !important; font-weight: 700 !important; }
.stTabs [aria-selected="true"] * { color: #1a3d2b !important; }
.stTabs [aria-selected="true"] p { color: #1a3d2b !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] div { color: #1a3d2b !important; }

.stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.1) !important; }

.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important; color: #FFFFFF !important;
    padding: 12px 16px !important; font-size: 14px !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.4) !important; }
.stTextInput label { color: rgba(255,255,255,0.8) !important; }

.stAlert { background-color: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 10px !important; color: #FFFFFF !important; }
hr { border-color: rgba(255,255,255,0.12) !important; margin: 28px 0 !important; }

.stDownloadButton > button {
    background-color: #FFFFFF !important; color: #1a3d2b !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; padding: 10px 20px !important;
    width: 100% !important; font-size: 13px !important;
}
.stDownloadButton > button:hover { background-color: rgba(255,255,255,0.88) !important; }

/* Paragraph and body text — bright enough to read */
p, li, .stMarkdown p { color: rgba(255,255,255,0.88) !important; }
.stCaption, small, [data-testid="stCaptionContainer"] p { color: rgba(255,255,255,0.55) !important; font-size: 12px !important; }
[data-testid="stInfo"] { background-color: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 10px !important; color: #FFFFFF !important; }

/* Dropdowns — menus */
[data-baseweb="popover"], [data-baseweb="menu"] { background-color: #122b1e !important; }
[data-baseweb="option"] { background-color: #122b1e !important; color: #FFFFFF !important; }
[data-baseweb="option"]:hover { background-color: rgba(255,255,255,0.12) !important; }

/* Multiselect tags — WHITE bg, DARK text, always readable */
[data-baseweb="tag"] { background-color: #FFFFFF !important; color: #1a3d2b !important; }
[data-baseweb="tag"] span { color: #1a3d2b !important; }
[data-baseweb="tag"] svg { fill: #1a3d2b !important; }
[data-baseweb="tag"] button { color: #1a3d2b !important; }

/* Selectbox single selected value */
[data-baseweb="select"] [class*="singleValue"] { color: #FFFFFF !important; }
[data-baseweb="select"] [class*="placeholder"] { color: rgba(255,255,255,0.45) !important; }
[data-baseweb="select"] > div > div { color: #FFFFFF !important; }
[data-baseweb="select"] input { color: #FFFFFF !important; }

/* Number input stepper buttons */
[data-testid="stNumberInput"] button {
    background-color: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* Download button — always dark text on white */
.stDownloadButton > button { color: #1a3d2b !important; }
.stDownloadButton > button * { color: #1a3d2b !important; }

/* Bold text visible */
strong, b { color: #FFFFFF !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.25); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 3. HELPER COMPONENTS
# ═══════════════════════════════════════════════════════════════
BENETTON_COLORS = ["#FFFFFF","#B3DFCA","#66BF94","#2d7a52","#1a3d2b","#FFD700","#FF6B35","#4ECDC4"]

def benetton_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.12)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        legend=dict(bgcolor="rgba(0,0,0,0.25)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1, font=dict(color="#FFFFFF",size=12)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", tickfont=dict(color="rgba(255,255,255,0.75)"), title_font=dict(color="rgba(255,255,255,0.75)")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", tickfont=dict(color="rgba(255,255,255,0.75)"), title_font=dict(color="rgba(255,255,255,0.75)")),
        margin=dict(t=40, b=40, l=10, r=10)
    )
    return fig

def section_header(icon, title, subtitle=None):
    sub = f'<div style="font-size:13px;color:rgba(255,255,255,0.55);margin-top:4px;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div style="margin:32px 0 16px 0;">
        <div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px;">{icon} SECTION</div>
        <div style="font-size:22px;font-weight:700;color:#FFFFFF;letter-spacing:-0.3px;">{title}</div>{sub}
    </div>""", unsafe_allow_html=True)

def insight_card(html):
    st.markdown(f"""<div style="background:rgba(255,255,255,0.06);border-left:3px solid #FFFFFF;border-radius:0 10px 10px 0;padding:14px 20px;margin:12px 0;font-size:14px;color:rgba(255,255,255,0.88);line-height:1.7;">💡 {html}</div>""", unsafe_allow_html=True)

def warning_card(msg):
    st.markdown(f"""<div style="background:rgba(255,200,0,0.1);border-left:3px solid #FFD700;border-radius:0 10px 10px 0;padding:14px 20px;margin:12px 0;font-size:14px;color:rgba(255,255,255,0.88);">⚠️ {msg}</div>""", unsafe_allow_html=True)

def event_card(tag, when, direction, colours, mood, why_now, key_cats, key_fits):
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:22px 24px;margin:12px 0 20px 0;">
        <div style="margin-bottom:14px;">
            <span style="background:rgba(255,255,255,0.15);color:#FFFFFF;padding:4px 12px;border-radius:20px;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">{tag}</span>
            <span style="margin-left:12px;color:rgba(255,255,255,0.45);font-size:12px;">{when}</span>
        </div>
        <p style="color:rgba(255,255,255,0.9);font-size:15px;line-height:1.7;margin:0 0 16px 0;">{direction}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">
            <div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:12px 14px;">
                <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Colour Palette</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.88);">{colours}</div>
            </div>
            <div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:12px 14px;">
                <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Mood</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.88);">{mood}</div>
            </div>
            <div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:12px 14px;">
                <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Priority Categories</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.88);">{' · '.join(key_cats)}</div>
            </div>
            <div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:12px 14px;">
                <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Key Silhouettes</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.88);">{' · '.join(key_fits)}</div>
            </div>
        </div>
        <div style="margin-top:12px;background:rgba(255,255,255,0.05);border-radius:8px;padding:12px 14px;">
            <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;">Why This Works Commercially</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.8);line-height:1.6;">{why_now}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 4. LOAD DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    basepath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(basepath, "data_cleaned.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, low_memory=False)
        df.columns = df.columns.astype(str).str.strip().str.upper()
        return df
    return None

df = load_data()
if df is None:
    st.error("data_cleaned.csv not found. Run clean_data.py first.")
    st.stop()

# ═══════════════════════════════════════════════════════════════
# 5. SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:16px 0 8px 0;text-align:center;">
        <img src="data:image/png;base64,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" style="width:160px;border-radius:10px;display:block;margin:0 auto;" />
        <div style="margin-top:10px;font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;">SS27 Controls</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">SEASON</p>', unsafe_allow_html=True)
    season_list = sorted(df["SEASON"].dropna().unique()) if "SEASON" in df.columns else []
    selected_seasons = st.multiselect("", season_list, default=season_list, label_visibility="collapsed")

    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin:12px 0 4px 0;">TARGET REGION</p>', unsafe_allow_html=True)
    region_list = sorted(df["REGION"].dropna().unique())
    selected_region = st.selectbox("", region_list, label_visibility="collapsed")

    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin:12px 0 4px 0;">GENDER</p>', unsafe_allow_html=True)
    gender_list = sorted(df["GENDER"].dropna().unique()) if "GENDER" in df.columns else []
    selected_gender = st.multiselect("", gender_list, default=gender_list, label_visibility="collapsed")

    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin:12px 0 4px 0;">CATEGORIES</p>', unsafe_allow_html=True)
    cat_list = sorted(df["CAT"].dropna().unique())
    selected_cats = st.multiselect("", cat_list, default=cat_list, label_visibility="collapsed")

    st.divider()
    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">PRICE BAND (MRP ₹)</p>', unsafe_allow_html=True)
    m_min = int(df["MRP/ UNIT"].min()) if "MRP/ UNIT" in df.columns else 0
    m_max = int(df["MRP/ UNIT"].max()) if "MRP/ UNIT" in df.columns else 5000
    price_range = st.slider("", m_min, m_max, (m_min, m_max), label_visibility="collapsed")

    st.divider()
    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">BUYING LOGIC</p>', unsafe_allow_html=True)
    st.markdown("""<div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:12px 14px;font-size:12px;color:rgba(255,255,255,0.85);line-height:1.9;">
        <b style="color:#FFFFFF;">STR-Based Growth Logic</b><br>
        🟢 STR ≥ 70% &nbsp;→&nbsp; <b>×1.4</b> (bestseller)<br>
        🟡 STR 60–70% → <b>×1.2</b> (strong)<br>
        🟠 STR 50–60% → <b>×1.1</b> (healthy)<br>
        🔵 STR 40–50% → <b>×1.0</b> (hold flat)<br>
        🔴 STR &lt; 40% &nbsp;&nbsp;→&nbsp; <b>×0.9</b> (reduce)<br>
        <span style="color:rgba(255,255,255,0.5);font-size:11px;">Core & basic articles only</span>
    </div>""", unsafe_allow_html=True)
    min_buy_qty = st.number_input("Min Buy Floor (units)", value=5, min_value=0)

    st.divider()
    st.markdown('<p style="font-size:9px;color:rgba(255,255,255,0.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">CAPSULE SIZE</p>', unsafe_allow_html=True)
    capsule_size = st.slider("", 5, 50, 20, label_visibility="collapsed")

    st.divider()
    st.markdown('<p style="font-size:10px;color:rgba(255,255,255,0.3);text-align:center;line-height:1.7;">Benetton India Pvt. Ltd.<br>NIFT Kangra · Graduation Project<br>Medha Yada · Remya VK · 2025–26</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 6. HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;padding:18px 0 12px 0;border-bottom:1px solid rgba(255,255,255,0.12);margin-bottom:28px;">
    <div style="display:flex;align-items:center;gap:18px;">
        <img src="data:image/png;base64,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" style="width:90px;border-radius:8px;" />
        <div>
            <div style="font-size:10px;color:rgba(255,255,255,0.45);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:4px;">KIDSWEAR DIVISION — BUYING INTELLIGENCE</div>
            <div style="font-size:28px;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;">SS27 Pro-Planner Portal</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:3px;">Powered by SS23 · SS24 · SS25 Performance Data</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);border-radius:8px;padding:10px 18px;font-size:12px;color:rgba(255,255,255,0.65);letter-spacing:0.3px;">🔒 Internal Use Only &nbsp;|&nbsp; Benetton India Pvt. Ltd.</div>
</div>""", unsafe_allow_html=True)

# Search bar
search_query = st.text_input("", placeholder="🔍  Search by style name...", label_visibility="collapsed").strip().upper()
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 7. FILTER + AGGREGATE
# ═══════════════════════════════════════════════════════════════
mask = (df["REGION"] == selected_region) & (df["CAT"].isin(selected_cats)) & (df["MRP/ UNIT"] >= price_range[0]) & (df["MRP/ UNIT"] <= price_range[1])
if selected_seasons and "SEASON" in df.columns: mask = mask & df["SEASON"].isin(selected_seasons)
if selected_gender and "GENDER" in df.columns:  mask = mask & df["GENDER"].isin(selected_gender)
if search_query: mask = mask & df["DES"].astype(str).str.upper().str.contains(search_query, na=False)

rdf = df[mask].copy()
if rdf.empty:
    warning_card("No data matches your current filters. Try widening the Price Band or selecting more Categories.")
    st.stop()

grp_cols = ["CAT","DES","ORIGIN","CORE_FLAG","GENDER","PRICE BAND"]
if "FIT_TYPE" in df.columns: grp_cols.append("FIT_TYPE")

matrix = rdf.groupby(grp_cols).agg({"ORDER QUANTITY":"sum","SOLD QTY":"sum","NET RECD":"sum","REALIZED SALE- CR":"sum","MRP/ UNIT":"mean"}).reset_index()
matrix["STR %"] = 0.0
valid = matrix["NET RECD"] > 0
matrix.loc[valid, "STR %"] = (matrix["SOLD QTY"] / matrix["NET RECD"] * 100).clip(upper=100.0).round(1)

def smart_buy(row, min_qty):
    s    = row["STR %"]
    recd = row["NET RECD"]   # units that actually hit the shop floor — the true baseline
    # Growth factor applied to NET RECD (not order qty, not sold qty)
    # e.g. NET RECD=1000, STR=75% → buy 1000 × 1.4 = 1400 units next season
    # 1.4 = 40% MORE than last season's floor stock
    if   s >= 70: f = 1.4   # bestseller — grow aggressively
    elif s >= 60: f = 1.2   # strong — grow 20%
    elif s >= 50: f = 1.1   # healthy — grow 10%
    elif s >= 40: f = 1.0   # mediocre — flat repeat
    else:         f = 0.9   # poor — reduce 10%
    return max(round(recd * f), min_qty)

# Apply smart_buy to ALL articles — STR tiers handle reduction automatically
# CORE_FLAG is kept as a display/filter column but does NOT gate the buy qty
matrix["PROPOSED_BUY"] = matrix.apply(lambda r: smart_buy(r, min_buy_qty), axis=1)
# Show what CORE_FLAG values exist in the data (for transparency)
if "CORE_FLAG" in matrix.columns:
    unique_flags = matrix["CORE_FLAG"].astype(str).str.upper().str.strip().unique().tolist()
    # Mark which are core/basic for display purposes only
    BASIC_CORE_FLAGS = ["CORE","BASIC","Y","YES","C","B","1","TRUE"]
    matrix["IS_CORE"] = matrix["CORE_FLAG"].astype(str).str.upper().str.strip().isin(BASIC_CORE_FLAGS)
dominant = matrix.groupby("DES")["ORDER QUANTITY"].transform("max")
matrix_dedup = matrix[matrix["ORDER QUANTITY"] == dominant].drop_duplicates(subset=["DES","GENDER"])

# ═══════════════════════════════════════════════════════════════
# 8. KPIs
# ═══════════════════════════════════════════════════════════════
st.markdown(f'<div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:14px;">REGION SNAPSHOT — {selected_region}</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Avg Sell-Through %",  f"{matrix['STR %'].mean():.1f}%")
k2.metric("SS25 Total Demand", f"{int(matrix['ORDER QUANTITY'].sum()):,}")
k3.metric("SS27 Rec. Buy (units)", f"{int(matrix['PROPOSED_BUY'].sum()):,}")
k4.metric("Buy Value (Cr)",    f"₹{(matrix['PROPOSED_BUY']*matrix['MRP/ UNIT']).sum()/10_000_000:.2f} Cr")
k5.metric("Avg MRP",           f"₹{matrix['MRP/ UNIT'].mean():.0f}")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
top_sku = matrix.sort_values("ORDER QUANTITY",ascending=False).iloc[0]
top_str = matrix.sort_values("STR %",ascending=False).iloc[0]
risky   = matrix[matrix["STR %"]<30]
insight_card(f"<b>Volume Leader:</b> '{top_sku['DES']}' — highest demand in {selected_region} &nbsp;·&nbsp; <b>Best Sell-Through:</b> '{top_str['DES']}' at {top_str['STR %']:.1f}% STR &nbsp;·&nbsp; <b>At Risk:</b> {len(risky)} style(s) below 30% STR — buy quantities auto-reduced")

# ═══════════════════════════════════════════════════════════════
# 9. MAIN CHARTS
# ═══════════════════════════════════════════════════════════════
st.divider()
section_header("◆", "Performance Overview", f"Top performers and demand mix for {selected_region}")

c1,c2 = st.columns([1.4,0.6], gap="large")
with c1:
    st.markdown("**Top 15 Styles by Demand**")
    st.caption("Colour = STR% — white/green = strong sell-through, red = weak")
    top15 = matrix.sort_values("ORDER QUANTITY",ascending=False).head(15)
    fig1 = px.bar(top15, x="ORDER QUANTITY", y="DES", orientation="h", color="STR %",
        color_continuous_scale=["#CC2929","#E8A020","#FFFFFF"], range_color=[0,100],
        template="plotly_dark", labels={"ORDER QUANTITY":"Order Qty","DES":""})
    # FIX: use title=dict() instead of deprecated titlefont
    fig1.update_layout(
        yaxis={"categoryorder":"total ascending"},
        coloraxis_colorbar=dict(
            title=dict(text="STR%", font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF")
        )
    )
    st.plotly_chart(benetton_fig(fig1), use_container_width=True)

with c2:
    st.markdown("**Stock Origin Mix**")
    st.caption("Proposed SS27 buy distribution by origin channel")
    fig2 = px.pie(matrix, values="PROPOSED_BUY", names="ORIGIN", hole=0.6, template="plotly_dark",
        color_discrete_sequence=["#FFFFFF","#B3DFCA","#66BF94","#2d7a52"])
    fig2.update_traces(textposition="outside", textinfo="percent+label", textfont=dict(color="#FFFFFF",size=12))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(benetton_fig(fig2), use_container_width=True)

d1,d2 = st.columns(2, gap="large")
with d1:
    st.markdown("**STR % Distribution**")
    st.caption("How sell-through is spread across all filtered styles")
    fig3 = px.histogram(matrix, x="STR %", nbins=20, template="plotly_dark", color_discrete_sequence=["rgba(255,255,255,0.55)"])
    fig3.add_vline(x=50, line_dash="dash", line_color="#FFD700", annotation_text="50% benchmark", annotation_font_color="#FFD700")
    st.plotly_chart(benetton_fig(fig3), use_container_width=True)

with d2:
    st.markdown("**Demand by Gender**")
    st.caption("Volume split Boys vs Girls for selected filters")
    if "GENDER" in matrix.columns:
        gdf = matrix.groupby("GENDER")["ORDER QUANTITY"].sum().reset_index()
        fig4 = px.pie(gdf, values="ORDER QUANTITY", names="GENDER", hole=0.6, template="plotly_dark",
            color_discrete_sequence=["#FFFFFF","#66BF94"])
        fig4.update_traces(textposition="outside", textinfo="percent+label", textfont=dict(color="#FFFFFF",size=13))
        fig4.update_layout(showlegend=False)
        st.plotly_chart(benetton_fig(fig4), use_container_width=True)

# YOY
if "SEASON" in rdf.columns and rdf["SEASON"].nunique() > 1:
    st.divider()
    section_header("◆", "Season-on-Season Trend", "Demand and sell-through evolution across SS23 · SS24 · SS25")
    yoy = rdf.groupby("SEASON").agg(Total_Demand=("ORDER QUANTITY","sum"), Avg_STR=("STR %","mean")).reset_index().sort_values("SEASON")
    y1,y2 = st.columns(2,gap="large")
    with y1:
        fig_y1 = px.bar(yoy,x="SEASON",y="Total_Demand",color="SEASON",template="plotly_dark",
            color_discrete_sequence=["#66BF94","#B3DFCA","#FFFFFF"],labels={"Total_Demand":"Total Demand","SEASON":""})
        fig_y1.update_layout(showlegend=False)
        st.plotly_chart(benetton_fig(fig_y1),use_container_width=True)
    with y2:
        fig_y2 = px.line(yoy,x="SEASON",y="Avg_STR",markers=True,template="plotly_dark",
            color_discrete_sequence=["#FFFFFF"],labels={"Avg_STR":"Avg STR %","SEASON":""})
        fig_y2.add_hline(y=50,line_dash="dash",line_color="#FFD700",annotation_text="50% target",annotation_font_color="#FFD700")
        fig_y2.update_traces(line=dict(width=3),marker=dict(size=10))
        st.plotly_chart(benetton_fig(fig_y2),use_container_width=True)

# Category scatter
st.divider()
section_header("◆","Category Intelligence","Which categories deliver both volume and sell-through? Bubble size = no. of styles")
cat_sum = matrix.groupby("CAT").agg(Total_Demand=("ORDER QUANTITY","sum"),Avg_STR=("STR %","mean"),Styles=("DES","nunique")).reset_index()
fig5 = px.scatter(cat_sum,x="Total_Demand",y="Avg_STR",size="Styles",color="CAT",template="plotly_dark",
    color_discrete_sequence=BENETTON_COLORS,labels={"Total_Demand":"Total Order Qty","Avg_STR":"Avg STR %"},hover_data=["Styles"])
fig5.add_hline(y=50,line_dash="dash",line_color="#FFD700",annotation_text="50% STR benchmark",annotation_font_color="#FFD700")
fig5.add_vline(x=cat_sum["Total_Demand"].median(),line_dash="dot",line_color="rgba(255,255,255,0.15)")
st.plotly_chart(benetton_fig(fig5),use_container_width=True)
st.caption("Top-right quadrant = high demand + strong sell-through = PRIORITY categories for SS27 investment")

# ═══════════════════════════════════════════════════════════════
# 10. BUYING PLANS
# ═══════════════════════════════════════════════════════════════
st.divider()
section_header("◆","SS27 Buying Plans","Article · Option · Price level planning powered by SS25 performance data")

tab_article, tab_option, tab_price = st.tabs(["  📝  Article-Wise Plan  ","  🗂️  Option-Wise Plan  ","  💰  Price-Wise Plan  "])

with tab_article:
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    st.caption("Every style ranked by demand · STR% progress bar = sell-through · Proposed Buy uses tiered STR-based growth logic")
    show_cols = ["CAT","DES","GENDER","ORIGIN","CORE_FLAG","PRICE BAND","ORDER QUANTITY","NET RECD","SOLD QTY","STR %","MRP/ UNIT","PROPOSED_BUY","REALIZED SALE- CR"]
    if "FIT_TYPE" in matrix.columns: show_cols.insert(5,"FIT_TYPE")
    final_view = matrix.sort_values(["ORDER QUANTITY","STR %"],ascending=[False,False])[show_cols]
    st.dataframe(final_view,
        column_config={"STR %":st.column_config.ProgressColumn("STR %",format="%.1f%%",min_value=0,max_value=100),"MRP/ UNIT":st.column_config.NumberColumn("MRP",format="₹%d"),"PROPOSED_BUY":st.column_config.NumberColumn("SS27 Rec. Buy ✅",format="%d"),"ORDER QUANTITY":st.column_config.NumberColumn("Past Demand"),"REALIZED SALE- CR":st.column_config.NumberColumn("Revenue (Cr)",format="%.4f")},
        use_container_width=True,hide_index=True,height=480)

with tab_option:
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    if "FIT_TYPE" not in matrix.columns:
        warning_card("FIT_TYPE column not found. Re-run clean_data.py to generate it.")
    else:
        st.caption("How buying depth should be distributed across silhouettes / fit types within a category")
        selected_cat_opt = st.selectbox("Category",sorted(matrix["CAT"].unique()),key="opt_cat")
        cat_fit = matrix[matrix["CAT"]==selected_cat_opt].groupby(["FIT_TYPE","GENDER"]).agg(
            Styles=("DES","nunique"),Total_Demand=("ORDER QUANTITY","sum"),
            Avg_STR=("STR %","mean"),Rec_Buy=("PROPOSED_BUY","sum"),Avg_MRP=("MRP/ UNIT","mean")
        ).reset_index().sort_values("Total_Demand",ascending=False)
        cat_fit["Avg_STR"]=cat_fit["Avg_STR"].round(1)
        cat_fit["Avg_MRP"]=cat_fit["Avg_MRP"].round(0).astype(int)
        def opt_rec(r):
            if r["Avg_STR"]>=70: return "✅ Must Have"
            elif r["Avg_STR"]>=50: return "🟡 Should Have"
            elif r["Avg_STR"]>=30: return "🟠 Consider"
            else: return "❌ Drop / Reduce"
        cat_fit["Recommendation"]=cat_fit.apply(opt_rec,axis=1)
        total_rec=cat_fit["Rec_Buy"].sum()
        cat_fit["% of Buy"]=(cat_fit["Rec_Buy"]/total_rec*100).round(1) if total_rec>0 else 0
        # Bar chart — full width
        fig_opt=px.bar(cat_fit.sort_values("Rec_Buy",ascending=True),x="Rec_Buy",y="FIT_TYPE",
            color="Avg_STR",orientation="h",color_continuous_scale=["#CC2929","#E8A020","#FFFFFF"],
            range_color=[0,100],template="plotly_dark",
            facet_col="GENDER" if cat_fit["GENDER"].nunique()>1 else None,
            labels={"FIT_TYPE":"","Rec_Buy":"Recommended Buy Qty","Avg_STR":"STR %"})
        fig_opt.update_layout(coloraxis_colorbar=dict(
            title=dict(text="STR%", font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF")
        ))
        st.plotly_chart(benetton_fig(fig_opt),use_container_width=True)

        # Pie charts — split Boys vs Girls side by side
        st.markdown("**Buy Split by Fit Type — Boys vs Girls**")
        pie_genders = [g for g in ["BOYS","GIRLS"] if g in cat_fit["GENDER"].values]
        if len(pie_genders) == 2:
            pg1, pg2 = st.columns(2, gap="large")
            pie_cols = [pg1, pg2]
        else:
            pie_cols = [st.container()]
        for idx_g, gender_val in enumerate(pie_genders):
            gfit = cat_fit[cat_fit["GENDER"] == gender_val]
            fig_pie_g = px.pie(gfit, values="Rec_Buy", names="FIT_TYPE", hole=0.45,
                title=f"{'👦 Boys' if gender_val=='BOYS' else '👧 Girls'} — Buy Split",
                template="plotly_dark", color_discrete_sequence=BENETTON_COLORS)
            fig_pie_g.update_traces(textposition="outside", textinfo="percent+label",
                textfont=dict(color="#FFFFFF", size=11))
            fig_pie_g.update_layout(showlegend=False, height=420,
                margin=dict(t=50,b=30,l=60,r=60),
                title_font=dict(color="#FFFFFF", size=14))
            with pie_cols[idx_g]:
                st.plotly_chart(benetton_fig(fig_pie_g), use_container_width=True)
        top_fit=cat_fit.sort_values("Avg_STR",ascending=False).iloc[0]
        insight_card(f"For <b>{selected_cat_opt}</b> in <b>{selected_region}</b> — <b>{top_fit['FIT_TYPE']}</b> is the strongest fit at <b>{top_fit['Avg_STR']:.1f}% avg STR</b>. Total rec. buy across all fits: <b>{int(total_rec):,} units</b>")
        st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)
        st.dataframe(cat_fit.rename(columns={"FIT_TYPE":"Fit / Silhouette","Total_Demand":"Past Demand","Avg_STR":"Avg STR %","Rec_Buy":"SS27 Rec. Buy","Avg_MRP":"Avg MRP (₹)","% of Buy":"% of Total Buy"}),
            column_config={"Avg STR %":st.column_config.ProgressColumn("Avg STR %",format="%.1f%%",min_value=0,max_value=100),"Avg MRP (₹)":st.column_config.NumberColumn("Avg MRP",format="₹%d")},
            use_container_width=True,hide_index=True)
        st.markdown("---")
        st.markdown("**Drill into a specific Fit Type**")
        fit_options=sorted(cat_fit["FIT_TYPE"].unique())
        selected_fit=st.selectbox("Select Fit Type",fit_options,key="fit_drill")
        fit_styles=matrix[(matrix["CAT"]==selected_cat_opt)&(matrix["FIT_TYPE"]==selected_fit)].sort_values("ORDER QUANTITY",ascending=False)[["DES","GENDER","PRICE BAND","STR %","MRP/ UNIT","ORDER QUANTITY","PROPOSED_BUY","CORE_FLAG"]]
        st.caption(f"All styles within **{selected_cat_opt} → {selected_fit}**")
        st.dataframe(fit_styles,column_config={"STR %":st.column_config.ProgressColumn("STR %",format="%.1f%%",min_value=0,max_value=100),"MRP/ UNIT":st.column_config.NumberColumn("MRP",format="₹%d"),"PROPOSED_BUY":st.column_config.NumberColumn("SS27 Rec. Buy ✅")},use_container_width=True,hide_index=True)

with tab_price:
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    st.caption("How many units and styles to buy at each price point — identify where to go deep and where to pull back")
    selected_cat_price=st.selectbox("Category",sorted(matrix["CAT"].unique()),key="price_cat")
    price_plan=matrix[matrix["CAT"]==selected_cat_price].groupby(["PRICE BAND","MRP/ UNIT"]).agg(
        Styles=("DES","nunique"),Total_Demand=("ORDER QUANTITY","sum"),Avg_STR=("STR %","mean"),Proposed_Buy=("PROPOSED_BUY","sum")
    ).reset_index().sort_values("MRP/ UNIT")
    price_plan["Buy Value (Cr)"]=(price_plan["Proposed_Buy"]*price_plan["MRP/ UNIT"]/10_000_000).round(4)
    price_plan["Avg_STR"]=price_plan["Avg_STR"].round(1)
    pc1,pc2=st.columns(2,gap="large")
    with pc1:
        fig_p1=px.bar(price_plan,x="MRP/ UNIT",y="Proposed_Buy",color="Avg_STR",
            color_continuous_scale=["#CC2929","#E8A020","#FFFFFF"],range_color=[0,100],template="plotly_dark",
            labels={"MRP/ UNIT":"MRP (₹)","Proposed_Buy":"Rec. Buy Qty"})
        # FIX: use title=dict() instead of deprecated titlefont
        fig_p1.update_coloraxes(colorbar=dict(
            title=dict(text="STR%", font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF")
        ))
        st.plotly_chart(benetton_fig(fig_p1),use_container_width=True)
    with pc2:
        fig_p2=px.bar(price_plan,x="MRP/ UNIT",y="Styles",color="PRICE BAND",template="plotly_dark",
            color_discrete_sequence=BENETTON_COLORS,labels={"MRP/ UNIT":"MRP (₹)","Styles":"No. of Styles"})
        st.plotly_chart(benetton_fig(fig_p2),use_container_width=True)
    best_price=price_plan.sort_values("Avg_STR",ascending=False).iloc[0]
    insight_card(f"For <b>{selected_cat_price}</b> in <b>{selected_region}</b> — best price point is <b>₹{int(best_price['MRP/ UNIT'])}</b> with <b>{best_price['Avg_STR']:.1f}% avg STR</b> and <b>{int(best_price['Styles'])} styles</b>. Recommend deepening buy here for SS27.")
    st.dataframe(price_plan.rename(columns={"PRICE BAND":"Price Band","MRP/ UNIT":"MRP (₹)","Total_Demand":"Past Demand","Avg_STR":"Avg STR %","Proposed_Buy":"SS27 Rec. Buy"}),
        column_config={"Avg STR %":st.column_config.ProgressColumn("Avg STR %",format="%.1f%%",min_value=0,max_value=100),"MRP (₹)":st.column_config.NumberColumn("MRP",format="₹%d")},
        use_container_width=True,hide_index=True)

# ═══════════════════════════════════════════════════════════════
# 11. CAPSULE PLANS
# ═══════════════════════════════════════════════════════════════
st.divider()
section_header("◆","Curated Capsule Plans","Festive replenishment · Cultural theme capsules with moodboards & design concepts")

cap_tab1,cap_tab2=st.tabs(["  🎉  Festive Capsule (Regional)  ","  🌍  Pan India Cultural Capsule  "])

with cap_tab1:
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    FESTIVE={"NORTH":("Diwali · Holi · Navratri","Bright colours, occasion wear, gifting styles"),"SOUTH":("Onam · Pongal · Ugadi","Traditional-meets-casual, lightweight fabrics, ethnic fusion"),"EAST":("Durga Puja · Bihu","Vibrant prints, festive occasion Dresses, ethnic fusion"),"WEST":("Ganesh Chaturthi · Navratri","Festive casuals, bright and printed styles")}
    fest_name,fest_context=FESTIVE.get(selected_region,("Regional Festive Season","Occasion-led styles"))
    st.markdown(f"""<div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:20px 24px;margin-bottom:20px;">
        <div style="font-size:9px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">{selected_region} FESTIVE CONTEXT</div>
        <div style="font-size:18px;font-weight:700;color:#FFFFFF;margin-bottom:6px;">{fest_name}</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.8);">{fest_context}</div>
        <div style="margin-top:10px;font-size:12px;color:rgba(255,255,255,0.55);">📦 Showing replenishable basics & core styles only — generic pieces that sell more during festive without needing a theme-specific design</div>
    </div>""",unsafe_allow_html=True)

    # Replenishable = STR >= 50% (CORE_FLAG not used as hard gate — STR is the signal)
    replen = matrix_dedup[matrix_dedup["STR %"] >= 50].copy().sort_values("STR %", ascending=False)

    num_festive = st.slider("Replenishment Styles to Show", 5, 30, 15, key="fest_size")
    festive_cap = replen.head(num_festive)

    if not festive_cap.empty:
        st.markdown("**🔄 Replenishment Chart — Styles to Stock Up During Festive**")
        st.caption("Only core/basic articles with STR ≥ 50% — these are the safe bets to replenish during festive peaks")

        # Replenishment uplift — festive gets +20% on top of proposed buy
        festive_cap = festive_cap.copy()
        festive_cap["FESTIVE_REPLEN_QTY"] = (festive_cap["PROPOSED_BUY"] * 1.20).round(0).astype(int)
        festive_cap["UPLIFT_UNITS"] = festive_cap["FESTIVE_REPLEN_QTY"] - festive_cap["PROPOSED_BUY"]

        fig_replen = px.bar(
            festive_cap.sort_values("FESTIVE_REPLEN_QTY", ascending=True),
            x=["PROPOSED_BUY","UPLIFT_UNITS"], y="DES", orientation="h",
            template="plotly_dark", barmode="stack",
            color_discrete_map={"PROPOSED_BUY":"rgba(255,255,255,0.5)","UPLIFT_UNITS":"#FFD700"},
            labels={"DES":"","value":"Units","variable":""}
        )
        fig_replen.update_layout(
            yaxis={"categoryorder":"total ascending"},
            legend=dict(orientation="h", y=1.05,
                title_text="",
                itemsizing="constant"
            )
        )
        newnames = {"PROPOSED_BUY":"Base SS27 Buy","UPLIFT_UNITS":"Festive Uplift (+20%)"}
        fig_replen.for_each_trace(lambda t: t.update(name=newnames.get(t.name, t.name)))
        st.plotly_chart(benetton_fig(fig_replen), use_container_width=True)

        fc1,fc2,fc3,fc4 = st.columns(4)
        fc1.metric("Replen Styles", len(festive_cap))
        fc2.metric("Avg STR %", f"{festive_cap['STR %'].mean():.1f}%")
        fc3.metric("Base Buy", f"{int(festive_cap['PROPOSED_BUY'].sum()):,}")
        fc4.metric("With Festive Uplift", f"{int(festive_cap['FESTIVE_REPLEN_QTY'].sum()):,}")

        show_f=["CAT","DES","GENDER","STR %","MRP/ UNIT","PROPOSED_BUY","FESTIVE_REPLEN_QTY","UPLIFT_UNITS"]
        if "FIT_TYPE" in festive_cap.columns: show_f.insert(4,"FIT_TYPE")
        st.dataframe(festive_cap[[c for c in show_f if c in festive_cap.columns]].sort_values("STR %",ascending=False),
            column_config={
                "STR %":st.column_config.ProgressColumn("STR %",format="%.1f%%",min_value=0,max_value=100),
                "MRP/ UNIT":st.column_config.NumberColumn("MRP",format="₹%d"),
                "PROPOSED_BUY":st.column_config.NumberColumn("Base Buy"),
                "FESTIVE_REPLEN_QTY":st.column_config.NumberColumn("Festive Qty ✅",format="%d"),
                "UPLIFT_UNITS":st.column_config.NumberColumn("+Uplift Units",format="%d"),
            },
            use_container_width=True,hide_index=True)
    else:
        warning_card("No replenishable core/basic styles found with STR ≥ 50% under current filters.")

with cap_tab2:
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)

    EVENTS = {
        "🏎️ F1 Season 2026 — Boys": {
            "tag":"BOYS THEME","gender_target":"BOYS",
            "when":"F1 World Championship 2026 — Full season March–November 2026",
            "direction":"Speed, precision, colour blocking — racing stripes, number graphics, team colours, pit lane energy. The most global sport becomes the most wearable kids aesthetic of 2026.",
            "key_cats":["TEE","WOVEN TOP","KNIT BOTTOM","JACKET"],
            "key_fits":["Regular Tee","Boxy / Oversized","Cargo","Polo"],
            "colours":"Ferrari Red · McLaren Papaya · Mercedes Silver · Red Bull Navy · Race White · Podium Gold",
            "mood":"Fast · Precise · Team energy — pit lane meets playground",
            "why_now":"F1 is the fastest growing sport among Indian youth. Drive to Survive has created a new generation of fans aged 6–14. No kidswear brand in India has owned this space yet.",
            "replen_cats":["TEE","KNIT BOTTOM","WOVEN TOP"],
            "replen_desc":"Solid red tees, navy polos, white basics, orange colour-block tops — the F1 team palette applied to core boys basics. Parents restock these throughout the full race calendar.",
            "moodboard_colours":["#CC1100","#FF6B00","#C0C0C0","#001F5B","#FFFFFF","#FFD700"],
            "moodboard_labels":["Ferrari Red","McLaren Papaya","Mercedes Silver","Red Bull Navy","Race White","Podium Gold"],
            "print_direction":"Vertical racing stripes (bold 3–5cm width) · Chequered flag micro-repeat · Bold number graphics (1, 16, 44, 63) · Colour-block panels mimicking team liveries · Carbon fibre texture on collar/cuff · Tonal speed-line emboss",
            "design_concepts":[
                {"name":"Chequered Flag Tee","cat":"TEE","gender":"Boys","desc":"White base tee with bold chequered flag graphic across chest. Boxy fit, 100% cotton. The race day essential.","colour":"#FFFFFF","accent":"#1a1a1a"},
                {"name":"Racing Stripe Polo","cat":"WOVEN TOP","gender":"Boys","desc":"Pique polo with bold red vertical stripe down front. Clean collar, short sleeve. Ferrari energy without the logo.","colour":"#CC1100","accent":"#FFFFFF"},
                {"name":"Podium Cargo Short","cat":"KNIT BOTTOM","gender":"Boys","desc":"6-pocket cargo short in deep navy, orange tab detail at pocket. Mid-length. McLaren meets playground.","colour":"#001F5B","accent":"#FF6B00"},
                {"name":"Pit Lane Bomber","cat":"JACKET","gender":"Boys","desc":"Zip bomber in silver with colour-block side panels in red. Lightweight. Number patch on sleeve.","colour":"#C0C0C0","accent":"#CC1100"},
                {"name":"Number Graphic Tee","cat":"TEE","gender":"Boys","desc":"Oversized tee with bold race number 1 chest print in gold on navy. 100% cotton jersey.","colour":"#001F5B","accent":"#FFD700"},
            ]
        },
        "⚓ One Piece Live Action S2 — Boys": {
            "tag":"BOYS THEME","gender_target":"BOYS",
            "when":"One Piece Live Action Season 2 — Netflix 2026",
            "direction":"Nautical adventure, anime energy — anchor motifs, ocean colour palette, oversized silhouettes, bold graphic prints. The Grand Line comes to the streets.",
            "key_cats":["TEE","SHIRT","DENIM","KNIT BOTTOM"],
            "key_fits":["Boxy / Oversized","Printed Shirt","Cargo","Regular Tee"],
            "colours":"Ocean Navy · Stark White · Anchor Red · Golden Yellow · Sea Teal · Rope Khaki",
            "mood":"Bold · Adventurous · Free — anime fandom meets nautical street style",
            "why_now":"One Piece S1 was Netflix most-watched globally in 2023. S2 will be bigger. Anime-inspired fashion is the single biggest youth trend of 2025–27 in India.",
            "replen_cats":["TEE","SHIRT","KNIT BOTTOM"],
            "replen_desc":"Solid navy tees, white oversized basics, khaki cargo shorts — the nautical colour palette in replenishable core boys styles. Spike during the Netflix release window.",
            "moodboard_colours":["#001F5B","#FFFFFF","#CC1100","#FFD700","#2E8B6E","#8B7355"],
            "moodboard_labels":["Ocean Navy","Stark White","Anchor Red","Golden Yellow","Sea Teal","Rope Khaki"],
            "print_direction":"Anchor motifs (bold, chest placement) · Nautical rope knot prints · Wave micro-repeat · Jolly Roger skull (graphic, non-violent) · Tonal navy stripe · Map/compass graphic prints",
            "design_concepts":[
                {"name":"Anchor Graphic Tee","cat":"TEE","gender":"Boys","desc":"Bold anchor motif chest print, oversized fit, white base navy print. 100% soft cotton. The One Piece essential.","colour":"#FFFFFF","accent":"#001F5B"},
                {"name":"Jolly Roger Tee","cat":"TEE","gender":"Boys","desc":"Graphic skull-and-crossbones in gold on black. Boxy fit. Anime energy, totally wearable.","colour":"#1a1a1a","accent":"#FFD700"},
                {"name":"Navigator Denim","cat":"DENIM","gender":"Boys","desc":"Straight fit denim, medium wash, anchor embroidery on back pocket. Classic 5-pocket.","colour":"#4A6FA5","accent":"#FFD700"},
                {"name":"Crew Cargo Short","cat":"KNIT BOTTOM","gender":"Boys","desc":"6-pocket cargo in khaki with red drawstring detail. Mid-length. Adventure-ready silhouette.","colour":"#8B7355","accent":"#CC1100"},
                {"name":"Straw Hat Printed Shirt","cat":"SHIRT","gender":"Boys","desc":"Relaxed printed shirt in white with navy nautical map print. Open collar, short sleeve.","colour":"#FFFFFF","accent":"#001F5B"},
            ]
        },
        "🖤 Wednesday Season 2 — Girls": {
            "tag":"GIRLS THEME","gender_target":"GIRLS",
            "when":"Wednesday Season 2 — Netflix 2026 (most-watched English series ever)",
            "direction":"Dark academia gothic casual — monochrome dominance, classic stripes, structural silhouettes, deadpan cool. Black and white as the most stylish palette of the season.",
            "key_cats":["TEE","SWEATSHIRT","DENIM","JACKET"],
            "key_fits":["Regular Tee","Crew Neck","Straight Fit","Front Closed"],
            "colours":"Wednesday Black · Stark White · Charcoal Grey · Deep Burgundy · Forest Green · Silver Chain",
            "mood":"Deadpan · Moody · Effortlessly cool — the anti-trend trend",
            "why_now":"Wednesday S1 created a documented kidswear buying surge globally. S2 will be larger. Dark academic dressing for girls is a proven, growing commercial segment in India.",
            "replen_cats":["TEE","SWEATSHIRT","DENIM"],
            "replen_desc":"Solid black tees, grey crew necks, dark denim, charcoal sweatshirts — the Wednesday palette in replenishable basics. No character print needed. The colour IS the costume.",
            "moodboard_colours":["#1a1a1a","#FFFFFF","#4A4A4A","#6B1A1A","#1A3D2B","#C0C0C0"],
            "moodboard_labels":["Wednesday Black","Stark White","Charcoal","Deep Burgundy","Forest Green","Silver"],
            "print_direction":"Black & white vertical stripes · Gothic crest emboss · Barcode micro-print · Tonal charcoal melange · Subtle crosshatch texture · Silver chain-link print at hem",
            "design_concepts":[
                {"name":"Wednesday Stripe Tee","cat":"TEE","gender":"Girls","desc":"Classic B&W horizontal stripe, fitted tee, round neck. The Wednesday uniform — no character print needed.","colour":"#1a1a1a","accent":"#FFFFFF"},
                {"name":"Dark Academia Sweat","cat":"SWEATSHIRT","gender":"Girls","desc":"Charcoal crew neck with subtle embossed gothic crest at chest. French terry. Moody but school-appropriate.","colour":"#4A4A4A","accent":"#C0C0C0"},
                {"name":"Monochrome Pinafore","cat":"DRESS","gender":"Girls","desc":"Black pinafore dress over white puff-sleeve tee (coord set). Dark academia staple for any school day.","colour":"#1a1a1a","accent":"#FFFFFF"},
                {"name":"Deadpan Straight Jean","cat":"DENIM","gender":"Girls","desc":"Dark wash straight leg jean, clean finish. The gothic-casual bottom that goes with everything black.","colour":"#2B3A52","accent":"#1a1a1a"},
                {"name":"Crest Bomber","cat":"JACKET","gender":"Girls","desc":"Black zip bomber with silver crest embroidery on chest. Structured shoulder. Nevermore Academy energy.","colour":"#1a1a1a","accent":"#C0C0C0"},
            ]
        },
        "😈 Devil Wears Benetton — Unisex": {
            "tag":"UNISEX THEME","gender_target":"BOTH",
            "when":"Devil Wears Prada 2 — Global Release 2026",
            "direction":"High-fashion editorial kidswear — sharp tailoring, monochrome power dressing, bold colour pop. The runway comes to the playground. Benetton's Italian DNA makes this uniquely ownable.",
            "key_cats":["JACKET","WOVEN TOP","DENIM","DRESS"],
            "key_fits":["Front Closed","Shift Dress","Straight Fit","Resort Shirt"],
            "colours":"Editorial Black · Runway White · Cobalt Blue · Power Red · Camel · Gold Detail",
            "mood":"Polished · Confident · Fashion-editor energy — mini runway ready",
            "why_now":"The sequel to the most iconic fashion film ever will dominate global conversations. Benetton's Italian heritage is the only kidswear brand that can own this narrative authentically.",
            "replen_cats":["TEE","DENIM","JACKET"],
            "replen_desc":"Solid black tees, crisp white shirts, classic dark denim — the building blocks of a power outfit. Replenish basics that work as editorial foundations during the film window.",
            "moodboard_colours":["#0A0A0A","#F5F5F0","#1B3A8C","#CC1100","#C19A6B","#8B6914"],
            "moodboard_labels":["Editorial Black","Runway White","Cobalt Blue","Power Red","Camel","Gold Detail"],
            "print_direction":"Clean solid editorials (no print) · Cobalt colour-block · Pinstripe suiting fabric · Gold button hardware · Tonal texture panels · Italian woven structured fabric",
            "design_concepts":[
                {"name":"Power Blazer — Girls","cat":"JACKET","gender":"Girls","desc":"Fitted mini blazer in jet black with gold button detail. Fully lined. The statement piece of the season.","colour":"#0A0A0A","accent":"#8B6914"},
                {"name":"Editor Shirt — Boys","cat":"WOVEN TOP","gender":"Boys","desc":"Crisp white poplin shirt with black contrast collar band. Slim fit. Effortlessly editorial.","colour":"#F5F5F0","accent":"#0A0A0A"},
                {"name":"Runway Shift Dress","cat":"DRESS","gender":"Girls","desc":"Cobalt blue shift dress, structured fabric, knee length. The colour-pop hero of the collection.","colour":"#1B3A8C","accent":"#F5F5F0"},
                {"name":"Dark Wash Straight Jean","cat":"DENIM","gender":"Unisex","desc":"Dark wash straight jean, clean finish, minimal branding. The editorial base layer for any look.","colour":"#2B3A52","accent":"#0A0A0A"},
                {"name":"Camel Coord Set","cat":"JACKET","gender":"Girls","desc":"Camel tone blazer + straight trouser coord. Italian tailoring for tiny fashionistas.","colour":"#C19A6B","accent":"#0A0A0A"},
            ]
        },
        "❄️ Frozen 3 — Girls": {
            "tag":"GIRLS THEME","gender_target":"GIRLS",
            "when":"Frozen 3 — Disney Theatrical Release 2026",
            "direction":"Icy magic, pastel winter wonder, snow-dusted romance — ice blues, lavenders, frost whites. Feminine silhouettes with magical texture. Elsa energy without the costume.",
            "key_cats":["DRESS","TEE","KNIT BOTTOM","SWEATSHIRT"],
            "key_fits":["Tiered / Flared Dress","Smocked Dress","Regular Tee","Crew Neck"],
            "colours":"Ice Blue · Lavender Frost · Snow White · Powder Pink · Crystal · Midnight Winter",
            "mood":"Magical · Dreamy · Icy wonder — let it go, let it glow",
            "why_now":"Frozen is Disney highest-grossing animated franchise ever. Frozen 3 will be the biggest kids film of 2026. Every girl aged 3-12 is the target. Parents will seek inspired not licensed pieces.",
            "replen_cats":["DRESS","TEE","KNIT BOTTOM"],
            "replen_desc":"Ice blue dresses, white tiered skirts, lavender tops, snow-white basics — the Frozen colour palette applied to core girls basics. These replenish strongly in the 4 weeks around theatrical release.",
            "moodboard_colours":["#A8D8EA","#C9B8D8","#F0F8FF","#F4C2C2","#E8F4F8","#1B3A6B"],
            "moodboard_labels":["Ice Blue","Lavender Frost","Snow White","Powder Pink","Crystal","Midnight Winter"],
            "print_direction":"Snowflake jacquard texture · Ice crystal micro-print · Shimmer thread knit · Tonal frost ombré · Embossed snowflake at hem · Iridescent fabric finish (no character print needed)",
            "design_concepts":[
                {"name":"Ice Kingdom Dress","cat":"DRESS","gender":"Girls","desc":"A-line dress in ice blue with snowflake jacquard texture at hem. No character print — pure magical aesthetic. Fully lined.","colour":"#A8D8EA","accent":"#FFFFFF"},
                {"name":"Frost Tiered Skirt","cat":"KNIT BOTTOM","gender":"Girls","desc":"3-tier mini skirt in snow white ribbed knit with shimmer thread. Elastic waist. Magical without being costume-y.","colour":"#F0F8FF","accent":"#A8D8EA"},
                {"name":"Lavender Magic Tee","cat":"TEE","gender":"Girls","desc":"Soft lavender cotton tee with embossed snowflake at chest. Fitted, round neck. The everyday Frozen essential.","colour":"#C9B8D8","accent":"#FFFFFF"},
                {"name":"Crystal Sweat Dress","cat":"DRESS","gender":"Girls","desc":"Powder pink sweat-fabric dress with tonal snowflake emboss. Relaxed fit, midi length. Cosy magic.","colour":"#F4C2C2","accent":"#C9B8D8"},
                {"name":"Winter Wonderland Coord","cat":"SWEATSHIRT","gender":"Girls","desc":"Ice blue crew neck + matching jogger set with shimmer thread detail. The holiday coord girls will live in.","colour":"#A8D8EA","accent":"#1B3A6B"},
            ]
        },
    }

    selected_event = st.selectbox("Select Cultural Theme", list(EVENTS.keys()))
    ev = EVENTS[selected_event]
    event_card(ev["tag"], ev["when"], ev["direction"], ev["colours"], ev["mood"], ev["why_now"], ev["key_cats"], ev["key_fits"])

    # ══════════════════════════════════════════════
    # WGSN MOODBOARD — colour swatches + print direction
    # ══════════════════════════════════════════════
    st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
    st.markdown("""<div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:12px;">🎨 WGSN MOODBOARD</div>""", unsafe_allow_html=True)

    mb_cols = ev["moodboard_colours"]
    mb_labs = ev["moodboard_labels"]
    swatch_html = "<div style='display:flex;gap:14px;flex-wrap:wrap;margin:0 0 16px 0;'>"
    for col, lab in zip(mb_cols, mb_labs):
        r_v = int(col[1:3],16); g_v = int(col[3:5],16); b_v = int(col[5:7],16)
        lum = (0.299*r_v + 0.587*g_v + 0.114*b_v)/255
        border_c = "rgba(255,255,255,0.25)" if lum < 0.5 else "rgba(0,0,0,0.2)"
        swatch_html += f"""<div style="text-align:center;">
            <div style="width:88px;height:88px;background:{col};border-radius:14px;border:2px solid {border_c};margin-bottom:8px;box-shadow:0 4px 12px rgba(0,0,0,0.3);"></div>
            <div style="font-size:11px;color:#FFFFFF;font-weight:600;margin-bottom:2px;">{lab}</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.4);font-family:monospace;">{col.upper()}</div>
        </div>"""
    swatch_html += "</div>"
    st.markdown(swatch_html, unsafe_allow_html=True)

    st.markdown(f"""<div style="background:rgba(255,255,255,0.06);border-left:3px solid #FFD700;border-radius:0 10px 10px 0;padding:14px 20px;margin:0 0 28px 0;font-size:13px;color:rgba(255,255,255,0.88);line-height:1.8;">
        <b style="color:#FFD700;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;">Print & Texture Direction</b><br><br>{ev["print_direction"]}
    </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # CAPSULE DESIGN CONCEPTS
    # ══════════════════════════════════════════════
    st.markdown("""<div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:12px;">👗 CAPSULE DESIGN CONCEPTS</div>""", unsafe_allow_html=True)
    st.caption("New style concepts for this theme — brief these to the design team. Not existing stock.")

    designs = ev["design_concepts"]
    d_cols = st.columns(len(designs), gap="small")
    for i, d in enumerate(designs):
        with d_cols[i]:
            r_v = int(d["colour"][1:3],16); g_v = int(d["colour"][3:5],16); b_v2 = int(d["colour"][5:7],16)
            lum2 = (0.299*r_v + 0.587*g_v + 0.114*b_v2)/255
            # Draw a simple garment silhouette using HTML/CSS
            shape = "border-radius:4px 4px 0 0;" if d["cat"] in ["TEE","WOVEN TOP","SWEATSHIRT","SHIRT"] else (
                    "border-radius:50% 50% 4px 4px;" if d["cat"] == "DRESS" else "border-radius:4px;")
            st.markdown(f"""<div style="background:rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:16px 12px 14px;text-align:center;">
                <div style="width:64px;height:76px;background:{d["colour"]};{shape}margin:0 auto 12px;border:2px solid {d["accent"]};position:relative;display:flex;align-items:center;justify-content:center;">
                    <div style="width:28px;height:3px;background:{d["accent"]};border-radius:2px;opacity:0.8;"></div>
                </div>
                <div style="font-size:11px;font-weight:700;color:#FFFFFF;margin-bottom:4px;line-height:1.3;">{d["name"]}</div>
                <div style="font-size:9px;color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{d["cat"]} · {d["gender"]}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.78);line-height:1.55;text-align:left;">{d["desc"]}</div>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # REPLENISHMENT CHART
    # ══════════════════════════════════════════════
    st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
    st.markdown("""<div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px;">🔄 REPLENISHMENT PLAN</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:14px 18px;margin-bottom:16px;font-size:13px;color:rgba(255,255,255,0.85);line-height:1.7;">
        {ev["replen_desc"]}
    </div>""", unsafe_allow_html=True)
    st.caption("Basic replenishable stock only — core/basic CORE_FLAG, STR ≥ 50%, theme-relevant categories. White bar = base SS27 buy. Gold bar = extra units to stock for the theme release window (+20% uplift).")

    replen_cats = [c.upper() for c in ev.get("replen_cats",[])]
    gender_target = ev.get("gender_target","BOTH")

    all_mask2 = df["CAT"].isin(selected_cats) & (df["MRP/ UNIT"] >= price_range[0]) & (df["MRP/ UNIT"] <= price_range[1])
    if selected_seasons and "SEASON" in df.columns: all_mask2 = all_mask2 & df["SEASON"].isin(selected_seasons)
    all_rdf2 = df[all_mask2].copy()

    pan_matrix = all_rdf2.groupby(["CAT","DES","GENDER"]).agg(
        Regions_Present=("REGION","nunique"),
        Avg_STR=("STR %","mean"),
        Net_Recd=("NET RECD","sum"),
        Total_Demand=("ORDER QUANTITY","sum"),
        Avg_MRP=("MRP/ UNIT","mean")
    ).reset_index()
    if "FIT_TYPE" in all_rdf2.columns:
        fit_map2 = all_rdf2.groupby(["CAT","DES"])["FIT_TYPE"].first().reset_index()
        pan_matrix = pan_matrix.merge(fit_map2, on=["CAT","DES"], how="left")
    if "CORE_FLAG" in all_rdf2.columns:
        cf_map = all_rdf2.groupby(["CAT","DES"])["CORE_FLAG"].first().reset_index()
        pan_matrix = pan_matrix.merge(cf_map, on=["CAT","DES"], how="left")

    # Replenishment filter: STR >= 50% + theme categories + gender
    # CORE_FLAG NOT used as hard gate — STR is the quality signal
    replen_mask = pan_matrix["Avg_STR"] >= 50
    if replen_cats:
        replen_mask = replen_mask & pan_matrix["CAT"].isin(replen_cats)
    if gender_target != "BOTH" and "GENDER" in pan_matrix.columns:
        replen_mask = replen_mask & (pan_matrix["GENDER"].str.upper() == gender_target)

    replen_df = pan_matrix[replen_mask].copy()

    # BASE BUY = NET RECD × growth factor (same logic as smart_buy)
    def growth_f(s):
        if s >= 70: return 1.4
        elif s >= 60: return 1.2
        elif s >= 50: return 1.1
        elif s >= 40: return 1.0
        else: return 0.9

    replen_df["Base_Buy"] = (replen_df["Net_Recd"] * replen_df["Avg_STR"].apply(growth_f)).round(0).astype(int)
    replen_df["Theme_Uplift_Qty"] = (replen_df["Base_Buy"] * 0.20).round(0).astype(int)
    replen_df["Total_Replen"] = replen_df["Base_Buy"] + replen_df["Theme_Uplift_Qty"]
    replen_df = replen_df[replen_df["Base_Buy"] > 0].sort_values("Avg_STR", ascending=False).head(20)

    if not replen_df.empty:
        fig_replen2 = px.bar(
            replen_df.sort_values("Total_Replen", ascending=True),
            x=["Base_Buy","Theme_Uplift_Qty"], y="DES", orientation="h",
            template="plotly_dark", barmode="stack",
            color_discrete_map={"Base_Buy":"rgba(255,255,255,0.5)","Theme_Uplift_Qty":"#FFD700"},
            labels={"DES":"","value":"Units","variable":""}
        )
        fig_replen2.update_layout(
            yaxis={"categoryorder":"total ascending"},
            legend=dict(orientation="h",y=1.02,title_text=""),
            height=max(350, len(replen_df) * 28)
        )
        newnames2 = {"Base_Buy":"Base SS27 Buy (NET RECD × growth)","Theme_Uplift_Qty":"Theme Window Uplift (+20%)"}
        fig_replen2.for_each_trace(lambda t: t.update(name=newnames2.get(t.name,t.name)))
        st.plotly_chart(benetton_fig(fig_replen2), use_container_width=True)

        rp1,rp2,rp3,rp4 = st.columns(4)
        rp1.metric("Replen Styles", len(replen_df))
        rp2.metric("Avg STR %", f"{replen_df['Avg_STR'].mean():.1f}%")
        rp3.metric("Base Buy Total", f"{int(replen_df['Base_Buy'].sum()):,}")
        rp4.metric("With Theme Uplift", f"{int(replen_df['Total_Replen'].sum()):,}")

        show_r = ["CAT","DES","GENDER","Avg_STR","Avg_MRP","Net_Recd","Base_Buy","Theme_Uplift_Qty","Total_Replen"]
        if "FIT_TYPE" in replen_df.columns: show_r.insert(4,"FIT_TYPE")
        st.dataframe(
            replen_df[[c for c in show_r if c in replen_df.columns]].rename(columns={
                "Avg_STR":"Avg STR %","Avg_MRP":"Avg MRP (₹)",
                "Net_Recd":"Net Recd (Past)","Base_Buy":"Base Buy",
                "Theme_Uplift_Qty":"+Theme Units","Total_Replen":"Total Replen ✅","FIT_TYPE":"Fit"
            }),
            column_config={
                "Avg STR %":st.column_config.ProgressColumn("Avg STR %",format="%.1f%%",min_value=0,max_value=100),
                "Avg MRP (₹)":st.column_config.NumberColumn("MRP",format="₹%d"),
                "Net Recd (Past)":st.column_config.NumberColumn("Net Recd",format="%d"),
                "Total Replen ✅":st.column_config.NumberColumn("Total Replen ✅",format="%d"),
            },
            use_container_width=True, hide_index=True
        )
    else:
        warning_card("No replenishable core/basic styles found for this theme's categories. Try selecting more categories in the sidebar or check CORE_FLAG values in your data.")


# ═══════════════════════════════════════════════════════════════
# 12. EXPORT
# ═══════════════════════════════════════════════════════════════
st.divider()
buffer=io.BytesIO()
with pd.ExcelWriter(buffer,engine="openpyxl") as writer:
    final_view.to_excel(writer,index=False,sheet_name="Article_Plan")
    if "FIT_TYPE" in matrix.columns:
        matrix.groupby(["CAT","FIT_TYPE","GENDER"]).agg(Styles=("DES","nunique"),Total_Demand=("ORDER QUANTITY","sum"),Avg_STR=("STR %","mean"),Rec_Buy=("PROPOSED_BUY","sum")).reset_index().to_excel(writer,index=False,sheet_name="Option_Plan")
    matrix.groupby(["CAT","PRICE BAND","MRP/ UNIT"]).agg(Styles=("DES","nunique"),Total_Demand=("ORDER QUANTITY","sum"),Avg_STR=("STR %","mean"),Proposed_Buy=("PROPOSED_BUY","sum")).reset_index().to_excel(writer,index=False,sheet_name="Price_Plan")

st.sidebar.divider()
st.sidebar.download_button("📥  Export Full Buying Plan",buffer.getvalue(),f"SS27_BuyPlan_{selected_region}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.markdown('<p style="font-size:10px;color:rgba(255,255,255,0.3);text-align:center;margin-top:4px;">3 sheets: Article · Option · Price</p>',unsafe_allow_html=True)