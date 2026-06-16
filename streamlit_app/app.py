"""
NovaSales - Landing Page (Forma.ai Style)
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle, lucide_icon

st.set_page_config(
    page_title="NovaSales | Sales Compensation Analytics",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Dynamic Theme CSS ─────────────────────────────────────
inject_theme_css()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2>{lucide_icon('activity', size=28)} NOVASALES</h2>", unsafe_allow_html=True)
    st.caption("COMPENSATION ANALYTICS")
    st.markdown("---")
    st.markdown("**ABOUT NOVASALES**")
    st.info("""
    **B2B SaaS Company**
    - 80 Sales Reps
    - 4 Regions (N/S/E/W)
    - 3 Product Lines
    - FY 2024 Data
    - 960 Records
    """)
    
    # Theme toggle goes in sidebar
    render_theme_toggle()

# ── Top Banner ───────────────────────────────────────────────────
st.markdown(f"""
<div style="background:var(--card-bg-solid); color:var(--text-color); padding:12px 20px;
            text-align:center; font-size:14px; font-weight:600;
            border-bottom: var(--card-border);
            border-radius:0 0 12px 12px; margin-bottom:30px;
            box-shadow: var(--card-shadow);
            display: flex; align-items: center; justify-content: center;">
    {lucide_icon('flame', size=18, color='var(--warning)', extra_style='margin-right:8px;')}
    <span><strong>NovaSales Analytics 2024</strong> — Real-time sales compensation insights</span>
</div>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────
left, right = st.columns([3, 2])

with left:
    st.markdown(f"""
    <div style="background:var(--accent-light); display:inline-block; padding:8px 16px;
                border-radius:20px; border:var(--card-border); margin-bottom:20px;
                display: inline-flex; align-items: center;">
        {lucide_icon('sparkles', size=16, color='var(--accent-primary)', extra_style='margin-right:8px;')}
        <span style="color:var(--accent-primary); font-weight:700; font-size:13px;">
            AI-Powered Analytics Platform
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="font-size:52px; font-weight:800; line-height:1.1;
               letter-spacing:-0.03em; margin:20px 0;">
        Optimize sales
        <span style="color:var(--accent-primary);">compensation</span><br>
        with data-driven
        <span style="color:var(--accent-primary);">insights</span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:17px; color:var(--muted-text); line-height:1.7; max-width:550px;">
        NovaSales is a comprehensive sales compensation analytics platform
        combining intelligent commission engines, real-time performance tracking,
        and what-if scenario modeling — enabling finance teams to make
        data-driven decisions at scale.
    </p>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, var(--card-bg), var(--accent-light));
                border:var(--card-border); border-radius:20px;
                padding:30px; margin-top:20px; box-shadow:var(--card-shadow);
                backdrop-filter: blur(12px);">
        <div style="font-size:18px; font-weight:700; color:var(--text-color);
                    margin-bottom:5px; display:flex; align-items:center;">
            {lucide_icon('trending-up', size=22, color='var(--accent-primary)', extra_style='margin-right:8px;')}
            <span>Quota Performance</span>
        </div>
        <div style="font-size:12px; color:var(--muted-text); margin-bottom:20px;">Live Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bars using Streamlit native inside the right block
    st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
    st.markdown("<b style='color:var(--text-color);'>Total Payout</b>", unsafe_allow_html=True)
    st.progress(78, text="₹1.2Cr")

    st.markdown("<b style='color:var(--text-color);'>Quota Hit Rate</b>", unsafe_allow_html=True)
    st.progress(68, text="68%")

    st.markdown("<b style='color:var(--text-color);'>Top Performers</b>", unsafe_allow_html=True)
    st.progress(90, text="8 Reps")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Tech Stack Strip ─────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
            padding:30px; border-radius:16px; text-align:center; margin:40px 0;
            box-shadow: var(--card-shadow);">
    <div style="color:white; font-size:14px; font-weight:600;
                letter-spacing:0.1em; margin-bottom:15px;">
        POWERED BY MODERN DATA STACK
    </div>
    <div style="color:white; font-size:18px; font-weight:700;
                display:flex; justify-content:space-around; flex-wrap:wrap; gap:10px;">
        <span>PYTHON</span><span>PANDAS</span><span>PLOTLY</span>
        <span>SQLITE</span><span>STREAMLIT</span><span>POWER BI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Features Section ─────────────────────────────────────────────
st.markdown("""
<h1 style="text-align:center; font-size:42px; font-weight:800; margin:50px 0 10px 0;">
    A complete <span style="color:var(--accent-primary);">sales compensation</span><br>
    analytics platform
</h1>
<p style="text-align:center; font-size:16px; color:var(--muted-text); margin-bottom:40px;">
    NovaSales unifies all aspects of sales performance management.
</p>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

features = [
    ("layout-dashboard", "Executive Overview", "Real-time KPIs, top performers, monthly payout trends."),
    ("user", "Rep Drilldown", "Individual rep gauges, peer comparisons, commission details."),
    ("globe", "Regional Insights", "Geographic heatmaps, product line analysis by region."),
    ("sliders", "What-If Simulator", "Adjust commission slabs, see instant payout impact."),
]

for col, (icon_name, title, desc) in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(f"""
        <div class="custom-card" style="height:220px;">
            <div style="width:44px; height:44px; background:linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
                        border-radius:10px; display:flex; align-items:center;
                        justify-content:center; margin-bottom:15px;">
                {lucide_icon(icon_name, size=24, color='white', extra_style='margin-right:0px;')}
            </div>
            <div style="width:30px; height:2px; background:var(--accent-primary); margin:12px 0;"></div>
            <div style="font-size:18px; font-weight:700; color:var(--text-color);
                        margin-bottom:10px;">{title}</div>
            <div style="font-size:13px; color:var(--muted-text); line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)
stats = [("80", "Sales Reps"), ("960", "Records"), ("₹13.2Cr", "Total Payouts"), ("18+", "DAX Measures")]

for col, (num, label) in zip([q1, q2, q3, q4], stats):
    with col:
        st.markdown(f"""
        <div class="custom-card" style="text-align:center;">
            <div style="font-size:42px; font-weight:800; color:var(--accent-primary);">{num}</div>
            <div style="font-size:12px; color:var(--muted-text); text-transform:uppercase;
                        letter-spacing:0.1em; font-weight:600; margin-top:10px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ── CTA Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            margin:50px 0 30px 0; padding:60px; border-radius:24px; text-align:center;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);">
    <div style="color:var(--text-color); font-size:42px; font-weight:800;
                letter-spacing:-0.02em;">
        Ready to explore the <span style="color:var(--accent-primary);">dashboard?</span>
    </div>
    <div style="color:var(--muted-text); font-size:16px; margin:18px 0 0 0;">
        ← Use the sidebar to navigate all 5 analytics pages
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<p style="text-align:center; color:var(--muted-text); font-size:12px; display:flex; align-items:center; justify-content:center;">
    Built with {lucide_icon('heart', size=12, color='var(--accent-primary)')} | Portfolio Project | NovaSales Pvt Ltd © 2024
</p>
""", unsafe_allow_html=True)