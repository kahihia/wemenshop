from django.conf.urls import include, url
from django.contrib import admin

from about import views

urlpatterns = [
    url(r'', views.About.as_view(), name='about'),
]
