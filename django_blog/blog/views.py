from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post
from .forms import UserEditForm, ProfileEditForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    def form_valid(self, form):
        user = form.save()
        
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
            return redirect('profile')
    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


class PostsListView (ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('posts_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    login_url = 'login'
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        if self.request.user == self.get_object().author:
            post = self.get_object()
            return self.request.user == post.author
            return 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts_list')
    context_object_name = 'post'
    login_url = 'login'

    def test_func(self):
        if self.request.user == self.get_object().author:
            post = self.get_object()
            return self.request.user == post.author