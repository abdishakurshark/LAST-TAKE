import streamlit as st
import pickle
import random
from io import BytesIO
import base64

# ===== EMBEDDED MODEL (No file loading needed) =====
MODEL_DATA = """
COPY_THE_ENTIRE_CONTENT_OF_fitbot_model.pkl_HERE
"""

# Simple response database
RESPONSES = {
    "workout": [
        "Do 3 sets of 10 push-ups daily",
        "Planks are great for core strength",
        "Try squats for leg muscles"
    ],
    "diet": [
        "Eat more protein for muscle growth",
        "Drink 2L water daily",
        "Vegetables help with weight loss"
    ],
    "gym": [
        "Wipe equipment after use",
        "Ask staff for machine help",
        "Avoid peak hours (5-8PM)"
    ]
}

def load_model():
    try:
        # Decode embedded model
        model_bytes = base64.b64decode(MODEL_DATA)
        return pickle.load(BytesIO(model_bytes))
    except Exception as e:
        st.error(f"Model error: {str(e)}")
        return None

def main():
    st.title("FitBot 💪")
    st.write("Ask about workouts, diet, or gym tips!")
    
    model = load_model()
    if not model:
        return
    
    user_input = st.text_input("Your question:").lower()
    
    if user_input:
        # Simple classification
        if "workout" in user_input or "exercise" in user_input:
            category = "workout"
        elif "diet" in user_input or "food" in user_input:
            category = "diet"
        else:
            category = "gym"
            
        st.success(f"FitBot: {random.choice(RESPONSES[category])}")
        st.info(f"Category: {category}")

if __name__ == "__main__":
    main()
