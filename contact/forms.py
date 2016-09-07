from django import forms
from django.utils.translation import ugettext as _

class ContactForm(forms.Form):

	your_name = forms.CharField(label=_('Your name'), max_length=30
								required=True)
	your_email = forms.EmailField(label=_('Your email'),required=True)
	your_message = forms.TextField(label=_('Your message to us, no mo then 500 characters please'), 
								   max_length=500, required=True,
								   widget=forms.Textarea)
