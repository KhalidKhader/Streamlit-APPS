import streamlit as st
import fitz  # PyMuPDF
import docx
import re

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_word(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_information(text):
    def safe_search(pattern, text):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            print(f"Pattern not found: {pattern}")
            return "Not found"

    info = {
        "Name": safe_search(r"Name:\s*(.*)", text),
        "Gender": safe_search(r"Gender:\s*(.*)", text),
        "Age": safe_search(r"Age:\s*(.*)", text),
        "Education": [],
        "Work Experience": []
    }

    education_matches = re.findall(r"Education:\s*(.*)", text)
    for edu in education_matches:
        edu_info = {
            "Academic level": safe_search(r"Academic level:\s*(.*)", edu),
            "Institution": safe_search(r"Institution:\s*(.*)", edu),
            "GPA/Grade": safe_search(r"GPA/Grade:\s*(.*)", edu),
            "Start date": safe_search(r"Start date:\s*(.*)", edu),
            "End date": safe_search(r"End date:\s*(.*)", edu)
        }
        info["Education"].append(edu_info)

    work_matches = re.findall(r"Work Experience:\s*(.*)", text)
    for work in work_matches:
        work_info = {
            "Company": safe_search(r"Company:\s*(.*)", work),
            "Location": safe_search(r"Location:\s*(.*)", work),
            "Role": safe_search(r"Role:\s*(.*)", work),
            "Start date": safe_search(r"Start date:\s*(.*)", work),
            "End date": safe_search(r"End date:\s*(.*)", work),
            "Description": safe_search(r"Description:\s*(.*)", work)
        }
        info["Work Experience"].append(work_info)

    return info



def main():
    st.title("CV Information Extractor")

    uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_word(uploaded_file)
        else:
            st.error("Unsupported file type!")
            return

        info = parse_information(text)
        st.write("### Extracted Information")
        st.json(info)

if __name__ == "__main__":
    main()
