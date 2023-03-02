from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join),
    path('login/', views.user_login)
]