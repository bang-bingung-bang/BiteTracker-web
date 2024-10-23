from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def main(request):
    products = Product.objects.all()
    return render(request, 'main.html', {'products': products})

# @login_required
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'editbites/admin_dashboard.html', {
        'products': products
    })

# @login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan')
            return redirect('editbites:admin_dashboard')
        messages.error(request, 'Terjadi kesalahan. Silakan periksa form kembali.')
    else:
        form = ProductForm()
    return render(request, 'editbites/product_form.html', {
        'form': form, 
        'action': 'Add'
    })

# @login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui')
            return redirect('editbites:admin_dashboard')
        messages.error(request, 'Terjadi kesalahan. Silakan periksa form kembali.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'editbites/product_form.html', {
        'form': form, 
        'action': 'Edit'
    })

# @login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if product.image:
            product.image.delete()
        product.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_products_json(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'id': product.pk,
            'store': product.get_store_display(),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'calories': product.calories,
            'calorie_tag': product.get_calorie_tag_display(),
            'vegan_tag': product.get_vegan_tag_display(),
            'sugar_tag': product.get_sugar_tag_display(),
            'image_url': product.image,
        })
    return JsonResponse(data, safe=False)