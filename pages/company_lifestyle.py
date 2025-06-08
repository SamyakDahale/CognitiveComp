import streamlit as st
import sidebar



st.set_page_config(
    page_title="Lifestyle Factors",
    layout="wide",
)

sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("companystyle.css")



# ---------- Page Heading ----------
st.markdown("## 🧬 Lifestyle Factors")
st.markdown("Set the percentage impact of lifestyle factors on insurance premiums")

# ---------- Input Fields ----------
with st.form("lifestyle_form"):
    exercise = st.number_input("Exercise (%)", min_value=0, max_value=100, step=1, key="ex")
    smoking = st.number_input("Smoking (%)", min_value=0, max_value=100, step=1, key="sm")
    drinking = st.number_input("Drinking (%)", min_value=0, max_value=100, step=1, key="dr")
    job_hazard = st.number_input("Job Hazard (%)", min_value=0, max_value=100, step=1, key="jh")
    mental_stress = st.number_input("Mental Stress (%)", min_value=0, max_value=100, step=1, key="ms")

    submitted = st.form_submit_button("💾 Save Lifestyle Factors")

    if submitted:
        st.success("✅ Lifestyle factors updated successfully!")
        st.write("### Summary:")
        st.write(f"- **Exercise:** {exercise}%")
        st.write(f"- **Smoking:** {smoking}%")
        st.write(f"- **Drinking:** {drinking}%")
        st.write(f"- **Job Hazard:** {job_hazard}%")
        st.write(f"- **Mental Stress:** {mental_stress}%")
