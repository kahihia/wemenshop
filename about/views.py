from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class About(TemplateView):
	template_name = "about/_about.html"
