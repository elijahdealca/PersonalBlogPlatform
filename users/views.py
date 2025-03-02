from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def home(request):
    return render(request, "users/home.html")
# User registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")  # Ensure "home" is a valid URL name
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

# User login
def login_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)  # Built-in Django form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "users/login.html", {"form": form})

# User logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")
