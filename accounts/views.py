from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages



# def login_view(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('officers_affairs/officers_home')  # إعادة التوجيه إلى الصفحة الرئيسية أو أي صفحة أخرى
#     else:
#         form = CustomLoginForm()
    
#     return render(request, 'accounts/login.html', {'form': form})





@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after changing password
            messages.success(request, 'تم تغيير كلمة المرور بنجاح.')
            return redirect('home')  # Redirect to a success page or another appropriate page
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})