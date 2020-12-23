from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_v'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate_account'),

    path('login/', LoginView.as_view(), name='login_v'),
    path('logout/', login_required(LogOutView.as_view()), name='logout_v'),

    path('delete/', login_required(DeleteProfileView.as_view()), name='delete_profile'),

    path('theme/', login_required(ChangeTheme.as_view()), name='change_theme'),

    path('<str:username>', UserProfileView.as_view(), name='my_profile'),

    path('password/change/', login_required(PasswordChange.as_view()), name='password_change'),


    path('password/reset/', CustomPasswordResetView.as_view(),
         name='password_reset'),

    path('password/reset/confirmation', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('password/reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password/reset/completed', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
