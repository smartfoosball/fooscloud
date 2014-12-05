from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from smartfoosball import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wifitest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Index.as_view(), name="index"), # html
    url(r'^game/(.+)/score_board', views.GameScore.as_view(), name="game_score"), # html
)
