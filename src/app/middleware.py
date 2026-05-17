from django.shortcuts import render

from app.providers import services


class ProviderAPIErrorMiddleware:
    """Middleware to handle ProviderAPIError exceptions."""

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request and handle exceptions."""
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Handle exceptions raised during request processing."""
        if isinstance(exception, services.ProviderAPIError):
            return render(
                request,
                "500.html",
                {
                    "error_message": str(exception),
                    "provider": exception.provider,
                },
                status=500,
            )
        return None


class AutoLoginMiddleware:
    """
    Automatically log in the first user if nobody is authenticated.
    This removes the login page for local single/dual-user setups.
    Only activates when ALLOW_AUTO_LOGIN=True in settings (default: True locally).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings as django_settings
        if not getattr(django_settings, "ALLOW_AUTO_LOGIN", True):
            return self.get_response(request)

        # Skip static files, admin, and allauth endpoints
        skip_paths = ("/static/", "/admin/", "/accounts/", "/__debug__/")
        if any(request.path.startswith(p) for p in skip_paths):
            return self.get_response(request)

        if not request.user.is_authenticated:
            from django.contrib.auth import get_user_model, login as auth_login
            User = get_user_model()
            first_user = User.objects.order_by("id").first()
            if first_user:
                first_user.backend = "django.contrib.auth.backends.ModelBackend"
                auth_login(request, first_user)

        return self.get_response(request)
