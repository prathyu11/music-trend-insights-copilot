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

## How to run

```bash
./venv/bin/python fetch_youtube_data.py
./venv/bin/python analyze_music_trends.py
./venv/bin/python ai_insights.py


## AI Layer

This project uses a local open-source LLM through Ollama to generate executive-friendly recommendations from live YouTube performance data.

## Environment Setup

Create a `.env` file locally:

```bash
cp .env.example .env