from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from django.contrib.auth import authenticate


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "users/profile.html", {"form": form})
