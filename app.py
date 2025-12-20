from flask import Flask, request, send_from_directory
import os
import PyPDF2
import docx
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from skills import SKILLS, JOB_ROLES

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= STATIC FILES =================

@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")

# ✅ REQUIRED FOR PREVIEW & DOWNLOAD
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ================= TEXT WRAPPING HELPER =================

def draw_wrapped_text(c, text, x, y, max_width, size=11):
    if not text:
        return y

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = size
    style.leading = size + 4

    para = Paragraph(text.replace("\n", "<br/>"), style)
    w, h = para.wrap(max_width, 800)

    if y - h < 50:
        c.showPage()
        y = 800

    para.drawOn(c, x, y - h)
    return y - h - 10

# ================= RESUME ANALYZER HELPERS =================

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    return text.lower()

def extract_skills(text):
    return [s for s in SKILLS if s in text]

def analyze_job(skills_found):
    best_job = "Not Suitable"
    best_score = 0
    for job, req_skills in JOB_ROLES.items():
        score = len(set(skills_found) & set(req_skills))
        if score > best_score:
            best_score = score
            best_job = job
    suitability = "YES" if best_score >= 2 else "NO"
    return best_job, best_score, suitability

def suggestions(skills_found):
    tips = []
    if "python" not in skills_found:
        tips.append("Learn Python to increase job opportunities.")
    if "sql" not in skills_found:
        tips.append("Add SQL skills for data-related roles.")
    if "projects" not in skills_found:
        tips.append("Mention academic or personal projects.")
    if "internship" not in skills_found:
        tips.append("Add internship or training experience.")
    return tips

# ================= TEMPLATE FUNCTIONS =================

def classic_template(c, data):
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, y, data["name"])
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"{data['email']} | {data['phone']}")
    y -= 15
    if data.get("address"):
        c.drawString(50, y, f"Address: {data['address']}")
        y -= 30
    else:
        y -= 15

    for title, value in [
        ("Introduction", data["intro"]),
        ("Education", data["education"]),
        ("Skills", data["skills"]),
        ("Projects", data["projects"]),
        ("Experience", data["experience"]),
        ("Certifications", data["certifications"]),
        ("Hobbies", data["hobbies"]),
    ]:
        if value:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y, title)
            y -= 15
            y = draw_wrapped_text(c, value, 50, y, width - 100)

def modern_template(c, data):
    width, height = A4

    c.setFillColorRGB(0.4, 0.45, 0.9)
    c.rect(0, 0, 170, height, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 18)

    name_y = height - 50
    name_x = 20
    name_width = 130

    name_y = draw_wrapped_text(
        c, data["name"], name_x, name_y, name_width, size=18
    )

    c.setFont("Helvetica", 10)
    c.drawString(20, name_y - 15, data["email"])
    c.drawString(20, name_y - 30, data["phone"])
    if data.get("address"):
        c.drawString(20, name_y - 45, f"Address: {data['address']}")

    x = 190
    y = height - 60
    max_width = width - x - 40
    c.setFillColorRGB(0, 0, 0)

    for title, value in [
        ("Introduction", data["intro"]),
        ("Education", data["education"]),
        ("Skills", data["skills"]),
        ("Projects", data["projects"]),
        ("Experience", data["experience"]),
        ("Certifications", data["certifications"]),
        ("Hobbies", data["hobbies"]),
    ]:
        if value:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(x, y, title)
            y -= 15
            y = draw_wrapped_text(c, value, x, y, max_width)

def minimal_template(c, data):
    width, height = A4
    y = height - 80

    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, y, data["name"])
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, y, f"{data['email']} | {data['phone']}")
    y -= 15
    if data.get("address"):
        c.drawCentredString(width / 2, y, f"Address: {data['address']}")
        y -= 30
    else:
        y -= 30

    c.line(50, y, width - 50, y)
    y -= 30

    for title, value in [
        ("Introduction", data["intro"]),
        ("Education", data["education"]),
        ("Skills", data["skills"]),
        ("Projects", data["projects"]),
        ("Experience", data["experience"]),
        ("Certifications", data["certifications"]),
        ("Hobbies", data["hobbies"]),
    ]:
        if value:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, title)
            y -= 15
            y = draw_wrapped_text(c, value, 50, y, width - 100)

# ================= NEW TEMPLATE FUNCTIONS (ADDED ONLY) =================

def elegant_template(c, data):
    width, height = A4
    y = height - 60

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, y, data["name"])
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"{data['email']} | {data['phone']}")
    y -= 15
    if data.get("address"):
        c.drawString(50, y, f"Address: {data['address']}")
        y -= 25
    else:
        y -= 15

    for title, value in [
        ("Profile", data["intro"]),
        ("Education", data["education"]),
        ("Skills", data["skills"]),
        ("Projects", data["projects"]),
        ("Experience", data["experience"]),
        ("Certifications", data["certifications"]),
        ("Hobbies", data["hobbies"]),
    ]:
        if value:
            c.line(50, y, width - 50, y)
            y -= 15
            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y, title)
            y -= 15
            y = draw_wrapped_text(c, value, 50, y, width - 100)

def corporate_template(c, data):
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, y, data["name"])
    y -= 25

    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, y, f"{data['email']} | {data['phone']}")
    y -= 20
    if data.get("address"):
        c.drawCentredString(width / 2, y, f"Address: {data['address']}")
        y -= 30
    else:
        y -= 20

    for title, value in [
        ("Professional Summary", data["intro"]),
        ("Education", data["education"]),
        ("Technical Skills", data["skills"]),
        ("Projects", data["projects"]),
        ("Experience", data["experience"]),
        ("Certifications", data["certifications"]),
        ("Hobbies", data["hobbies"]),
    ]:
        if value:
            c.setFont("Helvetica-Bold", 13)
            c.drawString(60, y, title)
            y -= 15
            y = draw_wrapped_text(c, value, 60, y, width - 120)

# ================= ROUTES =================

@app.route("/")
def index():
    return open("index.html", encoding="utf-8").read()

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        file = request.files.get("resume")
        if not file or file.filename == "":
            return "<h2>No file selected</h2><a href='/analyze'>Go Back</a>"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        text = extract_text(filepath)
        skills_found = extract_skills(text)
        job, score, suitable = analyze_job(skills_found)
        tips = suggestions(skills_found)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume Analysis</title>
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>
        <div class="container">
            <div class="home-card">
                <h1>📊 Resume Analysis Result</h1>
                <p><b>Suggested Job Role:</b> {job}</p>
                <p><b>Skill Match Score:</b> {score}</p>
                <p><b>Job Suitable:</b> {suitable}</p>

                <h3>🛠 Skills Found</h3>
                <p>{', '.join(skills_found) if skills_found else 'No skills detected'}</p>

                <h3>📝 Suggestions</h3>
                <ul>
                    {''.join(f"<li>{t}</li>" for t in tips) if tips else "<li>Your resume looks good 👍</li>"}
                </ul>

                <a href="/analyze" class="generate-btn">🔄 Analyze Another</a>
                <a href="/" class="generate-btn">🏠 Back to Home</a>
            </div>
        </div>
        </body>
        </html>
        """
    return open("analyze.html", encoding="utf-8").read()

@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "education": request.form.get("education"),
            "intro": request.form.get("intro"),
            "skills": request.form.get("skills"),
            "projects": request.form.get("projects"),
            "experience": request.form.get("experience"),
            "certifications": request.form.get("certifications"),
            "hobbies": request.form.get("hobbies"),
        }

        template = request.form.get("template", "classic")
        filename = f"{data['name'].replace(' ', '_')}_resume.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        c = canvas.Canvas(filepath, pagesize=A4)

        if template == "modern":
            modern_template(c, data)
        elif template == "minimal":
            minimal_template(c, data)
        elif template == "elegant":          # ✅ ADDED
            elegant_template(c, data)
        elif template == "corporate":        # ✅ ADDED
            corporate_template(c, data)
        else:
            classic_template(c, data)

        c.save()

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume Preview</title>
            <link rel="stylesheet" href="/style.css">
        </head>
        <body>
        <div class="container">
            <div class="home-card" style="max-width:900px;">
                <h1>👀 Resume Preview</h1>
                <p class="subtitle">Please review your resume before downloading</p>

                <iframe src="/uploads/{filename}"
                        width="100%"
                        height="500px"
                        style="border:1px solid #ccc;border-radius:8px;">
                </iframe>

                <a href="/uploads/{filename}" download class="btn">⬇️ Download Resume</a>
                <a href="/generate" class="generate-btn">🔄 Generate Another</a>
                <a href="/" class="generate-btn">🏠 Back to Home</a>
            </div>
        </div>
        </body>
        </html>
        """

    return open("generate.html", encoding="utf-8").read()

if __name__ == "__main__":
    app.run(debug=True)
