from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages, SUCCESS, ERROR
from app import models


class TestUserCanViewAllBooks(TestCase):
    def test_home_page_shows_all_books(self):
        books = [
            models.Book.objects.create(
                title=f"Super Good Book #{i}",
                author="Nate",
                genre="Computers",
                in_stock=True,
                published=timezone.now(),
                description="It's a good book. You should read it",
            )
            for i in range(3)
        ]

        response = self.client.get(reverse("home"))

        for book in books:
            self.assertContains(response, book.title)


class TestUserCanBorrowABook(TestCase):
    def test_borrowing_a_book_makes_it_unavailable(self):
        book_to_borrow = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        self.client.post(reverse("borrow_book", args=[book_to_borrow.id]))

        book_to_borrow.refresh_from_db()

        self.assertFalse(
            book_to_borrow.in_stock,
            "Borrowing a book should mark the book as out of stock in the DB",
        )

    def test_borrowing_a_book_flashes_a_success_message(self):
        book_to_borrow = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("borrow_book", args=[book_to_borrow.id]))

        messages = [(m.level, m.message) for m in get_messages(response.wsgi_request)]
        self.assertIn((SUCCESS, "Borrowed Super Good Book by Nate"), messages)

    def test_borrowing_a_book_that_is_unavailable_flashes_an_error_message(self):
        book_to_borrow = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=False,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("borrow_book", args=[book_to_borrow.id]))

        messages = [(m.level, m.message) for m in get_messages(response.wsgi_request)]
        self.assertIn((ERROR, "Super Good Book by Nate is unavailable"), messages)

    def test_redirects_to_home(self):
        book_to_borrow = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("borrow_book", args=[book_to_borrow.id]))

        self.assertRedirects(response, reverse("home"))

    def test_borrowing_a_book_creates_a_transaction(self):
        book_to_borrow = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        self.client.post(reverse("borrow_book", args=[book_to_borrow.id]))

        self.assertTrue(
            book_to_borrow.transaction_set.filter(action="CHECKOUT").exists()
        )


class TestUserCanReturnABook(TestCase):
    def test_returning_a_book_makes_it_available(self):
        book_to_return = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=False,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        self.client.post(reverse("return_book", args=[book_to_return.id]))

        book_to_return.refresh_from_db()

        self.assertTrue(
            book_to_return.in_stock,
            "Returning a book should mark the book as in stock in the DB",
        )

    def test_returning_a_book_flashes_a_success_message(self):
        book_to_return = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=False,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("return_book", args=[book_to_return.id]))

        messages = [(m.level, m.message) for m in get_messages(response.wsgi_request)]
        self.assertIn((SUCCESS, "Returned Super Good Book by Nate"), messages)

    def test_returning_a_book_that_is_available_flashes_an_error_message(self):
        book_to_return = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("return_book", args=[book_to_return.id]))

        messages = [(m.level, m.message) for m in get_messages(response.wsgi_request)]
        self.assertIn((ERROR, "Super Good Book by Nate is already here"), messages)

    def test_redirects_to_home(self):
        book_to_return = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=True,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        response = self.client.post(reverse("return_book", args=[book_to_return.id]))

        self.assertRedirects(response, reverse("home"))

    def test_returning_a_book_creates_a_transaction(self):
        book_to_return = models.Book.objects.create(
            title="Super Good Book",
            author="Nate",
            genre="Computers",
            in_stock=False,
            published=timezone.now(),
            description="It's a good book. You should read it",
        )

        self.client.post(reverse("return_book", args=[book_to_return.id]))

        self.assertTrue(
            book_to_return.transaction_set.filter(action="CHECKIN").exists()
        )
