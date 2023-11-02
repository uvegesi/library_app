from django.urls import path, include
from django.contrib import admin, auth
from library import views
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Import the module from the parent directory
import authentication.views

app_name = 'library'

urlpatterns = [
	path("login/", authentication.views.login_page, name='login'),
	path('logout/', authentication.views.logout_page, name='logout'),
	path('admin/list/', views.BookList.as_view(), name='list'),
	path('admin/create/', views.BookCreate.as_view(), name='create'),
	path('admin/<pk>/details/', views.BookDetailsView.as_view(), name='details'),
	path('admin/<pk>/update/', views.BookUpdateView.as_view(), name='update'),
	path('list/', views.BookListUser.as_view(), name='book_user_list'),
	path('borrow/<pk>', views.borrow_return_book, name='borrow'),
	path('borrowed_books', views.BorrowedBooks.as_view(), name='borrowed_books')
]