import streamlit as st
import os
import json
from datetime import datetime

DATA_FILE = "user_data.json"
st.set_page_config(page_title="Luna – Your PCOS Companion", page_icon="🌙")

# ---------------------------- Utilities ---------------------------- #

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
        json.dump(data, f, indent=2)

def add_period_date(date_str):
    data = load_data()
    if date_str not in data:
        data.append(date_str)
        data.sort(reverse=True)  # most recent first
        save_data(data)

# ---------------------------- UI ---------------------------- #

st.markdown("<h1 style='text-align: center;'>🌙 Luna – Your PCOS Companion</h1>", unsafe_allow_html=True)

# --- Log today's period
if st.button("📍 I started my period today"):
    today = datetime.today().strftime("%Y-%m-%d")
    add_period_date(today)
    st.success(f"Logged period for today ({today})")

# --- Log a custom date
st.markdown("### 📅 Or log a period for a different date")
custom_date = st.text_input("Enter date (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"))
if st.button("Log selected date"):
    try:
        datetime.strptime(custom_date, "%Y-%m-%d")  # Validate date format
        add_period_date(custom_date)
        st.success(f"Logged period for {custom_date}")
    except ValueError:
        st.error("❌ Please enter a valid date in YYYY-MM-DD format.")

# --- Display history
st.markdown("## 🔴 Period History")
data = load_data()
if data:
    st.write("Here are your logged period dates (most recent first):")
    for date in data:
        st.markdown(f"- 📌 {date}")
else:
    st.info("No period data logged yet. Use the buttons above to start tracking!")
