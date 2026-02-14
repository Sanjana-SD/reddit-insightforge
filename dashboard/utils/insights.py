import pandas as pd

def generate_insights(df):
    insights = []
    
    if df.empty:
        return ["No data available for insights."]
    
    # 1. Top Subreddit Contribution
    top_sub = df['subreddit'].mode()[0]
    top_sub_count = df[df['subreddit'] == top_sub].shape[0]
    total_count = len(df)
    percentage = (top_sub_count / total_count) * 100
    insights.append(f"🏆 **r/{top_sub}** contributes **{percentage:.1f}%** of total volume.")
    
    # 2. Peak Posting Time
    if 'created_utc' in df.columns:
        df['hour'] = df['created_utc'].dt.hour
        peak_hour = df['hour'].mode()[0]
        # Format hour
        period = "AM" if peak_hour < 12 else "PM"
        display_hour = peak_hour if peak_hour <= 12 else peak_hour - 12
        if display_hour == 0: display_hour = 12
        insights.append(f"⏰ Peak posting time is around **{display_hour} {period}**.")
    
    # 3. Average Engagement (if score exists)
    if 'score' in df.columns:
        avg_score = df['score'].mean()
        insights.append(f"⭐ Average post score is **{avg_score:.1f}**.")
        
    return insights
