from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/', views.profile, name="profile"),


    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order" ),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order" ),
    path('create_product', views.create_product, name="create_product"),
    path('account/', views.accountSettings, name="account")

]
