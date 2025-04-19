from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    TrainerLoginView,
    UserLogoutView,
    UserProfileView,
    SpecificUserProfileView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordChangeView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    UserListView,
    TrainerViewSet,
    StudentViewSet,
)
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("trainer-login/", TrainerLoginView.as_view(), name="trainer-login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/<int:user_id>/", SpecificUserProfileView.as_view(), name="specific-user-profile"),

    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),

    path("token/", MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token-refresh"),
    
    path("cusers/", UserListView.as_view(), name="users"),
]
urlpatterns += router.urls