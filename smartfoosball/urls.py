from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from django.contrib import admin
admin.autodiscover()


from smartfoosball import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wifitest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Index.as_view(), name="index"), # html

    # url(r'^register/(.+)', views.PlayerRegister.as_view(), name="player_reg"),
    # url(r'^player/(.+)/creategame', views.GameCreate.as_view(), name="game_create"),
    # url(r'^game/(.+)/player/(.+)/position/(\d+)/(\d+)', views.GamePosition.as_view(), name="game_pos"),
    # url(r'^game/(.+)/score_board', views.GameScore.as_view(), name="game_score"), # html
    # simulater
    #'/db/game/(.+)/player/(\d+)/goal/(\d+)', 'PlayerGoal',

    url(r'^wechat_echo$', csrf_exempt(views.WechatEcho.as_view()), name="wechat_echo"),
    url(r'^games$', views.GameView.as_view(), name="games"),
    url(r'^players$', views.PlayerView.as_view(), name="players"),
    url(r'^me$', views.MeView.as_view(), name="me"),
    url(r'^wechat/oauth2$', views.wechat_oauth2, name="wechat_oauth2")
)
