from django.contrib import admin
from django.urls import path, include

from product import views

app_name = 'product'

urlpatterns = [
    path('list/<str:keyword>', views.getlist, name="list"),
    path('info/', views.getProduct, name="info"),
    path('view/', views.search, name="list"),
    path('main/', views.index, name="index"),
    path('<int:code>/', views.detail, name="detail"),
    path('search/', views.index, name="search"),
]
