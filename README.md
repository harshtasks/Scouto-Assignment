# Scouto-Assignment
Making a set of APIs to query a library database
---

### Note
* The `books` collection already contains 20 books.
* There are some transaction already present in `transactions` collection.


## APIs


### Find
* #### Find books (Using Search term)
```css
/api/find?term=search_term
```
* #### Find books (Using Rent lower and higher than values)
```css
/api/find?lt=rentlower&gt=rentgreater
```
* #### Find books (Using Search term, Rent lower and higher than, Category)
```css
/api/find?term=search_term&lt=rentlower&gt=rentgreater&category=category
```
---
* ## ⚠️Important: Date format in below APIs should be of the form `DD-MM-YYYY`
---
### Issue Book
```css
/api/issue?book=book_name&person=person_name&date=issue_date
```

### Return Book
```css
/api/return?book=book_name&person=person_name&date=return_date
```

### List of people having a book issued (total_count and currently having)
```css
/api/book/issued?book=book_name
```

### Total rent earned from a book (only returned ones)
```css
/api/book/rent?book=book_name
```

### All books issued by a person (currently)
```css
/api/person/books?person=person_name
```

### List of books issued during a date range (both inclusive)
```css
/api/book/daterange?start=start_date&end=end_date
```

