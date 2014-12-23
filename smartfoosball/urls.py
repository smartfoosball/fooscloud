from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


from smartfoosball import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wifitest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Index.as_view(), name="index"), # html

    url(r'^wechat_echo$', csrf_exempt(views.WechatEcho.as_view()), name="wechat_echo"),
    url(r'^games$', views.GameView.as_view(), name="games"),
    url(r'^games/(?P<gid>\d+)/join$', views.GameJoinView.as_view(), name='game_join'),
    url(r'^games/(?P<gid>\d+)/start$', views.GameStartView.as_view(), name='game_start'),
    url(r'^games/(?P<gid>\d+)/end$', views.GameEndView.as_view(), name='game_end'),
    url(r'^games/(?P<gid>\d+)/$', views.GameDetailView.as_view(), name='game_detail'),
    url(r'^games/history/$', views.GameHistoryView.as_view(), name='game_history'),
    url(r'^games/(?P<gid>\d+)/score$', views.GameScoreView.as_view(), name='game_score'),
    url(r'^players$', views.PlayerView.as_view(), name="players"),
    url(r'^me$', views.MeView.as_view(), name="me"),
    url(r'^wechat/oauth2$', views.wechat_oauth2, name="wechat_oauth2"),
    url(r'^qrcode$', views.qrcode, name="qrcode")
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
