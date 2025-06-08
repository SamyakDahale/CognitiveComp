import streamlit as st
import sidebar
sidebar.render_sidebar()

# === Load External CSS ===
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("userstyle.css")

st.subheader("Lifestyle")

# Option labels and corresponding numeric values
options = {
    "Never": 0,
    "Rarely": 1,
    "Occasionally": 2,
    "Frequently": 3,
    "Very Frequently": 4,
    "Always": 5
}

# Inputs
exercise_label = st.selectbox("Exercise", list(options.keys()))
smoking_label = st.selectbox("Smoking", list(options.keys()))
drinking_label = st.selectbox("Drinking", list(options.keys()))
job_hazard_label = st.selectbox("Job Hazard", list(options.keys()))
mental_stress_label = st.selectbox("Mental Stress", list(options.keys()))

if st.button("Submit"):
    # Convert labels to numeric values
    exercise = options[exercise_label]
    smoking = options[smoking_label]
    drinking = options[drinking_label]
    job_hazard = options[job_hazard_label]
    mental_stress = options[mental_stress_label]

    # Adjusted exercise
    adjusted_exercise = 5 - exercise

    # Weights
    weights = {
        "exercise": 0.2,
        "smoking": 0.25,
        "drinking": 0.15,
        "jobHazard": 0.2,
        "mentalStress": 0.2,
    }

    # Calculate weighted sum
    weighted_sum = (
        adjusted_exercise * weights["exercise"] +
        smoking * weights["smoking"] +
        drinking * weights["drinking"] +
        job_hazard * weights["jobHazard"] +
        mental_stress * weights["mentalStress"]
    )

    # Clamp result between 0 and 5
    health_score = max(0, min(5, weighted_sum))

    st.info(f"Your calculated health score is: **{health_score:.2f} / 5**")
