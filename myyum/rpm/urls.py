from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myyum.rpm.views',
    url(r"^$", 'repository_index', name="rpm_root"),
    
    url(r"repo$", 'repository_index'),
    url(r"repo/create$", 'repository_create'),
    url(r"repo/(\d+)$", 'repository_view'),
    url(r"repo/(\d+)/update$", 'repository_update'),
    url(r"repo/(\d+)/config$", 'repository_config'),
    url(r"repo/(\d+)/edit$", 'repository_edit'),
    url(r"repo/(\d+)/delete$", 'repository_delete'),
    url(r"repo/(\d+)/pkg/upload$", 'package_upload'),
    url(r"repo/(\d+)/pkg/(\d+)$", 'package_view'),
    url(r"repo/(\d+)/pkg/(\d+)/delete$", 'package_delete'),
)
