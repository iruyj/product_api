from django.contrib import admin
from django.urls import path, include

from product import views

app_name = 'product'

urlpatterns = [
    # path('list/<str:keyword>', views.getlist, name="list"),
    path('', views.index, name="index"),
    path('info/', views.getProduct, name="info"),
    path('filter/<int:type>', views.filtering, name="filter"),
    path('<int:code>/', views.detail, name="detail"),
]
