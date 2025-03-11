import streamlit as st
from ai_recommendations import get_ai_recommendations  
from product_api import fetch_products_from_dataset
from weather_api import get_weather, skincare_recommendations
from diet_recommendations import get_diet_recommendations

st.set_page_config(page_title="🌿Skincare Genius", layout="wide")

# Custom CSS for Styling Output Cards
st.markdown("""
    <style>
        /* Main Layout */
        .main-container {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 20px;
            width: 100%;
            transition: all 0.3s ease-in-out;
        }

        @media (max-width: 1000px) {
            .main-container {
                grid-template-columns: 1fr;
            }
        }

        /* Title Styling */
        .title-container {
            text-align: center;
        }

        h1 {
            font-size: 2rem;
            color: #4CAF50;
            margin-bottom: 5px;
        }

        .tagline {
            font-size: 1.2rem;
            color: #666;
        }

        /* Button Styling */
        .stButton > button {
            background-color: #6BCB77;
            color: white;
            font-size: 18px;
            padding: 12px;
            width: 80%;
            transition: 0.3s ease-in-out;
        }

        @media (max-width: 1200px) {
            .stButton > button {
                font-size: 16px;
                width: 100%;
            }
        }

        /* Custom Output Cards */
        .custom-card {
           
            padding: 15px;
            border-radius: 12px;
            box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.2);
            margin: 15px 0;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
        }
        .custom-card h3 {
            color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<div class="title-container"><h1>🌿Skincare Genius</h1><p class="tagline">✨ Unlock your perfect skin with AI-powered advice ✨</p></div>', unsafe_allow_html=True)

# Main Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Sidebar: User Inputs
with st.sidebar:
    st.header("📝 Personal Details")
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Non-Binary", "Prefer not to say"])
    skin_type = st.selectbox("Select your skin type:", ["Oily", "Dry", "Combination", "Sensitive", "Normal"])
    age = st.number_input("Enter your age:", min_value=10, max_value=100, step=1)
    city = st.text_input("🌍 Enter your city for weather-based skincare recommendations:")
    user_input = st.text_area("✍️ Describe your skin concerns (e.g., acne, dark spots, wrinkles):")

# Main Content
st.markdown('<div class="content">', unsafe_allow_html=True)

# AI Skincare Advice Button
if st.button("💬 Get AI Advice"):
    with st.spinner("Analyzing your skin concerns..."):
        full_input = f"Gender: {gender}\nSkin Type: {skin_type}\nAge: {age}\nConcerns: {user_input}"
        ai_response = get_ai_recommendations(full_input)
    
    st.markdown(f"""
        <div class="custom-card">
            <h3>✅ AI Skincare Recommendations</h3>
            <p>{ai_response}</p>
        </div>
    """, unsafe_allow_html=True)

# Weather-Based Skincare Tips Button
if st.button("☁️ Get Weather-Based Skincare Tips"):
    with st.spinner("Fetching weather data..."):
        weather = get_weather(city,)
    
    if "error" not in weather:
        skincare_tips = skincare_recommendations(skin_type, weather, user_input)
        st.markdown(f"""
            <div class="custom-card">
                <h3>✅ Weather-Based Skincare Tips</h3>
                <p>🌡️ <b>Temperature:</b> {weather['temperature']}°C</p>
                <p>💧 <b>Humidity:</b> {weather['humidity']}%</p>
                <p>🌤️ <b>Condition:</b> {weather['condition'].capitalize()}</p>
                <p>{skincare_tips}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Unable to fetch weather data. Please check your city name.")

# Diet Recommendations Button
if st.button("🍽️ Get Personalized Diet Plan"):
    with st.spinner("Generating diet plan..."):
        diet_plan = get_diet_recommendations(gender, age, skin_type, user_input)

    st.markdown(f"""
        <div class="custom-card">
            <h3>✅ AI-Powered Diet Recommendations</h3>
            <p>{diet_plan}</p>
        </div>
    """, unsafe_allow_html=True)

# Skincare Product Recommendations Button
if st.button("🔍 Get Product Recommendations"):
    with st.spinner("Fetching skincare products..."):
        recommended_products = fetch_products_from_dataset(skin_type, user_input)

    if not recommended_products.empty:
        st.subheader("🛍️ Recommended Skincare Products")
        for _, row in recommended_products.iterrows():
            st.markdown(f"""
                <div class="custom-card">
                    <h3>{row['ProductId']}</h3> 
                    <p>🛒 <b>Type:</b> {row['ProductType']}</p>
                    <p>⭐ <b>Rating:</b> {row['Rating']}</p>
                    <p><a href='{row['URL']}' target='_blank'>🔗 View Product</a></p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ No matching products found. Try refining your skin concerns.")

# Close Main Container
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
