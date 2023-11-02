from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


from . import forms

def logout_page(request):
    logout(request)
    #return redirect(reverse_lazy('library:login'))
    return redirect('/library/login')


def login_page(request):
    message = ''
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('/library/list/')
            else:
                return redirect('/library/login')
                message = 'Login failed!'
    return render(request, 'authentication/login.html', context={'form': form})
            
