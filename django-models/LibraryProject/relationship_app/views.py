from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .models import Library
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required

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

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('book_list')
    return render(request, 'edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'book': book})