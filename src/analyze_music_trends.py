import pandas as pd

df = pd.read_csv("data/tseries_music_data.csv")

top = df.sort_values("momentum_score", ascending=False).head(3)

print("\nTop 3 high-momentum T-Series videos:\n")

for i, row in top.iterrows():
    print(f"{row['title']}")
    print(f"- Views per day: {row['views_per_day']:.0f}")
    print(f"- Likes per day: {row['likes_per_day']:.0f}")
    print(f"- Comments per day: {row['comments_per_day']:.0f}")
    print(f"- Momentum score: {row['momentum_score']:.0f}")
    print(f"- URL: {row['youtube_url']}")
    print()
best = top.iloc[0]

print("Executive recommendation:\n")
print(
    f"'{best['title']}' should receive the highest promotion focus right now because "
    f"it has the strongest current momentum among recent T-Series videos. "
    f"It is gaining approximately {best['views_per_day']:.0f} views/day, "
    f"{best['likes_per_day']:.0f} likes/day, and "
    f"{best['comments_per_day']:.0f} comments/day."
)