from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from food.models import Food, Like

from .forms import SignUpForm, UserProfileForm, UserUpdateForm
from .models import User, UserProfile


def sign_up(request):
    if not request.user.is_authenticated:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully")
                return redirect("foods")
        return render(request, "users/sign_up.html", {"form": form})
    else: 
        return redirect("foods")


def profile(request, username):
    user_profile = UserProfile.objects.get(user__username=username)
    foods = Food.objects.filter(user__username=username)
    tab = "foods"
    if "tab" in request.GET:
        tab = request.GET.get("tab")
        if tab == "liked-foods":
            likes = Like.objects.filter(user=request.user)
            foods = map(lambda like:like.food, likes)
        elif tab == "foods":
            foods = Food.objects.filter(user__username=username)
    return render(request, "users/user_profile.html", {"user_profile":user_profile, "foods":foods, "tab":tab})


@login_required()
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("user_profile", username=profile.user.username)
    else:
        return render(request, "users/edit_profile.html", {"form": form})


@login_required()
def edit_user(request):
    user = User.objects.get(username=request.user.username)
    form = UserUpdateForm(instance=user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully")
            return redirect("edit_user")
    return render(request, "users/edit_user.html", {"form": form})


@login_required()
def delete_user(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        user.delete()
        return redirect("foods")
    return render(request, "users/delete_user.html")

