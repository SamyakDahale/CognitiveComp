import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Set GOOGLE_APPLICATION_CREDENTIALS path if not set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebase_key.json"

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
import sidebar


st.set_page_config(
    page_title="Add Insurance Plan",
    layout="wide",
)

sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("companystyle.css")

# ---------- Top Navigation ----------
st.markdown('<div class="top-bar">Insurance Admin Dashboard</div>', unsafe_allow_html=True)
st.markdown("📄 Add New Insurance Plan")

# ---------- Form Layout ----------
with st.form("insurance_form"):
    col1, col2 = st.columns(2)

    with col1:
        insurance_name = st.text_input("Insurance Plan Name")
        ExistingDiagnosis = st.text_area("Pre-existing diseases covered")
        Med_Condition = st.text_input("Medical Condition covered")
        premium = st.number_input("Premium (per 10L of SA (in ₹))", min_value=0)

    with col2:
        addons = st.text_area("Addon")
        health_score = st.slider(" Minimum Health Score required", 0.0, 5.0, 2.0)
        description = st.text_area("Description")

    submitted = st.form_submit_button("➕ Add Insurance Plan")
    if submitted:
        if "username" not in st.session_state:
            st.error("⚠️ Company name not found in session. Please log in again.")
        else:
            # Structure the data
            insurance_data = {
                "insurance_name": insurance_name,
                "existing_diagnosis": ExistingDiagnosis,
                "medical_condition": Med_Condition,
                "premium": premium,
                "addons": addons,
                "min_health_score": health_score,
                "description": description,
                "company_name": st.session_state["username"]
            }

            try:
                db.collection("INSURANCE_PLANS").add(insurance_data)
                st.success("✅ Insurance Plan added successfully!")
            except Exception as e:
                st.error(f"❌ Failed to add plan: {e}")

      