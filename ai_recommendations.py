import google.generativeai as genai
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load the .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key is missing. Please check your .env file.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_recommendations(user_input):
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")  

        # Get AI-generated recommendations
        response = model.generate_content(user_input)

        # Return the text response
        return response.text if response else "No response from AI."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_input = "What are some skincare tips for dry skin?"
    print(get_ai_recommendations(user_input))
