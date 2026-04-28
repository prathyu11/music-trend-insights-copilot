import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


df = pd.read_csv("tseries_music_data.csv")

# Create labels from momentum score
# Top 30% = High, middle 40% = Medium, bottom 30% = Low
high_threshold = df["momentum_score"].quantile(0.70)
low_threshold = df["momentum_score"].quantile(0.30)

def label_priority(score):
    if score >= high_threshold:
        return "High"
    elif score <= low_threshold:
        return "Low"
    else:
        return "Medium"

df["promotion_priority"] = df["momentum_score"].apply(label_priority)

features = [
    "views",
    "likes",
    "comments",
    "days_since_release",
    "views_per_day",
    "likes_per_day",
    "comments_per_day",
    "momentum_score",
]

X = df[features]
y = df["promotion_priority"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# With small data, train/test split may be unstable, but good for demo
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y if y.value_counts().min() > 1 else None
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Model evaluation:")
print(classification_report(y_test, predictions, zero_division=0))

joblib.dump(model, "promotion_priority_model.pkl")
joblib.dump(features, "model_features.pkl")

df.to_csv("tseries_music_data_with_labels.csv", index=False)

print("Saved trained model: promotion_priority_model.pkl")
print("Saved labeled data: tseries_music_data_with_labels.csv")