"""
NovaSales - Landing Page (Forma.ai Style)
"""
import streamlit as st

st.set_page_config(
    page_title="NovaSales | Sales Compensation Analytics",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
.stApp { background: #FFFFFF; color: #1A0B2E; }
[data-testid="stSidebar"] { background: #FAFAFC; border-right: 1px solid #E9E5F5; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; font-weight:800 !important; color:#1A0B2E !important; }
#MainMenu, footer, header { visibility: hidden; }

.stButton > button {
    background: #6D28D9 !important; color: white !important;
    border: none !important; border-radius: 30px !important;
    padding: 12px 28px !important; font-weight: 600 !important;
}
.stButton > button:hover {
    background: #5B21B6 !important;
    box-shadow: 0 8px 20px rgba(109,40,217,0.3) !important;
}
.stSelectbox > div > div {
    background: #F5F3FF !important; border: 1px solid #E9E5F5 !important;
    border-radius: 10px !important;
}
[data-testid="stMetric"] {
    background: #F5F3FF; border: 1px solid #E9E5F5;
    border-radius: 14px; padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💜 NOVASALES")
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

# ── Top Banner ───────────────────────────────────────────────────
st.markdown("""
<div style="background:#1A0B2E; color:white; padding:12px 20px;
            text-align:center; font-size:14px; font-weight:500;
            border-radius:0 0 12px 12px; margin-bottom:30px;">
    🔥 <strong>NovaSales Analytics 2024</strong> — Real-time sales compensation insights
</div>
""", unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────────
left, right = st.columns([3, 2])

with left:
    st.markdown("""
    <div style="background:#F5F3FF; display:inline-block; padding:8px 16px;
                border-radius:20px; border:1px solid #E9E5F5; margin-bottom:20px;">
        <span style="color:#6D28D9; font-weight:600; font-size:13px;">
            ✨ AI-Powered Analytics Platform
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="font-size:52px; font-weight:800; line-height:1.1;
               letter-spacing:-0.03em; margin:20px 0;">
        Optimize sales
        <span style="color:#6D28D9;">compensation</span><br>
        with data-driven
        <span style="color:#6D28D9;">insights</span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:17px; color:#64748B; line-height:1.7; max-width:550px;">
        NovaSales is a comprehensive sales compensation analytics platform
        combining intelligent commission engines, real-time performance tracking,
        and what-if scenario modeling — enabling finance teams to make
        data-driven decisions at scale.
    </p>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#F5F3FF,#FAFAFC);
                border:1px solid #E9E5F5; border-radius:20px;
                padding:30px; margin-top:40px;">
        <div style="font-size:18px; font-weight:700; color:#1A0B2E;
                    margin-bottom:5px;">
            💜 Quota Performance
        </div>
        <div style="font-size:12px; color:#64748B; margin-bottom:20px;">Live Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bars using Streamlit native
    st.markdown("**Total Payout**")
    st.progress(78, text="₹1.2Cr")

    st.markdown("**Quota Hit Rate**")
    st.progress(68, text="68%")

    st.markdown("**Top Performers**")
    st.progress(90, text="8 Reps")

# ── Tech Stack Strip ─────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#6D28D9,#8B5CF6);
            padding:30px; border-radius:16px; text-align:center; margin:40px 0;">
    <div style="color:white; font-size:14px; font-weight:600;
                letter-spacing:0.1em; margin-bottom:15px;">
        POWERED BY MODERN DATA STACK
    </div>
    <div style="color:white; font-size:18px; font-weight:700;
                display:flex; justify-content:space-around;">
        <span>PYTHON</span><span>PANDAS</span><span>PLOTLY</span>
        <span>SQLITE</span><span>STREAMLIT</span><span>POWER BI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Features Section ─────────────────────────────────────────────
st.markdown("""
<h1 style="text-align:center; font-size:42px; font-weight:800; margin:50px 0 10px 0;">
    A complete <span style="color:#6D28D9;">sales compensation</span><br>
    analytics platform
</h1>
<p style="text-align:center; font-size:16px; color:#64748B; margin-bottom:40px;">
    NovaSales unifies all aspects of sales performance management.
</p>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

features = [
    ("📊", "Executive Overview", "Real-time KPIs, top performers, monthly payout trends."),
    ("👤", "Rep Drilldown", "Individual rep gauges, peer comparisons, commission details."),
    ("🗺️", "Regional Insights", "Geographic heatmaps, product line analysis by region."),
    ("⚙️", "What-If Simulator", "Adjust commission slabs, see instant payout impact."),
]

for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(f"""
        <div style="background:#F5F3FF; border:1px solid #E9E5F5;
                    border-radius:16px; padding:25px; height:220px;">
            <div style="width:44px; height:44px; background:linear-gradient(135deg,#6D28D9,#8B5CF6);
                        border-radius:10px; display:flex; align-items:center;
                        justify-content:center; font-size:22px; color:white;
                        margin-bottom:15px;">{icon}</div>
            <div style="width:30px; height:2px; background:#6D28D9; margin:12px 0;"></div>
            <div style="font-size:18px; font-weight:700; color:#1A0B2E;
                        margin-bottom:10px;">{title}</div>
            <div style="font-size:13px; color:#64748B; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)
stats = [("80", "Sales Reps"), ("960", "Records"), ("₹13.2Cr", "Total Payouts"), ("18+", "DAX Measures")]

for col, (num, label) in zip([q1, q2, q3, q4], stats):
    with col:
        st.markdown(f"""
        <div style="background:white; border:1px solid #E9E5F5;
                    border-radius:16px; padding:30px; text-align:center;">
            <div style="font-size:42px; font-weight:800; color:#6D28D9;">{num}</div>
            <div style="font-size:12px; color:#64748B; text-transform:uppercase;
                        letter-spacing:0.1em; font-weight:600; margin-top:10px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ── CTA Footer ────────────────────────────────────────────────────
# ── CTA Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A0B2E,#2D1B4E);
            margin:50px 0 30px 0; padding:60px; border-radius:24px; text-align:center;
            box-shadow: 0 15px 50px rgba(109,40,217,0.2);">
    <div style="color:#FFFFFF; font-size:42px; font-weight:800;
                letter-spacing:-0.02em;">
        Ready to explore the <span style="color:#A78BFA;">dashboard?</span>
    </div>
    <div style="color:#C4B5FD; font-size:16px; margin:18px 0 0 0;">
        ← Use the sidebar to navigate all 5 analytics pages
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#64748B; font-size:12px;">
    Built with 💜 | Portfolio Project | NovaSales Pvt Ltd © 2024
</p>
""", unsafe_allow_html=True)