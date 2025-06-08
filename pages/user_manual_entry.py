import streamlit as st
import sidebar
sidebar.render_sidebar()

# === Load External CSS ===
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("userstyle.css")

st.subheader("🧪 Medical Test Results")

# === Manual Entry Fields ===
blood_glucose = st.text_input("Blood Glucose")
hb_a1c = st.text_input("HbA1c")
systolic_bp = st.text_input("Systolic Blood Pressure")
diastolic_bp = st.text_input("Diastolic Blood Pressure")
cholesterol = st.text_input("Cholesterol")
heart_rate = st.text_input("Heart Rate")
bmi = st.text_input("BMI")

# === Optional Upload ===
st.markdown("### 📎 Upload Test Report (optional)")
uploaded_file = st.file_uploader("Upload PDF or Image (JPG, JPEG)", type=["pdf", "jpg", "jpeg"])

# === Submit Button ===
if st.button("Submit"):
    st.success("Manual data saved successfully!")
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# === Close any open container tag if used ===
st.markdown('</div>', unsafe_allow_html=True)
