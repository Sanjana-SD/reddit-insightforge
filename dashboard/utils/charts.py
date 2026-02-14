import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
try:
    from wordcloud import WordCloud
    KEY_WORDCLOUD_AVAILABLE = True
except ImportError:
    KEY_WORDCLOUD_AVAILABLE = False
import matplotlib.pyplot as plt

# Reddit Color Palette
REDDIT_ORANGE = "#FF4500"
REDDIT_BLUE = "#5F99CF"
DARK_BG = "#0e1117"

def get_common_layout(title):
    """Returns a consistent Plotly layout"""
    return dict(
        title=title,
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Work Sans, sans-serif", color="#ffffff"),
        title_font=dict(size=20)
    )

def chart_posts_per_subreddit(df):
    counts = df['subreddit'].value_counts().reset_index()
    counts.columns = ['subreddit', 'count']
    
    fig = px.bar(
        counts, 
        x='subreddit', 
        y='count',
        color='count',
        color_continuous_scale=[REDDIT_BLUE, REDDIT_ORANGE],
        labels={'count': 'Posts', 'subreddit': 'Subreddit'}
    )
    fig.update_layout(get_common_layout("Posts per Subreddit"))
    return fig

def chart_subreddit_distribution(df):
    counts = df['subreddit'].value_counts().reset_index()
    counts.columns = ['subreddit', 'count']
    
    fig = px.pie(
        counts, 
        names='subreddit', 
        values='count',
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_layout(get_common_layout("Subreddit Distribution"))
    return fig

def chart_posts_over_time(df):
    # Ensure created_utc is datetime
    if 'created_utc' not in df.columns:
        return None
        
    df['date'] = pd.to_datetime(df['created_utc']).dt.date
    time_series = df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        time_series, 
        x='date', 
        y='count',
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(line_color=REDDIT_ORANGE, line_width=3)
    fig.update_layout(get_common_layout("Posts Over Time"))
    return fig

def chart_top_active(df):
    # Top 10 Active Authors (if author column exists)
    if 'author' not in df.columns:
        return None

    top_authors = df['author'].value_counts().head(10).reset_index()
    top_authors.columns = ['author', 'count']
    
    fig = px.bar(
        top_authors,
        y='author',
        x='count',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(get_common_layout("Top 10 Active Authors"))
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

def chart_word_cloud(df):
    if not KEY_WORDCLOUD_AVAILABLE:
        return None
        
    if 'title' not in df.columns:
        return None
        
    text = " ".join(title for title in df['title'].dropna())
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='black',
        colormap='Oranges'
    ).generate(text)
    
    # Convert to image for Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    # Set background to transparent
    fig.patch.set_alpha(0)
    return fig
