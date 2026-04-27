import pandas as pd
import streamlit as st
import ollama

st.set_page_config(page_title="Music Trend Insights Copilot", layout="wide")

st.title("🎵 Music Trend Insights Copilot")
st.write("Analyzes live T-Series YouTube data and generates AI-powered promotion recommendations.")

df = pd.read_csv("tseries_music_data.csv")

st.subheader("Recent Video Performance Data")
st.dataframe(df)

top_videos = df.sort_values("momentum_score", ascending=False).head(5)

st.subheader("Top 5 Videos by Momentum")
st.dataframe(top_videos[["title", "views", "likes", "comments", "momentum_score", "youtube_url"]])

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