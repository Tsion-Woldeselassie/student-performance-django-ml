from django.contrib import admin
from .models import StudentProfile, PredictionResult

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "course", "year", "contact")
    search_fields = ("user__username", "roll_number", "course")
    list_filter = ("course", "year")

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ("student", "predicted_grade", "probability", "created_at")
    search_fields = ("student__user__username", "predicted_grade")
    list_filter = ("predicted_grade", "created_at")
