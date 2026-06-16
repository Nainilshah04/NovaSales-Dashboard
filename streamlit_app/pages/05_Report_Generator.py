"""
Page 5: Report Generator - Dynamic Theme
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data, get_month_options
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle, lucide_icon

st.set_page_config(page_title="Report Generator", page_icon="📋", layout="wide")

# ── CSS & Theme ──────────────────────────────────────────────────
inject_theme_css()

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    render_theme_toggle()

# ── Header ────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);
            display: flex; align-items: center;">
    <div style="margin-right:20px;">
        {lucide_icon('file-text', size=42, color='var(--accent-primary)')}
    </div>
    <div>
        <div style="color:var(--text-color); font-size:38px; font-weight:800;
                    letter-spacing:-0.02em; line-height:1.2;">
            Report <span style="color:var(--accent-primary);">Generator</span>
        </div>
        <div style="color:var(--muted-text); font-size:15px; margin-top:10px; font-weight:500;">
            Auto-generate compensation reports. Export to Excel.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Parameters ────────────────────────────────────────────────────
p1, p2, p3 = st.columns(3)
with p1:
    mo = get_month_options(df)
    sel_month = st.selectbox("📅 Month", mo, index=len(mo)-1)
with p2:
    sel_reg = st.selectbox("🗺️ Region", ['All Regions'] + sorted(df['region'].unique().tolist()))
with p3:
    sel_prod = st.selectbox("📦 Product", ['All Products'] + sorted(df['product_line'].unique().tolist()))

rdf = df[df['month_label'] == sel_month].copy()
if sel_reg != 'All Regions': rdf = rdf[rdf['region'] == sel_reg]
if sel_prod != 'All Products': rdf = rdf[rdf['product_line'] == sel_prod]

if len(rdf) == 0:
    st.warning("No data found matching current filter choices.")
    st.stop()

total_reps = len(rdf)
above = (rdf['attainment_pct']>=1.0).sum()
at_risk = (rdf['attainment_pct']<0.60).sum()
avg_att = rdf['attainment_pct_display'].mean()
total_comm = rdf['commission_earned'].sum()
total_bonus = rdf['bonus_earned'].sum()
total_pay = rdf['total_payout'].sum()
total_sales = rdf['actual_sales'].sum()
total_target = rdf['monthly_target'].sum()
oa = (total_sales/total_target*100) if total_target>0 else 0

reg_disp = sel_reg if sel_reg!='All Regions' else 'All'

# ── Report Card Header ────────────────────────────────────────────
st.markdown(f"""
<div class="custom-card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
    <div>
        <div style="font-size:22px; font-weight:800; color:var(--accent-primary); display:flex; align-items:center;">
            {lucide_icon('file-text', size=24, color='var(--accent-primary)', extra_style='margin-right:8px;')}
            <span>NovaSales Compensation Report Summary</span>
        </div>
        <div style="color:var(--muted-text); margin-top:8px; font-size:14px;">
            Period: <strong>{sel_month}</strong> •
            Region: <strong>{reg_disp}</strong> •
            Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:36px; color:var(--accent-primary); font-weight:800; line-height:1;">{oa:.1f}%</div>
        <div style="color:var(--muted-text); font-size:13px; font-weight:600;">Team Attainment</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Summary KPIs ──────────────────────────────────────────────────
s1, s2, s3, s4, s5, s6 = st.columns(6)
s1.metric("Total Payout", f"₹{total_pay/100000:.1f}L")
s2.metric("Commission", f"₹{total_comm/100000:.1f}L")
s3.metric("Bonus", f"₹{total_bonus/1000:.0f}K")
s4.metric("Above Quota", f"{above}/{total_reps}")
s5.metric("Avg Attainment", f"{avg_att:.1f}%")
s6.metric("At-Risk", f"{at_risk} reps")

# ── Top / Risk Lists ──────────────────────────────────────────────
t_col, r_col = st.columns(2)

with t_col:
    st.markdown("### 🌟 Top Performers")
    top5 = rdf.nlargest(5, 'attainment_pct_display')
    medals = ['🥇','🥈','🥉','🏅','🏅']
    for i, (_, row) in enumerate(top5.iterrows()):
        st.markdown(f"""
        <div style="background:var(--card-bg); border:var(--card-border);
                    border-radius:12px; padding:12px 16px; margin:6px 0;
                    display:flex; justify-content:space-between; align-items:center;
                    box-shadow: var(--card-shadow);">
            <div>
                <span style="font-size:16px;">{medals[i]}</span>
                <strong style="color:var(--text-color);"> {row['name']}</strong>
                <span style="color:var(--muted-text); font-size:12px;"> • {row['region']}</span>
            </div>
            <span style="background:var(--accent-primary); color:white; padding:4px 12px;
                         border-radius:20px; font-weight:700; font-size:13px;">
                {row['attainment_pct_display']:.0f}%
            </span>
        </div>
        """, unsafe_allow_html=True)

with r_col:
    st.markdown("### ⚠️ At-Risk Reps")
    risk = rdf[rdf['attainment_pct_display']<60].nsmallest(5,'attainment_pct_display')
    if len(risk)==0:
        st.success("✅ No reps below 60% attainment this month!")
    else:
        for _, row in risk.iterrows():
            st.markdown(f"""
            <div style="background:var(--danger-bg); border:1px solid var(--danger);
                        border-left:3px solid var(--danger) !important;
                        border-radius:12px; padding:12px 16px; margin:6px 0;
                        display:flex; justify-content:space-between; align-items:center;
                        box-shadow: var(--card-shadow);">
                <div style="display:flex; align-items:center;">
                    {lucide_icon('alert-triangle', size=14, color='var(--danger)', extra_style='margin-right:8px;')}
                    <div>
                        <strong style="color:var(--text-color);">{row['name']}</strong>
                        <span style="color:var(--muted-text); font-size:12px;"> • {row['region']}</span>
                    </div>
                </div>
                <span style="background:var(--danger); color:white; padding:4px 12px;
                             border-radius:20px; font-weight:700; font-size:13px;">
                    {row['attainment_pct_display']:.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

# ── Full Ledger ───────────────────────────────────────────────────
st.markdown("### 📑 Commission Ledger")

ledger = rdf[['name','region','product_line','monthly_target','actual_sales',
              'deals_closed','attainment_pct_display','commission_rate',
              'commission_earned','bonus_earned','monthly_base','total_payout',
              'is_top_performer']].sort_values('attainment_pct_display', ascending=False).copy()
ledger.columns = ['Name','Region','Product','Quota','Sales','Deals','Attain %',
                   'Rate','Commission','Bonus','Base','Total Payout','Top']

st.dataframe(
    ledger.style
    .background_gradient(subset=['Attain %'], cmap='Purples' if st.session_state.theme == 'dark' else 'RdYlGn', vmin=50, vmax=130)
    .format({'Quota':'₹{:,.0f}','Sales':'₹{:,.0f}','Attain %':'{:.1f}%',
             'Rate':'{:.0%}','Commission':'₹{:,.0f}','Bonus':'₹{:,.0f}',
             'Base':'₹{:,.0f}','Total Payout':'₹{:,.0f}'}),
    use_container_width=True, height=400,
)

# ── Excel Export ──────────────────────────────────────────────────
st.markdown("### ⬇️ Download Report")

def gen_excel(rdf, ledger):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        # We can keep clean styles for the output excel file
        hdr = wb.add_format({'bold':True,'bg_color':'#6D28D9','font_color':'white','border':1})
        ttl = wb.add_format({'bold':True,'font_size':16,'font_color':'#6D28D9'})

        ws = wb.add_worksheet('Summary')
        ws.set_column('A:A', 30); ws.set_column('B:B', 25)
        ws.write('A1', 'NovaSales Report', ttl)
        ws.write('A2', f'Period: {sel_month} | Region: {reg_disp}')
        for i, (m, v) in enumerate([
            ('Total Payout', f'Rs.{total_pay:,.0f}'),
            ('Commission', f'Rs.{total_comm:,.0f}'),
            ('Bonus', f'Rs.{total_bonus:,.0f}'),
            ('Reps', total_reps), ('Above Quota', above),
            ('Avg Attainment', f'{avg_att:.1f}%'), ('At-Risk', at_risk),
        ], 4):
            ws.write(i, 0, m); ws.write(i, 1, v)

        ledger.to_excel(w, sheet_name='Ledger', index=False, startrow=1)
        ws2 = w.sheets['Ledger']
        ws2.write('A1', f'Ledger — {sel_month}', ttl)
        for c, col in enumerate(ledger.columns):
            ws2.write(1, c, col, hdr); ws2.set_column(c, c, 18)

        top10 = rdf.nlargest(10,'attainment_pct_display')[
            ['name','region','product_line','attainment_pct_display',
             'commission_earned','total_payout']]
        top10.to_excel(w, sheet_name='Top Performers', index=False, startrow=1)

        risk_df = rdf[rdf['attainment_pct_display']<60][
            ['name','region','attainment_pct_display','commission_earned']]
        risk_df.to_excel(w, sheet_name='At-Risk', index=False, startrow=1)

    return buf.getvalue()

excel = gen_excel(rdf, ledger)
fname = f"NovaSales_{sel_month.replace(' ','_')}.xlsx"

_, dl, _ = st.columns([1, 2, 1])
with dl:
    st.download_button(
        label="⬇️ Download Excel Report (.xlsx)",
        data=excel, file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True, type="primary",
    )