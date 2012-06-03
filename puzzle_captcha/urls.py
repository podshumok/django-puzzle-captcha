from django.conf.urls.defaults import *

urlpatterns = patterns('puzzle_captcha.views',
    url(r'download/(?P<pk>.+)$', 'download_handler_piece', name='puzzle-piece'),
    url(r'thumb/(?P<key>.+)$', 'download_handler_thumb', name='puzzle-thumb'),
)
