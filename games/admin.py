from django.contrib import admin
from .models import Game, Team, Sport, TeamAlias

admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Sport)
admin.site.register(TeamAlias)
# Register your models here.
