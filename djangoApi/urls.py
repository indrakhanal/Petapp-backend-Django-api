"""djangoApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
# from reviews.views import ProductViewSet, ImageViewSet
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='User API')
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
API_TITLE = 'Pets App API Docs' # new
API_DESCRIPTION = 'REST API v1'
# schema_view = get_schema_view(title=API_TITLE)

schema_view = get_schema_view(
   openapi.Info(
      title="Pets App API Docs",
      default_version='v1',
      description="REST API v1",
      contact=openapi.Contact(email=""),
      license=openapi.License(name="GNU License"),
      terms_of_service="http://65.0.18.97/swagger/policies/terms/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls')),
    path('', include('accounts.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
    path('api/', include('pets.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', include_docs_urls(title=API_TITLE,description=API_DESCRIPTION)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

