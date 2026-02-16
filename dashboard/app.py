import streamlit as st
import pandas as pd
from datetime import datetime

# Import Custom Modules
from utils import ui, data_loader, charts, insights

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Reddit Insight | Intelligence Platform",
    page_icon="https://www.iconpacks.net/icons/2/free-reddit-logo-icon-2436-thumb.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Initialize UI & Data
# -------------------------------
ui.load_css()
df = data_loader.load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
with st.sidebar:
    st.image("https://www.iconpacks.net/icons/2/free-reddit-logo-icon-2436-thumb.png", width=70) # Updated logo
    st.markdown("## 🎛 Dashboard Filters")
    
    if not df.empty:
        # Subreddit Filter
        all_subs = sorted(df['subreddit'].unique())
        selected_subs = st.multiselect("Select Subreddits", all_subs, default=all_subs[:5])
        
        # Date Filter
        if 'created_utc' in df.columns:
            # Convert to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(df['created_utc']):
                df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
            min_date = pd.Timestamp(df['created_utc'].min()).date()
            max_date = pd.Timestamp(df['created_utc'].max()).date()
            date_range = st.date_input("Date Range", [min_date, max_date])
        
        # Min Posts Slider
        min_posts = st.slider("Minimum Posts", 0, 100, 0)
        
        if st.button("Reset Filters"):
            st.rerun()
            
        # Apply Filters
        filtered_df = df[df['subreddit'].isin(selected_subs)]
        if 'created_utc' in df.columns and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['created_utc'].dt.date >= date_range[0]) &
                (filtered_df['created_utc'].dt.date <= date_range[1])
            ]
    else:
        st.warning("No data loaded. Check MinIO connection.")
        filtered_df = pd.DataFrame()

# -------------------------------
# Main Content
# -------------------------------

# Header
st.markdown('<h1 class="gradient-text">Reddit Insight Intelligence Platform</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Subreddit Analytics powered by Scalable Data Engineering")
st.markdown("---")

if filtered_df.empty:
    st.info("Waiting for data ingestion... Please start the pipeline.")
    st.stop()

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)
with c1: ui.render_kpi_card("Total Posts", f"{len(filtered_df):,}", "📄")
with c2: ui.render_kpi_card("Unique Subreddits", f"{filtered_df['subreddit'].nunique()}", "🧠")
with c3: 
    active_sub = filtered_df['subreddit'].mode()[0] if not filtered_df.empty else "N/A"
    ui.render_kpi_card("Most Active", f"r/{active_sub}", "🔥")
with c4: 
    avg_posts = len(filtered_df) / filtered_df['subreddit'].nunique() if not filtered_df.empty else 0
    ui.render_kpi_card("Avg Posts/Sub", f"{avg_posts:.1f}", "📊")
with c5: ui.render_kpi_card("Data Freshness", datetime.now().strftime("%H:%M"), "⏱")

st.markdown("---")

# Charts Layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.plotly_chart(charts.chart_posts_over_time(filtered_df))
    st.plotly_chart(charts.chart_posts_per_subreddit(filtered_df))

with col_right:
    st.plotly_chart(charts.chart_subreddit_distribution(filtered_df))
    st.plotly_chart(charts.chart_top_active(filtered_df))

# Insights Panel
st.markdown("### 🧠 Automated Insights")
insight_list = insights.generate_insights(filtered_df)

for i, insight in enumerate(insight_list):
    st.info(insight)

# Data Explorer
with st.expander("📂 Data Explorer & Export"):
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download CSV",
        csv,
        "reddit_analysis.csv",
        "text/csv",
        key='download-csv'
    )
