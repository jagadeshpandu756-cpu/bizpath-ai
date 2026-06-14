import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="BizPath AI", page_icon="🧭", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0a0a1a; }
    h1 { background: linear-gradient(90deg, #f59e0b, #ef4444);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🧭 BizPath AI")
st.caption("AI-Powered Business Roadmap for Beginners")

st.header("Tell us about yourself")

with st.form("roadmap_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="e.g. Rahul Sharma")
    with col2:
        location = st.text_input("City / Location", placeholder="e.g. Mumbai, India")

    col3, col4 = st.columns(2)
    with col3:
        currency = st.selectbox("Currency", ["INR ₹", "USD $", "EUR €"])
    with col4:
        budget = st.number_input("Investment Budget", min_value=0, step=10000, value=100000)

    interests = st.multiselect(
        "Select Your Business Interests",
        ["Food and Beverage", "Technology", "Retail", "Education",
         "Health and Wellness", "Agriculture", "Manufacturing", "Services"]
    )

    col5, col6 = st.columns(2)
    with col5:
        risk_level = st.slider("Risk Level", 1, 10, 5)
    with col6:
        time_horizon = st.slider("Time Horizon (years)", 1, 10, 3)

    goal = st.text_input("Your Goal", placeholder="e.g. Replace my job, build passive income...")

    submitted = st.form_submit_button("🚀 Generate My Business Roadmap", type="primary")

if submitted:
    if not name or not location or not budget or not interests:
        st.error("Please fill in all required fields and select at least one interest!")
    else:
        with st.spinner("AI is analyzing your profile... This may take 20-30 seconds"):

            prompt = "You are a top-tier business consultant.\n"
            prompt += "Analyze this investor profile and create a detailed beginner-friendly business roadmap.\n\n"
            prompt += "INVESTOR PROFILE\n"
            prompt += "Name: " + name + "\n"
            prompt += "Location: " + location + "\n"
            prompt += "Budget: " + currency + " " + str(budget) + "\n"
            prompt += "Interests: " + ", ".join(interests) + "\n"
            prompt += "Risk Tolerance: " + str(risk_level) + "/10\n"
            prompt += "Time Horizon: " + str(time_horizon) + " years\n"
            prompt += "Goal: " + (goal if goal else "Build a profitable business") + "\n\n"
            prompt += "Generate roadmap with these sections:\n"
            prompt += "## Top 3 Business Ideas\n"
            prompt += "## Best Recommended Business\n"
            prompt += "## Investment Breakdown in " + currency + "\n"
            prompt += "## 12-Month Profit Forecast\n"
            prompt += "## 90-Day Launch Plan\n"
            prompt += "## Growth Strategies\n"
            prompt += "## Risk Analysis\n\n"
            prompt += "Be specific to " + location + ". Simple language for a complete beginner."

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000
                )
                roadmap = response.choices[0].message.content

                st.success("Your roadmap is ready!")
                st.markdown("## 📋 Your Personalized Business Roadmap")
                st.markdown(roadmap)

            except Exception as e:
                st.error(f"Error: {str(e)}")