from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from inventory import views

urlpatterns = patterns('',
        url(r'^order$', views.order, name='order'),
        url(r'^report$', views.report, name='report'),
        url(r'^entry$', views.entry, name='entry'),
        )

urlpatterns += staticfiles_urlpatterns()
