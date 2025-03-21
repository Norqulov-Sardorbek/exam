from django.urls import path
from shop.views import  *

app_name = 'shop'

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category'),
    path('product/<int:category_id>/', ProductListView.as_view(), name='index'),
    path('product_detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products-of-category/<int:category_id>/', ProductListView.as_view(), name='products_of_category'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer-delete/<int:customer_id>/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer-edit/<int:customer_id>/', CustomerUpdateView.as_view(), name='customer-edit'),
    path('customer-add/', CustomerCreateView.as_view(), name='customer-add'),
    path('download-customers/', DownloadCustomersView.as_view(), name='download-customers'),
    path('send-email/', EmailFormView.as_view(), name='send-email'),
]
