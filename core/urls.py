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



urlpatterns = [
    path('', home_view, name='home'),  # Page d'accueil HTML
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),  # API principale
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
