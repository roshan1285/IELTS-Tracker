from django.urls import path
from . import views


app_name='core'

urlpatterns=[
    # path('home', views.home, name="home"),
    path("settings/", views.settings_view, name="settings"),

    path("writing/tests/", views.writing_tests, name="writing_tests"),
    path("writing/new/", views.writing_setup, name="writing_setup"),
    path("writing/<int:pk>/", views.writing_practice, name="writing_practice"),
    path("writing/<int:pk>/score/", views.writing_score, name="writing_score"),

    # Add to core/urls.py, inside urlpatterns

    path("listening/tests/", views.listening_tests, name="listening_tests"),
    path("listening/new/", views.listening_practice, name="listening_practice"),
    path("listening/<int:pk>/score/", views.listening_score, name="listening_score"),

    path("reading/tests/", views.reading_tests, name="reading_tests"),
    path("reading/new/", views.reading_practice, name="reading_practice"),
    path("reading/<int:pk>/score/", views.reading_score, name="reading_score"),
    path("reading/<int:pk>/revisit/", views.reading_revisit, name="reading_revisit"),

    path("speaking/tests/", views.speaking_tests, name="speaking_tests"),
    path("speaking/new/", views.speaking_practice, name="speaking_practice"),

    path('theme/toggle/', views.toggle_theme, name='toggle_theme'),
]