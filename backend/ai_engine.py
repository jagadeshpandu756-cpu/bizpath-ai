from groq import Groq
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def generate_roadmap(profile, market_data: dict) -> str:

    news_context = ""
    if market_data.get("trending_news"):
        news_items = market_data["trending_news"][:3]
        news_context = "\n".join([f"- {n['title']}" for n in news_items if n['title']])

    economic = market_data.get("economic_indicators", {})
    gdp = economic.get("gdp_growth_rate", "N/A")

    prompt = "You are a top-tier business consultant.\n"
    prompt += "Analyze this investor profile and create a detailed beginner-friendly business roadmap.\n\n"
    prompt += "INVESTOR PROFILE\n"
    prompt += "Name: " + profile.name + "\n"
    prompt += "Location: " + profile.location + "\n"
    prompt += "Budget: " + profile.currency + " " + str(profile.budget) + "\n"
    prompt += "Interests: " + ", ".join(profile.interests) + "\n"
    prompt += "Risk Tolerance: " + str(profile.risk_level) + "/10\n"
    prompt += "Time Horizon: " + str(profile.time_horizon) + " years\n"
    prompt += "Experience: " + str(profile.experience) + " years\n"
    prompt += "Goal: " + profile.goal + "\n\n"
    prompt += "LIVE MARKET DATA\n"
    prompt += "GDP Growth Rate: " + gdp + "\n"
    prompt += "Recent Trends:\n" + (news_context if news_context else "General market conditions apply") + "\n\n"
    prompt += "Generate roadmap with these sections:\n"
    prompt += "## Top 3 Business Ideas\n"
    prompt += "## Best Recommended Business\n"
    prompt += "## Investment Breakdown in " + profile.currency + "\n"
    prompt += "## 12-Month Profit Forecast\n"
    prompt += "## 90-Day Launch Plan\n"
    prompt += "## Growth Strategies\n"
    prompt += "## Risk Analysis\n\n"
    prompt += "Be specific to " + profile.location + ". Simple language for a complete beginner."

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
          model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
    )

    return response.choices[0].message.content