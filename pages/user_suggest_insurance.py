
import streamlit as st
import sidebar
sidebar.render_sidebar()
import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



db = firestore.client()

# === Show stored health data ===
st.subheader("📋 Your Health Summary")

if "health_score" in st.session_state and "medical_conditions" in st.session_state and "existing_diagnosis" in st.session_state:
    health_score = st.session_state.health_score
    medical_conditions = st.session_state.medical_conditions
    existing_diagnosis = st.session_state.existing_diagnosis

    st.markdown(f"- **Health Score**: `{health_score}`")
    st.markdown(f"- **Medical Conditions**: `{', '.join(medical_conditions)}`")
    st.markdown(f"- **Existing Diagnoses**: `{', '.join(existing_diagnosis)}`")
else:
    st.warning("Health data not found in session.")
    st.stop()

# === Suggest Plan Button ===
if st.button("🎯 Suggest Suitable Plans"):
    plans_ref = db.collection("INSURANCE_PLANS").stream()

    plans = []
    similarities = []

    for doc in plans_ref:
        plan = doc.to_dict()
        plan_name = plan.get("insurance_name", "Unnamed Plan")
        plan_health = plan.get("min_health_score", 0)
        plan_conditions = plan.get("medical_condition", [])
        plan_diagnosis = plan.get("existing_diagnosis", [])

        # === Build Binary vectors ===
        match_health = 1 if health_score >= plan_health else 0
        match_condition = 1 if any(cond in medical_conditions for cond in plan_conditions) else 0
        match_diagnosis = 1 if any(diag in existing_diagnosis for diag in plan_diagnosis) else 0

        # User vector and plan vector
        user_vector = np.array([1, 1, 1])  # Always [1, 1, 1] for full preference
        plan_vector = np.array([match_health, match_condition, match_diagnosis])

        similarity = cosine_similarity([user_vector], [plan_vector])[0][0]

        similarities.append((similarity, plan_name, plan))

    # Sort by similarity descending
    similarities.sort(reverse=True, key=lambda x: x[0])

    # === Show Results ===
    if similarities:
        st.success("📑 Plans Matched Based on Your Health Profile:")
        for sim, name, plan in similarities:
            st.markdown(f"### 🛡️ {name}")
            st.markdown(f"- **Match Score**: `{sim:.2f}`")
            st.markdown(f"- **Min Health Score**: `{plan.get('min_health_score')}`")
            st.markdown(f"- **Medical Conditions Covered**: `{', '.join(plan.get('medical_condition', []))}`")
            st.markdown(f"- **Existing Diagnoses Covered**: `{', '.join(plan.get('existing_diagnosis', []))}`")
            st.markdown("---")
    else:
        st.info("No matching plans found.")

