from django.shortcuts import render, get_object_or_404
from games.models import Game
from tips.models import Tip
from django.db.models import Count

from datetime import datetime

# Create your views here.


# def game_list(request):
#     games = Game.objects.annotate(num_tips=Count('tip')).all().order_by('-game_date')
#     print(games)
#     return render(request, 'game_list.html', {'games': games})

def game_list(request):
    game_date = request.GET.get('game_date')
    games_query = Game.objects.annotate(num_tips=Count('tip'))

    

    if game_date:
        # Convert the date string to a datetime object
        game_date_obj = datetime.strptime(game_date, '%Y-%m-%d').date()
        games_query = games_query.filter(game_date=game_date_obj)
    
    games = games_query.order_by('-game_date').all()
    return render(request, 'game_list.html', {'games': games})



def game_tips(request, game_id=None):

    if game_id is None:

        tips = Tip.objects.all()
        print(tips)
        return render(request, 'game_tips.html', {'game': None, 'tips': tips})
    else:
        game = get_object_or_404(Game, pk=game_id)
        tips = Tip.objects.filter(game=game)

        return render(request, 'game_tips.html', {'game': game, 'tips': tips})