from django.db import models
from django.urls import reverse
import os
import uuid

def product_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('product_images', str(instance.product.id), filename)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
                models.Index(fields=['name']),
                ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # related_name='images' makes it possible to access all images from the Product object as Product.images
    image = models.ImageField(upload_to=product_image_upload_to)
    is_cover = models.BooleanField(default=False)

    def save(self):
        if self.is_cover:
            # Set all other images for this product as not cover
            ProductImage.objects.filter(product=self.product, is_cover=True).update(is_cover=False)
        super(ProductImage, self).save()

    def __str__(self):
        return f"{self.product.name} Image"

    class Meta:
        ordering = ['-is_cover', 'id']  # Ensures cover image appears first if queried

class Order(models.Model):
    product = models.ForeignKey(Product, related_name='order', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    settled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_absolute_url(self):
        return reverse("shop:order_list", args=[self.id])