
from django.contrib import admin
from django.urls import path, include
from players import views as player_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('players.urls')),
    path('generate/', player_views.generate_player, name='generate_player'),
    path('register/', player_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', player_views.home, name='home'), 
]
