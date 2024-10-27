from django.shortcuts import render, redirect, get_object_or_404
from MyBites.models import MyBites
from editbites.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def show_main(request):
    return render(request, 'main/main.html')

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def add_to_wishlist(request, product_id):
    # if request.user.is_authenticated:
    product = get_object_or_404(Product, id=product_id)
    MyBites.objects.get_or_create(user=request.user, product=product)
    messages.success(request, "Product added to wishlist!")
    return redirect('MyBites:wishlist')
    # else:
    #     messages.warning(request, "You need to log in to add products to your wishlist.")
    #     return redirect('MyBites:show_main')

@login_required
def view_wishlist(request):
    # if request.user.is_authenticated:
    wishlist_items = MyBites.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    # else:
    #     return render(request, 'MyBites/wishlist.html', {'wishlist_items': [], 'message': 'Please log in to see your wishlist.'})
    
@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    MyBites.objects.filter(user=request.user, product=product).delete()
    messages.success(request, "Product removed from wishlist.")
    return redirect('MyBites:wishlist')

@login_required
def show_product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})