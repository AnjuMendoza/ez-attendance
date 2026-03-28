from django.shortcuts import render

# Home page view
def home(request):
    return render(request, 'ez_attendance/home.html')