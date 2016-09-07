from django.conf.urls import include, url
from .views import KlarnaCheckout

urlpatterns = [
    url(r'$', KlarnaCheckout.as_view(), name="klarna-checkout"),
]