from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^forums/get/$', 'forums.views.getData'),
    (r'^forums/post/$', 'forums.views.postData'),                       
    
    url(r'^admin/', include(admin.site.urls)),
)
