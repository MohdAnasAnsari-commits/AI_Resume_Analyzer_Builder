📄 Smart Resume Generator & Analyzer

A Flask-based web application that allows users to generate professional resumes using multiple templates and analyze existing resumes to extract skills, suggest job roles, and provide improvement tips.

**********************************************************************************************************************************

🚀 Project Overview

This project provides two main functionalities:

Resume Generator – Create a well-designed resume by filling a form and choosing from different templates.

Resume Analyzer – Upload an existing resume (PDF/DOCX) to analyze skills, job suitability, and get suggestions.

The application is designed with a clean UI, multiple resume templates, and real-time feedback, making it useful for students and job seekers.

*********************************************************************************************************************************

✨ Key Features
📝 Resume Generator

Multiple resume templates:

{ Classic, Modern, Minimal}

Automatic PDF generation

Clean text wrapping (no text cutting)

Download resume instantly

Option to generate again or return to home

🔍 Resume Analyzer

Upload resume in PDF or DOCX

Displays uploaded resume name

Extracts skills automatically

Suggests best matching job role

Shows skill match score

Provides improvement suggestions

🎨 User Interface

Consistent and responsive design

Loader animation during analysis

Clear success and status messages

Simple and user-friendly navigation

**********************************************************************************************************************************

🛠️ Technologies Used

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

PDF Generation: ReportLab

Resume Parsing: PyPDF2, python-docx

**********************************************************************************************************************************

📂 Project Structure
├── app.py
├── skills.py
├── requirements.txt
├── style.css
├── index.html
├── generate.html
├── analyze.html
├── uploads/
└── README.md

**********************************************************************************************************************************

⚙️ How It Works
Resume Generation

User fills resume details in the form.

Selects a resume template.

Backend generates a PDF using ReportLab.

Resume is displayed with a download option.

Resume Analysis

User uploads a resume file.

Text is extracted from PDF/DOCX.

Skills are matched with predefined job roles.

Analysis result and suggestions are displayed.

**********************************************************************************************************************************

▶️ How to Run the Project

Install required packages:

pip install -r requirements.txt


Run the Flask app:

python app.py


Open browser and visit:

http://127.0.0.1:5000/

**********************************************************************************************************************************

🎯 Use Case

College mini project

Resume building for students

Skill analysis for job preparation

Portfolio project for web development

**********************************************************************************************************************************

📌 Future Enhancements (Optional)
More professional templates

Resume score with percentage

User authentication

Online hosting support



