from django.contrib import admin
from .models import Player
from .models import Club


admin.site.register(Player)
admin.site.register(Club)
admin.site.register(Lineup)
admin.site.register(LineupPlayer)