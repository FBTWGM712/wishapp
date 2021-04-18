from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wishes', views.wishes),
    path('wishes/new', views.addwish),
    path('delete/<int:id>', views.delete),
    path('wishes/add_wish_to_db', views.add_wish_to_db),
    path('stats', views.stats),
    path('wishes/edit/<int:id>', views.edit_wish),
    path('edit_wish_to_db/<int:id>', views.edit_wish_to_db),
    path('granted/add/<int:id>', views.granted_wish),
    path('like', views.like),


]