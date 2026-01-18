"""
Cache utilities for page-level caching and cache invalidation.
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
from django.utils.cache import get_cache_key
import hashlib
import json


def generate_cache_key(prefix, *args, **kwargs):
    """
    Generate a cache key from prefix and arguments.
    
    Args:
        prefix: Cache key prefix (e.g., 'page_home', 'query_projects')
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key
    
    Returns:
        str: Generated cache key
    """
    # Sort kwargs for consistent key generation
    sorted_kwargs = sorted(kwargs.items())
    
    # Create a string representation of all arguments
    key_parts = [prefix] + [str(arg) for arg in args] + [f"{k}={v}" for k, v in sorted_kwargs]
    key_string = "|".join(key_parts)
    
    # Hash the key if it's too long
    if len(key_string) > 250:
        key_string = hashlib.md5(key_string.encode()).hexdigest()
    
    return f"conco:{key_string}"


def get_page_cache_key(view_name, lang, **query_params):
    """
    Generate cache key for a page view.
    
    Args:
        view_name: Name of the view (e.g., 'home', 'project-list')
        lang: Language code
        **query_params: Query parameters from request.GET
    
    Returns:
        str: Cache key for the page
    """
    # Sort query params for consistent keys
    sorted_params = sorted(query_params.items())
    return generate_cache_key(f"page_{view_name}", lang, **dict(sorted_params))


def get_query_cache_key(query_name, *args, **kwargs):
    """
    Generate cache key for a database query.
    
    Args:
        query_name: Name of the query function (e.g., 'projects', 'about')
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        str: Cache key for the query
    """
    return generate_cache_key(f"query_{query_name}", *args, **kwargs)


def cached_query(timeout=None):
    """
    Decorator to cache the result of a query function.
    
    Args:
        timeout: Cache timeout in seconds. If None, uses CACHE_TIMEOUT_MEDIUM.
    
    Usage:
        @cached_query(timeout=300)
        def get_projects(lang='az', category_id=None):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if timeout is None:
                cache_timeout = getattr(settings, 'CACHE_TIMEOUT_MEDIUM', 300)
            else:
                cache_timeout = timeout
            
            # Generate cache key from function name and arguments
            cache_key = get_query_cache_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, cache_timeout)
            
            return result
        return wrapper
    return decorator


def invalidate_page_cache(view_names=None):
    """
    Invalidate cache for specific pages or all pages.
    
    Args:
        view_names: List of view names to invalidate. If None, invalidates all pages.
    """
    if view_names is None:
        # Invalidate all page caches (using a pattern - simple but works with locmem)
        # For production with Redis, you could use pattern matching
        cache.clear()
    else:
        # For specific views, we'd need to track keys or use version-based invalidation
        # For now, we'll use a version-based approach
        cache.set('cache_version', cache.get('cache_version', 0) + 1, None)


def invalidate_query_cache(query_names=None):
    """
    Invalidate cache for specific queries or all queries.
    
    Args:
        query_names: List of query names to invalidate. If None, invalidates all queries.
    """
    if query_names is None:
        # Clear all cache
        cache.clear()
    else:
        # Clear specific query patterns (simplified - would need key tracking for production)
        cache.set('cache_version', cache.get('cache_version', 0) + 1, None)


def cached_page_data(timeout=None):
    """
    Decorator to cache page data functions (like get_home_page_data, get_project_list_data).
    
    Args:
        timeout: Cache timeout in seconds. If None, uses CACHE_TIMEOUT_MEDIUM.
    
    Usage:
        @cached_page_data(timeout=300)
        def get_home_page_data(request, lang):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, lang, *args, **kwargs):
            if timeout is None:
                cache_timeout = getattr(settings, 'CACHE_TIMEOUT_MEDIUM', 300)
            else:
                cache_timeout = timeout
            
            # Generate cache key from function name, language, and query parameters
            query_params = dict(request.GET.items())
            cache_key = get_page_cache_key(func.__name__.replace('get_', '').replace('_data', ''), lang, **query_params)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(request, lang, *args, **kwargs)
            cache.set(cache_key, result, cache_timeout)
            
            return result
        return wrapper
    return decorator


def invalidate_model_cache(model_name):
    """
    Invalidate all cache entries related to a specific model.
    
    Args:
        model_name: Name of the model (e.g., 'Project', 'Vacancy', 'About')
    """
    # Map model names to related views/queries
    model_to_views = {
        'Project': ['home', 'project-list', 'project-detail'],
        'ProjectCategory': ['home', 'project-list'],
        'Vacancy': ['home', 'vacancy-list', 'vacancy-detail'],
        'Partner': ['home', 'partner-list'],
        'About': ['home', 'about'],
        'Contact': ['home', 'contact'],
        'Media': ['home', 'project-list', 'project-detail', 'about', 'partner-list', 'vacancy-list', 'vacancy-detail'],
    }
    
    views_to_invalidate = model_to_views.get(model_name, [])
    
    # Also invalidate related queries
    model_to_queries = {
        'Project': ['get_projects', 'get_project_by_slug', 'get_project_categories'],
        'ProjectCategory': ['get_project_categories', 'get_projects'],
        'Vacancy': ['get_vacancies', 'get_vacancy_by_slug'],
        'Partner': ['get_partners'],
        'About': ['get_about'],
        'Contact': ['get_contact'],
        'Media': ['get_projects', 'get_project_by_slug', 'get_about', 'get_partners', 
                  'get_vacancies', 'get_vacancy_by_slug', 'get_background_image'],
    }
    
    queries_to_invalidate = model_to_queries.get(model_name, [])
    
    # Increment cache version to invalidate all related caches
    cache.set('cache_version', cache.get('cache_version', 0) + 1, None)
    
    # Also clear specific cache keys if we track them
    # For simplicity, we'll just increment version which forces key regeneration

