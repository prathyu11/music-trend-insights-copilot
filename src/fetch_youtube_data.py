import os
import requests
import pandas as pd
from datetime import datetime

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCq-Fj5jknLsUf-MWSy4_brA"

url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}"
res = requests.get(url).json()
uploads_playlist = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist}&maxResults=10&key={API_KEY}"
res = requests.get(url).json()

video_ids = []
videos_data = []

for item in res["items"]:
    video_id = item["snippet"]["resourceId"]["videoId"]
    title = item["snippet"]["title"]
    published_at = item["snippet"]["publishedAt"]

    video_ids.append(video_id)
    videos_data.append({
        "video_id": video_id,
        "title": title,
        "published_at": published_at
    })

ids = ",".join(video_ids)
url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={ids}&key={API_KEY}"
res = requests.get(url).json()

for i, item in enumerate(res["items"]):
    stats = item["statistics"]

    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))

    published_date = datetime.strptime(videos_data[i]["published_at"], "%Y-%m-%dT%H:%M:%SZ")
    days = (datetime.utcnow() - published_date).days + 1

    views_per_day = views / days
    likes_per_day = likes / days
    comments_per_day = comments / days

    momentum_score = views_per_day * 0.6 + likes_per_day * 0.3 + comments_per_day * 0.1

    videos_data[i].update({
        "views": views,
        "likes": likes,
        "comments": comments,
        "days_since_release": days,
        "views_per_day": views_per_day,
        "likes_per_day": likes_per_day,
        "comments_per_day": comments_per_day,
        "momentum_score": momentum_score,
        "youtube_url": f"https://www.youtube.com/watch?v={videos_data[i]['video_id']}"
    })

df = pd.DataFrame(videos_data)
df.to_csv("data/tseries_music_data.csv", index=False)

print("Data saved to tseries_music_data.csv")