from functools import wraps
from urllib.parse import urlparse
from django.shortcuts import resolve_url

####connection
def user_passes_test(test_func, login_url='/'):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            login_scheme, login_netloc = urlparse(resolve_url('/'))[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if login_scheme != current_scheme and login_netloc != current_netloc:
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(path, resolve_url('/'))
        return _wrapped_view
    return decorator


def login_connect(function=None):
    actual_decorator = user_passes_test(lambda u: u.is_authenticated, login_url='/',)
    return actual_decorator(function) if function else actual_decorator

def user_passes_connecter(test_func, login_url='/'):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            login_scheme, login_netloc = urlparse(resolve_url('/'))[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (login_scheme == current_scheme) and (login_netloc == current_netloc):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(path, resolve_url('/'))
        return _wrapped_view
    return decorator

def login_non_connect(function=None):
    actual_decorator = user_passes_connecter(lambda u: not u.is_authenticated, login_url='/',)
    return actual_decorator(function) if function else actual_decorator