"""
Theme Manager for NovaSales Dashboard.
Handles Light/Dark Mode styles using CSS variables and provides the sidebar toggle widget.
"""
import streamlit as st

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
    st.sidebar.subheader("🎨 Customize Interface")
    
    # Toggle switch logic
    is_dark = st.sidebar.toggle("🌙 Dark Mode", value=(st.session_state.theme == 'dark'))
    
    new_theme = 'dark' if is_dark else 'light'
    
    # Rerun only if the theme changes
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

def inject_theme_css():
    """Injects the CSS variables and Streamlit overrides based on the active theme."""
    theme = get_theme()
    
    if theme == 'dark':
        css_vars = """
        :root {
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
        }
        """
    else:
        css_vars = """
        :root {
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
        }
        """
        
    common_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
    
    /* Apply Font and Core Theme Colors */
    html, body, [class*="css"], .stApp {
        font-family: 'Manrope', sans-serif !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: var(--sidebar-border) !important;
        transition: background-color 0.3s ease, border 0.3s ease;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--text-color) !important;
    }
    
    /* Hide default Streamlit header bar to keep it clean */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    #MainMenu, footer { visibility: hidden; }
    
    /* Inputs / Selectboxes */
    .stSelectbox > div > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        color: var(--text-color) !important;
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }
    .stSelectbox > div > div:hover {
        border-color: var(--accent-primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover)) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: var(--card-shadow) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(109, 40, 217, 0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Native Metric Override */
    [data-testid="stMetric"] {
        background-color: var(--card-bg) !important;
        border: var(--card-border) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: var(--card-shadow) !important;
        backdrop-filter: blur(12px);
    }
    
    /* Slider Styling */
    div[data-testid="stSlider"] [data-baseweb="slider"] {
        color: var(--accent-primary) !important;
    }
    
    /* Markdown Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
        font-weight: 800 !important;
    }
    p, span, label {
        color: var(--text-color);
    }
    
    /* Expander Container overrides */
    div[data-testid="stExpander"] {
        background-color: var(--card-bg) !important;
        border: var(--card-border) !important;
        border-radius: 12px !important;
        box-shadow: var(--card-shadow) !important;
    }
    
    /* Custom Card CSS Helper Class for html injections */
    .custom-card {
        background-color: var(--card-bg) !important;
        border: var(--card-border) !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--card-shadow);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }
    .custom-card:hover {
        transform: translateY(-4px);
    }
    </style>
    """
    
    st.markdown(css_vars, unsafe_allow_html=True)
    st.markdown(common_css, unsafe_allow_html=True)
