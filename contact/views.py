from django.shortcuts import render
from django.views import generic
from .forms import ContactForm
# Create your views here.

class Contact(generic.FormView):
	template_name = 'contact/contact.html'
	form_class = ContactForm

	def form_isvalid(self, form):
		"""
		Logic for when form is valid, send email to
		admins.
		"""
		
		return HttpResponseRedirect(self.get_success_url())
