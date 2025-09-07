## input:
```
from library.models import Book
book = Book.objects.create(title="1984", author="George Orwell" , publication_year= "1949")
book.save()
Book.objects.get(id=1)
```

## output:
```
<Book: Book object (1)>
```