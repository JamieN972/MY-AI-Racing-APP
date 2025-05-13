import streamlit as st
import requests
import pandas as pd

st.title("Live AI Horse Racing Predictor")

# Load API credentials from secrets
API_KEY = st.secrets["rapidapi"]["key"]
API_HOST = st.secrets["rapidapi"]["host"]

headers = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

# Step 1: Fetch today's races
race_list_url = f"https://{API_HOST}/races?date=today"
race_list_response = requests.get(race_list_url, headers=headers)
race_list_data = race_list_response.json()

# Step 2: Create dropdown of races
try:
    races = race_list_data["races"]

    # Add filter for number of runners
    races_with_runners = [r for r in races if len(r.get("runners", [])) > 0]
    min_runners = st.slider("Minimum number of runners", 1, 30, 1)
    filtered_races = [r for r in races_with_runners if r.get("num_runners", 0) >= min_runners]

    race_options = {f"{r['meeting']['name']} - {r['name']} ({r['race_time']})": r["id"] for r in filtered_races}
    selected_race = st.selectbox("Select a race", list(race_options.keys()))
    race_id = race_options[selected_race]

    # Step 3: Fetch selected race data
    race_url = f"https://{API_HOST}/race/{race_id}"
    response = requests.get(race_url, headers=headers)
    data = response.json()

    runners = data["race"]["runners"]
    df = pd.DataFrame(runners)

    df["Odds"] = df["oddsDecimal"].astype(float)
    df["AI Win Probability"] = 1 / df["Odds"]
    df["AI Win Probability"] /= df["AI Win Probability"].sum()
    df["Value Score"] = (df["AI Win Probability"] * df["Odds"]) - 1

    # Add extra columns for form, trainer, jockey, age, and draw
    df["Form"] = df["form"] if "form" in df.columns else "N/A"
    df["Trainer"] = df["trainerName"] if "trainerName" in df.columns else "N/A"
    df["Jockey"] = df["jockeyName"] if "jockeyName" in df.columns else "N/A"
    df["Age"] = df["age"] if "age" in df.columns else "N/A"
    df["Draw"] = df["draw"] if "draw" in df.columns else "N/A"

    st.subheader(f"Race: {data['race']['meeting']['name']} - {data['race']['name']}")
    st.dataframe(df[["name", "Age", "Draw", "Trainer", "Jockey", "Form", "Odds", "AI Win Probability", "Value Score"]].sort_values(by="Value Score", ascending=False))

    top = df.sort_values(by="Value Score", ascending=False).iloc[0]
    st.markdown(f"### 🏇 Top Value Bet: **{top['name']}**")
    st.markdown(f"- Age: {top['Age']}")
    st.markdown(f"- Draw: {top['Draw']}")
    st.markdown(f"- Trainer: {top['Trainer']}")
    st.markdown(f"- Jockey: {top['Jockey']}")
    st.markdown(f"- Form: {top['Form']}")
    st.markdown(f"- Odds: {top['Odds']}")
    st.markdown(f"- Win Probability: {top['AI Win Probability']*100:.2f}%")
    st.markdown(f"- Value Score: {top['Value Score']:.2f}")

except Exception as e:
    st.error("⚠️ Failed to load race data.")
    st.exception(e)
