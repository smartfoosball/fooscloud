from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from smartfoosball.models import *


class PlayerInline(admin.StackedInline):
    model = Player

class UserAdmin(UserAdmin):

    list_display = ('username', 'weixin', 'date_joined')
    inlines = (PlayerInline,)

    def weixin(self, instance):
        return instance.player.nickname

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GWUser)
admin.site.register(FoosBall)
