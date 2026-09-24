from django.urls import path
from . import views


app_name='core'

urlpatterns=[
    # path('home', views.home, name="home"),
    
    path("writing/tests/", views.writing_tests, name="writing_tests"),
    path("writing/new/", views.writing_setup, name="writing_setup"),
    path("writing/<int:pk>/", views.writing_practice, name="writing_practice"),
    path("writing/<int:pk>/score/", views.writing_score, name="writing_score"),

    # Add to core/urls.py, inside urlpatterns

    path("listening/new/", views.listening_practice, name="listening_practice"),
    path("listening/<int:pk>/score/", views.listening_score, name="listening_score"),
    path("reading/new/", views.reading_practice, name="reading_practice"),
    path("reading/<int:pk>/score/", views.reading_score, name="reading_score"),

]