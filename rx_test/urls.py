from django.conf.urls import include, url
from django.contrib.admin import site as admin_site

from resources.api import RespaAPIRouter
from resources.views.ical import ICalFeedView
from resources.views.images import ResourceImageView

router = RespaAPIRouter()

urlpatterns = [
    url(r'^admin/', include(admin_site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^resource_image/(?P<pk>\d+)$', ResourceImageView.as_view(), name='resource-image-view'),
    url(r'^v1/', include(router.urls)),
    url(r'^v1/reservation/ical/(?P<ical_token>[-\w\d]+).ics$', ICalFeedView.as_view(), name='ical-feed'),
]
