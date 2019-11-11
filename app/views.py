from django.shortcuts import render, redirect
from app.models import Book, Transaction
from django.contrib import messages
from django.utils import timezone


# Renders the home page with all the book objects currently in
# the database returned in the context.


def home(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})


# Selects the associated book within the database,
# runs check to make sure book is in stock,
# if in stock, raises succes message and changes book's
# in stock status, else
# raises errror.
# Then redirects home.


def borrow_book(request, id):
    book = Book.objects.get(id=id)
    if book.in_stock:
        messages.success(request, f"Borrowed {book.title} by {book.author}")
        book.in_stock = False
        book.transaction_set.create(action="CHECKOUT")
        book.save()
    else:
        messages.error(request, f"{book.title} by {book.author} is unavailable")
    return redirect("home")


# Selects the associated book within the database,
# runs check to make sure book is out of stock,
# if out of stock, raises succes message and changes book's
# in stock status, else
# raises errror.
# Then redirects home.


def return_book(request, id):
    book = Book.objects.get(id=id)
    if book.in_stock:
        messages.error(request, f"{book.title} by {book.author} is already here")
    else:
        messages.success(request, f"Returned {book.title} by {book.author}")
        book.in_stock = True
        book.transaction_set.create(action="CHECKIN")
        book.save()
    return redirect("home")
