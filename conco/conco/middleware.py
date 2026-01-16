from django.utils import translation
from django.conf import settings
from django.middleware.locale import LocaleMiddleware

class CustomLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        admin_path = f'/{settings.ADMIN_URL.rstrip("/")}'
        
        if request.path.startswith(admin_path):
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        else:
            language = request.session.get('django_language', settings.LANGUAGE_CODE)
            if language not in dict(settings.LANGUAGES):
                language = settings.LANGUAGE_CODE
            translation.activate(language)
            request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        return super().process_response(request, response)
