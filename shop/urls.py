from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('category/', views.categories_page, name='category'),
    path('product/<int:category_id>/', views.index, name='index'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products-of-category/<int:category_id>/', views.index, name='products_of_category'),
    path('customers/', views.customers_page, name='customers'),
    path('customer-delete/<int:customer_id>/', views.customer_delete, name='customer-delete'),
    path('customer-edit/<int:customer_id>/', views.customer_edit, name='customer-edit'),
path('customer-add/', views.customer_add, name='customer-add'),
path('download-customers/', views.download_customers, name='download-customers'),



]
