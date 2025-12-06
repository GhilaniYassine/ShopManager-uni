from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignUpView,
    SignInView,
    SignOutView,
    UserProfileViewSet,
    check_auth,
    verify_username,
    verify_email
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    # Authentication endpoints
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/signin/', SignInView.as_view(), name='signin'),
    path('auth/signout/', SignOutView.as_view(), name='signout'),
    path('auth/check/', check_auth, name='check_auth'),
    
    # Verification endpoints
    path('verify/username/', verify_username, name='verify_username'),
    path('verify/email/', verify_email, name='verify_email'),
    
    # Profile endpoints
    path('', include(router.urls)),
]
