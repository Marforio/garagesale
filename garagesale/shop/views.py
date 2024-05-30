from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Category, Product, Order, ProductImage
from .forms import OrderCreateForm, ProductCreateForm, ProductImageForm
from django.contrib.auth.decorators import login_required

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    # access the images through product bc the ProductImage object is related
    product_images = product.images.all()  
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'product_images': product_images
        })

def product_order(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('shop:order_success')
    else:
        form = OrderCreateForm(initial={'product': product})
    return render(request, 'shop/product/order.html', {'form': form, 'product': product})
    
def order_success(request):
    return render(request, "shop/product/success.html")

@login_required
def order_list(request, settled_or_open="open"):
    orders = Order.objects.filter(settled=False)
    filter = "open"
    if settled_or_open=="settled":
        orders = Order.objects.filter(settled=True)
        filter = "settled"
    if settled_or_open=="all":
        orders = Order.objects.all()
        filter = "all"

    return render(request, 'shop/dashboard.html', {
        'orders': orders,
        'filter': filter
    })

@login_required
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)
    if request.method == 'POST':
        product_form = ProductCreateForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = ProductImage(product=product, image=image)
                    photo.save()

            return redirect('shop:product_add_success')
    else:
        product_form = ProductCreateForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())
        
    return render(request, 'shop/add.html', {'product_form': product_form, 'formset': formset})

def product_add_success(request):
    return render(request, "shop/add_success.html")