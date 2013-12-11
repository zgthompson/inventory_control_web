from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from inventory import views

urlpatterns = patterns('',
        url(r'^$', views.order, name='order'),
        )

urlpatterns += staticfiles_urlpatterns()
