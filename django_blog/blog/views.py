from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from .forms import UserEditForm, ProfileEditForm, CommentForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

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

#posts views #
class PostsListView (ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


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
    fields = ['title', 'content', 'tag']
    login_url = 'login'
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        if self.request.user == self.get_object().author:
            post = self.get_object()
            return self.request.user == post.author

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
        
# comments views #
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        response = super().form_valid(form)
        return redirect('post_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
        
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment_edit.html'
    fields = ['content']
    login_url = 'login'
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        if self.request.user == self.get_object().author:
            comment = self.get_object()
            return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        if self.request.user == self.get_object().author:
            comment = self.get_object()
            return self.request.user == comment.author
        
class CommentListView(ListView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'
    login_url = 'login'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])
    
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)

class PostByTagView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(tag__name=tag)


def search_posts(query):
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return results


