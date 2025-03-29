from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from users.forms import LoginForm
from users.models import *
from django.core.mail import send_mail
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
            email = cd['email']
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Account with this email already exists.')
            else:
                verification_code = get_random_string(length=6, allowed_chars='0123456789')
                VerificationCode.objects.create(email=email, code=verification_code)

                send_mail(
                    subject="Email tasdiqlash kodi",
                    message=f"Sizning tasdiqlash kodingiz: {verification_code}",
                    from_email="nsardorbek776@gmail.com",
                    recipient_list=[email],
                    fail_silently=False,
                )

                request.session['email'] = email
                request.session['password'] = cd['password']
                return redirect('users:verify')
        return render(request, 'users/register.html', {'form': form})


class VerifyEmailView(View):
    def get(self, request):
        return render(request, 'users/verify.html')

    def post(self, request):
        code = request.POST.get('code')
        email = request.session.get('email')

        if not email:
            messages.error(request, 'Kod vaqti muddati tugagan. Iltimos, qayta ro‘yxatdan o‘ting.')
            return redirect('users:register')

        try:
            verification = VerificationCode.objects.get(email=email, code=code)
            user = CustomUser.objects.create_user(email=email, password=request.session.get('password'))
            user.save()

            verification.delete()
            del request.session['email']
            del request.session['password']

            messages.success(request, 'Email muvaffaqiyatli tasdiqlandi!')
            return redirect('shop:category')
        except VerificationCode.DoesNotExist:
            messages.error(request, 'Noto‘g‘ri kod. Iltimos, qayta urinib ko‘ring.')
            return render(request, 'users/verify.html')

class LogoutPageView(View):
    def post(self, request):
        logout(request)
        return redirect('shop:category')