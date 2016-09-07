# wemenshop/checkout/views.py
import logging

from django import http
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils import six
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.views import generic

from oscar.apps.shipping.methods import NoShippingRequired
from oscar.core.loading import get_class, get_classes, get_model


ShippingAddressForm, ShippingMethodForm, GatewayForm \
	= get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])
OrderCreator = get_class('order.utils', 'OrderCreator')
UserAddressForm = get_class('address.forms', 'UserAddressForm')
Repository = get_class('shipping.repository', 'Repository')
AccountAuthView = get_class('customer.views', 'AccountAuthView')
RedirectRequired, UnableToTakePayment, PaymentError \
	= get_classes('payment.exceptions', ['RedirectRequired',
										 'UnableToTakePayment',
										 'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
Order = get_model('order', 'Order')
ShippingAddress = get_model('order', 'ShippingAddress')
CommunicationEvent = get_model('order', 'CommunicationEvent')
PaymentEventType = get_model('order', 'PaymentEventType')
PaymentEvent = get_model('order', 'PaymentEvent')
UserAddress = get_model('address', 'UserAddress')
Basket = get_model('basket', 'Basket')
Email = get_model('customer', 'Email')
Country = get_model('address', 'Country')
CommunicationEventType = get_model('customer', 'CommunicationEventType')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')

# Import klarnacheckout
import klarnacheckout

# override here
