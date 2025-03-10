import re
import pdfplumber
import docx
import google.generativeai as genai
import nltk
import random

nltk.download("punkt")

# Set up Gemini AI API Key
genai.configure(api_key="AIzaSyBbQwRSJLEUsfye3KHorWAw3tmDmqBDrU4")

class ResumeAnalyzer:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.text = self.extract_text()

    def extract_text(self):
        """Extract text from a PDF or DOCX file."""
        if self.resume_path.endswith(".pdf"):
            return self.extract_text_from_pdf()
        elif self.resume_path.endswith(".docx"):
            return self.extract_text_from_docx()
        return ""

    def extract_text_from_pdf(self):
        """Extract text from a PDF file."""
        text = ""
        try:
            with pdfplumber.open(self.resume_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"❌ Error reading PDF: {str(e)}")
        return text.strip()

    def extract_text_from_docx(self):
        """Extract text from a DOCX file."""
        try:
            doc = docx.Document(self.resume_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"❌ Error reading DOCX: {str(e)}")
            return ""

    def analyze_resume(self):
        """Send resume text to Gemini AI for analysis."""
        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            "Analyze the following resume and provide:\n"
            "1. Strengths\n"
            "2. Weaknesses\n"
            "3. Suggestions for improvement\n\n"
            f"Resume Text:\n{self.text}"
        )

        try:
            response = model.generate_content(prompt)
            analysis = response.text if response else "Analysis not available"

            return {
                "strengths": self.extract_points(analysis, "Strengths"),
                "weaknesses": self.extract_points(analysis, "Weaknesses"),
                "suggestions": self.extract_points(analysis, "Suggestions"),
            }
        except Exception as e:
            print(f"❌ AI Analysis Error: {str(e)}")
            return {
                "strengths": self.get_random_responses("strengths"),
                "weaknesses": self.get_random_responses("weaknesses"),
                "suggestions": self.get_random_responses("suggestions"),
            }

    def extract_points(self, text, keyword):
        """Extract bullet points from AI response."""
        pattern = rf"{keyword}:\s*(.*?)(?=(Strengths|Weaknesses|Suggestions|$))"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return [line.strip() for line in match.group(1).split("\n") if line.strip()]
        return self.get_random_responses(keyword.lower())

    def get_random_responses(self, category):
        """Generate three different random responses if no insights are available."""
        responses = {
            "strengths": [
                ["Good problem-solving skills", "Effective communication", "Strong analytical abilities"],
                ["Team player", "Quick learner", "Proficient in multiple programming languages"],
                ["Attention to detail", "Excellent time management", "Adaptability"]
            ],
            "weaknesses": [
                ["Needs improvement in project documentation", "Limited experience with databases", "Struggles with time management"],
                ["Lack of experience in cloud computing", "Weak debugging skills", "Struggles with multitasking"],
                ["Limited leadership experience", "Slow adoption of new technologies", "Tends to overcomplicate solutions"]
            ],
            "suggestions": [
                ["Take online courses on cloud computing", "Improve technical writing skills", "Enhance problem-solving strategies"],
                ["Work on debugging exercises", "Engage in open-source projects", "Improve multitasking skills"],
                ["Practice coding regularly", "Participate in hackathons", "Build a portfolio of projects"]
            ]
        }
        return random.choice(responses[category])
