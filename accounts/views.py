from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from jobs.utils import extract_resume_text, calculate_ats_score
from .models import Profile
from jobs.models import Job, Application


# ==========================
# Register
# ==========================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("login")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        profile = user.profile
        profile.role = role
        profile.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


# ==========================
# Login
# ==========================
def login_view(request):
    if request.user.is_authenticated:
        # If already logged in, redirect properly
        if request.user.profile.role == "candidate":
            return redirect("candidate_dashboard")
        elif request.user.profile.role == "company":
            return redirect("company_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.profile.role == "candidate":
                return redirect("candidate_dashboard")
            elif user.profile.role == "company":
                return redirect("company_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ==========================
# Logout
# ==========================
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ==========================
# Candidate Dashboard
# ==========================
@login_required
def candidate_dashboard(request):
    if request.user.profile.role != "candidate":
        return redirect("company_dashboard")

    applications = Application.objects.filter(candidate=request.user)

    return render(request, "accounts/candidate_dashboard.html", {
        "applications": applications
    })

# ==========================
# Company Dashboard
# ==========================
@login_required
def company_dashboard(request):
    if request.user.profile.role != "company":
        return redirect("candidate_dashboard")

    jobs = Job.objects.filter(company=request.user)

    applications = Application.objects.filter(job__company=request.user)

    total_jobs = jobs.count()
    total_applications = applications.count()
    accepted = applications.filter(status="accepted").count()
    rejected = applications.filter(status="rejected").count()
    pending = applications.filter(status="pending").count()

    return render(request, "accounts/company_dashboard.html", {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "accepted": accepted,
        "rejected": rejected,
        "pending": pending,
        "jobs": jobs
    })


# ==========================
# View Jobs
# ==========================
@login_required
def view_jobs(request):
    jobs = Job.objects.all()

    search_query = request.GET.get("search")
    location_filter = request.GET.get("location")

    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    applied_jobs = Application.objects.filter(
        candidate=request.user
    ).values_list("job_id", flat=True)

    return render(request, "accounts/view_jobs.html", {
        "jobs": jobs,
        "applied_jobs": applied_jobs
    })


# ==========================
# Apply Job
# ==========================
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You already applied.")
        return redirect("view_jobs")

    if request.method == "POST":
        resume = request.FILES.get("resume")

        application = Application.objects.create(
            job=job,
            candidate=request.user,
            resume=resume
        )

        # ---------- ATS SCORE CALCULATION ----------
        try:
            resume_text = extract_resume_text(application.resume.path)
            score = calculate_ats_score(resume_text, job.description)

            application.ats_score = score
            application.save()
        except:
            application.ats_score = 0
            application.save()

        messages.success(request, "Application submitted successfully!")
        return redirect("view_jobs")

    return redirect("view_jobs")


# ==========================
# View Applications (Company)
# ==========================
@login_required
def view_applications(request):
    if request.user.profile.role != "company":
        return redirect("candidate_dashboard")

    applications = Application.objects.filter(job__company=request.user)

    return render(request, "accounts/view_applications.html", {
        "applications": applications
    })


# ==========================
# Create Job
# ==========================
@login_required
def create_job(request):
    if request.user.profile.role != "company":
        return redirect("candidate_dashboard")

    if request.method == "POST":
        Job.objects.create(
            company=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            salary_min=request.POST.get("salary_min"),
            salary_max=request.POST.get("salary_max")
        )

        return redirect("company_dashboard")

    return render(request, "accounts/create_job.html")


# ==========================
# Update Application Status
# ==========================
@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    if application.job.company != request.user:
        return redirect("company_dashboard")

    if status == "accepted":
        application.status = "accepted"
        application.save()
        return redirect("schedule_interview", app_id=application.id)

    application.status = status
    application.save()

    return redirect("view_applications")


# ==========================
# Candidate - My Applications
# ==========================
@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)

    return render(request, "accounts/my_applications.html", {
        "applications": applications
    })


# ==========================
# Delete Job
# ==========================
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.company != request.user:
        return redirect("company_dashboard")

    job.delete()
    return redirect("company_dashboard")


# ==========================
# Schedule Interview
# ==========================
@login_required
def schedule_interview(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == "POST":
        mode = request.POST.get("mode")
        date = request.POST.get("date")
        link = request.POST.get("link")
        location = request.POST.get("location")

        interview_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M")

        application.interview_mode = mode
        application.interview_date = interview_datetime

        if mode == "online":
            application.interview_link = link
            application.interview_location = None
        else:
            application.interview_location = location
            application.interview_link = None

        application.save()

        return redirect("view_applications")

    return render(request, "accounts/schedule_interview.html", {
        "application": application
    })