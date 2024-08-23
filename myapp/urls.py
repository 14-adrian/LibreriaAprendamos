from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   #path("", views.loginaction, name='login'),
   path('', views.login_view, name='login'),
   path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),

    path('sign_up/', views.sign_up_view, name='sign_up_view'),
    path('main/', views.listar_documentos, name='Libreria Aprendamos'),
    path("main/", views.dashboard_view, name='Libreria Aprendamos'),
    
    path("agregar/", views.agregar_documento, name="agregar")
]
