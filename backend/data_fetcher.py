import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_live_market_data(location: str, interests: list):
    market_data = {}

    news = await fetch_business_news(interests)
    market_data["trending_news"] = news

    economic = await fetch_economic_data(location)
    market_data["economic_indicators"] = economic

    return market_data

async def fetch_business_news(interests: list) -> list:
    api_key = os.getenv("NEWS_API_KEY")
    query = " OR ".join(interests[:3])

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f"{query} business startup",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            data = response.json()
            articles = data.get("articles", [])
            return [{"title": a["title"], "summary": a["description"]}
                    for a in articles if a["title"]]
        except Exception:
            return []

async def fetch_economic_data(location: str) -> dict:
    country_map = {
        "india": "IN", "usa": "US", "uk": "GB",
        "canada": "CA", "australia": "AU", "uae": "AE"
    }
    location_lower = location.lower()
    country_code = "IN"
    for key, code in country_map.items():
        if key in location_lower:
            country_code = code
            break

    async with httpx.AsyncClient() as client:
        try:
            url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?format=json&mrv=1"
            response = await client.get(url, timeout=10)
            data = response.json()
            gdp_growth = data[1][0]["value"] if data[1] else None
            return {
                "country": country_code,
                "gdp_growth_rate": f"{gdp_growth:.1f}%" if gdp_growth else "N/A"
            }
        except Exception:
            return {"country": "IN", "gdp_growth_rate": "N/A"}