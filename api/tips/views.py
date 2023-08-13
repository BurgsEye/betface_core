from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from tips.models import Tip, Tipster

from .serializers import TipSerializer, TipsterSerializer


class Tipsters(generics.ListCreateAPIView):
    serializer_class = TipsterSerializer
    def get_queryset(self):
        return Tipsters.objects.all()


class Tips(generics.ListCreateAPIView):
    serializer_class = TipSerializer
    def get_queryset(self):
        return Tip.objects.all().order_by('game__game_date')
