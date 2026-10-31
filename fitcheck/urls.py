from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FitCheckViewSet

router = DefaultRouter()
router.register(r"fitcheck", FitCheckViewSet, basename="fitcheck")

urlpatterns = [path("", include(router.urls))]
