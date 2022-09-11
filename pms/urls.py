from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('products', views.products, name='products'),
    path('products/add', views.add_drug, name='add_drug'),
]
