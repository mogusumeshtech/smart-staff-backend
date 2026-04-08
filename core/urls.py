from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

router = DefaultRouter()
router.register(r'settings', views.SchoolSettingsViewSet, basename='settings')

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('', include(router.urls)),
]
