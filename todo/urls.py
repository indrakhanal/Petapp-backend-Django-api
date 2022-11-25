# from django.contrib import admin
from django.urls import path, include
from .views import TodoView
from rest_framework import routers
router = routers.DefaultRouter()
router.register('task', TodoView, 'task')
app_name = 'todo'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('auth/', include('auth.urls')),
]


