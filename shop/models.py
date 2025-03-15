from decimal import Decimal

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_image = models.ImageField(upload_to='category_images', null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)

    @property
    def image_abs(self):
        return self.category_image.url

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']


class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description_little = models.TextField(null=True, blank=True)
    description_big = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            discounted = self.price * Decimal(1 - self.discount / 100)
            return Decimal(f'{discounted}').quantize(Decimal('0.00'))
        return Decimal(f'{self.price}').quantize(Decimal('0.00'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        ordering = ['my_order']


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.image.url if self.image else "No Image"


class ProductKeys(BaseModel):
    key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.key


class ProductValues(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specifications_key = models.ForeignKey(ProductKeys, on_delete=models.CASCADE)
    specifications_value = models.ForeignKey(ProductValues, on_delete=models.CASCADE)
