from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic import ListView
from django.views.generic.detail import DetailView

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
