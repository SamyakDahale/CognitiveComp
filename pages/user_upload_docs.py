import streamlit as st
import fitz  # PyMuPDF
import requests

# === Load External Sidebar & CSS ===
import sidebar
sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("userstyle.css")

st.subheader("Upload Medical Documents")
file = st.file_uploader("Upload PDF, JPG, or PNG", type=["pdf", "jpg", "png"])

# Sample dictionary of medical terms to extract
medical_keywords = {"asthma", "cancer", "hiv", "tuberculosis", "parkinsons"}

# === PDF TEXT EXTRACTION ===
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# === OCR.SPACE TEXT EXTRACTION ===
def extract_text_from_image(file):
    url = "https://api.ocr.space/parse/image"
    response = requests.post(
        url,
        files={file.name: file},
        data={
            "apikey": "helloworld",  # Replace with your API key from https://ocr.space/ocrapi
            "language": "eng"
        }
    )
    result = response.json()
    if result["IsErroredOnProcessing"]:
        return "OCR Failed"
    return result["ParsedResults"][0]["ParsedText"]

# === Process Upload ===
if file:
    st.success(f"Uploaded: {file.name}")
    extracted_text = ""

    if file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(file.read())
    elif file.type.startswith("image/"):
        extracted_text = extract_text_from_image(file)

    if extracted_text:
        st.markdown("### Extracted Text (Filtered):")
        found_words = [word for word in extracted_text.lower().split() if word in medical_keywords]
        if found_words:
            st.write("**Matched Keywords:**", ", ".join(set(found_words)))
            existing_diagnosis = found_words
            st.session_state.existing_diagnosis = existing_diagnosis
        else:
            st.warning("No medical keywords matched.")
        with st.expander("View Full Extracted Text"):
            st.text(extracted_text)
