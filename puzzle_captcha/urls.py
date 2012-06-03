from django.conf.urls.defaults import *

urlpatterns = patterns('puzzle_captcha.views',
    url(r'download/(?P<pk>.+)$', 'download_handler', name='puzzle-piece'),
)
