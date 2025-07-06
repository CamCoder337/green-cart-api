"""
Configuration des URLs principales du projet.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import render
import django


def home_view(request):
    """Vue d'accueil avec template HTML."""
    context = {
        'debug': settings.DEBUG,
        'version': django.get_version(),
    }
    return render(request, 'home.html', context)


def api_home_view(request):
    """Vue d'accueil API qui renvoie un JSON."""
    return JsonResponse({
        'message': 'Bienvenue sur votre Django Boilerplate API! 🚀',
        'status': 'success',
        'debug': settings.DEBUG,
        'version': django.get_version()
    })


urlpatterns = [
    path('', home_view, name='home'),  # Page d'accueil HTML
    path('api/', api_home_view, name='api_home'),  # Page d'accueil API
    path('admin/', admin.site.urls),
    # path('api/auth/', include('accounts.urls')),  # À décommenter quand l'app sera créée
    # path('api/v1/', include('api.urls')),          # À décommenter quand l'app sera créée
]

# Servir les fichiers statiques et média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Debug Toolbar (uniquement en développement)
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
