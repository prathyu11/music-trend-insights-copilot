import pandas as pd
import streamlit as st
import ollama

st.set_page_config(page_title="Music Trend Insights Copilot", layout="wide")

st.title("🎵 Music Trend Insights Copilot")
st.markdown("""
### What this app does
- Pulls real YouTube data from T-Series
- Calculates engagement momentum
- Uses an AI model to generate promotion recommendations
""")
st.write("Analyzes live T-Series YouTube data and generates AI-powered promotion recommendations.")

df = pd.read_csv("tseries_music_data.csv")
st.download_button(
    label="Download Data as CSV",
    data=df.to_csv(index=False),
    file_name="tseries_music_data.csv",
    mime="text/csv"
)

st.subheader("Recent Video Performance Data")
display_df = df.drop(columns=["video_id"], errors="ignore")
st.dataframe(display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "youtube_url": st.column_config.LinkColumn("YouTube Link"),
        "momentum_score": st.column_config.NumberColumn("Momentum Score", format="%.0f"),
        "views_per_day": st.column_config.NumberColumn("Views / Day", format="%.0f"),
        "likes_per_day": st.column_config.NumberColumn("Likes / Day", format="%.0f"),
        "comments_per_day": st.column_config.NumberColumn("Comments / Day", format="%.0f"),
    })

st.subheader("Dashboard Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Videos", len(df))
col2.metric("Total Views", f"{df['views'].sum():,.0f}")
col3.metric("Total Likes", f"{df['likes'].sum():,.0f}")
col4.metric("Total Comments", f"{df['comments'].sum():,.0f}")

top_videos = df.sort_values("momentum_score", ascending=False).head(5)

st.subheader("Top 5 Videos by Momentum")
st.dataframe(top_videos[["title", "views", "likes", "comments", "momentum_score", "youtube_url"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "youtube_url": st.column_config.LinkColumn("YouTube Link"),
        "momentum_score": st.column_config.NumberColumn("Momentum Score", format="%.0f"),
    })

st.subheader("Top Videos by Momentum")

chart_df = df.sort_values("momentum_score", ascending=False).head(10)

st.bar_chart(
    chart_df.set_index("title")["momentum_score"]
)
if st.button("Generate AI Recommendation"):
    data_text = top_videos.to_string(index=False)

    prompt = f"""
    You are a business analyst for a music label like T-Series.

    Based on the recent YouTube video performance data below:
    1. Which video should get highest promotion focus?
    2. Why?
    3. What is the executive recommendation?

    Do not invent data.

    Data:
    {data_text}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("AI Recommendation")
    st.write(response["message"]["content"])