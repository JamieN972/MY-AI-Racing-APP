
# 🏇 AI Horse Racing Predictor

This Streamlit app uses AI logic and real-time data from RapidAPI to predict value bets in UK and Irish horse racing.

## 🔍 Features

- Dropdown to select today's races
- Calculates AI Win Probability & Value Score
- Displays form, trainer, jockey, draw, and odds

## 🚀 How to Deploy on Streamlit Cloud

1. Fork or clone this repo
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and click **New app**
3. Select this repo and use `streamlit_app.py` as the entry point

## 🔐 Add API Credentials

Go to **Settings > Secrets** in Streamlit Cloud and paste:

```toml
[rapidapi]
key = "your-api-key"
host = "horse-racing.p.rapidapi.com"
```

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## ✅ Example

<img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg" width="200"/>

Deployed with [Streamlit](https://streamlit.io).
