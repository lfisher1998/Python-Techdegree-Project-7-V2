from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import (UserRegisterForm, UserUpdateForm,
                    ProfileUpdateForm, PasswordChangeCustomForm)
from django.contrib.auth import update_session_auth_hash
from .models import Profile


def home(request):
    # home view for users with and without profile
    return render(request, 'accounts/home.html')


def sign_up(request):
    # sign up view
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(
                request,
                "You're now a user! Click sign in to log in to your account."
            )
            return redirect('accounts-home')  # TODO: go to profile
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def profile(request):
    # view that brings in the info from forms.py
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request,
                "Your account has been updated!"
            )
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def change_password(request):
    # change current password to new password
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeCustomForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request,
                "Your password has been updated!"
            )
            return redirect('accounts-home')
        
        else:
            return render(request, 'accounts/change_password.html', {'form': form})
        
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})



