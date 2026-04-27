# Music Trend Insights Copilot

A lightweight data + AI project that analyzes recent T-Series YouTube videos and identifies which videos have the strongest current momentum.

## What it does

- Pulls live public YouTube data
- Collects views, likes, comments, and publish date
- Calculates views/day, likes/day, comments/day
- Creates a custom momentum score
- Gives an executive-style recommendation on what to promote next

## Why this matters

Music labels release many songs and videos. Business teams need a quick way to identify which content is gaining traction and deserves more marketing focus.

## Tech Stack

- Python
- YouTube Data API v3
- Pandas
- Ollama
- Llama 3 open-source LLM

## App Preview

![App Preview](app_screenshot1.png) 
![App Preview](app_screenshot2.png) 
![App Preview](app_screenshot3.png)

## Architecture

```text
YouTube Data API
      ↓
Python Data Pipeline
      ↓
CSV Dataset
      ↓
Momentum Score Calculation
      ↓
Streamlit Dashboard
      ↓
Ollama + Llama 3
      ↓
AI Promotion Recommendation
```

## How to run

```bash
./venv/bin/python fetch_youtube_data.py
./venv/bin/python analyze_music_trends.py
./venv/bin/python ai_insights.py
```

## Run the Streamlit App

```bash
./venv/bin/python -m streamlit run app.py
```

## AI Layer

This project uses a local open-source LLM through Ollama to generate executive-friendly recommendations from live YouTube performance data.

## Environment Setup

Create a `.env` file locally:

```bash
cp .env.example .env
```

## Limitations

- Uses only public YouTube data.
- Does not include private analytics like watch time, CTR, revenue, retention, or demographics.
- Momentum score is a simple heuristic, not a trained prediction model.
- AI recommendations are generated from available metrics and should be used as decision support, not final business truth.