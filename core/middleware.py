from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class Midoudou(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        host = request.META.get('HTTP_HOST')

        if host.startswith('www.'):
            non_www = host.replace('www.', '')
            return redirect(f'https://{non_www}{request.get_full_path()}')

        return response