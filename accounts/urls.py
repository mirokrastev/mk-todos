from django.contrib.auth.decorators import login_required
from django.urls import path
from .forms import CustomPasswordResetForm
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_v'),
    path('login/', views.login_view, name='login_v'),
    path('logout/', login_required(views.LogOutView.as_view()), name='logout_v'),

    path('<str:username>', views.UserProfileView.as_view(), name='my_profile'),

    path('password/change/', views.password_change, name='password_change'),

    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/reset/password_reset_form.html',
        form_class=CustomPasswordResetForm),
         name='password_reset'),

    path('password/reset/confirmation', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/reset/password_reset_done.html'),
         name='password_reset_done'),

    path('password/reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(
        template_name='accounts/reset/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password/reset/completed', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
