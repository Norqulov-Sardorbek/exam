from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from users.forms import LoginForm
from users.models import CustomUser

class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:category')
                messages.error(request, 'Disabled account')
            else:
                messages.error(request, 'Username or Password invalid')
        return render(request, 'users/login.html', {'form': form})

class RegisterPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if CustomUser.objects.filter(email=cd['email']).exists():
                messages.error(request, 'Account with this email already exists.')
            else:
                user = CustomUser.objects.create_user(email=cd['email'], password=cd['password'])
                user.save()
                messages.success(request, 'You have successfully registered')
                login(request, user)
                return redirect('shop:category')
        return render(request, 'users/register.html', {'form': form})

class LogoutPageView(View):
    def post(self, request):
        logout(request)
        return redirect('shop:category')