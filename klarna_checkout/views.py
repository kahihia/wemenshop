from django.shortcuts import render
from django.views import generic

# Import klarnacheckout
import klarnacheckout


def decimal_to_longint(decimal):
	# Converting decimal i.e 129.00 to 12900
	# for klarna data
	str_repr = str(decimal)
	longint = str_repr.replace('.', '')
	return int(longint)

class KlarnaCheckout(generic.TemplateView):

	template_name = 'klarna_checkout/klarna_snippet.html'

	def connect_to_klarna(self, request):
		"""
		Connects to klarnas API and make an order
		object at klarna with products from basket.

		Cart example below:
		cart = [(
				{
					'quantity': 1,
					'reference': '123456789',
					'name': 'Klarna t-shirt',
					'unit_price': 12300,
					'discount_rate': 1000,
					'tax_rate': 2500
				}, {
					'quantity': 1,
					'type': 'shipping_fee',
					'reference': 'SHIPPING',
					'name': 'Shipping Fee',
					'unit_price': 4900,
					'tax_rate': 2500
				}
			)]
		
		
		"""
		cart = []
		basket = self.request.basket
		for line in basket.all_lines():
			# Adding each line from basket to klarna cart
			# klarna requires list of tuples where shippment
			# price is included for each product
			line_json = ({
				'quantity' : line.quantity,
				'reference' : str(line.product.pk),
				'name' : str(line.product.get_title()),
				'unit_price' : decimal_to_longint(line.unit_price_incl_tax),
				'discount_rate' : decimal_to_longint(line.discount_value),
				'tax_rate' : decimal_to_longint(line._tax_ratio),

			},{
				'quantity': 1,
				'type': 'shipping_fee',
				'reference': 'SHIPPING',
				'name': 'Shipping Fee',
				'unit_price': 0,
				'discount_rate' : 0,
				'tax_rate': 0,
			})
			cart.append(line_json)
		
		# Creating data for klarna
		create_data = {}
		create_data["cart"] = {"items": []}

		for obj in cart:
			for item in obj:
				create_data["cart"]["items"].append(item)

		create_data['purchase_country'] = 'SE'
		create_data['purchase_currency'] = 'SEK'
		create_data['locale'] = 'sv-se'
		create_data['merchant'] = {
			'id': '7485',
			'back_to_store_uri': 'http://109.124.136.183:8000',
			'terms_uri': 'http://109.124.136.183:8000/terms',
			'checkout_uri': 'http://109.124.136.183:8000/checkout',
			'confirmation_uri': ('http://109.124.136.183:8000/thank-you' +
								 '?klarna_order_id={checkout.order.id}'),
			'push_uri': ('http://109.124.136.183:8000/push' +
						 '?klarna_order_id={checkout.order.id}')
		}
		connector = klarnacheckout.create_connector('axxB71XSbDuTyox',
											klarnacheckout.BASE_TEST_URL)
		order = klarnacheckout.Order(connector)
		order.create(create_data)

		order.fetch()
		# Store order id of checkout session
		request.session['klarna_order_id'] = order['id']

		return order["gui"]["snippet"]

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['klarna_order'] = self.connect_to_klarna(request)

		return self.render_to_response(context)