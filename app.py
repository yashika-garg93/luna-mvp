import streamlit as st
from datetime import date
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-pro')

st.set_page_config(page_title="Luna – Your PCOS Companion")
st.title("🌙 Luna – Your PCOS Companion")

# Log period
if st.button("📍 I started my period today"):
    today = str(date.today())
    os.makedirs("data", exist_ok=True)
    with open("data/user_data.json", "a") as f:
        f.write(json.dumps({"date": today}) + "\n")
    st.success(f"Logged period for {today}")

# Chatbot
prompt = st.text_input("Ask Luna anything...")

if prompt:
    response = model.generate_content(prompt)
    st.markdown("**Luna says:**")
    st.write(response.text)
