from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add",views.add,name="add"),
    path("wiki/<str:title>",views.getPage,name="getPage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path('search', views.search_feature, name='search-view')
   
]
