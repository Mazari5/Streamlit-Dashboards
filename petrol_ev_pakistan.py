"""
Pakistan: Petrol vs Electric Bike Cost Comparison
==================================================
Single-column mobile-friendly Streamlit app
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Petrol vs EV Bike — Pakistan",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.block-container { max-width: 720px; }
.metric-card {
    background: white; border-radius: 14px; padding: 18px 20px;
    border: 1px solid #E8EAF0; box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 0;
}
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
}
.metric-grid-full { margin-bottom: 12px; }
.metric-label { font-size: 12px; color: #6B7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }
.metric-value { font-size: 24px; font-weight: 700; margin: 4px 0 2px; }
.metric-sub { font-size: 12px; color: #9CA3AF; }
.petrol-color { color: #D85A30; }
.ev-color { color: #0F9B6E; }
.rec-box { border-radius: 14px; padding: 20px 24px; border-left: 5px solid; margin-top: 8px; }
.rec-save    { background: #F0FDF8; border-color: #0F9B6E; }
.rec-neutral { background: #F8F9FF; border-color: #6B7280; }
.rec-warn    { background: #FFF7ED; border-color: #D85A30; }
.tree-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 10px;
}
.tree-box {
    background: #F0FDF4; border-radius: 14px; padding: 20px 10px;
    border: 1px solid #86EFAC;
}
.tree-stat { text-align: center; }
.tree-val  { font-size: 22px; font-weight: 700; color: #15803D; }
.tree-lbl  { font-size: 11px; color: #166534; margin-top: 2px; }
.wh-hint {
    background: #EFF6FF; border-radius: 10px; padding: 10px 14px;
    border: 1px solid #BFDBFE; font-size: 12px; color: #1E40AF; margin-top: 6px; line-height: 1.6;
}
.wh-caution {
    background: #FFFBEB; border-radius: 10px; padding: 10px 14px;
    border: 1px solid #FCD34D; font-size: 12px; color: #92400E; margin-top: 6px; line-height: 1.6;
}
.bat-warn {
    background: #FFF7ED; border-radius: 10px; padding: 10px 14px;
    border: 1px solid #FDBA74; font-size: 12px; color: #9A3412; margin-top: 6px; line-height: 1.6;
}
[data-testid="stSidebar"] { background: #1E2235; }
[data-testid="stSidebar"] label { color: #CBD5E1 !important; }
[data-testid="stSidebar"] p { color: #94A3B8 !important; }
[data-testid="stSidebar"] h2 { color: #F1F5F9 !important; }
[data-testid="stSidebar"] h3 { color: #94A3B8 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.07em; }
</style>
""", unsafe_allow_html=True)

C_PETROL = "#D85A30"
C_EV     = "#0F9B6E"
C_INDIGO = "#6366F1"
FONT     = "Plus Jakarta Sans"
CO2_PER_TREE_YR = 21.77

VOLTAGE_OPTIONS = [36, 48, 60, 72, 84, 96]
AH_OPTIONS = [12, 15, 20, 24, 26, 30, 32, 36, 40, 45, 50, 60]

BAT_INFO = {
    "LFP (Lithium Iron Phosphate)": {
        "life_yrs": 6, "life_km": 27_500,
        "note": "Most common in Pakistani EVs. Lasts 5–8 years (2,000+ cycles). Safest chemistry, handles Pakistan's heat well.",
    },
    "Li-ion / NMC": {
        "life_yrs": 4, "life_km": 22_000,
        "note": "Higher energy density but shorter life (~3–5 years / 500–1,000 cycles). Degraded faster by heat.",
    },
    "Graphene": {
        "life_yrs": 8, "life_km": 35_000,
        "note": "Premium long-life option. Claims 8–10 years. Fast-charge capable. Less common; replacement parts harder to source.",
    },
}

def fmt(val): return f"Rs {int(round(val)):,}"

with st.sidebar:
    st.markdown("## ⚡ Petrol vs EV\n**Pakistan Cost Calculator**")
    st.markdown("---")
    st.markdown("### ⛽ Petrol Bike")
    p_price    = st.number_input("Purchase price (Rs)", value=165_000, step=5_000, min_value=30_000, max_value=1_000_000)
    p_mileage  = st.slider("Mileage (km per litre)", 20, 80, 55, 1, help="70cc=55 · 100cc=48 · 125cc=40 · 150cc=35 km/L")
    p_service  = st.slider("Monthly service & oil change (Rs)", 500, 6_000, 2_000, 100)
    fuel_price = st.slider("Petrol price (Rs / litre)", 200, 500, 268, 1, help="OGRA: Rs 268.41/L RON-92, March 2025")
    st.markdown("---")
    st.markdown("### ⚡ Electric Bike")
    e_price    = st.number_input("Purchase price (Rs) ", value=185_000, step=5_000, min_value=30_000, max_value=1_000_000)
    elec_price = st.slider("Electricity rate (Rs / kWh)", 20, 80, 52, 1, help="NEPRA residential ~Rs 52/kWh for >300 units/month")
    st.markdown("**Battery & Range**")
    bat_voltage = st.selectbox("Battery voltage (V)", VOLTAGE_OPTIONS, index=VOLTAGE_OPTIONS.index(60))
    bat_ah      = st.selectbox("Battery capacity (Ah)", AH_OPTIONS, index=AH_OPTIONS.index(26))
    bat_kwh     = round(bat_voltage * bat_ah / 1000, 2)
    st.caption(f"📦 Pack size: **{bat_kwh:.2f} kWh** ({bat_voltage}V × {bat_ah}Ah)")
    claimed_range = st.slider("Company-claimed range (km)", 0, 600, 120, 5)
    st.markdown(f"""<div class='wh-caution'>
        ⚠️ <b>Caution:</b> Manufacturer range is tested under ideal conditions.
        Estimated real-world range: <b>{int(claimed_range*0.80)}–{int(claimed_range*0.85)} km</b> (80–85% of claimed).
    </div>""", unsafe_allow_html=True)
    if claimed_range > 0:
        real_range = claimed_range * 0.80
        wh_per_km  = round((bat_kwh * 1000) / real_range, 1)
    else:
        real_range = 1
        wh_per_km  = 22
    st.markdown(f"""<div class='wh-hint'>
        ⚡ Calculated consumption: <b>{wh_per_km} Wh/km</b><br>
        <small>({bat_voltage}V × {bat_ah}Ah) ÷ {int(real_range)} km = <b>{wh_per_km} Wh/km</b></small>
    </div>""", unsafe_allow_html=True)
    st.markdown("**Battery type & replacement**")
    bat_type   = st.selectbox("Battery type", list(BAT_INFO.keys()))
    bat_info   = BAT_INFO[bat_type]
    st.caption(bat_info["note"])
    bat_warranty_km  = st.slider("Battery warranty (km)", 10_000, 50_000, 25_000, 1_000)
    bat_warranty_yr  = st.slider("Battery warranty (years)", 1, 5, 3, 1)
    bat_replace_cost = st.slider("Battery replacement cost (Rs)", 40_000, 150_000, 70_000, 5_000)
    st.markdown("**EV running costs**")
    e_maint_m = st.slider("Monthly EV maintenance (Rs)", 100, 3_000, 500, 100)
    st.markdown("---")
    st.markdown("### 📊 Usage")
    dist_monthly = st.slider("Monthly distance (km)", 200, 4_000, 1_000, 50)
    years        = st.slider("Years to keep bike", 1, 10, 5, 1)
    st.markdown("---")
    st.caption("Sources: OGRA · NEPRA/LESCO · NTDC · IPCC AR6 · PakWheels · April 2025")

# Battery replacement logic
total_months = years * 12
dist_cum = [dist_monthly * m for m in range(total_months + 1)]
warranty_expire_month = None
for m in range(1, total_months + 1):
    if dist_cum[m] >= bat_warranty_km or m >= bat_warranty_yr * 12:
        warranty_expire_month = m
        break
bat_replace_months = []
if warranty_expire_month is not None:
    first_replace = warranty_expire_month + 12
    m = first_replace
    while m <= total_months:
        bat_replace_months.append(m)
        m += int(bat_info["life_yrs"] * 12)
bat_replacements = len(bat_replace_months)

# Calculations
p_fuel_m   = (dist_monthly / p_mileage) * fuel_price
p_run_m    = p_fuel_m + p_service
p_tco      = p_price + p_run_m * 12 * years
e_elec_m   = (dist_monthly * wh_per_km / 1000) * elec_price
e_run_m    = e_elec_m + e_maint_m
e_tco      = e_price + e_run_m * 12 * years + bat_replacements * bat_replace_cost
save_m     = p_run_m - e_run_m
net_save   = p_tco - e_tco
price_diff = e_price - p_price
p_cpkm     = p_run_m / dist_monthly
e_cpkm     = e_run_m / dist_monthly
if save_m > 0 and price_diff > 0:
    be_months = price_diff / save_m
elif save_m > 0 and price_diff <= 0:
    be_months = 0
else:
    be_months = float("inf")
p_co2_m     = (dist_monthly / p_mileage) * 2.31
e_co2_m     = (dist_monthly * wh_per_km / 1000) * 0.45
co2_saved_m = max(0, p_co2_m - e_co2_m)
trees_m     = co2_saved_m / (CO2_PER_TREE_YR / 12)
trees_yr    = co2_saved_m * 12 / CO2_PER_TREE_YR
trees_total = co2_saved_m * 12 * years / CO2_PER_TREE_YR

# Header
st.markdown("# 🏍️ Petrol vs Electric Bike — Pakistan")
st.markdown(f"Custom petrol bike &nbsp;·&nbsp; **{dist_monthly:,} km/month** &nbsp;·&nbsp; **{years} year{'s' if years > 1 else ''}**")
st.markdown("---")

# Metric cards
def mcard_html(label, value, sub, color):
    return f"""<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>"""

save_col = C_EV if save_m >= 0 else C_PETROL
net_col  = C_EV if net_save >= 0 else C_PETROL
if not np.isfinite(be_months):
    be_str, be_sub, be_col = "Never", "EV costs more to run", C_PETROL
elif be_months == 0:
    be_str, be_sub, be_col = "Day 1", "EV cheaper upfront too", C_EV
elif be_months < 12:
    be_str, be_sub, be_col = f"{be_months:.0f} months", "break-even point", C_EV
else:
    be_str, be_sub, be_col = f"{be_months/12:.1f} years", "break-even point", C_EV
bat_note = f"incl. {bat_replacements} battery swap{'s' if bat_replacements != 1 else ''}" if bat_replacements > 0 else "no battery swaps in this period"

st.markdown(f"""<div class="metric-grid">
  {mcard_html("Petrol monthly cost", fmt(p_run_m), f"Rs {p_cpkm:.2f} per km", C_PETROL)}
  {mcard_html("EV monthly cost", fmt(e_run_m), f"Rs {e_cpkm:.2f} per km", C_EV)}
</div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="metric-grid">
  {mcard_html("Monthly saving (EV)", f"{'+'if save_m>=0 else ''}{fmt(save_m)}", "per month on running", save_col)}
  {mcard_html("Break-even point", be_str, be_sub, be_col)}
</div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="metric-grid-full">
  {mcard_html(f"Net saving ({years} yr)", f"{'+'if net_save>=0 else ''}{fmt(net_save)}", bat_note, net_col)}
</div>""", unsafe_allow_html=True)

# Battery warning
if warranty_expire_month is not None:
    expire_yr  = warranty_expire_month / 12
    replace_yr = (warranty_expire_month + 12) / 12
    w_km_hit   = dist_cum[min(warranty_expire_month, total_months)] >= bat_warranty_km
    trigger    = f"{bat_warranty_km:,} km limit" if w_km_hit else f"{bat_warranty_yr}-year time limit"
    st.markdown(f"""<div class='bat-warn'>
        🔋 <b>Battery replacement alert:</b> Your {bat_type} battery hits its warranty {trigger} around
        <b>Year {expire_yr:.1f}</b>. Replacement expected ~<b>Year {replace_yr:.1f}</b>
        ({fmt(bat_replace_cost)} × {bat_replacements} = {fmt(bat_replacements * bat_replace_cost)} included above).
    </div>""", unsafe_allow_html=True)

st.markdown("")

# Climate
st.markdown("### 🌳 Climate Impact — choosing EV saves...")
st.markdown(f"""<div class="tree-grid">
  <div class="tree-box"><div class="tree-stat"><div style="font-size:26px">🌿</div><div class="tree-val">{trees_m:.1f}</div><div class="tree-lbl">trees / month</div></div></div>
  <div class="tree-box"><div class="tree-stat"><div style="font-size:26px">🌲</div><div class="tree-val">{trees_yr:.0f}</div><div class="tree-lbl">trees / year</div></div></div>
  <div class="tree-box"><div class="tree-stat"><div style="font-size:26px">🌍</div><div class="tree-val">{trees_total:.0f}</div><div class="tree-lbl">trees / {years} yrs</div></div></div>
</div>
<div class="tree-grid">
  <div class="tree-box"><div class="tree-stat"><div style="font-size:26px">💨</div><div class="tree-val">{co2_saved_m:.0f} kg</div><div class="tree-lbl">CO₂ / month</div></div></div>
  <div class="tree-box"><div class="tree-stat"><div style="font-size:26px">💨</div><div class="tree-val">{co2_saved_m*12:.0f} kg</div><div class="tree-lbl">CO₂ / year</div></div></div>
  <div class="tree-box" style="visibility:hidden"></div>
</div>""", unsafe_allow_html=True)
st.caption("1 tree absorbs ~21.77 kg CO₂/year (IPCC). Pakistan grid: 0.45 kg CO₂/kWh (NTDC 2023). Petrol: 2.31 kg CO₂/litre (IPCC AR6 2021).")

# Charts
months_range = list(range(0, years * 12 + 1))
p_cumul = [p_price + p_run_m * m for m in months_range]
e_cumul = []
for m in months_range:
    swaps = sum(1 for rm in bat_replace_months if rm <= m)
    e_cumul.append(e_price + e_run_m * m + swaps * bat_replace_cost)

st.subheader("📈 Cumulative Cost Over Time")
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=months_range, y=p_cumul, mode="lines", name="Petrol",
    line=dict(color=C_PETROL, width=3), hovertemplate="Month %{x}<br>Total: Rs %{y:,.0f}<extra></extra>"))
fig_line.add_trace(go.Scatter(x=months_range, y=e_cumul, mode="lines", name="Electric",
    line=dict(color=C_EV, width=3, dash="dash"), hovertemplate="Month %{x}<br>Total: Rs %{y:,.0f}<extra></extra>"))
for rm in bat_replace_months:
    if rm <= years * 12:
        fig_line.add_vline(x=rm, line_dash="dot", line_color="#F59E0B", line_width=1.5)
        fig_line.add_annotation(x=rm, y=e_cumul[rm], text="🔋 Bat. swap", showarrow=True, arrowhead=2,
            arrowcolor="#F59E0B", font=dict(color="#92400E", size=10, family=FONT),
            bgcolor="#FFFBEB", bordercolor="#F59E0B", borderwidth=1)
if np.isfinite(be_months) and 0 < be_months <= years * 12:
    be_idx = int(round(be_months))
    be_y   = e_cumul[min(be_idx, len(e_cumul)-1)]
    fig_line.add_vline(x=be_months, line_dash="dot", line_color=C_INDIGO, line_width=1.5)
    fig_line.add_annotation(x=be_months, y=be_y, text=f"Break-even<br>{be_months/12:.1f} yrs",
        showarrow=True, arrowhead=2, arrowcolor=C_INDIGO,
        font=dict(color=C_INDIGO, size=11, family=FONT), bgcolor="white", bordercolor=C_INDIGO, borderwidth=1)
yr_ticks  = [m for m in months_range if m % 12 == 0]
yr_labels = ["Now" if m == 0 else f"Yr {m//12}" for m in yr_ticks]
fig_line.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", y=1.12, x=0),
    xaxis=dict(tickvals=yr_ticks, ticktext=yr_labels, showgrid=True, gridcolor="#F0F0F0"),
    yaxis=dict(tickformat=",", tickprefix="Rs ", showgrid=True, gridcolor="#F0F0F0"),
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family=FONT))
st.plotly_chart(fig_line, use_container_width=True)

st.subheader(f"🏁 {years}-Year Cost Breakdown")
cats   = ["Purchase", "Fuel / Elec", "Service / Maint", "Battery swap"]
p_vals = [p_price, p_fuel_m*12*years, p_service*12*years, 0]
e_vals = [e_price, e_elec_m*12*years, e_maint_m*12*years, bat_replacements*bat_replace_cost]
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(name="Petrol",   x=cats, y=p_vals, marker_color=C_PETROL,
    hovertemplate="%{x}<br>Rs %{y:,.0f}<extra>Petrol</extra>"))
fig_bar.add_trace(go.Bar(name="Electric", x=cats, y=e_vals, marker_color=C_EV,
    hovertemplate="%{x}<br>Rs %{y:,.0f}<extra>Electric</extra>"))
fig_bar.update_layout(barmode="group", height=320, margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", y=1.12, x=0),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(tickformat=",", tickprefix="Rs ", showgrid=True, gridcolor="#F0F0F0"),
    plot_bgcolor="white", paper_bgcolor="white", font=dict(family=FONT))
st.plotly_chart(fig_bar, use_container_width=True)

# Table
st.markdown("---")
st.subheader("📋 Full Cost Comparison Table")
rows = [
    ("💰 Purchase price",                  fmt(p_price),           fmt(e_price),          fmt(p_price - e_price)),
    ("⛽ Fuel / electricity (monthly)",    fmt(p_fuel_m),          fmt(e_elec_m),         fmt(p_fuel_m - e_elec_m)),
    ("🔧 Service / maintenance (monthly)", fmt(p_service),         fmt(e_maint_m),        fmt(p_service - e_maint_m)),
    ("🔋 Battery replacements (total)",    "Rs 0",                 fmt(bat_replacements * bat_replace_cost), "—"),
    ("━━━", "━━━━━━━", "━━━━━━━", "━━━━━━━"),
    ("📊 Total monthly running",           fmt(p_run_m),           fmt(e_run_m),          fmt(save_m)),
    ("🗓️ Annual running cost",             fmt(p_run_m * 12),      fmt(e_run_m * 12),     fmt(save_m * 12)),
    (f"📅 {years}-yr running cost",        fmt(p_run_m*12*years),  fmt(e_run_m*12*years), fmt(save_m*12*years)),
    (f"🏁 Total {years}-yr ownership",     fmt(p_tco),             fmt(e_tco),            fmt(net_save)),
    ("📍 Cost per km",                     f"Rs {p_cpkm:.2f}",     f"Rs {e_cpkm:.2f}",   f"Rs {p_cpkm - e_cpkm:.2f}"),
    ("⚡ Battery pack size",               "N/A",                  f"{bat_kwh:.2f} kWh ({bat_voltage}V × {bat_ah}Ah)", "—"),
    ("🔄 Wh/km (calculated)",              "N/A",                  f"{wh_per_km} Wh/km", "—"),
    ("🌿 CO₂ per month",                   f"{p_co2_m:.0f} kg",    f"{e_co2_m:.0f} kg",  f"{co2_saved_m:.0f} kg saved"),
    ("🌳 Tree equivalent per year",        "—",                    "—",                   f"{trees_yr:.0f} trees"),
]
df = pd.DataFrame(rows, columns=["Cost Item", "Petrol Bike", "Electric Bike", "Petrol saves / EV saves"])
st.dataframe(df, use_container_width=True, hide_index=True)

# Recommendation
st.markdown("---")
st.subheader("🎯 Recommendation")
if not np.isfinite(be_months):
    rc, ri = "rec-warn", "⚠️"
    rt = "Petrol bike is more economical for your current usage"
    rb = (f"At {dist_monthly:,} km/month with electricity at Rs {elec_price}/kWh, the EV costs "
          f"<b>{fmt(abs(save_m))}/month MORE</b> to run. Tips: ride more km/month, "
          f"install solar panels to cut electricity cost, or choose a more efficient EV model.")
elif be_months == 0:
    rc, ri = "rec-save", "🏆"
    rt = "Switch to Electric — cheaper upfront AND cheaper to run!"
    rb = (f"The EV is <b>{fmt(abs(price_diff))} cheaper</b> to buy and saves "
          f"<b>{fmt(save_m)}/month</b> on running. Over {years} years: save <b>{fmt(net_save)}</b> "
          f"(after {bat_replacements} battery swap{'s' if bat_replacements != 1 else ''}). "
          f"Plus you avoid {co2_saved_m*12:.0f} kg CO₂/year.")
elif be_months > years * 12:
    rc, ri = "rec-neutral", "⏳"
    rt = f"Break-even in {be_months/12:.1f} yrs — beyond your {years}-year ownership plan"
    rb = (f"EV saves <b>{fmt(save_m)}/month</b> on running costs, but the upfront premium "
          f"of <b>{fmt(price_diff)}</b> won't be recovered in {years} years. "
          f"If you plan to keep it longer, or petrol prices rise further, the EV wins over time.")
else:
    rc, ri = "rec-save", "✅"
    rt = f"Switch to Electric — break-even in {be_months/12:.1f} yrs, then pure savings"
    rb = (f"After <b>{be_months:.0f} months</b> you save <b>{fmt(save_m)}/month</b>. "
          f"Total saving over {years} years: <b>{fmt(net_save)}</b>. "
          f"Bonus: reduce CO₂ by <b>{co2_saved_m:.0f} kg/month</b> — equal to planting "
          f"<b>{trees_yr:.0f} trees per year</b>.")
st.markdown(f"""<div class="rec-box {rc}">
    <h3 style="margin:0 0 8px;">{ri} {rt}</h3>
    <p style="margin:0; color:#374151; line-height:1.6;">{rb}</p>
</div>""", unsafe_allow_html=True)

# References
st.markdown("---")
with st.expander("📚 References & Methodology"):
    st.markdown("""
### Fuel & Energy Prices
| Reference | Detail |
|---|---|
| **OGRA** | Petrol RON-92: **Rs 268.41/L**, March 2025. [ogra.org.pk](https://www.ogra.org.pk) |
| **NEPRA** | Residential >300 units/month: ~**Rs 52/kWh**. [nepra.org.pk](https://www.nepra.org.pk) |
| **LESCO** | Domestic tariff April 2025. [lesco.gov.pk](https://www.lesco.gov.pk) |

---
### Wh/km Methodology
**Formula:** `Wh/km = (Voltage × Ah) ÷ Real-world range` | Real-world = 80% of claimed range.

---
### Battery Replacement Logic
Warranty: **25,000–30,000 km OR 3 years** (whichever first). Replacement ~12 months after expiry.

| Battery Type | Lifespan | Cycles |
|---|---|---|
| LFP | 5–8 yrs | 2,000–3,000 |
| Li-ion/NMC | 3–5 yrs | 500–1,000 |
| Graphene | 7–10 yrs | 3,000+ |

Replacement: **Rs 60,000–90,000** (2025 market rates).

---
### CO₂ Factors
| Factor | Value | Source |
|---|---|---|
| Petrol | 2.31 kg CO₂/L | IPCC AR6 2021 |
| Grid | 0.45 kg CO₂/kWh | NTDC 2023 |
| Tree | 21.77 kg CO₂/yr | IPCC |

> ⚠️ All figures are estimates. Verify current prices before purchasing.

**Built for Pakistan · April 2025 · By Mohsin Ahmad Mazari**
    """)

st.markdown("""<div style="text-align:center; color:#9CA3AF; font-size:12px; padding:20px 0 8px;">
    Data: OGRA · NEPRA/LESCO · NTDC · IPCC AR6 · PakWheels --- Created by Mohsin Mazari
</div>""", unsafe_allow_html=True)
