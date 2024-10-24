from django.shortcuts import render, redirect, get_object_or_404
from MyBites.models import Product, MyBites
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def show_main(request):
    return render(request, 'mybites.html')

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def add_to_wishlist(request, product_id):
    # if request.user.is_authenticated:
    product = get_object_or_404(Product, id=product_id)
    MyBites.objects.get_or_create(user=None, product=product)
    return redirect('MyBites:wishlist')
    # else:
    #     messages.warning(request, "You need to log in to add products to your wishlist.")
    #     return redirect('MyBites:show_main')


def view_wishlist(request):
    # if request.user.is_authenticated:
    wishlist_items = MyBites.objects.all()
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    # else:
    #     return render(request, 'MyBites/wishlist.html', {'wishlist_items': [], 'message': 'Please log in to see your wishlist.'})
    
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    MyBites.objects.filter(user=None, product=product).delete()
    return redirect('MyBites:wishlist')

def show_product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})