from django.contrib import admin
from django.urls import path, include
from players import views as player_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from players.views import index 


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('players.urls')),
    path('generate/', player_views.generate_player, name='generate_player'),
    path('register/', player_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('', player_views.home, name='home'), 
]