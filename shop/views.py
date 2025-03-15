
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from shop.models import *


# Create your views here.

def categories_page(request):
    categories = Category.objects.all()
    return render(request, 'shop/category.html', {'categories': categories})

def index(request, category_id: int | None = None):
    search_query = request.GET.get('q', '')
    filter_query = request.GET.get('filter', '')

    if category_id:
        products = Product.objects.filter(category_id=category_id)

    else:
        products = Product.objects.all().order_by('-updated_at')

    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if filter_query == 'expensive':
        products = products.order_by('-price')

    elif filter_query == 'cheap':
        products = products.order_by('price')

    for product in products:
        image = ProductImage.objects.filter(product=product).first()
    context = {
        'products': products,
        'image': image,
    }
    return render(request, 'shop/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    specifications = ProductSpecifications.objects.filter(product=product)

    context = {
        'product': product,
        'images': images,
        'specifications': specifications,
    }
    return render(request, 'shop/detail.html', context)

