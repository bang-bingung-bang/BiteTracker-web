from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

def is_admin(user):
    return user.is_staff

@login_required
def product_list(request):
    filter_param = request.GET.get('filter')
    products = Product.objects.all()

    if filter_param:
        if filter_param == 'high_calories':
            products = products.filter(calorie_tag='HIGH')
        elif filter_param == 'high_sugar':
            products = products.filter(sugar_tag='HIGH')
        elif filter_param == 'low_calorie':
            products = products.filter(calorie_tag='LOW')
        elif filter_param == 'low_sugar':
            products = products.filter(sugar_tag='LOW')
        elif filter_param == 'non_vegan':
            products = products.filter(vegan_tag='NON_VEGAN')
        elif filter_param == 'vegan':
            products = products.filter(vegan_tag='VEGAN')

    return render(request, 'editbites/product_list.html', {
        'products': products,
        'is_admin': request.user.is_staff
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'editbites/product_detail.html', {
        'product': product,
        'is_admin': request.user.is_staff
    })

@login_required
@user_passes_test(is_admin)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('editbites:product_list')
    else:
        form = ProductForm()
    return render(request, 'editbites/product_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
@user_passes_test(is_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('editbites:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'editbites/product_form.html', {
        'form': form,
        'action': 'Edit'
    })

@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('editbites:product_list')
    return render(request, 'editbites/product_confirm_delete.html', {
        'product': product
    })

@login_required
def get_product_json(request):
    data = Product.objects.all()
    
    if data.exists():
        return JsonResponse(serializers.serialize("json", data), safe=False)
    else:
        return JsonResponse([], safe=False)