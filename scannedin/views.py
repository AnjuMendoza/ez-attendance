from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm
from .models import UserProfile


def home(request):
    # Existing landing page
    return render(request, "scannedin/home.html")


def register_view(request):
    # Dedicated register page (not side-by-side with login)
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # Create base auth user using email as username for easy login
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )

        # Create related profile for phone + role
        UserProfile.objects.create(
            user=user,
            phone_number=form.cleaned_data.get("phone_number", "").strip(),
            role=form.cleaned_data["role"],
        )

        messages.success(request, "Account created! You can now log in.")
        return redirect("login")

    return render(request, "scannedin/register.html", {"form": form})


def login_view(request):
    # Dedicated login page with prompt to create account
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "scannedin/login.html", {"form": form})


@login_required
def dashboard(request):
    # Basic post-login page for now
    role = getattr(request.user.profile, "role", "unknown")
    return render(request, "scannedin/dashboard.html", {"role": role})


@login_required
def logout_view(request):
    # Standard logout flow
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")