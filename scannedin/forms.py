# Registration form taken from web
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, AttendanceSession


class RegisterForm(forms.Form):
    # Registration fields required by the project
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        # Normalize email and prevent duplicate account creation
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        # Ensure both password fields match
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    # Simple login form (using email + password)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class QuickAttendanceSetupForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = ["course_name", "class_name", "duration_minutes"]
        widgets = {
            "course_name": forms.TextInput(attrs={"placeholder": "e.g., CS101"}),
            "class_name": forms.TextInput(attrs={"placeholder": "e.g., Class 1"}),
            "duration_minutes": forms.NumberInput(attrs={"min": 1, "max": 180}),
        }

    def clean_duration_minutes(self):
        minutes = self.cleaned_data["duration_minutes"]
        if minutes < 1 or minutes > 180:
            raise forms.ValidationError("Duration must be between 1 and 180 minutes.")
        return minutes