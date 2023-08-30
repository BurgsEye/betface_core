# urls.py

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('games/', views.game_list, name='game_list'),
    
    path('games/tips/<int:game_id>/', views.game_tips, name='game_tips'),
    path('games/tips/', views.game_tips, name='game_tips_all'),
    path('scrapers/', views.latest_logs, name='latest_logs'),
    path('scrapers/run_script/', views.run_script, name='run_script'),
]