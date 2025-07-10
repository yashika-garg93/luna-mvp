import streamlit as st
import os
import json
from datetime import datetime, timedelta
from streamlit_calendar import calendar

DATA_FILE = "user_data.json"
st.set_page_config(page_title="Luna – Your PCOS Companion", page_icon="🌙")

# ------------------ Utils ------------------ #

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(sorted(list(set(data)), reverse=True), f, indent=2)

def add_period_date(date_str):
    data = load_data()
    if date_str not in data:
        data.append(date_str)
        save_data(data)

# ------------------ UI ------------------ #

st.markdown("<h1 style='text-align: center;'>🌙 Luna – Your PCOS Companion</h1>", unsafe_allow_html=True)

# --- Log today's period
if st.button("📍 I started my period today"):
    today = datetime.today().strftime("%Y-%m-%d")
    add_period_date(today)
    st.success(f"Logged period for today ({today})")

# --- Log other date
st.markdown("### 📅 Or log a period for a different date")
custom_date = st.date_input("Select a date", value=datetime.today())
if st.button("Log selected date"):
    add_period_date(custom_date.strftime("%Y-%m-%d"))
    st.success(f"Logged period for {custom_date.strftime('%Y-%m-%d')}")

# --- Load data
data = load_data()

# --- Calendar view
st.markdown("## 🔴 Period Calendar")
events = [{
    "title": "Period Day",
    "start": date,
    "end": date,
    "color": "#e63946"
} for date in data]

calendar_options = {
    "initialView": "dayGridMonth",
    "height": 600,
    "locale": "en",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar(events=events, options=calendar_options)

# --- Prediction (basic)
if len(data) >= 2:
    last = datetime.strptime(data[0], "%Y-%m-%d")
    second_last = datetime.strptime(data[1], "%Y-%m-%d")
    avg_cycle = (last - second_last).days
    next_date = last + timedelta(days=avg_cycle)
    st.info(f"📆 Based on your last 2 periods, your average cycle is ~{avg_cycle} days.\n\n👉 Your next expected period might be around **{next_date.strftime('%Y-%m-%d')}**")
else:
    st.info("Log at least 2 periods to predict your next cycle.")
