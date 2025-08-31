## input:
```
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book_data)
```

## output:
```
<QuerySet [{'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>
```