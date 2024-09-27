import streamlit as st
from PyPDF2 import PdfReader
import docx
import re

# Function to extract text from a PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Improved function to extract personal information
def extract_personal_info(text):
    # Search for name as the first line, typically in the format of two capitalized words
    name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
    
    # Searching for gender (Male/Female)
    gender_match = re.search(r'\b(Male|Female)\b', text, re.IGNORECASE)
    
    # Searching for year of birth or DOB
    dob_match = re.search(r'(Date of Birth|DOB|Born)\s*:\s*(\d{4})', text, re.IGNORECASE)
    
    # Extract name, gender, and age (calculate from year of birth)
    name = name_match.group(1) if name_match else "Not found"
    gender = gender_match.group(1) if gender_match else "Not found"
    
    year_of_birth = int(dob_match.group(2)) if dob_match else None
    age = 2024 - year_of_birth if year_of_birth else "Not found"
    
    return {"Name": name, "Gender": gender, "Age": age}

# Improved function to extract education details
def extract_education(text):
    # Example pattern for degrees, institutions, and GPA
    education_pattern = re.compile(r'(Bachelor|Master|PhD|Degree)\s+in\s+(.*)\n(Institution|University|College)\s*:\s*(.*)\n(GPA|Grade)\s*:\s*(.*)\n(Start|From)\s*:\s*(\d{4})\s*(End|To)\s*:\s*(\d{4})', re.IGNORECASE)
    
    education_matches = education_pattern.findall(text)
    education_list = []
    
    for match in education_matches:
        education_list.append({
            "Degree": match[0],
            "Field": match[1],
            "Institution": match[3],
            "GPA/Grade": match[5],
            "Start Year": match[7],
            "End Year": match[9]
        })
    return education_list

# Improved function to extract work experience details
def extract_work_experience(text):
    # Example pattern for work experience
    work_pattern = re.compile(r'(Company|Employer|Organization)\s*:\s*(.*)\n(Location|Place)\s*:\s*(.*)\n(Role|Position)\s*:\s*(.*)\n(Start|From)\s*:\s*(\d{4})\s*(End|To|Present)\s*:\s*(.*)\n(Description|Details)\s*:\s*(.*)', re.IGNORECASE)
    
    experience_matches = work_pattern.findall(text)
    experience_list = []
    
    for match in experience_matches:
        experience_list.append({
            "Company": match[1],
            "Location": match[3],
            "Role": match[5],
            "Start Year": match[7],
            "End Year": match[9],
            "Description": match[10]
        })
    return experience_list

# Streamlit UI
st.title("Resume Information Extractor")

uploaded_file = st.file_uploader("Upload your resume (PDF or Word)", type=['pdf', 'docx'])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)

    # Extract and display personal information
    personal_info = extract_personal_info(text)
    st.subheader("Personal Information")
    st.write(personal_info)
    
    # Extract and display education details
    education_info = extract_education(text)
    st.subheader("Education Details")
    if education_info:
        for edu in education_info:
            st.write(edu)
    else:
        st.write("No education details found.")
    
    # Extract and display work experience details
    work_experience = extract_work_experience(text)
    st.subheader("Work Experience")
    if work_experience:
        for exp in work_experience:
            st.write(exp)
    else:
        st.write("No work experience found.")

    # Optionally, display the raw text for debugging purposes
    st.subheader("Extracted Text")
    st.text(text)
