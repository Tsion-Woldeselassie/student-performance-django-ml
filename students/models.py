from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey("custom_admin.Course", on_delete=models.SET_NULL, null=True) 
    year = models.IntegerField()
    contact = models.CharField(max_length=15)
    address = models.TextField()
    # ML-related fields (optional for later analytics)
    attendance = models.FloatField(default=0.0)
    study_hours = models.FloatField(default=0.0)
    past_score = models.FloatField(default=0.0)
    assignments_submitted = models.IntegerField(default=0)
    extracurricular = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class PredictionResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    predicted_grade = models.CharField(max_length=20)
    probability = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} -> {self.predicted_grade} ({self.probability:.2f})"
