from django import forms
from django.utils.text import slugify
from parler.forms import TranslatableModelForm
from .models import Order, Product, ProductImage

class OrderCreateForm(TranslatableModelForm):
    class Meta:
        model = Order
        fields = ['product','first_name', 'last_name', 'email', 'phone', 'address', 'comment']
        widgets = { 'product': forms.HiddenInput()}

class ProductCreateForm(TranslatableModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price']

    def save(self):
        instance = super(ProductCreateForm, self).save(commit=False)
        instance.slug = slugify(instance.name)
        instance.save()
        return instance

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_cover']