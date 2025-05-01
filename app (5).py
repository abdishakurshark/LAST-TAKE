
import streamlit as st
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import random

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load model
@st.cache_resource
def load_model():
    with open('fitbot_model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['vectorizer'], data['model']

# Preprocessing
class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)
        processed = []
        for word, tag in tagged:
            if word.isalpha() and word not in self.stop_words:
                pos = tag[0].lower()
                pos = pos if pos in ['a', 'r', 'n', 'v'] else 'n'
                processed.append(self.lemmatizer.lemmatize(word, pos))
        return ' '.join(processed)

# Response Generator
def generate_response(query, label):
    workout_responses = [
        "Try 3 sets of planks (30-60 sec each).",
        "Push-ups & bench press are great for chest.",
        "Bodyweight squats & lunges need no equipment."
    ]
    diet_responses = [
        "Eat lean protein & veggies for weight loss.",
        "Chicken, eggs, and tofu are high in protein.",
        "Carbs post-workout help muscle recovery."
    ]
    gym_responses = [
        "Wipe machines after use & re-rack weights.",
        "Ask staff if unsure about equipment.",
        "Peak hours: 5-8 PM (try mornings)."
    ]
    if label == 'workout':
        return random.choice(workout_responses)
    elif label == 'diet':
        return random.choice(diet_responses)
    else:
        return random.choice(gym_responses)

# Streamlit App
def main():
    st.title("FitBot 💪")
    st.write("Ask me about workouts, diet, or gym tips!")
    
    vectorizer, model = load_model()
    preprocessor = TextPreprocessor()
    
    user_input = st.text_input("Your question:")
    
    if user_input:
        processed = preprocessor.preprocess(user_input)
        vec = vectorizer.transform([processed])
        pred = model.predict(vec)[0]
        
        response = generate_response(user_input, pred)
        st.success(f"FitBot says: {response}")
        st.info(f"Category: {pred}")

if __name__ == "__main__":
    main()
