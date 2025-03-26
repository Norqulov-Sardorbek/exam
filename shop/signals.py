from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.text import slugify
from .models import *
import random
def send_email_to_admins(subject, message):
    admins = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
    if admins:
        send_mail(
            subject,
            message,
            'nsardorbek776@gmail.com',
            list(admins),
            fail_silently=False
        )
def random():
    return random.randit(100000000,999999999)

@receiver(post_save, sender=Category)
def category(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Kategoriya yaratildi', f'Yangi kategoriya {instance} qo‘shildi.')
    else:
        send_email_to_admins('Kategoriya yangilandi', f'Kategoriya {instance} yangilandi.')

@receiver(post_delete, sender=Category)
def category_del(sender, instance, **kwargs):
    send_email_to_admins('Kategoriya o‘chirildi', f'Kategoriya {instance} o‘chirildi.')

@receiver(post_save, sender=Product)
def product(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Mahsulot yaratildi', f'Yangi mahsulot {instance} qo‘shildi.')
    else:
        send_email_to_admins('Mahsulot yangilandi', f'Mahsulot {instance} yangilandi.')

@receiver(post_delete, sender=Product)
def product_del(sender, instance, **kwargs):
    send_email_to_admins('Mahsulot o‘chirildi', f'Mahsulot {instance} o‘chirildi.')

@receiver(post_save, sender=ProductImage)
def product_image(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Mahsulot rasmi yaratildi', f'Mahsulot {instance.product} uchun yangi rasm qo‘shildi.')
    else:
        send_email_to_admins('Mahsulot rasmi yangilandi', f'Mahsulot {instance.product} rasmi yangilandi.')

@receiver(post_delete, sender=ProductImage)
def product_image_del(sender, instance, **kwargs):
    send_email_to_admins('Mahsulot rasmi o‘chirildi', f'Mahsulot {instance.product} rasmi o‘chirildi.')

@receiver(post_save, sender=ProductKeys)
def product_keys(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Mahsulot kaliti yaratildi', f'Yangi kalit {instance} qo‘shildi.')
    else:
        send_email_to_admins('Mahsulot kaliti yangilandi', f'Kalit {instance} yangilandi.')

@receiver(post_delete, sender=ProductKeys)
def product_keys_del(sender, instance, **kwargs):
    send_email_to_admins('Mahsulot kaliti o‘chirildi', f'Kalit {instance} o‘chirildi.')

@receiver(post_save, sender=ProductValues)
def product_values(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Mahsulot qiymati yaratildi', f'Yangi qiymat {instance} qo‘shildi.')
    else:
        send_email_to_admins('Mahsulot qiymati yangilandi', f'Qiymat {instance} yangilandi.')

@receiver(post_delete, sender=ProductValues)
def product_values_del(sender, instance, **kwargs):
    send_email_to_admins('Mahsulot qiymati o‘chirildi', f'Qiymat {instance} o‘chirildi.')

@receiver(post_save, sender=ProductSpecifications)
def product_specifications(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Mahsulot xususiyati yaratildi', f'Mahsulot {instance.product} uchun yangi xususiyat qo‘shildi.')
    else:
        send_email_to_admins('Mahsulot xususiyati yangilandi', f'Mahsulot {instance.product} xususiyati yangilandi.')

@receiver(post_delete, sender=ProductSpecifications)
def product_specifications_del(sender, instance, **kwargs):
    send_email_to_admins('Mahsulot xususiyati o‘chirildi', f'Mahsulot {instance.product} xususiyati o‘chirildi.')

@receiver(post_save, sender=Customers)
def customers(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Customer yaratildi', f'Yangi mijoz {instance.full_name} qo‘shildi.')
        print(random())
    else:
        send_email_to_admins('Customer yangilandi', f'Customer {instance.full_name} yangilandi.')

@receiver(post_delete, sender=Customers)
def customers_del(sender, instance, **kwargs):
    send_email_to_admins('Customer o‘chirildi', f'Customer {instance.full_name} o‘chirildi.')