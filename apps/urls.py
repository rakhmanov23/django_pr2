from django.urls import path

from apps.views import FalconTemplateView, ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('falcon/', FalconTemplateView.as_view(), name='tmp_pg'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='pr_detail'),
]