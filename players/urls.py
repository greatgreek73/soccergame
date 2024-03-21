from django.urls import path
from . import views
from players.views import index

urlpatterns = [
    # ... другие маршруты ...
    path('generate/', views.generate_player, name='generate_player'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),
    path('create_club/', views.create_club, name='create_club'),
    path('club/<int:club_id>/generate_player/', views.generate_player_for_club, name='generate_player_for_club'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('', index, name='index'),
    path('match/<int:club1_id>/<int:club2_id>/', views.start_match, name='start_match'),

]
