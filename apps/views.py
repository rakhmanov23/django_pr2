from django.views.generic import TemplateView, DetailView

from django.views.generic import ListView

from apps.models import Product, Category


class ProductListView(ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'


class FalconTemplateView(TemplateView):
    template_name = 'apps/index.html'
