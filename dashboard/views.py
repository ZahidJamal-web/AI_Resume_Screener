from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume
from .forms import ResumeUploadForm
from resume_processing.parser import ResumeAnalyzer
import random

def home(request):
    """Renders the homepage."""
    return render(request, 'index.html')

@login_required
def dashboard(request):
    """Displays all resumes uploaded by the logged-in user."""
    resumes = Resume.objects.filter(user=request.user)

    # Optionally: Generate random scores for demonstration (for example purposes)
    for resume in resumes:
        if not resume.score:
            resume.score = random.randint(50, 80)  # Random score for demonstration
            resume.save()

    return render(request, 'dashboard.html', {'resumes': resumes})

def get_random_responses(category):
    """Generates three different random responses if no insights are available."""
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

@login_required
def upload_resume(request):
    """Handles resume upload and generates random resume analysis."""
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.filename = request.FILES['resume'].name
            resume.save()

            try:
                # Initialize the ResumeAnalyzer for extracting text from the resume
                analyzer = ResumeAnalyzer(resume.resume.path)
                extracted_text = analyzer.extract_text()

                if not extracted_text.strip():
                    raise ValueError("Resume text extraction failed! Ensure file format is supported.")

                # Instead of AI analysis, generate random strengths, weaknesses, and suggestions
                resume.details = {
                    "strengths": get_random_responses("strengths"),
                    "weaknesses": get_random_responses("weaknesses"),
                    "suggestions": get_random_responses("suggestions"),
                }
                resume.save()

                messages.success(request, "Resume uploaded and analyzed successfully!")
                return redirect("dashboard")

            except Exception as e:
                messages.error(request, f"Error processing resume: {str(e)}")
                return redirect("upload_resume")

    else:
        form = ResumeUploadForm()

    return render(request, "upload_resume.html", {"form": form})

@login_required
def view_resume(request, resume_id):
    """Displays the random resume analysis."""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    analysis = resume.details if resume.details else {}

    context = {
        "resume": resume,
        "resume_details": {
            "strengths": analysis.get("strengths", []),
            "weaknesses": analysis.get("weaknesses", []),
            "suggestions": analysis.get("suggestions", []),
        },
    }
    return render(request, "view_resume.html", context)

@login_required
def delete_resume(request, resume_id):
    """View to delete a resume."""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Resume deleted successfully!")
        return redirect('dashboard')  # Redirect to the dashboard after deletion
    return redirect('dashboard')  # If not POST, simply redirect to dashboard