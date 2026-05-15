"""
Page 2: Rep Performance - Forma.ai Purple Theme
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data

st.set_page_config(page_title="Rep Performance", page_icon="👤", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
.stApp { background: #FFFFFF; color: #1A0B2E; }
[data-testid="stSidebar"] { background: #FAFAFC; border-right: 1px solid #E9E5F5; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; font-weight:800 !important; color:#1A0B2E !important; }
#MainMenu, footer, header { visibility: hidden; }
.stSelectbox > div > div { background:#F5F3FF !important; border:1px solid #E9E5F5 !important; border-radius:10px !important; }
</style>
""", unsafe_allow_html=True)

PURPLE_THEME = dict(
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#1A0B2E', family='Manrope'),
    xaxis=dict(gridcolor='#F5F3FF'), yaxis=dict(gridcolor='#F5F3FF'),
)

df = load_data()

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A0B2E,#2D1B4E);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: 0 10px 40px rgba(109,40,217,0.15);">
    <div style="color:#FFFFFF; font-size:38px; font-weight:800;
                letter-spacing:-0.02em; line-height:1.2;">
        👤 Rep Performance <span style="color:#A78BFA;">Drilldown</span>
    </div>
    <div style="color:#C4B5FD; font-size:15px; margin-top:10px; font-weight:500;">
        Deep-dive analytics for individual sales representatives
    </div>
</div>
""", unsafe_allow_html=True)

# ── Selector ──────────────────────────────────────────────────────
sel1, sel2 = st.columns([3, 5])
with sel1:
    selected_rep = st.selectbox("🔍 Select Rep", sorted(df['name'].unique().tolist()))

rep_df = df[df['name'] == selected_rep].sort_values('month')
info = rep_df.iloc[0]
avg_attain = rep_df['attainment_pct_display'].mean()
total_earnings = rep_df['commission_earned'].sum() + rep_df['bonus_earned'].sum()
best_month = rep_df.loc[rep_df['attainment_pct_display'].idxmax(), 'month_label']
top_months = rep_df['is_top_performer'].sum()

# ── Rep Profile ───────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#F5F3FF,#EDE9FE);
            border:1px solid #DDD6FE; border-radius:20px;
            padding:30px; margin-bottom:25px;
            display:flex; justify-content:space-between; align-items:center;">
    <div>
        <div style="font-size:26px; font-weight:800; color:#1A0B2E;">
            👤 {selected_rep}
        </div>
        <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
            <span style="background:white; border:1px solid #E9E5F5;
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:#64748B;">🗺️ {info['region']}</span>
            <span style="background:white; border:1px solid #E9E5F5;
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:#64748B;">📦 {info['product_line']}</span>
            <span style="background:white; border:1px solid #E9E5F5;
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:#64748B;">⏱️ {int(info['tenure_months'])} months</span>
            <span style="background:white; border:1px solid #E9E5F5;
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:#64748B;">💼 ₹{info['base_salary']/100000:.1f}L base</span>
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:42px; color:#6D28D9; font-weight:800;">{avg_attain:.0f}%</div>
        <div style="color:#64748B; font-size:13px;">Avg Attainment</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Variable Earnings", f"₹{total_earnings/1000:.0f}K")
k2.metric("📊 Total Sales", f"₹{rep_df['actual_sales'].sum()/100000:.1f}L")
k3.metric("🤝 Total Deals", f"{rep_df['deals_closed'].sum()}")
k4.metric("⭐ Best Month", best_month)

st.markdown("<br>", unsafe_allow_html=True)

# ── Gauge + Table ─────────────────────────────────────────────────
g_col, t_col = st.columns([1, 2])

with g_col:
    latest = rep_df.iloc[-1]['attainment_pct_display']
    color = '#EF4444' if latest < 60 else '#F59E0B' if latest < 85 else '#10B981'

    fig_g = go.Figure(go.Indicator(
        mode='gauge+number+delta', value=latest,
        delta={'reference': 100, 'suffix': '%'},
        title={'text': 'Latest Month Attainment', 'font': {'size': 14}},
        number={'suffix': '%', 'font': {'size': 32, 'color': '#1A0B2E'}},
        gauge={
            'axis': {'range': [0, 150], 'ticksuffix': '%'},
            'bar': {'color': color, 'thickness': 0.3},
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 80], 'color': '#FEF3C7'},
                {'range': [80, 100], 'color': '#D1FAE5'},
                {'range': [100, 150], 'color': '#EDE9FE'},
            ],
            'threshold': {'line': {'color': '#6D28D9', 'width': 3},
                          'thickness': 0.8, 'value': 100},
        }
    ))
    fig_g.update_layout(height=280, paper_bgcolor='white',
                         font=dict(color='#1A0B2E', family='Manrope'),
                         margin=dict(t=60, b=10, l=20, r=20))
    st.plotly_chart(fig_g, use_container_width=True)

with t_col:
    st.markdown("**📅 Monthly Performance**")
    show_df = rep_df[['month_label','monthly_target','actual_sales',
                       'attainment_pct_display','commission_earned',
                       'bonus_earned','deals_closed']].copy()
    show_df.columns = ['Month','Target','Actual','Attainment %',
                        'Commission','Bonus','Deals']
    st.dataframe(
        show_df.style
        .background_gradient(subset=['Attainment %'], cmap='RdYlGn', vmin=50, vmax=130)
        .format({'Target':'₹{:,.0f}','Actual':'₹{:,.0f}',
                 'Attainment %':'{:.1f}%','Commission':'₹{:,.0f}','Bonus':'₹{:,.0f}'}),
        use_container_width=True, height=300,
    )

# ── Charts ────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    rep_sorted = rep_df.sort_values('month')
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=rep_sorted['month_label'], y=rep_sorted['monthly_target'],
        name='Quota', marker_color='rgba(109,40,217,0.3)',
        marker_line_color='#6D28D9', marker_line_width=1.5,
    ))
    fig_bar.add_trace(go.Bar(
        x=rep_sorted['month_label'], y=rep_sorted['actual_sales'],
        name='Actual', marker_color='#6D28D9',
    ))
    fig_bar.update_layout(barmode='group', title='<b>Quota vs Actual Sales</b>',
                           legend=dict(orientation='h', y=1.12), **PURPLE_THEME)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=rep_sorted['month_label'], y=rep_sorted['commission_earned'],
        mode='lines+markers', name='Commission',
        line=dict(color='#6D28D9', width=3), marker=dict(size=8),
        fill='tozeroy', fillcolor='rgba(109,40,217,0.08)',
    ))
    fig_line.add_trace(go.Scatter(
        x=rep_sorted['month_label'], y=rep_sorted['bonus_earned'],
        mode='lines+markers', name='Bonus',
        line=dict(color='#A78BFA', width=2, dash='dot'), marker=dict(size=6),
    ))
    fig_line.update_layout(title='<b>Commission & Bonus Trend</b>',
                            hovermode='x unified', **PURPLE_THEME)
    st.plotly_chart(fig_line, use_container_width=True)

# ── Attainment Trend ──────────────────────────────────────────────
fig_at = go.Figure()
fig_at.add_trace(go.Scatter(
    x=rep_sorted['month_label'], y=rep_sorted['attainment_pct_display'],
    mode='lines+markers+text', line=dict(color='#6D28D9', width=3),
    marker=dict(size=10, color=rep_sorted['attainment_pct_display'].apply(
        lambda x: '#10B981' if x >= 100 else '#EF4444')),
    text=rep_sorted['attainment_pct_display'].apply(lambda x: f'{x:.0f}%'),
    textposition='top center', textfont=dict(size=10),
))
fig_at.add_hline(y=100, line_dash='dash', line_color='#6D28D9', annotation_text='Quota')
fig_at.add_hline(y=80, line_dash='dot', line_color='#EF4444', annotation_text='Warning')
fig_at.update_layout(title=f'<b>{selected_rep} — Attainment Trend</b>',
                      yaxis_range=[0, max(rep_sorted['attainment_pct_display'].max()+20, 140)],
                      **PURPLE_THEME)
st.plotly_chart(fig_at, use_container_width=True)

# ── Peer Comparison ───────────────────────────────────────────────
st.markdown("### 🔄 Peer Comparison")
peers = (
    df[(df['region']==info['region']) & (df['product_line']==info['product_line'])]
    .groupby('name').agg(avg_att=('attainment_pct_display','mean'))
    .reset_index().sort_values('avg_att', ascending=False)
)
peers['highlight'] = peers['name'] == selected_rep

fig_p = px.bar(peers, x='name', y='avg_att', color='highlight',
               color_discrete_map={True:'#6D28D9', False:'#E9E5F5'},
               title=f'<b>Peer Comparison — {info["region"]} | {info["product_line"]}</b>')
fig_p.add_hline(y=100, line_dash='dash', line_color='#6D28D9')
fig_p.update_layout(showlegend=False, xaxis_tickangle=-45, **PURPLE_THEME)
st.plotly_chart(fig_p, use_container_width=True)