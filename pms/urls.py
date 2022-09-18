from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('signup', views.signup, name='signup'),

    path('drugs', views.drugs, name='drugs'),
    path('drugs-list', views.drugs_list, name='drugs_list'),
    path('drugs/add', views.add_drug, name='add_drug'),
    path('drugs/<int:drug_id>/update', views.update_drug, name='update_drug'),
    path('drugs/<int:drug_id>/delete', views.delete_drug, name='delete_drug'),
    path('drugs/<int:drug_id>/place-order', views.place_order, name='place_order'),
    path('drugs/search', views.search_drug, name='search_drug'),

    path('orders', views.orders, name='orders'),
    path('orders/<int:order_id>/bill', views.order_bill, name='order_bill'),
]
