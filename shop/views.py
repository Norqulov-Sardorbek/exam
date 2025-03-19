from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Category, Product, ProductImage, ProductSpecifications, Customers
from django.db.models import Q

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q', '')
        filter_query = self.request.GET.get('filter', '')
        
        products = Product.objects.all().order_by('-updated_at')
        if category_id:
            products = products.filter(category_id=category_id)
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if filter_query == 'expensive':
            products = products.order_by('-price')
        elif filter_query == 'cheap':
            products = products.order_by('price')
        
        for product in products:
            product.image = ProductImage.objects.filter(product=product).first()
        return products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object)
        context['specifications'] = ProductSpecifications.objects.filter(product=self.object)
        return context


class CustomerListView(ListView):
    model = Customers
    template_name = 'shop/customers.html'
    context_object_name = 'customers'


class CustomerDeleteView(DeleteView):
    model = Customers
    success_url = reverse_lazy('shop:customers')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CustomerUpdateView(UpdateView):
    model = Customers
    fields = ['first_name', 'last_name', 'email', 'number', 'address', 'image']
    template_name = 'shop/customer-edit.html'
    success_url = reverse_lazy('shop:customers')


class CustomerCreateView(CreateView):
    model = Customers
    fields = ['first_name', 'last_name', 'email', 'number', 'address', 'image']
    template_name = 'shop/customer-edit.html'
    success_url = reverse_lazy('shop:customers')


class DownloadCustomersView(View):
    def get(self, request, *args, **kwargs):
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
