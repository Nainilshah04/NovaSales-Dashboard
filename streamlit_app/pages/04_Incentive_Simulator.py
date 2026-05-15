"""
Page 4: Incentive Simulator - Forma.ai Purple Theme
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data

st.set_page_config(page_title="Incentive Simulator", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
.stApp { background: #FFFFFF; color: #1A0B2E; }
[data-testid="stSidebar"] { background: #FAFAFC; border-right: 1px solid #E9E5F5; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; font-weight:800 !important; color:#1A0B2E !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

PURPLE_THEME = dict(
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#1A0B2E', family='Manrope'),
    xaxis=dict(gridcolor='#F5F3FF'), yaxis=dict(gridcolor='#F5F3FF'),
)

df = load_data()

st.markdown("""
<div style="background:linear-gradient(135deg,#1A0B2E,#2D1B4E);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: 0 10px 40px rgba(109,40,217,0.15);">
    <div style="color:#FFFFFF; font-size:38px; font-weight:800;
                letter-spacing:-0.02em; line-height:1.2;">
        ⚙️ Incentive Plan <span style="color:#A78BFA;">Simulator</span>
    </div>
    <div style="color:#C4B5FD; font-size:15px; margin-top:10px; font-weight:500;">
        What-if analysis — adjust slabs, see real-time payout impact
    </div>
</div>
""", unsafe_allow_html=True)

def calc_sim(row, slabs):
    att = row['attainment_pct']
    sales = row['actual_sales']
    if att <= 0.50: rate = slabs['s1'] / 100
    elif att <= 0.80: rate = slabs['s2'] / 100
    elif att <= 1.00: rate = slabs['s3'] / 100
    elif att <= 1.20: rate = slabs['s4'] / 100
    else: rate = slabs['s5'] / 100
    return sales * rate

st.markdown("### 🎛️ Configure Commission Slabs")

col_slab, col_result = st.columns([2, 3])

with col_slab:
    st.markdown("**Slab 1: 0-50% Attainment**")
    s1 = st.slider("Rate %", 0.0, 10.0, 0.0, 0.5, key='s1')
    st.markdown("**Slab 2: 51-80%**")
    s2 = st.slider("Rate %", 0.0, 15.0, 5.0, 0.5, key='s2')
    st.markdown("**Slab 3: 81-100%**")
    s3 = st.slider("Rate %", 0.0, 20.0, 10.0, 0.5, key='s3')
    st.markdown("**Slab 4: 101-120%**")
    s4 = st.slider("Rate %", 0.0, 25.0, 15.0, 0.5, key='s4')
    st.markdown("**Slab 5: 120%+ (Accelerator)**")
    s5 = st.slider("Rate %", 0.0, 35.0, 20.0, 0.5, key='s5')
    st.markdown("---")
    bonus = st.slider("Top Performer Bonus %", 0.0, 15.0, 5.0, 0.5)

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

with col_result:
    st.markdown("### 📊 Real-Time Impact")

    m1, m2, m3 = st.columns(3)
    m1.metric("Baseline Payout", f"₹{base_total/1000000:.2f}M")
    m2.metric("Simulated Payout", f"₹{sim_total/1000000:.2f}M",
              f"{'+' if pct>=0 else ''}{pct:.1f}%")
    m3.metric("Commission Δ", f"₹{comm_delta/1000:+,.0f}K")

    # Slab comparison
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(
        x=['0-50%','51-80%','81-100%','101-120%','120%+'],
        y=[0, 5, 10, 15, 20], name='Current',
        marker_color='rgba(109,40,217,0.3)',
    ))
    fig_s.add_trace(go.Bar(
        x=['0-50%','51-80%','81-100%','101-120%','120%+'],
        y=[s1, s2, s3, s4, s5], name='Simulated',
        marker_color='#6D28D9',
    ))
    fig_s.update_layout(barmode='group', title='<b>Slab Rates Comparison</b>',
                         yaxis_title='Rate (%)', height=300, **PURPLE_THEME)
    st.plotly_chart(fig_s, use_container_width=True)

# ── Monthly Comparison ────────────────────────────────────────────
st.markdown("### 📈 Monthly Payout: Current vs Simulated")

mc = (sim.groupby(['month','month_label'])
      .agg(sim_p=('sim_pay','sum'), base_p=('total_payout','sum'))
      .reset_index().sort_values('month'))

fig_mc = go.Figure()
fig_mc.add_trace(go.Scatter(
    x=mc['month_label'], y=mc['base_p'], name='Current',
    mode='lines+markers', line=dict(color='#A78BFA', width=2.5),
))
fig_mc.add_trace(go.Scatter(
    x=mc['month_label'], y=mc['sim_p'], name='Simulated',
    mode='lines+markers', line=dict(color='#6D28D9', width=3, dash='dash'),
    fill='tonexty', fillcolor='rgba(109,40,217,0.08)',
))
fig_mc.update_layout(title='<b>Monthly Payout Comparison</b>',
                      hovermode='x unified', **PURPLE_THEME)
st.plotly_chart(fig_mc, use_container_width=True)

# ── Impact Table ──────────────────────────────────────────────────
st.markdown("### 👥 Rep-Level Impact")

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
    .background_gradient(subset=['avg_att'], cmap='RdYlGn', vmin=50, vmax=130)
    .format({'base_comm':'₹{:,.0f}','sim_comm':'₹{:,.0f}',
             'base_pay':'₹{:,.0f}','sim_pay':'₹{:,.0f}',
             'delta':'₹{:,.0f}','avg_att':'{:.1f}%','pct_chg':'{:+.1f}%'}),
    use_container_width=True, height=400,
)