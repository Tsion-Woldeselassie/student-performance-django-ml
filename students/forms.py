from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile
from custom_admin.models import Course  # ✅ import Course
from django.contrib.auth.forms import PasswordChangeForm

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    roll_number = forms.CharField(max_length=20)
    course = forms.ModelChoiceField(   # ✅ dropdown field
        queryset=Course.objects.all(),
        empty_label="-- Select Course --"
    )
    year = forms.IntegerField(min_value=1, max_value=8)
    contact = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea, max_length=500)

    class Meta:
        model = User
        fields = [
            'username', 'email','first_name', 'last_name', 'password1', 'password2',
            'roll_number', 'course', 'year', 'contact', 'address'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data['roll_number'],
                course=self.cleaned_data['course'],  # now saves Course object
                year=self.cleaned_data['year'],
                contact=self.cleaned_data['contact'],
                address=self.cleaned_data['address'],
            )
        return user

class StudentPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))