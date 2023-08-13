from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from games.models import Game, Sport, Team, TeamAlias

from .serializers import GamesBySportSerializer, GameSerializer, TeamSerializer, TeamAliasSerializer



# print('views.py')

class GamesBySportList(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        sport_name = self.kwargs['sport_name']
        return Game.objects.filter(sport__name=sport_name).order_by('game_date', 'game_time')


class Games(generics.ListCreateAPIView):
    
    serializer_class = GameSerializer
    print('Games root')
    def get_queryset(self):
        print('games queryset')

        return Game.objects.all().order_by('game_date', 'game_time')
    
    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    



class NestedGamesBySport(APIView):
    def get(self, request):
        sports = Sport.objects.all().prefetch_related('game_set')
        serializer = GamesBySportSerializer(sports, many=True)
        # print(serializer.data)
        data = {item['name'].lower(): item['games'] for item in serializer.data}
        return Response(data)
    


class Teams(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            is_many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=is_many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TeamAlias(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = TeamAlias.objects.all()
    serializer_class = TeamAliasSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            is_many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=is_many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)