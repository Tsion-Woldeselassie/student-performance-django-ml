from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentRegistrationForm
from .models import StudentProfile, PredictionResult
from custom_admin.models import Course
from .forms import StudentPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# ML predictor (safe import)
try:
    from ml_model.predictor import predict_performance
except Exception:
    def predict_performance(features):
        # Fallback if model isn't trained yet
        return 'Unknown', 0.0

def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student registered successfully! Please log in.")
            return redirect("student_login")
    else:
        form = StudentRegistrationForm()
    return render(request, "students/register.html", {"form": form})

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        contact = request.POST.get('mobile')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
            return render(request, 'students/reset_password.html')

        try:
            # Find user by email
            user = User.objects.get(email=email)
            # Check if contact matches in profile
            profile = StudentProfile.objects.get(user=user, contact=contact)

            # Update password
            user.password = make_password(new_password)
            user.save()

            messages.success(request, "✅ Your password has been successfully changed.")
            return redirect('student_login')  # redirect to login page

        except (User.DoesNotExist, StudentProfile.DoesNotExist):
            messages.error(request, "❌ Invalid email or mobile number.")

    return render(request, 'students/reset_password.html')

def student_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("student_profile")
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "students/login.html", {"form": form})

def student_logout(request):
    logout(request)
    return redirect("student_login")

@login_required
def student_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, "students/profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    courses = Course.objects.all()  # for dropdown

    if request.method == "POST":
        # Update User model fields
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update StudentProfile fields
        profile.contact = request.POST.get("contact")
        profile.address = request.POST.get("address")

        year = request.POST.get("year")
        if year:
            profile.year = int(year)

        course_id = request.POST.get("course")
        if course_id:
            try:
                profile.course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                pass

        profile.save()

        return redirect("student_profile")  # after save, redirect to profile page

    return render(request, "students/edit_profile.html", {
        "profile": profile,
        "courses": courses
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = StudentPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "✅ Password updated successfully!")
            return redirect('student_profile')  # Redirect to profile after success
        else:
            messages.error(request, "❌ Please fix the errors below.")
    else:
        form = StudentPasswordChangeForm(user=request.user)

    return render(request, 'students/change_password.html', {'form': form})

@login_required
def predict_view(request):
    profile = StudentProfile.objects.get(user=request.user)
    if request.method == "POST":
        attendance = float(request.POST.get('attendance', profile.attendance))
        study_hours = float(request.POST.get('study_hours', profile.study_hours))
        past_score = float(request.POST.get('past_score', profile.past_score))
        assignments = int(request.POST.get('assignments_submitted', profile.assignments_submitted))
        extracurricular = int(request.POST.get('extracurricular', profile.extracurricular))

        features = [attendance, study_hours, past_score, assignments, extracurricular]
        result, prob = predict_performance(features)

        PredictionResult.objects.create(
            student=profile,
            predicted_grade=result,
            probability=prob
        )
        return render(request, "students/result.html", {
            "result": result,
            "probability": round(prob * 100, 2)
        })
    return render(request, "students/predict_form.html", {"profile": profile})

@login_required
def student_prediction_history(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        student_profile = None

    predictions = PredictionResult.objects.filter(student=student_profile).order_by("-created_at")

    # Convert probability (0–1) into percentage
    labels = [p.created_at.strftime("%Y-%m-%d %H:%M") for p in predictions]
    values = [round(p.probability * 100, 2) for p in predictions]  # 👈 multiply by 100
    grades = [p.predicted_grade for p in predictions]

    return render(request, "students/prediction_history.html", {
        "predictions": predictions,
        "labels": labels,
        "values": values,
        "grades": grades,
    })
