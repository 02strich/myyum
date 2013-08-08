from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^", include('rpm.urls')),
    url(r"", include('social_auth.urls')),

    url(r"^login$", 'django.contrib.auth.views.login', {'template_name': "login.html"}),
    url(r"^logout$", 'django.contrib.auth.views.logout', {'next_page': "/"}),

    # REST API
    url(r'^api/', include('rpm.api')),
    # Uncomment the next line to support authentication when using the API in a browser
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    # Examples:
    # url(r'^$', 'myyum.views.home', name='home'),
    # url(r'^myyum/', include('myyum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
   )