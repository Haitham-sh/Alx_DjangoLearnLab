## input:
```
book01 = Book.objects.get(id=1)
book01.title = "Nineteen Eighty-Four"
book01.save()
print(book_data)
```

## output:
```
<QuerySet [{'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}]>
```