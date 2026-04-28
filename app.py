import pandas as pd
import streamlit as st
import ollama
import joblib

st.set_page_config(page_title="Music Trend Insights Copilot", layout="wide")

st.title("🎵 Music Trend Insights Copilot")
st.markdown("""
### What this app does
- Pulls real YouTube data from T-Series
- Calculates engagement momentum
- Uses an AI model to generate promotion recommendations
""")
st.write("Analyzes live T-Series YouTube data and generates AI-powered promotion recommendations.")

df = pd.read_csv("data/tseries_music_data.csv")

model = joblib.load("models/promotion_priority_model.pkl")
features = joblib.load("models/model_features.pkl")

df["promotion_priority"] = model.predict(df[features])

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

st.subheader("🎯 Focus Now")

top_choice = top_videos.iloc[0]

st.success(
    f"Prioritize: **{top_choice['title']}**  \n\n"
    f"ML Prediction: **{top_choice['promotion_priority']}**  \n"
    f"Momentum Score: **{top_choice['momentum_score']:.0f}**"
)

st.markdown(f"[Open on YouTube]({top_choice['youtube_url']})")

st.subheader("Top 5 Videos by Momentum")
def highlight_priority(val):
    if val == "High":
        return "background-color: #ff4d4d; color: white; font-weight: bold"
    elif val == "Medium":
        return "background-color: #ffcc00; color: black; font-weight: bold"
    else:
        return "background-color: #2ecc71; color: white; font-weight: bold"

styled_df = top_videos[
    [
        "title",
        "promotion_priority",
        "views",
        "likes",
        "comments",
        "momentum_score",
        "youtube_url",
    ]
].style.map(highlight_priority, subset=["promotion_priority"])

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("Top Videos by Momentum")

chart_df = df.sort_values("momentum_score", ascending=False).head(10)

st.bar_chart(
    chart_df.set_index("title")["momentum_score"]
)
if st.button("Generate AI Recommendation"):
    data_text = top_videos[[
        "title",
        "promotion_priority",
        "views",
        "likes",
        "comments",
        "days_since_release",
        "views_per_day",
        "likes_per_day",
        "comments_per_day",
        "momentum_score",
    ]].to_string(index=False)

    prompt = f"""
    You are a business analyst for a music label like T-Series.

    Based on the recent YouTube video performance data and ML-predicted promotion priority below:

    1. Which video should get the highest promotion focus?
    2. Why did the ML model likely classify it that way?
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