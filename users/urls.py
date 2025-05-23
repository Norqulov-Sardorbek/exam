from django.urls import path
from users.views import LoginPageView, RegisterPageView, LogoutPageView,VerifyEmailView

app_name = 'users'

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login_page'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('logout/', LogoutPageView.as_view(), name='logout_page'),
    path('verify/', VerifyEmailView.as_view(), name='verify'),
]
