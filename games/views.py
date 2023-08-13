from django.views.generic.list import ListView
from .models import Game, Sport


class GamesBySportView(ListView):
    model = Game
    template_name = 'games/game_list_by_sport.html'  # You can name the template as you see fit
    context_object_name = 'games'  # This will be the name of the list in the template

    def get_queryset(self):
        # Filter games based on the sport provided in the URL
        sport_name = self.kwargs.get('sport_name')
        return Game.objects.filter(sport__name=sport_name).order_by('game_date', 'game_time')
