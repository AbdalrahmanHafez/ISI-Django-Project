from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.contenttypes.models import ContentType




def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('officers_affairs/officers_home')  # إعادة التوجيه إلى الصفحة الرئيسية أو أي صفحة أخرى
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})





# @login_required
# def app_dashboard(request):
#     # الحصول على التطبيقات التي يمتلك المستخدم صلاحية الوصول إليها
#     user = request.user
#     apps = []
    
#     # استعراض جميع التطبيقات والموديلات
#     for app in ContentType.objects.all():
#         model = app.model_class()
#         if model and user.has_perm(f'{app.app_label}.view_{app.model}'):
#             apps.append({
#                 'name': model._meta.verbose_name_plural.title(),
#                 'url': f'/admin/{app.app_label}/{app.model}/'
#             })
#     return render(request, 'accounts/app_dashboard.html', {'apps': apps})