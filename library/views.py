from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Book, Issue
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# Create your views here.

from django.http import HttpResponse


class BookList(ListView):
    model = Book


class BookListUser(LoginRequiredMixin, ListView):
    login_url = "/library/login"
    redirect_field_name = ""

    def get_template_names(self) -> list[str]:
        return ["library/book_user_list.html"]

    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListUser, self).get_context_data(**kwargs)
        book_status = {}
        issue_list = Issue.objects.filter(returnDate=None)
        user = self.request.user.get_username()

        for issue in issue_list:
            name = issue.user.get_username()
            if name == user:
                book_status[issue.book.id] = ['Return', name]
            else:
                book_status[issue.book.id] = ['Unavailable', name]
        context['book_status'] = book_status
        return context


class BorrowedBooks(BookListUser):
    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        if user.is_superuser:
            all_issues = Issue.objects.filter(returnDate=None)
            return super().get_queryset().filter(issue__in=all_issues).order_by('issue__user__username')
        else:
            user_issues = Issue.objects.filter(user=user, returnDate=None)
            return super().get_queryset().filter(issue__in=user_issues)


class BookDetailsView(DetailView):
    model = Book


class BookUpdateView(UpdateView):
    model = Book

    fields = [
        "isbn",
        "title",
        "author",
        "year",
        "distributor",
        "genre",
        "defaultBorrowDays"
    ]

    success_url = "/library/admin/list"


class BookCreate(PermissionRequiredMixin, CreateView):
    login_url = "/library/login"
    redirect_field_name = ""
    permission_required = "library.book.add_book"
    model = Book
    fields = [
        "isbn",
        "title",
        "author",
        "year",
        "distributor",
        "genre",
        "defaultBorrowDays"
    ]

    success_url = "/library/admin/list"


@permission_required(perm=['library.add_issue', 'library.change_issue', 'library.view_issue',
                           'library.view_book'], raise_exception=True)
def borrow_return_book(request, pk):
    # Issue.objects.create(user=User.objects.get(pk=request.user.pk), book=Book.objects.get(pk=pk))
    # issue_obj = Issue(user=User.objects.get(pk=request.user.pk), book=Book.objects.get(pk=pk))
    # issue_obj.save()
    # print(request, pk)
    # print(request.user)
    # return redirect("/library/list")

    user = User.objects.get(pk=request.user.pk)
    book = Book.objects.get(pk=pk)

    issues = Issue.objects.filter(user=user, book=book)

    for issue in issues:
        if issue.issueDate and issue.returnDate is None:
            issue.save()
            break
    else:
        issue = Issue(user=user, book=book)
        issue.save()

    return redirect("/library/list")
