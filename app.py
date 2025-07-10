import streamlit as st
from datetime import datetime
import json
import os

# File to store user period data
DATA_FILE = "data/user_data.json"
os.makedirs("data", exist_ok=True)

# Load previous data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Add a new period entry
def log_period(date_str):
    data = load_data()
    if date_str not in [entry["date"] for entry in data]:
        data.append({"date": date_str})
        data.sort(key=lambda x: x["date"], reverse=True)
        save_data(data)
        return True
    return False

# Streamlit app UI
st.set_page_config(page_title="Luna — Your PCOS Companion")
st.title("🌙 Luna – Your PCOS Companion")

# Log period for today
if st.button("📍 I started my period today"):
    today_str = datetime.today().strftime("%Y-%m-%d")
    if log_period(today_str):
        st.success(f"Logged period for {today_str}")
    else:
        st.info(f"Period for {today_str} already logged")

# Log period for a custom date
custom_date = st.date_input("📆 Or log a period for a different date")
if st.button("Log selected date"):
    date_str = custom_date.strftime("%Y-%m-%d")
    if log_period(date_str):
        st.success(f"Logged period for {date_str}")
    else:
        st.warning(f"Period for {date_str} already exists")

# Display period history
st.markdown("---")
st.subheader("🩸 Period History")
data = load_data()
if data:
    for entry in data:
        st.write(f"• {entry['date']}")
else:
    st.info("No period history yet.")

# Chatbot (unchanged)
prompt = st.text_input("Ask Luna anything...")

if prompt:
    from dotenv import load_dotenv
    import google.generativeai as genai
    import os

    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-1.5-flash')  # Use a supported model

    response = model.generate_content(prompt)
    st.markdown("**🌙 Luna says:**")
    st.write(response.text)
