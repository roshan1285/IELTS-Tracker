from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name='core'

urlpatterns=[
    # path('home', views.home, name="home"),
    
    path("writing/new/", views.writing_setup, name="writing_setup"),
    path("writing/<int:pk>/", views.writing_practice, name="writing_practice"),
    path("writing/<int:pk>/score/", views.writing_score, name="writing_score"),

    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

]