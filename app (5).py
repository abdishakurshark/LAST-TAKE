import streamlit as st
import random

# Updated YouTube video database with verified links
YT_VIDEOS = {
    "weight_loss": {
        "title": "The Science of Fat Loss",
        "url": "https://www.youtube.com/watch?v=wpBSlBcxN4E",
        "channel": "Jeff Nippard"
    },
    "muscle_gain": {
        "title": "Hypertrophy Made Simple",
        "url": "https://www.youtube.com/watch?v=g3H9q5Qf_4E",
        "channel": "Renaissance Periodization"
    },
    "full_body": {
        "title": "Perfect Full Body Workout",
        "url": "https://www.youtube.com/watch?v=JEEG0hBNk3E",
        "channel": "Athlean-X"
    },
    "leg_day": {
        "title": "Complete Leg Workout",
        "url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
        "channel": "Jeremy Ethier"
    },
    "push_day": {
        "title": "Push Day Routine",
        "url": "https://www.youtube.com/watch?v=1f8yoFFdkcY",
        "channel": "Scott Herman Fitness"
    },
    "pull_day": {
        "title": "Ultimate Pull Day",
        "url": "https://www.youtube.com/watch?v=6kALZikXxLc",
        "channel": "Jeff Nippard"
    },
    "hiit": {
        "title": "20 Minute HIIT Workout",
        "url": "https://www.youtube.com/watch?v=ml6cT4AZdqI",
        "channel": "Fitness Blender"
    }
}

# Enhanced workout plans
WORKOUT_PLANS = {
    "beginner": {
        "full_body": [
            "Squats: 3x8-10",
            "Push-ups: 3x8-10",
            "Rows: 3x8-10",
            "Plank: 3x30sec"
        ],
        "video": YT_VIDEOS["full_body"]
    },
    "intermediate": {
        "leg_day": [
            "Back Squats: 4x6-8",
            "Romanian Deadlifts: 3x8-10",
            "Bulgarian Split Squats: 3x8/side",
            "Calf Raises: 3x12-15"
        ],
        "push_day": [
            "Bench Press: 4x6-8",
            "Overhead Press: 3x8-10",
            "Incline Dumbbell Press: 3x10-12",
            "Triceps Dips: 3xAMRAP"
        ],
        "pull_day": [
            "Pull-ups: 4x6-8",
            "Barbell Rows: 3x8-10",
            "Face Pulls: 3x12-15",
            "Hammer Curls: 3x10-12"
        ],
        "video": YT_VIDEOS["pull_day"]
    },
    "advanced": {
        "leg_day": [
            "Front Squats: 5x5",
            "Sumo Deadlifts: 4x6",
            "Leg Press: 3x8-10 (drop set last set)",
            "Walking Lunges: 3x12/side"
        ],
        "push_day": [
            "Weighted Dips: 4x6-8",
            "Military Press: 4x6",
            "Incline Flyes: 3x10-12 (superset with push-ups)",
            "Skull Crushers: 3x8-10"
        ],
        "pull_day": [
            "Weighted Pull-ups: 5x5",
            "Pendlay Rows: 4x6",
            "Rear Delt Flyes: 4x12-15",
            "Preacher Curls: 3x8-10"
        ],
        "video": YT_VIDEOS["push_day"]
    },
    "weight_loss": {
        "hiit": [
            "Jump Squats: 40s on/20s off",
            "Burpees: 40s on/20s off",
            "Mountain Climbers: 40s on/20s off",
            "Kettlebell Swings: 40s on/20s off"
        ],
        "circuit": [
            "Push-ups: 15 reps",
            "Bodyweight Squats: 20 reps",
            "Plank Rows: 12/side",
            "Jumping Jacks: 30 reps"
        ],
        "video": YT_VIDEOS["hiit"]
    }
}

# Add a title
st.title("FITBOT 💪 - Ultimate Fitness Planner")

# User information
with st.expander("📝 Enter Your Details"):
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (cm):", min_value=100.0, max_value=250.0, value=170.0)
    with col2:
        goal = st.selectbox("Primary Goal:", ["Weight loss", "Muscle gain", "Maintenance"])
        fitness_level = st.selectbox("Fitness Level:", ["Beginner", "Intermediate", "Advanced"])
    workout_days = st.slider("Workout Days/Week:", 1, 7, 4)

# Workout generator
def generate_workout_plan():
    plan = []
    if goal == "Weight loss":
        if workout_days <= 3:
            plan.append(("Full Body HIIT", WORKOUT_PLANS["weight_loss"]["hiit"]))
        else:
            plan.append(("Upper Body Circuit", WORKOUT_PLANS["weight_loss"]["circuit"]))
            plan.append(("Lower Body HIIT", WORKOUT_PLANS["weight_loss"]["hiit"]))
    else:
        if fitness_level == "Beginner":
            for i in range(workout_days):
                plan.append((f"Full Body Day {i+1}", WORKOUT_PLANS["beginner"]["full_body"]))
        else:
            splits = ["Push", "Pull", "Legs"] if workout_days >= 3 else ["Upper", "Lower"]
            for i in range(workout_days):
                day_type = splits[i % len(splits)]
                plan.append((f"{day_type} Day", WORKOUT_PLANS[fitness_level.lower()][f"{day_type.lower()}_day"]))
    return plan

# BMI Calculation
if st.button("Generate My Fitness Plan"):
    bmi = weight / ((height / 100) ** 2)
    st.subheader(f"Your BMI: {bmi:.2f}")
    
    if bmi < 18.5:
        st.warning("Underweight - Focus on muscle building")
    elif 18.5 <= bmi < 24.9:
        st.success("Healthy weight - Optimize your physique!")
    else:
        st.warning("Overweight - Focus on fat loss")
    
    st.markdown("---")
    
    # Workout Plan
    st.subheader(f"📅 {workout_days}-Day Workout Plan")
    workout_plan = generate_workout_plan()
    
    for day, exercises in workout_plan:
        with st.expander(day):
            for exercise in exercises:
                st.write(f"- {exercise}")
            if "HIIT" in day:
                st.video(YT_VIDEOS["hiit"]["url"])
            elif "Leg" in day:
                st.video(YT_VIDEOS["leg_day"]["url"])
            elif "Push" in day:
                st.video(YT_VIDEOS["push_day"]["url"])
            elif "Pull" in day:
                st.video(YT_VIDEOS["pull_day"]["url"])
            else:
                st.video(YT_VIDEOS["full_body"]["url"])

# Chatbot feature
st.markdown("---")
st.subheader("💬 Ask FitBot")

question = st.text_input("Your fitness question:")
if question:
    question = question.lower()
    if any(w in question for w in ["leg", "quad", "hamstring"]):
        st.write("For leg development, focus on squats, deadlifts, and lunges.")
        st.video(YT_VIDEOS["leg_day"]["url"])
    elif any(w in question for w in ["arm", "bicep", "tricep"]):
        st.write("Arm growth requires both compound and isolation exercises.")
    elif any(w in question for w in ["video", "watch"]):
        st.video(YT_VIDEOS["weight_loss"]["url"])
    else:
        st.write("I can help with workout plans, exercise form, and nutrition advice!")
