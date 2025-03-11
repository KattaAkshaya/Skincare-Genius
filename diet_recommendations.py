import google.generativeai as genai
import os
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key is missing. Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def get_diet_recommendations(gender, age, skin_type, skin_concerns):
    """Fetches AI-powered diet recommendations based on skin type, gender, age, and concerns."""
    prompt = (
        f"I am a {age}-year-old {gender} with {skin_type} skin. "
        f"I have the following skin concerns: {', '.join(skin_concerns)}. "
        "What are the best foods to eat and what should I avoid for healthy skin? "
        "Please provide a list of recommended and non-recommended foods."
    )
    
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text if response else "Unable to fetch diet recommendations."

# Example usage
if __name__ == "__main__":
    gender = "Female"
    age = 25
    skin_type = "Oily"
    skin_concerns = ["acne", "dark spots"]
    
    recommendations = get_diet_recommendations(gender, age, skin_type, skin_concerns)
    print(recommendations)
