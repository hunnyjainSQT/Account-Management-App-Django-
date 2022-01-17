from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.logIn, name="login"),
    path('logout/', views.logOut, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.account_settings, name="settings"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),

    path('products/', views.products, name="products"),
    path('customer/<int:id>', views.customer, name="customer"),
    path('create_order/<int:id>', views.create_order, name="create_order"),
    path('update_order/<int:id>', views.update_order, name="update_order"),
    path('delete_order/<int:id>', views.delete_order, name="delete_order"),
]
