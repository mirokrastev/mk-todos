from django.urls import path
from .forms import CustomPasswordResetForm
from .views import register_view, login_view, logout_view, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register_v'),
    path('login/', login_view, name='login_v'),
    path('logout/', logout_view, name='logout_v'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        form_class=CustomPasswordResetForm),
        name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',),
        name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
]
