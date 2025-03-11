import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("❌ OpenWeatherMap API key is missing. Please check your .env file.")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetches weather data for a given city from OpenWeatherMap API."""
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
        }
    else:
        return {"error": "Invalid city or API key"}

def skincare_recommendations(skin_type, weather_info, skin_concerns):
    """Provides skincare recommendations based on weather and skin concerns."""
    temperature = weather_info["temperature"]
    humidity = weather_info["humidity"]
    condition = weather_info["condition"]
    
    recommendations = f"🌡️ Current temperature: {temperature}°C\n"
    
    # 🌤️ Weather-based recommendations
    if temperature > 30:
        recommendations += "🔥 It's hot! Use a lightweight, oil-free sunscreen and stay hydrated.\n"
    elif temperature < 15:
        recommendations += "❄️ It's cold! Use a thick moisturizer with ceramides to prevent dryness.\n"
    
    if humidity > 70:
        recommendations += "🌧️ High humidity detected! Use water-based gel moisturizers and avoid heavy oils.\n"
    elif humidity < 30:
        recommendations += "💨 Low humidity detected! Apply hydrating serums with hyaluronic acid to lock in moisture.\n"
    
    if "rain" in condition:
        recommendations += "☔ Rainy weather! Avoid heavy makeup and use non-comedogenic products.\n"
    elif "clear" in condition:
        recommendations += "☀️ Sunny day! Apply SPF 50 sunscreen and reapply every 2 hours.\n"

    # 🧴 Skin concern-based recommendations
    skin_concerns = skin_concerns.lower()

    # ✅ Acne & Breakouts
    if "acne" in skin_concerns or "breakouts" in skin_concerns:
        recommendations += "🧼 Acne-prone skin? Use salicylic acid cleansers, niacinamide serum, and lightweight moisturizers.\n"
    if "hormonal acne" in skin_concerns:
        recommendations += "⚖️ Hormonal acne? Incorporate zinc supplements, spearmint tea, and adaptogens like ashwagandha.\n"

    # ✅ Skin Texture & Pores
    if "large pores" in skin_concerns or "clogged pores" in skin_concerns:
        recommendations += "🔍 Large pores? Try niacinamide, clay masks, and AHA/BHA exfoliants.\n"
    if "rough texture" in skin_concerns:
        recommendations += "🎭 Uneven skin texture? Exfoliate 2-3 times a week with glycolic acid.\n"

    # ✅ Skin Tone & Pigmentation
    if "dark spots" in skin_concerns or "hyperpigmentation" in skin_concerns:
        recommendations += "🌟 Dark spots? Use vitamin C serum in the morning and SPF to prevent pigmentation.\n"
    if "dull skin" in skin_concerns:
        recommendations += "✨ Dull skin? Apply exfoliating serums with AHA and niacinamide for brightening.\n"

    # ✅ Redness & Sensitivity
    if "redness" in skin_concerns or "rosacea" in skin_concerns:
        recommendations += "🍃 Redness? Avoid spicy foods and use calming ingredients like centella asiatica.\n"
    if "sensitive skin" in skin_concerns:
        recommendations += "🌿 Sensitive skin? Choose fragrance-free, gentle formulations with ceramides.\n"

    # ✅ Dry & Dehydrated Skin
    if "dryness" in skin_concerns or "dehydrated skin" in skin_concerns:
        recommendations += "💦 Hydrate! Use hyaluronic acid, drink more water, and avoid alcohol-based toners.\n"
    if "eczema" in skin_concerns or "psoriasis" in skin_concerns:
        recommendations += "🩹 Eczema/Psoriasis? Stick to barrier creams and avoid hot showers.\n"

    # ✅ Anti-Aging & Fine Lines
    if "wrinkles" in skin_concerns or "fine lines" in skin_concerns:
        recommendations += "⏳ Aging skin? Use retinol, peptides, and collagen-boosting serums.\n"
    if "sun damage" in skin_concerns:
        recommendations += "☀️ Sun damage? Use vitamin C, niacinamide, and broad-spectrum SPF daily.\n"

    # ✅ Eye Care
    if "dark circles" in skin_concerns or "puffy eyes" in skin_concerns:
        recommendations += "👀 Dark circles? Try caffeine eye creams and cold compress therapy.\n"

    # ✅ Special Cases
    if "pregnancy" in skin_concerns:
        recommendations += "🤰 Pregnancy-safe skincare? Avoid retinol, salicylic acid, and opt for gentle, natural ingredients.\n"
    if "keratosis pilaris" in skin_concerns:
        recommendations += "🐥 'Chicken Skin'? Use lactic acid lotions and exfoliate with AHA scrubs.\n"

    return recommendations if recommendations else "🌿 Your skin is in good condition! Keep up the good routine."

# Test script
if __name__ == "__main__":
    city = "London"
    weather = get_weather(city)
    skin_type = "Oily"
    skin_concerns = "acne, dryness, wrinkles, dark circles"
    
    print(skincare_recommendations(skin_type, weather, skin_concerns))
