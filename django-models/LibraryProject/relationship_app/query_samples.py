from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
def books_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        for book in books:
            return book.title
    except Author.DoesNotExist:
        return None
    
# List all books in a library.
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        for book in books:
            return book.title
    except Library.DoesNotExist:
        return None

# Retrieve the librarian for a library.
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = librarian.get(library=library)
        return librarian.name
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None