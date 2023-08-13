from django.urls import path

from . import views

urlpatterns = [
    path('', views.Games.as_view(), name='api_games'),

    path('teams/', views.Teams.as_view(), name='api_teams'),
    path('teams/alias', views.TeamAlias.as_view(), name='api_teams_alias'),
    path('games-by-sport/', views.NestedGamesBySport.as_view(), name='games-by-sport'),
    path('<str:sport_name>/', views.GamesBySportList.as_view(), name='api_games_by_sport'),
]
