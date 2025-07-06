"""
Main API URL configuration.
"""
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import django


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint with available endpoints."""
    return Response({
        'message': 'Welcome to Django Boilerplate API! 🚀',
        'version': '1.0.0',
        'django_version': django.get_version(),
        'debug_mode': settings.DEBUG,
        'available_endpoints': {
            'authentication': {
                'register': '/api/v1/auth/register/',
                'login': '/api/v1/auth/login/',
                'logout': '/api/v1/auth/logout/',
                'profile': '/api/v1/auth/profile/',
                'users': '/api/v1/auth/users/',
                'change_password': '/api/v1/auth/users/change_password/',
            },
            'documentation': {
                'api_docs': '/api/docs/' if settings.DEBUG else None,
                'schema': '/api/schema/' if settings.DEBUG else None,
            }
        },
        'authentication': {
            'type': 'Token-based',
            'header_format': 'Authorization: Token your_token_here',
            'obtain_token': 'POST /api/v1/auth/login/ with email and password'
        },
        'status': 'operational'
    })


app_name = 'api'

urlpatterns = [
    # API root
    path('', api_root, name='api_root'),

    # Version 1 API endpoints
    path('v1/auth/', include('accounts.urls', namespace='accounts')),

    # Health check
    path('health/', api_root, name='health_check'),
]