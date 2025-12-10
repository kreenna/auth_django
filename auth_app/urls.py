from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("delete/", views.DeleteAccountView.as_view(), name="delete"),

    # Mock ресурсы
    path("products/", views.ProductsView.as_view(), name="products"),
    path("orders/", views.OrdersView.as_view(), name="orders"),
]
