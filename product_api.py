import pandas as pd


# Function to load dataset from GitHub

def load_data():
    url = "https://raw.githubusercontent.com/KattaAkshaya/skincare-dataset/main/cleaned_skincare_products.csv.gz"
    return pd.read_csv(url, compression="gzip")

# Load dataset
df = load_data()

# Clean column names
df.columns = df.columns.str.strip()

# Ensure required columns exist
required_columns = {"ProductId", "ProductType", "Rating", "URL"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing required columns in dataset: {missing_columns}")

# Mapping of skin concerns to relevant product types
concern_to_product = {
    "Acne": ["Face Wash & Cleansers", "Face Serum", "Sunscreen"],
    "Oily": ["Face Wash & Cleansers", "Sunscreen", "Face Serum"],
    "Dry": ["Cream & Moisturizer", "Body Lotion", "Face Serum"],
    "Dark Spots": ["Face Serum", "Sunscreen", "Cream & Moisturizer"],
    "Sensitive": ["Face Wash & Cleansers", "Cream & Moisturizer", "Sunscreen"],
    "Normal": ["Face Wash & Cleansers", "Sunscreen", "Face Serum"],
    "Redness": ["Cream & Moisturizer", "Face Serum"],
    "Wrinkles": ["Face Serum", "Cream & Moisturizer", "Anti-Aging Cream"],
    "Hyperpigmentation": ["Face Serum", "Sunscreen"],
    "Blackheads": ["Face Wash & Cleansers", "Face Serum", "Exfoliating Scrub"],
    "Whiteheads": ["Face Wash & Cleansers", "Face Serum"],
    "Sunburn": ["Sunscreen", "Body Lotion", "Aloe Vera Gel"],
    "Pores": ["Face Wash & Cleansers", "Face Serum", "Toner"],
    "Eczema": ["Cream & Moisturizer", "Body Lotion", "Hydrating Balm"],
    "Rosacea": ["Face Wash & Cleansers", "Cream & Moisturizer", "Soothing Gel"],
    "Dull Skin": ["Face Serum", "Sunscreen", "Cream & Moisturizer", "Vitamin C Serum"],
    "Uneven Texture": ["Face Serum", "Face Wash & Cleansers", "Exfoliating Scrub"],
    "Dark Circles": ["Face Serum", "Cream & Moisturizer", "Eye Cream"],
    "Dehydration": ["Hydrating Serum", "Face Mist", "Cream & Moisturizer"],
    "Fine Lines": ["Anti-Aging Serum", "Cream & Moisturizer", "Retinol Cream"],
    "Sagging Skin": ["Firming Serum", "Collagen Cream", "Anti-Aging Moisturizer"],
    "Sensitive to Sun": ["Sunscreen", "Hydrating Moisturizer", "Soothing Gel"],
    "Redness & Irritation": ["Calming Serum", "Soothing Gel", "Sensitive Skin Moisturizer"],
    "Bumpy Skin": ["Exfoliating Scrub", "AHA/BHA Toner", "Face Serum"],
    "Flaky Skin": ["Hydrating Cream", "Exfoliating Scrub", "Face Oil"],
    "Chapped Lips": ["Lip Balm", "Lip Scrub", "Hydrating Lip Mask"],
    "Skin Barrier Damage": ["Barrier Repair Cream", "Ceramide Moisturizer", "Hydrating Serum"],
    "Tanning": ["Sunscreen", "Detan Face Pack", "Brightening Serum"],
    "Uneven Skin Tone": ["Vitamin C Serum", "Brightening Moisturizer", "Exfoliating Mask"],
    "Rough Patches": ["Exfoliating Scrub", "Body Butter", "Hydrating Balm"],
    "Stretch Marks": ["Body Lotion", "Vitamin E Oil", "Stretch Mark Cream"],
    "Scarring": ["Scar Gel", "Vitamin E Serum", "Healing Balm"],
    "Psoriasis": ["Soothing Balm", "Gentle Cleanser", "Eczema Cream"],
    "Melasma": ["Brightening Serum", "Sunscreen", "Hydroquinone Cream"],
    "Oily T-Zone": ["Oil Control Face Wash", "Mattifying Moisturizer", "Blotting Papers"],
}

# Mapping of skin types to general skincare products
skin_type_to_products = {
    "Oily": ["Face Wash & Cleansers", "Oil-Free Moisturizer", "Mattifying Sunscreen"],
    "Dry": ["Cream & Moisturizer", "Hydrating Serum", "Gentle Cleanser"],
    "Combination": ["Balancing Toner", "Face Serum", "Lightweight Moisturizer"],
    "Sensitive": ["Soothing Cleanser", "Fragrance-Free Moisturizer", "SPF 50 Sunscreen"],
    "Normal": ["Face Wash & Cleansers", "Basic Moisturizer", "Sunscreen"],
}

def fetch_products_from_dataset(skin_type, skin_issues=None, user_concerns=None, min_rating=4):
    skin_issues = [issue.strip().title() for issue in (skin_issues or [])]
    user_concerns_list = [concern.strip().title() for concern in (user_concerns or "").split(",") if concern.strip()]
    relevant_products = set()

    for issue in skin_issues:
        relevant_products.update(concern_to_product.get(issue, []))
    for concern in user_concerns_list:
        relevant_products.update(concern_to_product.get(concern, []))
    if not relevant_products and skin_type in skin_type_to_products:
        relevant_products.update(skin_type_to_products[skin_type])
    
    if not relevant_products:
        return pd.DataFrame()  # Return empty DataFrame if no matches

    filtered_products = df[(df["ProductType"].isin(relevant_products)) & (df["Rating"] >= min_rating)]
    if filtered_products.empty:
        return pd.DataFrame()

    filtered_products = filtered_products.drop_duplicates(subset=["ProductId"])
    diverse_products = (filtered_products.sort_values(by="Rating", ascending=False)
                        .groupby("ProductType").first()
                        .reset_index())
    return diverse_products.sort_values(by="Rating", ascending=False).head(5)
