import pandas as pd
import ollama

df = pd.read_csv("data/tseries_music_data.csv")

top_videos = df.sort_values("momentum_score", ascending=False).head(5)

data_text = top_videos[
    [
        "title",
        "views",
        "likes",
        "comments",
        "days_since_release",
        "views_per_day",
        "likes_per_day",
        "comments_per_day",
        "momentum_score",
        "youtube_url",
    ]
].to_string(index=False)

prompt = f"""
You are a business analyst for a music label like T-Series.

Based on the recent YouTube video performance data below, answer:

1. Which video should get the highest promotion focus this week?
2. Why?
3. What is the simple business recommendation?

Use clear executive-friendly language.
Do not invent data.

Data:
{data_text}
"""

response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "user", "content": prompt}
    ],
)

print(response["message"]["content"])