"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app.api_views import UsuarioViewSet, PersonaViewSet, DocumentoViewSet, EventoLogViewSet   


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API NUAM",
      default_version='v1',
      description="Documentación de la API REST",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Router de la API REST
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'personas', PersonaViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'logs', EventoLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas normales de la app
    path('', include('app.urls')),

    # Rutas de la API REST
    path('api/', include(router.urls)),  

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
