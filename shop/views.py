from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        product.image = ProductImage.objects.filter(product=product).first()
    context = {
        'products': products,
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


def customers_page(request):
    customers = Customers.objects.all()
    return render(request, 'shop/customers.html', {'customers': customers})


def customer_delete(request, customer_id):
    customer = get_object_or_404(Customers, id=customer_id)
    customer.delete()
    return redirect('shop:customers')


def customer_edit(request, customer_id):
    customer = get_object_or_404(Customers, id=customer_id)

    if request.method == "POST":
        customer.first_name = request.POST.get("first_name")
        customer.last_name = request.POST.get("last_name")
        customer.email = request.POST.get("email")
        customer.number = request.POST.get("number")
        customer.address = request.POST.get("address")

        if 'image' in request.FILES:
            customer.image = request.FILES['image']

        customer.save()
        return redirect('shop:customers')
    context = {
        'customer': customer,
    }
    return render(request, 'shop/customer-edit.html', context)


def customer_add(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        address = request.POST.get("address")
        image = request.FILES.get("image", None)

        customer = Customers.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            number=number,
            address=address,
            image=image
        )
        return redirect('shop:customers')

    return render(request, 'shop/customer-edit.html', )


def download_customers(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customers.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    y = 750


    pdf.drawString(30, y, "First Name")
    pdf.drawString(130, y, "Last Name")
    pdf.drawString(230, y, "Email")
    pdf.drawString(380, y, "Phone Number")
    pdf.drawString(530, y, "Address")

    y -= 20


    customers = Customers.objects.all()
    for customer in customers:
        pdf.drawString(30, y, customer.first_name)
        pdf.drawString(130, y, customer.last_name)
        pdf.drawString(230, y, customer.email)
        pdf.drawString(380, y, customer.number)
        pdf.drawString(530, y, customer.address)
        y -= 20
    pdf.save()
    return response
