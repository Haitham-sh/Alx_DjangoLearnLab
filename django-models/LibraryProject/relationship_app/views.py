from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def list_books(request):
      books = Book.objects.all()
      print(books)
      context = {'books': books}
      return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(ListView):
    model = Library
    queryset = Library.objects.get(name = "lib1")
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class Register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'

def is_admin(user):
     return user.is_authenticated and hasattr(user, 'UserProfile') and user.UserProfile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

def is_librarian(user):
     return user.is_authenticated and hasattr(user, 'UserProfile') and user.UserProfile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {"message": "Welcome, Librarian!"})

def is_member(user):
     return user.is_authenticated and hasattr(user, 'UserProfile') and user.UserProfile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {"message": "Welcome, Member!"})

