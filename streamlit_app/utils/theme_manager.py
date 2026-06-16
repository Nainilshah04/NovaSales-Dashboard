"""
Theme Manager for NovaSales Dashboard.
Handles Light/Dark Mode styles using CSS variables, custom overrides, and dynamic Lucide SVG icons.
"""
import streamlit as st
import textwrap

def init_theme():
    """Initializes the theme state in session_state if not already present."""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # Default to premium Dark Glassmorphic

def get_theme():
    """Returns the current active theme."""
    init_theme()
    return st.session_state.theme

def render_theme_toggle():
    """Renders the theme toggle in the sidebar and handles state changes."""
    init_theme()
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Render header using Lucide icon instead of emoji
    st_html(f"<h3>{lucide_icon('palette', size=20, color='var(--accent-primary)')} Customize Interface</h3>")
    
    # Toggle switch dynamic label
    theme_label = "🌙 Dark Mode" if st.session_state.theme == 'dark' else "☀️ Light Mode"
    is_dark = st.sidebar.toggle(theme_label, value=(st.session_state.theme == 'dark'))
    
    new_theme = 'dark' if is_dark else 'light'
    
    # Rerun only if the theme changes
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

def lucide_icon(icon_name, size=24, color="var(--accent-primary)", extra_style=""):
    """Returns raw HTML for rendering a Lucide icon dynamically using CSS mask-image."""
    return f"""<span class="lucide-icon" style="width: {size}px; height: {size}px; background-color: {color}; -webkit-mask-image: url('https://api.iconify.design/lucide:{icon_name}.svg'); mask-image: url('https://api.iconify.design/lucide:{icon_name}.svg'); {extra_style}"></span>"""

def st_html(html_content):
    """Renders HTML in Streamlit after dedenting it to prevent markdown code block formatting."""
    st.markdown(textwrap.dedent(html_content), unsafe_allow_html=True)

def inject_theme_css():
    """Injects the CSS variables and Streamlit overrides based on the active theme."""
    theme = get_theme()
    
    if theme == 'dark':
        css_vars = """
        --bg-color: #0A0516;
        --text-color: #F8FAFC;
        --muted-text: #94A3B8;
        
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-bg-solid: #130D26;
        --card-border: 1px solid rgba(167, 139, 250, 0.15);
        --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        
        --accent-primary: #A78BFA;
        --accent-hover: #C4B5FD;
        --accent-light: rgba(167, 139, 250, 0.08);
        
        --sidebar-bg: #0B071E;
        --sidebar-border: 1px solid rgba(167, 139, 250, 0.1);
        
        --input-bg: rgba(255, 255, 255, 0.02);
        --input-border: rgba(167, 139, 250, 0.2);
        
        --success: #34D399;
        --warning: #FBBF24;
        --danger: #F87171;
        --success-bg: rgba(52, 211, 153, 0.1);
        --danger-bg: rgba(248, 113, 113, 0.1);
        
        --chart-grid: rgba(255, 255, 255, 0.05);
        """
    else:
        css_vars = """
        --bg-color: #F8FAFC;
        --text-color: #0F172A;
        --muted-text: #475569;
        
        --card-bg: #FFFFFF;
        --card-bg-solid: #FFFFFF;
        --card-border: 1px solid #E2E8F0;
        --card-shadow: 0 10px 25px -5px rgba(109, 40, 217, 0.05), 0 8px 10px -6px rgba(109, 40, 217, 0.05);
        
        --accent-primary: #6D28D9;
        --accent-hover: #5B21B6;
        --accent-light: #F5F3FF;
        
        --sidebar-bg: #FAFAFC;
        --sidebar-border: 1px solid #E9E5F5;
        
        --input-bg: #FFFFFF;
        --input-border: #E2E8F0;
        
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --success-bg: #E6F4EA;
        --danger-bg: #FCE8E6;
        
        --chart-grid: #E2E8F0;
        """
        
    full_css = f"""
    <style>
    :root {{
        {textwrap.dedent(css_vars)}
    }}
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Apply Font and Core Theme Colors */
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', sans-serif !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        transition: background-color 0.2s ease, color 0.2s ease;
    }}
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: var(--sidebar-border) !important;
        transition: background-color 0.2s ease, border 0.2s ease;
    }}
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: var(--text-color) !important;
    }}
    
    /* Hide default Streamlit header bar to keep it clean */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    #MainMenu, footer {{ visibility: hidden; }}
    
    /* Inputs / Selectboxes */
    .stSelectbox > div > div {{
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        color: var(--text-color) !important;
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }}
    .stSelectbox > div > div:hover {{
        border-color: var(--accent-primary) !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover)) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: var(--card-shadow) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(109, 40, 217, 0.3) !important;
    }}
    .stButton > button:active {{
        transform: translateY(0px) !important;
    }}
    
    /* Native Metric Override - Dark Mode compliant */
    [data-testid="stMetric"] {{
        background-color: var(--card-bg-solid) !important;
        border: var(--card-border) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: var(--card-shadow) !important;
        backdrop-filter: blur(12px) !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricLabel"] > div {{
        color: var(--muted-text) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] > div {{
        color: var(--text-color) !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }}
    
    /* Slider Styling */
    div[data-testid="stSlider"] [data-baseweb="slider"] {{
        color: var(--accent-primary) !important;
    }}
    
    /* Markdown Text Colors */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color) !important;
        font-weight: 800 !important;
    }}
    p, span, label {{
        color: var(--text-color);
    }}
    
    /* Expander Container overrides */
    div[data-testid="stExpander"] {{
        background-color: var(--card-bg-solid) !important;
        border: var(--card-border) !important;
        border-radius: 12px !important;
        box-shadow: var(--card-shadow) !important;
    }}
    
    /* Custom Card CSS Helper Class for html injections */
    .custom-card {{
        background-color: var(--card-bg-solid) !important;
        border: var(--card-border) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--card-shadow);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }}
    .custom-card:hover {{
        transform: translateY(-4px);
    }}
    
    /* Lucide Dynamic Icon CSS Styling */
    .lucide-icon {{
        display: inline-block;
        background-color: var(--accent-primary);
        -webkit-mask-size: contain;
        mask-size: contain;
        -webkit-mask-repeat: no-repeat;
        mask-repeat: no-repeat;
        -webkit-mask-position: center;
        mask-position: center;
        vertical-align: middle;
        margin-right: 8px;
    }}
    </style>
    """
    
    st.markdown(textwrap.dedent(full_css), unsafe_allow_html=True)
