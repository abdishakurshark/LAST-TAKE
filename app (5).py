import streamlit as st
import subprocess
import sys
import os

# ===== 1. INSTALL DEPENDENCIES FIRST =====
def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk", "scikit-learn"])
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except Exception as e:
        st.error(f"Installation failed: {e}")

install_dependencies()

# ===== 2. NOW IMPORT LIBRARIES =====
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import random

# ===== 3. LOAD MODEL =====
@st.cache_resource
def load_model():
    try:
        with open('fitbot_model.pkl', 'rb') as f:
            data = pickle.load(f)
        return data['vectorizer'], data['model']
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None, None

# ===== 4. TEXT PROCESSING =====
class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess(self, text):
        try:
            tokens = word_tokenize(text.lower())
            tagged = pos_tag(tokens)
            processed = []
            for word, tag in tagged:
                if word.isalpha() and word not in self.stop_words:
                    pos = tag[0].lower()
                    pos = pos if pos in ['a', 'r', 'n', 'v'] else 'n'
                    processed.append(self.lemmatizer.lemmatize(word, pos))
            return ' '.join(processed)
        except Exception:
            return text.lower()  # Fallback

# ===== 5. RESPONSE GENERATOR =====
def generate_response(label):
    responses = {
        'workout': [
            "Do 3 sets of planks (30-60 sec)",
            "Try push-ups for chest strength",
            "Squats and lunges build leg muscles"
        ],
        'diet': [
            "Eat protein-rich foods for muscle growth",
            "Vegetables and lean meats aid weight loss",
            "Stay hydrated with 2-3L water daily"
        ],
        'gym': [
            "Wipe equipment after use",
            "Ask trainers for machine guidance",
            "Avoid peak hours (5-8PM)"
        ]
    }
    return random.choice(responses.get(label, ["I can help with workouts, diet, or gym tips!"]))

# ===== 6. STREAMLIT APP =====
def main():
    st.title("FitBot 💪")
    st.write("Ask me about fitness, nutrition, or gyms!")
    
    vectorizer, model = load_model()
    if vectorizer is None or model is None:
        return  # Error already shown
    
    preprocessor = TextPreprocessor()
    user_input = st.text_input("Your question:")
    
    if user_input:
        with st.spinner("Thinking..."):
            try:
                processed = preprocessor.preprocess(user_input)
                vec = vectorizer.transform([processed])
                pred = model.predict(vec)[0]
                response = generate_response(pred)
                st.success(f"FitBot: {response}")
                st.info(f"Category: {pred}")
            except Exception as e:
                st.error("Sorry, I encountered an error. Try a different question.")

if __name__ == "__main__":
    main()
