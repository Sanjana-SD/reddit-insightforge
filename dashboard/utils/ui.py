import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* Modern Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
            color: #ffffff;
        }

        /* Glassmorphism Card Style */
        .kpi-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .kpi-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
            border-color: #FF4500; /* Reddit Orange */
            box-shadow: 0 8px 12px rgba(255, 69, 0, 0.2);
        }

        .kpi-title {
            font-size: 0.9rem;
            color: #bfbfbf;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 5px;
        }

        .kpi-icon {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        /* Animated Title Gradient */
        .gradient-text {
            background: linear-gradient(45deg, #FF4500, #FF8700, #FF4500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradient 5s ease infinite;
            font-weight: 800;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0e1117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #333; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555; 
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #111318;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, icon, color="#FF4500"):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)
