from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserEditForm, ProfileEditForm

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    def form_valid(self, form):
        # حفظ المستخدم
        user = form.save()
        
        # إنشاء البروفيل مع بيانات إضافية
        profile = Profile.objects.create(user=user)
        profile.save()
        
        return super().form_valid(form)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'blog/logout.html')

@login_required
def profile_view(request):
    user = get_object_or_404(User, username=request.user.username)
    profile = Profile.objects.get(user=user)
    return render(request, 'blog/profile.html', {
        'user': user,
        'profile': profile,
    })
    


@login_required
def edit_profile(request):
    
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # redirect or show success message
    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
