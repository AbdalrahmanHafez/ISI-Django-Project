from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from officers_affairs.models import Officer
from .forms import CustomPasswordChangeForm, OfficerProfileForm, UserProfileForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages






@login_required  # Ensure the user is logged in
def profile_view(request):
    try:
        officer_instance = request.user.officer_profile  # This might raise an exception
    except Officer.DoesNotExist:
        officer_instance = None  # Handle case where officer does not exist

    user_form = UserProfileForm(instance=request.user)
    
    # Create an OfficerProfileForm instance if the officer exists
    officer_form = OfficerProfileForm(instance=officer_instance) if officer_instance else OfficerProfileForm()

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        officer_form = OfficerProfileForm(request.POST, request.FILES, instance=officer_instance)

        if user_form.is_valid() and officer_form.is_valid():
            user_form.save()
            # Save officer instance only if it exists or create a new one
            if officer_instance:
                officer_form.save()
            else:
                # If officer does not exist, create a new instance
                new_officer = Officer(user=request.user)
                new_officer.profile_image = officer_form.cleaned_data.get('profile_image')
                new_officer.save()
            return redirect('home')  # Redirect after successful save

    context = {
        'user_form': user_form,
        'officer_form': officer_form,
    }
    return render(request, 'accounts/profile.html', context)



@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تغيير كلمة المرور بنجاح.')
            return redirect('login')  # Redirect to a success page or another appropriate page
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})