from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from students.models import StudentProfile, PredictionResult # Example model
from custom_admin.models import Course
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.db.models import Count
from django.utils.timezone import localdate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash

@login_required(login_url="/admin-panel/login/")
def dashboard(request):
    total_students = StudentProfile.objects.count()
    total_results = PredictionResult.objects.count()
    total_predictions = PredictionResult.objects.count()

    # Time calculations
    today = localdate()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)

    # Counts
    predictions_all = PredictionResult.objects.all().count()
    predictions_today = PredictionResult.objects.filter(created_at__date=today).count()
    predictions_yesterday = PredictionResult.objects.filter(created_at__date=yesterday).count()
    predictions_last_7 = PredictionResult.objects.filter(created_at__date__gte=last_7_days).count()
    predictions_month = PredictionResult.objects.filter(created_at__month=today.month).count()

    context = {
        "predictions_all":predictions_all,
        "total_students": total_students,
        "total_results": total_results,
        "total_predictions": total_predictions,
        "predictions_today": predictions_today,
        "predictions_yesterday": predictions_yesterday,
        "predictions_last_7": predictions_last_7,
        "predictions_month": predictions_month,
    }
    return render(request, "custom_admin/dashboard.html", context)

@login_required(login_url="/admin-panel/login/")
def prediction_list(request, period=None):
    from datetime import timedelta
    from django.utils.timezone import localdate

    today = localdate()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)

    predictions = PredictionResult.objects.select_related('student', 'student__user').order_by('-created_at')

    if period == "today":
        predictions = predictions.filter(created_at__date=today)
    elif period == "yesterday":
        predictions = predictions.filter(created_at__date=yesterday)
    elif period == "last_7_days":
        predictions = predictions.filter(created_at__date__gte=last_7_days)
    elif period == "this_month":
        predictions = predictions.filter(created_at__month=today.month)

    context = {"predictions": predictions, "period": period}
    return render(request, "custom_admin/prediction_list.html", context)


@login_required(login_url="/admin-panel/login/")
def prediction_detail(request, pk):
    prediction = get_object_or_404(PredictionResult, pk=pk)
    context = {"prediction": prediction}
    return render(request, "custom_admin/prediction_detail.html", context)

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)

            # Only show login success if the user just came directly from login
            if request.POST.get("next") is None:
                messages.info(request, "Login successful!")

            return redirect("admin-dashboard")
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    return render(request, "custom_admin/login.html")


def admin_reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
            return render(request, 'students/reset_password.html')

        try:
            # Find user by email
            user = User.objects.get(email=email)
            # Check if contact matches in profile
           

            # Update password
            user.password = make_password(new_password)
            user.save()

            messages.success(request, "✅ Your password has been successfully changed.")
            return redirect('admin-login')  # redirect to login page

        except (User.DoesNotExist, StudentProfile.DoesNotExist):
            messages.error(request, "❌ Invalid email or mobile number.")

    return render(request, 'custom_admin/reset_password.html')

@login_required(login_url="/admin-panel/login/")
def admin_logout(request):
    logout(request)
    return redirect("admin-login")

@login_required(login_url="/admin-panel/login/")
def admin_profile(request):
    user = request.user

    if request.method == "POST":
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Update user fields
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "✅ Profile updated successfully!")
        return redirect('admin_profile')

    return render(request, "custom_admin/admin_profile.html", {'user': user})

@login_required(login_url="/admin-panel/login/")
def admin_change_password(request):
    user = request.user

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check current password
        if not check_password(current_password, user.password):
            messages.error(request, "❌ Current password is incorrect.")
            return redirect("admin_change_password")

        # Check match
        if new_password != confirm_password:
            messages.error(request, "❌ New password and confirm password do not match.")
            return redirect("admin_change_password")

        # Update password
        user.set_password(new_password)   # recommended
        user.save()

        # Keep user logged in
        update_session_auth_hash(request, user)

        messages.success(request, "✅ Password changed successfully!")
        return redirect("admin_change_password")

    return render(request, "custom_admin/admin_change_password.html")


@login_required(login_url="/admin-panel/login/")
def student_list(request):
    students = StudentProfile.objects.all()
    return render(request, "custom_admin/student_list.html", {"students": students})

@login_required(login_url="/admin-panel/login/")
def delete_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("admin-dashboard")


@login_required(login_url="/admin-panel/login/")
def view_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    return render(request, "custom_admin/view_student.html", {"student": student})

@login_required(login_url="/admin-panel/login/")
def predict_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)

    # Fetch all past predictions
    predictions = PredictionResult.objects.filter(student=student).order_by("-created_at")

    return render(request, "custom_admin/prediction_result.html", {
        "student": student,
        "predictions": predictions
    })




@login_required(login_url="/admin-panel/login/")
def course_list(request):
    courses = Course.objects.all()
    return render(request, "custom_admin/course_list.html", {"courses": courses})

@login_required(login_url="/admin-panel/login/")
def add_course(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        description = request.POST.get("description")

        if not name:
            messages.error(request, "❌ Course name is required.")
            return redirect("add-course")

        # Check if course already exists (case-insensitive)
        if Course.objects.filter(name__iexact=name).exists():
            messages.error(request, f"⚠️ Course '{name}' already exists.")
            return redirect("add-course")

        # Create new course
        Course.objects.create(name=name, description=description)
        messages.success(request, f"✅ Course '{name}' added successfully.")
        return redirect("course-list")

    return render(request, "custom_admin/add_course.html")

@login_required(login_url="/admin-panel/login/")
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.name = request.POST.get("name")
        course.description = request.POST.get("description")
        course.save()
        return redirect("course-list")
    return render(request, "custom_admin/edit_course.html", {"course": course})

@login_required(login_url="/admin-panel/login/")
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("course-list")
