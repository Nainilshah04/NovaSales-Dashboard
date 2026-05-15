"""
Page 3: Regional Analysis - Forma.ai Purple Theme
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data

st.set_page_config(page_title="Regional Analysis", page_icon="🗺️", layout="wide")

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

st.markdown("""
<div style="background:linear-gradient(135deg,#1A0B2E,#2D1B4E);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: 0 10px 40px rgba(109,40,217,0.15);">
    <div style="color:#FFFFFF; font-size:38px; font-weight:800;
                letter-spacing:-0.02em; line-height:1.2;">
        🗺️ Regional <span style="color:#A78BFA;">Analysis</span>
    </div>
    <div style="color:#C4B5FD; font-size:15px; margin-top:10px; font-weight:500;">
        Geographic performance across all NovaSales regions
    </div>
</div>
""", unsafe_allow_html=True)

# ── Region Stats ──────────────────────────────────────────────────
rs = (df.groupby('region').agg(
    avg_att=('attainment_pct_display','mean'),
    total_pay=('total_payout','sum'),
    reps=('rep_id','nunique'),
    deals=('deals_closed','sum'),
    above=('attainment_pct', lambda x: (x>=1.0).sum()),
    total=('rep_id','count'),
).reset_index())
rs['hit_rate'] = (rs['above'] / rs['total'] * 100).round(1)

best = rs.loc[rs['avg_att'].idxmax()]
worst = rs.loc[rs['avg_att'].idxmin()]

# ── Best / Worst Cards ────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div style="background:#F0FDF4; border:2px solid #86EFAC;
                border-radius:16px; padding:25px; text-align:center;">
        <div style="font-size:30px;">🏆</div>
        <div style="font-size:20px; font-weight:700; color:#10B981; margin:8px 0;">
            {best['region']} — Best Region
        </div>
        <div style="font-size:32px; font-weight:800; color:#1A0B2E;">
            {best['avg_att']:.1f}% Attainment
        </div>
        <div style="color:#64748B; font-size:13px; margin-top:8px;">
            {int(best['reps'])} reps • {best['hit_rate']:.0f}% quota hit •
            ₹{best['total_pay']/1000000:.1f}M payout
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background:#FEF2F2; border:2px solid #FCA5A5;
                border-radius:16px; padding:25px; text-align:center;">
        <div style="font-size:30px;">📉</div>
        <div style="font-size:20px; font-weight:700; color:#EF4444; margin:8px 0;">
            {worst['region']} — Needs Attention
        </div>
        <div style="font-size:32px; font-weight:800; color:#1A0B2E;">
            {worst['avg_att']:.1f}% Attainment
        </div>
        <div style="color:#64748B; font-size:13px; margin-top:8px;">
            {int(worst['reps'])} reps • {worst['hit_rate']:.0f}% quota hit •
            ₹{worst['total_pay']/1000000:.1f}M payout
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Region KPIs ───────────────────────────────────────────────────
rcols = st.columns(4)
colors = ['#6D28D9', '#8B5CF6', '#A78BFA', '#C4B5FD']
for i, (_, row) in enumerate(rs.iterrows()):
    with rcols[i]:
        st.metric(f"🗺️ {row['region']}", f"{row['avg_att']:.1f}%",
                  f"₹{row['total_pay']/1000000:.1f}M • {int(row['reps'])} reps")

st.markdown("<br>", unsafe_allow_html=True)

# ── Heatmap ───────────────────────────────────────────────────────
st.markdown("### 🌡️ Region × Month Heatmap")

pivot = (df.groupby(['region','month_label','month'])['attainment_pct_display']
         .mean().reset_index().sort_values('month')
         .pivot(index='region', columns='month_label', values='attainment_pct_display'))

month_order = [f'{m} 2024' for m in ['Jan','Feb','Mar','Apr','May','Jun',
                                       'Jul','Aug','Sep','Oct','Nov','Dec']]
pivot = pivot.reindex(columns=[c for c in month_order if c in pivot.columns])

fig_h = go.Figure(go.Heatmap(
    z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
    colorscale=[[0,'#FCA5A5'],[0.33,'#FCD34D'],[0.66,'#86EFAC'],[1,'#6D28D9']],
    zmin=50, zmax=130,
    text=pivot.values.round(1), texttemplate='%{text}%', textfont=dict(size=11),
    colorbar=dict(title='Attainment %', ticksuffix='%'),
))
fig_h.update_layout(title='<b>Quota Attainment Heatmap</b>', height=300, **PURPLE_THEME)
st.plotly_chart(fig_h, use_container_width=True)

# ── Product Performance ───────────────────────────────────────────
st.markdown("### 📦 Product Line by Region")

p1, p2 = st.columns([3, 2])

with p1:
    agg = (df.groupby(['region','product_line'])['attainment_pct_display']
           .mean().reset_index())
    fig_pb = px.bar(agg, x='region', y='attainment_pct_display',
                     color='product_line', barmode='group',
                     color_discrete_map={'CloudCore':'#6D28D9',
                                          'DataSync':'#A78BFA',
                                          'SecureAPI':'#DDD6FE'},
                     title='<b>Product Performance by Region</b>')
    fig_pb.add_hline(y=100, line_dash='dash', line_color='#6D28D9')
    fig_pb.update_layout(**PURPLE_THEME)
    st.plotly_chart(fig_pb, use_container_width=True)

with p2:
    region_sel = st.selectbox("🗺️ Region", sorted(df['region'].unique()))
    prod_df = (df[df['region']==region_sel].groupby('product_line')
               .agg(total=('actual_sales','sum')).reset_index())
    fig_pie = go.Figure(go.Pie(
        labels=prod_df['product_line'], values=prod_df['total'],
        hole=0.5, marker=dict(colors=['#6D28D9','#A78BFA','#DDD6FE']),
    ))
    fig_pie.update_layout(title=f'<b>Revenue — {region_sel}</b>',
                           paper_bgcolor='white', height=350,
                           font=dict(color='#1A0B2E', family='Manrope'))
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Monthly Region Trend ──────────────────────────────────────────
st.markdown("### 📈 Monthly Trend by Region")
mr = (df.groupby(['region','month','month_label'])['attainment_pct_display']
      .mean().reset_index().sort_values('month'))

fig_mt = go.Figure()
for region, color in zip(['North','South','East','West'], colors):
    rd = mr[mr['region'] == region]
    fig_mt.add_trace(go.Scatter(
        x=rd['month_label'], y=rd['attainment_pct_display'],
        name=region, mode='lines+markers',
        line=dict(color=color, width=2.5), marker=dict(size=7),
    ))
fig_mt.add_hline(y=100, line_dash='dash', line_color='#6D28D9', annotation_text='Quota')
fig_mt.update_layout(title='<b>Regional Trends — FY 2024</b>',
                      legend=dict(orientation='h', y=1.1),
                      hovermode='x unified', **PURPLE_THEME)
st.plotly_chart(fig_mt, use_container_width=True)