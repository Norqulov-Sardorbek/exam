from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import LoginForm
from users.models import CustomUser

# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:category')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Disabled account'
                    )
                    return render(request, 'users/login.html')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or Password invalid'
                )
                return render(request, 'users/login.html')

    return render(request, 'users/login.html', {'form': form} )

def register_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data


            if CustomUser.objects.filter(email=cd['email']).exists():
                messages.error(request, 'Account with this email already exists.')
            else:
                # Create user
                user = CustomUser.objects.create_user(
                    email=cd['email'],
                    password=cd['password']
                )
                user.save()
                messages.success(request, 'You have successfully registered')
                login(request, user)
                return redirect('shop:category')

    return render(request, 'users/register.html', {'form': form})

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:category')
