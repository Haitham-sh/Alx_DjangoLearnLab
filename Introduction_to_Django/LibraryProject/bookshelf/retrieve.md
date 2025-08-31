## input:
```
from library.models import Book
book = Book(title="1984", author="George Orwell" , publication_year= "1949")
book.save()
book_data = Book.objects.get(id=1).values('title', 'author', 'publication_year')
print(book_data)
```

## output:
```
<QuerySet [{'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]>
```