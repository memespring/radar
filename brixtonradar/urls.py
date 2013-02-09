from django.contrib import admin
from django.conf.urls.defaults import *
from main import views as main_views
import settings

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', main_views.index, name='index'),
    url(r'^e/(?P<event_id>[0-9]*)/$', main_views.event, name='event'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^site-media/(?P<path>.*)$',       'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT, 'show_indexes':True}),

)
