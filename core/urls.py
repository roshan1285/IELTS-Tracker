from django.urls import path
from . import views


app_name='core'

urlpatterns=[
    # path('home', views.home, name="home"),
    
    path("writing/new/", views.writing_setup, name="writing_setup"),
    path("writing/<int:pk>/", views.writing_practice, name="writing_practice"),
    path("writing/<int:pk>/score/", views.writing_score, name="writing_score"),

    

]