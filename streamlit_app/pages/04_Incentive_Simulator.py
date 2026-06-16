"""
Page 4: Incentive Simulator - Dynamic Theme
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle, lucide_icon, st_html
from streamlit_app.utils.chart_helpers import get_theme_colors

st.set_page_config(page_title="Incentive Simulator", page_icon="⚙️", layout="wide")

# ── CSS & Theme ──────────────────────────────────────────────────
inject_theme_css()
c = get_theme_colors()

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    render_theme_toggle()

# ── Header ────────────────────────────────────────────────────────
st_html(f"""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);
            display: flex; align-items: center;">
    <div style="margin-right:20px;">
        {lucide_icon('sliders', size=42, color='var(--accent-primary)')}
    </div>
    <div>
        <div style="color:var(--text-color); font-size:38px; font-weight:800;
                    letter-spacing:-0.02em; line-height:1.2;">
            Incentive Plan <span style="color:var(--accent-primary);">Simulator</span>
        </div>
        <div style="color:var(--muted-text); font-size:15px; margin-top:10px; font-weight:500;">
            What-if analysis — adjust slabs, see real-time payout impact
        </div>
    </div>
</div>
""")

# ── Simulation Logic Helper ──────────────────────────────────────
def calc_sim(row, slabs):
    att = row['attainment_pct']
    sales = row['actual_sales']
    if att <= 0.50: rate = slabs['s1'] / 100
    elif att <= 0.80: rate = slabs['s2'] / 100
    elif att <= 1.00: rate = slabs['s3'] / 100
    elif att <= 1.20: rate = slabs['s4'] / 100
    else: rate = slabs['s5'] / 100
    return sales * rate

# ── Main Content ──────────────────────────────────────────────────
st_html(f"### {lucide_icon('settings', size=20, color='var(--accent-primary)')} Configure Commission Slabs")

col_slab, col_result = st.columns([2, 3])

with col_slab:
    st_html("<div class='custom-card'>")
    st_html("<b style='color:var(--text-color);'>Slab 1: 0-50% Attainment</b>")
    s1 = st.slider("Rate %", 0.0, 10.0, 0.0, 0.5, key='s1')
    
    st_html("<b style='color:var(--text-color);'>Slab 2: 51-80%</b>")
    s2 = st.slider("Rate %", 0.0, 15.0, 5.0, 0.5, key='s2')
    
    st_html("<b style='color:var(--text-color);'>Slab 3: 81-100%</b>")
    s3 = st.slider("Rate %", 0.0, 20.0, 10.0, 0.5, key='s3')
    
    st_html("<b style='color:var(--text-color);'>Slab 4: 101-120%</b>")
    s4 = st.slider("Rate %", 0.0, 25.0, 15.0, 0.5, key='s4')
    
    st_html("<b style='color:var(--text-color);'>Slab 5: 120%+ (Accelerator)</b>")
    s5 = st.slider("Rate %", 0.0, 35.0, 20.0, 0.5, key='s5')
    
    st_html("<hr style='border-color:var(--input-border);'>")
    st_html("<b style='color:var(--text-color);'>Top Performer Bonus %</b>")
    bonus = st.slider("Bonus Rate %", 0.0, 15.0, 5.0)
    st_html("</div>")

# Run Simulation Calculations
slabs = {'s1':s1, 's2':s2, 's3':s3, 's4':s4, 's5':s5}
sim = df.copy()
sim['sim_comm'] = sim.apply(lambda r: calc_sim(r, slabs), axis=1)
thresh = sim.groupby('month')['attainment_pct'].transform(lambda x: x.quantile(0.90))
sim['sim_bonus'] = np.where(sim['attainment_pct']>=thresh,
                             sim['actual_sales']*(bonus/100), 0.0)
sim['sim_pay'] = sim['monthly_base'] + sim['sim_comm'] + sim['sim_bonus']

sim_total = sim['sim_pay'].sum()
base_total = df['total_payout'].sum()
delta = sim_total - base_total
pct = (delta / base_total * 100) if base_total > 0 else 0
comm_delta = sim['sim_comm'].sum() - df['commission_earned'].sum()

# Plotly theme setup
PLOTLY_THEME = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=c['text'], family='Manrope'),
    xaxis=dict(gridcolor=c['grid'], color=c['text']),
    yaxis=dict(gridcolor=c['grid'], color=c['text']),
)

with col_result:
    st.markdown("### 📊 Real-Time Impact")

    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Baseline Payout", f"₹{base_total/10000000:.2f}Cr")
    with m2:
        st.metric("Simulated Payout", f"₹{sim_total/10000000:.2f}Cr", f"{'+' if pct>=0 else ''}{pct:.1f}%")
    with m3:
        st.metric("Commission Δ", f"₹{comm_delta/1000:+,.0f}K")

    # Slab comparison chart
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(
        x=['0-50%','51-80%','81-100%','101-120%','120%+'],
        y=[0, 5, 10, 15, 20], name='Current Plan',
        marker_color=c['fill_primary'],
        marker_line_color=c['primary'],
        marker_line_width=1.5,
    ))
    fig_s.add_trace(go.Bar(
        x=['0-50%','51-80%','81-100%','101-120%','120%+'],
        y=[s1, s2, s3, s4, s5], name='Simulated Plan',
        marker_color=c['success'],
    ))
    fig_s.update_layout(
        barmode='group', 
        title='<b>Slab Rates Comparison</b>',
        title_font=dict(size=16, family='Manrope'),
        yaxis_title='Rate (%)', 
        height=320, 
        legend=dict(orientation='h', y=1.12),
        margin=dict(t=50, b=30, l=10, r=10),
        **PLOTLY_THEME
    )
    st.plotly_chart(fig_s, use_container_width=True)

# ── Monthly Comparison Trend ──────────────────────────────────────
st.markdown("### 📈 Monthly Payout: Current vs Simulated")

mc = (sim.groupby(['month','month_label'])
      .agg(sim_p=('sim_pay','sum'), base_p=('total_payout','sum'))
      .reset_index().sort_values('month'))

fig_mc = go.Figure()
fig_mc.add_trace(go.Scatter(
    x=mc['month_label'], y=mc['base_p'], name='Current Plan',
    mode='lines+markers', line=dict(color=c['primary'], width=2.5),
))
fig_mc.add_trace(go.Scatter(
    x=mc['month_label'], y=mc['sim_p'], name='Simulated Plan',
    mode='lines+markers', line=dict(color=c['success'], width=3, dash='dash'),
    fill='tonexty', fillcolor=c['fill_primary'],
))
fig_mc.update_layout(
    title='<b>Monthly Payout Comparison</b>',
    title_font=dict(size=16, family='Manrope'),
    legend=dict(orientation='h', y=1.12),
    hovermode='x unified', 
    margin=dict(t=50, b=30, l=10, r=10),
    **PLOTLY_THEME
)
st.plotly_chart(fig_mc, use_container_width=True)

# ── Rep-Level Impact Table ────────────────────────────────────────
st.markdown("### 👥 Rep-Level Impact Analysis")

impact = (sim.groupby(['name','region','product_line']).agg(
    base_comm=('commission_earned','sum'), sim_comm=('sim_comm','sum'),
    base_pay=('total_payout','sum'), sim_pay=('sim_pay','sum'),
    avg_att=('attainment_pct_display','mean'),
).reset_index())
impact['delta'] = impact['sim_comm'] - impact['base_comm']
impact['pct_chg'] = ((impact['sim_pay']-impact['base_pay'])/impact['base_pay']*100).round(1)
impact = impact.sort_values('delta', ascending=False)

st.dataframe(
    impact.style
    .background_gradient(subset=['avg_att'], cmap='Purples' if st.session_state.theme == 'dark' else 'RdYlGn', vmin=50, vmax=130)
    .format({'base_comm':'₹{:,.0f}','sim_comm':'₹{:,.0f}',
             'base_pay':'₹{:,.0f}','sim_pay':'₹{:,.0f}',
             'delta':'₹{:,.0f}','avg_att':'{:.1f}%','pct_chg':'{:+.1f}%'}),
    use_container_width=True, height=400,
)