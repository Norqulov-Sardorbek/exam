from django.contrib import admin
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('category/',views.categories_page,name='category'),
    path('product/<int:category_id>/', views.index, name='index'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products-of-category/<int:category_id>/', views.index, name='products_of_category')

]
