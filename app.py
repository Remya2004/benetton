import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io

st.set_page_config(
    page_title="Benetton Kidswear — SS27 Pro-Planner",
    page_icon="🟢", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #e6edf3; }
[data-testid="stMetricValue"] { font-size: 28px !important; color: #00CC96 !important; font-weight: 700 !important; }
[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
h1,h2,h3 { color: #f0f6fc !important; font-weight: 600 !important; }
.insight-box { background:#1c2128; border-left:4px solid #00CC96; padding:12px 16px; border-radius:6px; margin:8px 0; font-size:14px; }
</style>
""", unsafe_allow_html=True)

# ── LOAD ─────────────────────────────────
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
    st.error("🚨 data_cleaned.csv not found. Run clean_data.py first!")
    st.stop()

# ── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.title("🟢 SS27 Planning Controls")
    st.caption("Based on SS23 + SS24 + SS25 Data")
    st.divider()

    season_list = sorted(df["SEASON"].dropna().unique()) if "SEASON" in df.columns else []
    selected_seasons = st.multiselect("📅 Season(s)", season_list, default=season_list)

    region_list = sorted(df["REGION"].dropna().unique())
    selected_region = st.selectbox("📍 Target Region", region_list)

    gender_list = sorted(df["GENDER"].dropna().unique()) if "GENDER" in df.columns else []
    selected_gender = st.multiselect("👦👧 Gender", gender_list, default=gender_list)

    cat_list = sorted(df["CAT"].dropna().unique())
    selected_cats = st.multiselect("👕 Categories", cat_list, default=cat_list)

    st.divider()
    m_min = int(df["MRP/ UNIT"].min()) if "MRP/ UNIT" in df.columns else 0
    m_max = int(df["MRP/ UNIT"].max()) if "MRP/ UNIT" in df.columns else 5000
    price_range = st.slider("💰 Price Band (MRP ₹)", m_min, m_max, (m_min, m_max))

    st.divider()
    st.subheader("🛒 Buying Logic")
    buffer_growth = st.slider("Base Growth Factor", 1.0, 2.5, 1.2, 0.1,
        help="STR≥80% → factor+0.3 | STR 50-80% → factor | STR 30-50% → 1.0 | STR<30% → 0.7")
    min_buy_qty = st.number_input("Min Buy Floor (units)", value=5, min_value=0)

    st.divider()
    st.subheader("🧩 Capsule Strategy")
    capsule_size = st.slider("Total Styles in Capsule", 5, 50, 20)

# ── FILTER ───────────────────────────────
search_query = st.text_input("🔍 Search Styles...", "").strip().upper()

mask = (
    (df["REGION"] == selected_region) &
    (df["CAT"].isin(selected_cats)) &
    (df["MRP/ UNIT"] >= price_range[0]) &
    (df["MRP/ UNIT"] <= price_range[1])
)
if selected_seasons and "SEASON" in df.columns:
    mask = mask & df["SEASON"].isin(selected_seasons)
if selected_gender and "GENDER" in df.columns:
    mask = mask & df["GENDER"].isin(selected_gender)
if search_query:
    mask = mask & df["DES"].astype(str).str.upper().str.contains(search_query, na=False)

rdf = df[mask].copy()
if rdf.empty:
    st.warning("⚠️ No data matches filters.")
    st.stop()

# ── AGGREGATE ────────────────────────────
grp_cols = ["CAT","DES","ORIGIN","CORE_FLAG","GENDER","PRICE BAND"]
if "FIT_TYPE" in df.columns:
    grp_cols.append("FIT_TYPE")

matrix = rdf.groupby(grp_cols).agg({
    "ORDER QUANTITY":    "sum",
    "SOLD QTY":          "sum",
    "NET RECD":          "sum",
    "REALIZED SALE- CR": "sum",
    "MRP/ UNIT":         "mean",
}).reset_index()

matrix["STR %"] = 0.0
valid = matrix["NET RECD"] > 0
matrix.loc[valid, "STR %"] = (
    matrix["SOLD QTY"] / matrix["NET RECD"] * 100
).clip(upper=100.0).round(1)

# ── SMART BUY ────────────────────────────
def smart_buy(row, growth, min_qty):
    s = row["STR %"]
    q = row["ORDER QUANTITY"]
    if s >= 80:   f = growth + 0.3
    elif s >= 50: f = growth
    elif s >= 30: f = 1.0
    else:         f = 0.7
    return max(round(q * f), min_qty)

matrix["PROPOSED_BUY"] = matrix.apply(
    lambda r: smart_buy(r, buffer_growth, min_buy_qty), axis=1
)

dominant = matrix.groupby("DES")["ORDER QUANTITY"].transform("max")
matrix_dedup = matrix[matrix["ORDER QUANTITY"] == dominant].drop_duplicates(
    subset=["DES","GENDER"])

# ── KPIs ─────────────────────────────────
st.title(f"🟢 {selected_region} — SS27 Buying Plan")
st.caption("Powered by SS23+SS24+SS25 Data | United Colors of Benetton Kidswear")

k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Avg STR %",      f"{matrix['STR %'].mean():.1f}%")
k2.metric("Total Demand",   f"{int(matrix['ORDER QUANTITY'].sum()):,}")
k3.metric("Rec. Buy Units", f"{int(matrix['PROPOSED_BUY'].sum()):,}")
k4.metric("Buy Value (Cr)", f"₹{(matrix['PROPOSED_BUY']*matrix['MRP/ UNIT']).sum()/10_000_000:.2f}")
k5.metric("Avg MRP",        f"₹{matrix['MRP/ UNIT'].mean():.0f}")

top_sku  = matrix.sort_values("ORDER QUANTITY", ascending=False).iloc[0]
top_str  = matrix.sort_values("STR %", ascending=False).iloc[0]
risky    = matrix[matrix["STR %"] < 30]
st.markdown(f"""
<div class="insight-box">
📦 <b>Volume Leader:</b> '{top_sku['DES']}' — highest demand in {selected_region} &nbsp;|&nbsp;
🔥 <b>Best Seller:</b> '{top_str['DES']}' — {top_str['STR %']:.1f}% STR &nbsp;|&nbsp;
⚠️ <b>At Risk:</b> {len(risky)} style(s) below 30% STR — buy auto-reduced
</div>""", unsafe_allow_html=True)

# ── MAIN CHARTS ──────────────────────────
c1,c2 = st.columns([1.3,0.7], gap="large")
with c1:
    st.subheader("🔥 Top 15 Styles by Demand")
    top15 = matrix.sort_values("ORDER QUANTITY", ascending=False).head(15)
    fig1 = px.bar(top15, x="ORDER QUANTITY", y="DES", orientation="h",
                  color="STR %", color_continuous_scale="RdYlGn",
                  range_color=[0,100], template="plotly_dark",
                  labels={"ORDER QUANTITY":"Order Qty","DES":"Style"})
    fig1.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("📦 Stock Origin Mix")
    fig2 = px.pie(matrix, values="PROPOSED_BUY", names="ORIGIN",
                  hole=0.5, template="plotly_dark",
                  color_discrete_sequence=["#00CC96","#636EFA","#EF553B"])
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

d1,d2 = st.columns(2, gap="large")
with d1:
    st.subheader("📊 STR % Distribution")
    fig3 = px.histogram(matrix, x="STR %", nbins=20,
                        template="plotly_dark", color_discrete_sequence=["#00CC96"])
    fig3.add_vline(x=50, line_dash="dash", line_color="yellow", annotation_text="50% benchmark")
    st.plotly_chart(fig3, use_container_width=True)

with d2:
    st.subheader("👦👧 Demand by Gender")
    if "GENDER" in matrix.columns:
        gdf = matrix.groupby("GENDER")["ORDER QUANTITY"].sum().reset_index()
        fig4 = px.pie(gdf, values="ORDER QUANTITY", names="GENDER",
                      hole=0.5, template="plotly_dark",
                      color_discrete_sequence=["#636EFA","#EF553B"])
        st.plotly_chart(fig4, use_container_width=True)

# ── YOY TREND ────────────────────────────
if "SEASON" in rdf.columns and rdf["SEASON"].nunique() > 1:
    st.divider()
    st.subheader("📅 Season-on-Season Trend")
    yoy = rdf.groupby("SEASON").agg(
        Total_Demand=("ORDER QUANTITY","sum"),
        Avg_STR=("STR %","mean")
    ).reset_index().sort_values("SEASON")
    y1,y2 = st.columns(2)
    with y1:
        fig_y1 = px.bar(yoy, x="SEASON", y="Total_Demand", color="SEASON",
                        template="plotly_dark", title="Total Demand by Season",
                        color_discrete_sequence=["#636EFA","#00CC96","#EF553B"])
        st.plotly_chart(fig_y1, use_container_width=True)
    with y2:
        fig_y2 = px.line(yoy, x="SEASON", y="Avg_STR", markers=True,
                         template="plotly_dark", title="Avg STR % Trend",
                         color_discrete_sequence=["#00CC96"])
        fig_y2.add_hline(y=50, line_dash="dash", line_color="yellow")
        st.plotly_chart(fig_y2, use_container_width=True)

# ── CATEGORY SCATTER ─────────────────────
st.divider()
st.subheader("📈 Category — STR % vs Demand")
cat_sum = matrix.groupby("CAT").agg(
    Total_Demand=("ORDER QUANTITY","sum"),
    Avg_STR=("STR %","mean"),
    Styles=("DES","nunique")
).reset_index()
fig5 = px.scatter(cat_sum, x="Total_Demand", y="Avg_STR",
                  size="Styles", color="CAT", template="plotly_dark",
                  labels={"Total_Demand":"Total Order Qty","Avg_STR":"Avg STR %"},
                  hover_data=["Styles"])
fig5.add_hline(y=50, line_dash="dash", line_color="yellow", annotation_text="50% benchmark")
st.plotly_chart(fig5, use_container_width=True)
st.caption("Top-right = high demand + high STR = priority categories for SS27.")

# ═══════════════════════════════════════════
# BUYING PLANS — 3 TABS
# ═══════════════════════════════════════════
st.divider()
st.subheader("📋 SS27 Buying Plans")

tab_article, tab_option, tab_price = st.tabs([
    "📝 Article-Wise Plan",
    "🗂️ Option-Wise Plan (by Fit/Silhouette)",
    "💰 Price-Wise Plan"
])

# ── TAB 1: ARTICLE-WISE ──────────────────
with tab_article:
    st.caption("Every individual style ranked by demand with SS27 recommended buy quantity")

    show_cols = ["CAT","DES","GENDER","ORIGIN","CORE_FLAG","PRICE BAND",
                 "ORDER QUANTITY","NET RECD","SOLD QTY",
                 "STR %","MRP/ UNIT","PROPOSED_BUY","REALIZED SALE- CR"]
    if "FIT_TYPE" in matrix.columns:
        show_cols.insert(5, "FIT_TYPE")

    final_view = matrix.sort_values(
        ["ORDER QUANTITY","STR %"], ascending=[False,False]
    )[show_cols]

    st.dataframe(final_view,
        column_config={
            "STR %":           st.column_config.ProgressColumn("STR %", format="%.1f%%", min_value=0, max_value=100),
            "MRP/ UNIT":       st.column_config.NumberColumn("MRP", format="₹%d"),
            "PROPOSED_BUY":    st.column_config.NumberColumn("SS27 Rec. Buy ✅", format="%d"),
            "ORDER QUANTITY":  st.column_config.NumberColumn("Past Demand"),
            "REALIZED SALE- CR": st.column_config.NumberColumn("Revenue (Cr)", format="%.4f"),
        },
        use_container_width=True, hide_index=True)

# ── TAB 2: OPTION-WISE (FIT TYPE) ────────
with tab_option:
    st.caption("""
    Option planning = how many silhouettes/fits to carry per category.
    Example: In Denim, buy 5 Slim Fit + 4 Straight Fit + 2 Cargo.
    """)

    if "FIT_TYPE" not in matrix.columns:
        st.warning("FIT_TYPE column not found. Re-run clean_data.py to generate it.")
    else:
        # Select category
        selected_cat_opt = st.selectbox(
            "Select Category for Option Plan",
            sorted(matrix["CAT"].unique()), key="opt_cat"
        )

        cat_fit = matrix[matrix["CAT"] == selected_cat_opt].groupby(
            ["FIT_TYPE","GENDER"]
        ).agg(
            Styles=("DES","nunique"),
            Total_Demand=("ORDER QUANTITY","sum"),
            Avg_STR=("STR %","mean"),
            Rec_Buy=("PROPOSED_BUY","sum"),
            Avg_MRP=("MRP/ UNIT","mean"),
        ).reset_index().sort_values("Total_Demand", ascending=False)

        cat_fit["Avg_STR"] = cat_fit["Avg_STR"].round(1)
        cat_fit["Avg_MRP"] = cat_fit["Avg_MRP"].round(0).astype(int)

        # Recommendation
        def opt_rec(row):
            if row["Avg_STR"] >= 70:   return "✅ Must Have"
            elif row["Avg_STR"] >= 50: return "🟡 Should Have"
            elif row["Avg_STR"] >= 30: return "🟠 Consider"
            else:                      return "❌ Drop / Reduce"
        cat_fit["Recommendation"] = cat_fit.apply(opt_rec, axis=1)

        # Share of total buy per fit
        total_rec = cat_fit["Rec_Buy"].sum()
        cat_fit["% of Buy"] = (cat_fit["Rec_Buy"] / total_rec * 100).round(1) if total_rec > 0 else 0

        # Charts
        oc1, oc2 = st.columns([1.5, 0.5])
        with oc1:
            fig_opt = px.bar(
                cat_fit.sort_values("Rec_Buy", ascending=True),
                x="Rec_Buy", y="FIT_TYPE", color="Avg_STR",
                orientation="h", color_continuous_scale="RdYlGn",
                range_color=[0,100], template="plotly_dark",
                facet_col="GENDER" if cat_fit["GENDER"].nunique() > 1 else None,
                title=f"{selected_cat_opt} — Recommended Buy by Fit Type",
                labels={"FIT_TYPE":"Fit / Silhouette","Rec_Buy":"Rec. Buy Qty","Avg_STR":"STR %"}
            )
            st.plotly_chart(fig_opt, use_container_width=True)

        with oc2:
            fig_pie_opt = px.pie(
                cat_fit, values="Rec_Buy", names="FIT_TYPE",
                hole=0.5, template="plotly_dark",
                title="Buy % by Fit",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_pie_opt.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie_opt, use_container_width=True)

        # Summary insight
        top_fit = cat_fit.sort_values("Avg_STR", ascending=False).iloc[0]
        st.markdown(f"""
        <div class="insight-box">
        💡 For <b>{selected_cat_opt}</b> in <b>{selected_region}</b> —
        <b>{top_fit['FIT_TYPE']}</b> is the strongest fit with <b>{top_fit['Avg_STR']:.1f}% avg STR</b>.
        Recommend deepening this option for SS27.
        &nbsp;|&nbsp;
        Total recommended buy across all fits: <b>{int(total_rec):,} units</b>
        </div>""", unsafe_allow_html=True)

        # Table
        st.dataframe(
            cat_fit.rename(columns={
                "FIT_TYPE":    "Fit / Silhouette",
                "Styles":      "No. of Styles",
                "Total_Demand":"Past Demand",
                "Avg_STR":     "Avg STR %",
                "Rec_Buy":     "SS27 Rec. Buy",
                "Avg_MRP":     "Avg MRP (₹)",
                "% of Buy":    "% of Total Buy"
            }),
            column_config={
                "Avg STR %": st.column_config.ProgressColumn(
                    "Avg STR %", format="%.1f%%", min_value=0, max_value=100),
                "Avg MRP (₹)": st.column_config.NumberColumn("Avg MRP", format="₹%d"),
                "% of Total Buy": st.column_config.NumberColumn("% of Buy", format="%.1f%%"),
            },
            use_container_width=True, hide_index=True
        )

        # Drill into styles within a fit type
        st.markdown("---")
        st.markdown("**🔍 Drill into a specific Fit Type**")
        fit_options = sorted(cat_fit["FIT_TYPE"].unique())
        selected_fit = st.selectbox("Select Fit Type", fit_options, key="fit_drill")

        fit_styles = matrix[
            (matrix["CAT"] == selected_cat_opt) &
            (matrix["FIT_TYPE"] == selected_fit)
        ].sort_values("ORDER QUANTITY", ascending=False)[[
            "DES","GENDER","PRICE BAND","STR %","MRP/ UNIT",
            "ORDER QUANTITY","PROPOSED_BUY","CORE_FLAG"
        ]]

        st.caption(f"All styles within {selected_cat_opt} → {selected_fit}")
        st.dataframe(fit_styles,
            column_config={
                "STR %": st.column_config.ProgressColumn("STR %", format="%.1f%%", min_value=0, max_value=100),
                "MRP/ UNIT": st.column_config.NumberColumn("MRP", format="₹%d"),
                "PROPOSED_BUY": st.column_config.NumberColumn("SS27 Rec. Buy ✅"),
            },
            use_container_width=True, hide_index=True
        )

# ── TAB 3: PRICE-WISE ────────────────────
with tab_price:
    st.caption("How many units and styles to buy at each price point per category")

    selected_cat_price = st.selectbox(
        "Select Category for Price Plan",
        sorted(matrix["CAT"].unique()), key="price_cat"
    )

    price_plan = matrix[matrix["CAT"] == selected_cat_price].groupby(
        ["PRICE BAND","MRP/ UNIT"]
    ).agg(
        Styles=("DES","nunique"),
        Total_Demand=("ORDER QUANTITY","sum"),
        Avg_STR=("STR %","mean"),
        Proposed_Buy=("PROPOSED_BUY","sum"),
    ).reset_index().sort_values("MRP/ UNIT")

    price_plan["Buy Value (Cr)"] = (
        price_plan["Proposed_Buy"] * price_plan["MRP/ UNIT"] / 10_000_000
    ).round(4)
    price_plan["Avg_STR"] = price_plan["Avg_STR"].round(1)

    pc1,pc2 = st.columns(2)
    with pc1:
        fig_p1 = px.bar(price_plan, x="MRP/ UNIT", y="Proposed_Buy",
                        color="Avg_STR", color_continuous_scale="RdYlGn",
                        range_color=[0,100], template="plotly_dark",
                        title=f"{selected_cat_price} — Units to Buy at Each Price Point",
                        labels={"MRP/ UNIT":"MRP (₹)","Proposed_Buy":"Rec. Buy Qty"})
        st.plotly_chart(fig_p1, use_container_width=True)

    with pc2:
        fig_p2 = px.bar(price_plan, x="MRP/ UNIT", y="Styles",
                        color="PRICE BAND", template="plotly_dark",
                        title=f"{selected_cat_price} — Styles at Each Price Point",
                        labels={"MRP/ UNIT":"MRP (₹)","Styles":"No. of Styles"})
        st.plotly_chart(fig_p2, use_container_width=True)

    best_price = price_plan.sort_values("Avg_STR", ascending=False).iloc[0]
    st.markdown(f"""
    <div class="insight-box">
    💡 For <b>{selected_cat_price}</b> in <b>{selected_region}</b> —
    Best price point is <b>₹{int(best_price['MRP/ UNIT'])}</b>
    with <b>{best_price['Avg_STR']:.1f}% avg STR</b> and <b>{int(best_price['Styles'])} styles</b>.
    Recommend buying deeper at this price for SS27.
    </div>""", unsafe_allow_html=True)

    st.dataframe(
        price_plan.rename(columns={
            "PRICE BAND":"Price Band","MRP/ UNIT":"MRP (₹)",
            "Total_Demand":"Past Demand","Avg_STR":"Avg STR %",
            "Proposed_Buy":"SS27 Rec. Buy"
        }),
        column_config={
            "Avg STR %": st.column_config.ProgressColumn("Avg STR %", format="%.1f%%", min_value=0, max_value=100),
            "MRP (₹)": st.column_config.NumberColumn("MRP", format="₹%d"),
        },
        use_container_width=True, hide_index=True
    )

# ═══════════════════════════════════════════
# CAPSULE PLAN
# ═══════════════════════════════════════════
st.divider()
st.subheader("🧩 Curated SS27 Capsule Plan")

cap_tab1, cap_tab2 = st.tabs([
    "🎉 Festive Capsule (Regional)",
    "🌍 Pan India Capsule (Event-Based)"
])

with cap_tab1:
    st.caption(f"Region-specific festive collection for {selected_region}")
    FESTIVE = {
        "NORTH": "Diwali / Holi / Navratri — bright colours, occasion wear, gifting styles",
        "SOUTH": "Onam / Pongal / Ugadi — traditional-meets-casual, light fabrics",
        "EAST":  "Durga Puja / Bihu — ethnic fusion, vibrant prints",
        "WEST":  "Ganesh Chaturthi / Navratri — festive casuals, bright and printed styles",
    }
    st.info(f"🎊 **{selected_region} Festive Context:** {FESTIVE.get(selected_region,'Regional festive season')}")
    num_festive = st.slider("Styles in Festive Capsule", 5, 30, 15, key="fest_size")

    festive_cap = matrix_dedup.sort_values("STR %", ascending=False).head(num_festive)
    if not festive_cap.empty:
        fig_fest = px.bar(festive_cap, x="STR %", y="DES", color="CAT",
                          orientation="h", template="plotly_dark", range_x=[0,100],
                          title=f"{selected_region} Festive Capsule — Top {num_festive} Styles by STR %",
                          labels={"DES":"Style"})
        fig_fest.update_layout(yaxis={"categoryorder":"total ascending"})
        fig_fest.add_vline(x=50, line_dash="dash", line_color="yellow")
        st.plotly_chart(fig_fest, use_container_width=True)

        fc1,fc2,fc3 = st.columns(3)
        fc1.metric("Capsule Styles",   len(festive_cap))
        fc2.metric("Avg STR %",        f"{festive_cap['STR %'].mean():.1f}%")
        fc3.metric("Rec. Buy (Total)", f"{int(festive_cap['PROPOSED_BUY'].sum()):,}")

        show_f = ["CAT","DES","GENDER","STR %","MRP/ UNIT","PRICE BAND","PROPOSED_BUY"]
        if "FIT_TYPE" in festive_cap.columns:
            show_f.insert(4, "FIT_TYPE")
        st.dataframe(festive_cap[show_f].sort_values("STR %", ascending=False),
            column_config={
                "STR %": st.column_config.ProgressColumn("STR %", format="%.1f%%", min_value=0, max_value=100),
                "MRP/ UNIT": st.column_config.NumberColumn("MRP", format="₹%d"),
                "PROPOSED_BUY": st.column_config.NumberColumn("Rec. Buy ✅"),
            },
            use_container_width=True, hide_index=True)

with cap_tab2:
    st.caption("Pan India event-based capsule — styles with strong all-India performance")
    EVENTS = {
        "Formula 1 Indian Grand Prix 2027":  "Speed, sport, urban streetwear — graphic tees, bold prints, athleisure",
        "ICC Cricket World Cup 2027":         "National pride — patriotic prints, sport-casual, performance wear",
        "IPL Season 2027":                    "City fandom, casual sport — team-inspired casuals, comfort fits",
        "Diwali 2027 (Pan India)":            "All-India gifting — occasion wear, bright festive colours",
        "Summer Vacation 2027":               "School holidays — fun prints, lightweight fabrics, active casuals",
    }
    selected_event = st.selectbox("🎯 Select Upcoming Event", list(EVENTS.keys()))
    st.info(f"👟 **Style Direction:** {EVENTS[selected_event]}")
    num_pan = st.slider("Styles in Pan India Capsule", 5, 30, 20, key="pan_size")

    all_mask = (
        df["CAT"].isin(selected_cats) &
        (df["MRP/ UNIT"] >= price_range[0]) &
        (df["MRP/ UNIT"] <= price_range[1])
    )
    if selected_seasons and "SEASON" in df.columns:
        all_mask = all_mask & df["SEASON"].isin(selected_seasons)
    if selected_gender and "GENDER" in df.columns:
        all_mask = all_mask & df["GENDER"].isin(selected_gender)

    all_rdf = df[all_mask].copy()
    pan_matrix = all_rdf.groupby(["CAT","DES","GENDER"]).agg(
        Regions_Present=("REGION","nunique"),
        Avg_STR=("STR %","mean"),
        Total_Demand=("ORDER QUANTITY","sum"),
        Avg_MRP=("MRP/ UNIT","mean"),
    ).reset_index()
    pan_matrix["Pan_India_Score"] = (
        pan_matrix["Avg_STR"] * pan_matrix["Regions_Present"]
    ).round(1)
    pan_cap = pan_matrix.sort_values("Pan_India_Score", ascending=False).head(num_pan)

    if not pan_cap.empty:
        fig_pan = px.bar(
            pan_cap.sort_values("Pan_India_Score", ascending=True),
            x="Pan_India_Score", y="DES", color="Regions_Present",
            orientation="h", color_continuous_scale="Blues",
            template="plotly_dark",
            title=f"Pan India Capsule for '{selected_event}'",
            labels={"DES":"Style","Pan_India_Score":"Pan India Score","Regions_Present":"Regions"}
        )
        fig_pan.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig_pan, use_container_width=True)
        st.caption("Pan India Score = Avg STR % × Regions where style sold. Higher = more universally strong.")

        pi1,pi2,pi3 = st.columns(3)
        pi1.metric("Capsule Styles",      len(pan_cap))
        pi2.metric("Avg STR %",           f"{pan_cap['Avg_STR'].mean():.1f}%")
        pi3.metric("Avg Regions Present", f"{pan_cap['Regions_Present'].mean():.1f} / {df['REGION'].nunique()}")

        st.dataframe(pan_cap[[
            "CAT","DES","GENDER","Regions_Present","Avg_STR","Avg_MRP","Pan_India_Score"
        ]].rename(columns={
            "Regions_Present":"Regions","Avg_STR":"Avg STR %",
            "Avg_MRP":"Avg MRP (₹)","Pan_India_Score":"Pan India Score"
        }),
        column_config={
            "Avg STR %": st.column_config.ProgressColumn("Avg STR %", format="%.1f%%", min_value=0, max_value=100),
            "Avg MRP (₹)": st.column_config.NumberColumn("MRP", format="₹%d"),
        },
        use_container_width=True, hide_index=True)

# ── EXPORT ───────────────────────────────
st.divider()
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    final_view.to_excel(writer, index=False, sheet_name="Article_Plan")
    if "FIT_TYPE" in matrix.columns:
        opt_export = matrix.groupby(["CAT","FIT_TYPE","GENDER"]).agg(
            Styles=("DES","nunique"),
            Total_Demand=("ORDER QUANTITY","sum"),
            Avg_STR=("STR %","mean"),
            Rec_Buy=("PROPOSED_BUY","sum"),
        ).reset_index()
        opt_export.to_excel(writer, index=False, sheet_name="Option_Plan")
    price_export = matrix.groupby(["CAT","PRICE BAND","MRP/ UNIT"]).agg(
        Styles=("DES","nunique"),
        Total_Demand=("ORDER QUANTITY","sum"),
        Avg_STR=("STR %","mean"),
        Proposed_Buy=("PROPOSED_BUY","sum"),
    ).reset_index()
    price_export.to_excel(writer, index=False, sheet_name="Price_Plan")

st.sidebar.divider()
st.sidebar.download_button(
    "📥 Export Full Buying Plan (Excel)",
    buffer.getvalue(),
    f"SS27_BuyPlan_{selected_region}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.sidebar.caption("3 sheets: Article Plan + Option Plan + Price Plan")
