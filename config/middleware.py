from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        print(f"Request Method: {request.method}, Request Path: {request.path}")
        # Call the next middleware or view
        response = self.get_response(request)
        return response


class AutoLogoutMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activiy')
            if last_activity is not None:
                difference_time = (now() - now().fromisoformat(last_activity)).total_seconds()
                if difference_time > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('shop:category')

            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response
class LanguageDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get('Accept-Language', 'en')[:2]
        request.preferred_language = lang
        return self.get_response(request)

class HeaderInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Powered-By'] = 'MyCustomAPI v1.0'
        return response
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.maintenance = False  # True bo‘lsa har qanday requestni cancell qiladi

    def __call__(self, request):
        if self.maintenance and not request.user.is_staff:
            return HttpResponse("Maintenance mode enabled", status=503)
        return self.get_response(request)
class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        request.user_agent = user_agent
        return self.get_response(request)