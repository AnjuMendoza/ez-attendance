from django.db import models
from django.contrib.auth.models import User

# Basic course model
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

# User profile model for logins
class UserProfile(models.Model):
    # Extra profile fields that Django User does not include by default
    ROLE_STUDENT = "student"
    ROLE_PROFESSOR = "professor"
    ROLE_OTHER = "other"

    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_PROFESSOR, "Professor"),
        (ROLE_OTHER, "Other (Personal use)"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.role}"