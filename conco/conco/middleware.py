from django.utils import translation
from django.conf import settings


class CustomLocaleMiddleware:
    """
    Custom middleware to activate language from session.
    This ensures that translations work properly based on user's language selection.
    Django uses thread-local storage for translations, so we don't need to deactivate.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from session
        language = request.session.get('django_language')
        
        # If no language in session, try alternative key
        if not language:
            language = request.session.get('language')
        
        # Validate language
        if language and language in dict(settings.LANGUAGES):
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            # Use default language
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        
        response = self.get_response(request)
        
        # Note: We don't deactivate translation here because:
        # 1. Django uses thread-local storage, so it's safe
        # 2. Template rendering needs translation to be active
        # 3. Django's LocaleMiddleware also doesn't deactivate
        
        return response
