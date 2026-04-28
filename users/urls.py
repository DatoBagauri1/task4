from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserListDetailViewSet
from . import views

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'users', UserListDetailViewSet, basename='user')
router.register('password-reset-request', views.PasswordResetRequestViewSet, basename='password_reset')

urlpatterns = [
    path("password-reset-confirm/<uidb64>/<token>/", views.PasswordResetConfirmViewSet.as_view({'post': 'create'}), name="password-reset-confirm"),
    path('', include(router.urls)),
]