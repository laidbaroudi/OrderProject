from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AISettingView,
    DashboardView,
    MeView,
    ShopSettingView,
    SignInView,
    SignOutView,
    SignUpView,
    TeamMemberViewSet,
)

router = DefaultRouter()
router.register(r"team", TeamMemberViewSet, basename="team")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", SignUpView.as_view(), name="auth-signup"),
    path("auth/signin/", SignInView.as_view(), name="auth-signin"),
    path("auth/signout/", SignOutView.as_view(), name="auth-signout"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("ai-settings/", AISettingView.as_view(), name="ai-settings"),
    path("shop-settings/", ShopSettingView.as_view(), name="shop-settings"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
