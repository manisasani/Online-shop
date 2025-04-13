from django.shortcuts import render

from django.views.generic import TemplateView
from products.models import Category, Product

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(active=True)[:8]
        return context

class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'
