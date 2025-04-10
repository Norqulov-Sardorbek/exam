from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Category, Product, ProductImage, ProductSpecifications, Customers
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
import csv
import json
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from openpyxl import Workbook

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
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CustomerUpdateView(UpdateView):
    model = Customers
    fields = ['first_name', 'last_name', 'email', 'number', 'address', 'image']
    template_name = 'shop/customer-edit.html'
    success_url = reverse_lazy('shop:customers')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


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


class EmailFormView(View):
    template_name = "shop/emailSend.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        emails = request.POST.get("emails", "").strip()
        message = request.POST.get("message", "").strip()

        if not emails or not message:
            messages.error(request, "Iltimos, barcha maydonlarni to'ldiring.")
            return redirect("shop:send-email")

        email_list = emails.split()

        for email in email_list:
            send_mail(
                "Assalomu alekum!"
                "Norqulov Sardor",
                "nsardorbek776@gmail.com",
                [email],
                fail_silently=False,
            )

        messages.success(request, "Email yuborildi.")
        return redirect("shop:send-email")


def export_data(request):
    format = request.GET.get('format')
    if format == 'csv':
        meta = Customers._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=customer_list.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Customer.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customers.objects.all().values('id', 'full_name', 'email', 'phone_number', 'address', 'joined'))
        # response.content = json.dumps(data, indent=4)
        response.write(json.dumps(data, indent=4, default=str))
        response['Content-Disposition'] = 'attachment; filename=customers.json'
        return response


    elif format == 'xlsx':
        customers = Customers.objects.all()
        field_names = [field.name for field in Customers._meta.fields]
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(field_names)
        for customer in customers:
            row = [getattr(customer, field) for field in field_names]
            worksheet.append(row)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=customers.xlsx'
        workbook.save(response)
        return response


    elif format == 'xml':

        customers = Customers.objects.all()

        root = ET.Element('customers')

        for customer in customers:

            cust_elem = ET.SubElement(root, 'customer')

            for field in Customer._meta.fields:
                child = ET.SubElement(cust_elem, field.name)

                value = getattr(customer, field.name)

                child.text = str(value)

        tree = ET.ElementTree(root)

        response = HttpResponse(content_type='application/xml')

        response['Content-Disposition'] = 'attachment; filename=customers.xml'

        tree.write(response, encoding='unicode')

        return response
    else:
        response = HttpResponse(status=404)
        response.content = 'Bad request'
        return response