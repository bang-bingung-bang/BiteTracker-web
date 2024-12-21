#editbites/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

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
    
def add_products_from_fixtures(request):
    with open('editbites/fixtures/data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        if isinstance(item, dict):  # Pastikan item adalah dictionary
            fields = item.get('fields', {})  # Ambil 'fields' dari item
            
            # Buat instance baru dari model Product
            product = Product(
                store=fields.get('store'),
                name=fields.get('name'),
                price=fields.get('price'),
                description=fields.get('description'),
                calories=fields.get('calories'),
                calorie_tag=fields.get('calorie_tag'),
                vegan_tag=fields.get('vegan_tag'),
                sugar_tag=fields.get('sugar_tag'),
                image=fields.get('image'),
                created_at=fields.get('created_at'),
                updated_at=fields.get('updated_at')
            )
            
            # Simpan instance ke database
            product.save()

            print(product)

    return HttpResponse('Products added successfully!')

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def create_product_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                store=data['fields']['store'],
                name=data['fields']['name'],
                price=data['fields']['price'],
                description=data['fields']['description'],
                calories=data['fields']['calories'],
                calorie_tag=data['fields']['calorie_tag'],
                vegan_tag=data['fields']['vegan_tag'],
                sugar_tag=data['fields']['sugar_tag'],
                image=data['fields']['image']
            )
            return JsonResponse({
                "status": "success",
                "message": "Product created successfully!",
                "product_id": product.id
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def edit_product_mobile(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = get_object_or_404(Product, pk=pk)
            
            # Update fields
            for key, value in data['fields'].items():
                setattr(product, key, value)
            product.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Product updated successfully!"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_product_mobile(request, pk):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return JsonResponse({
                "status": "success",
                "message": "Product deleted successfully!"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)