from django.shortcuts import render, redirect, get_object_or_404
from MyBites.models import MyBites
from editbites.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

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

@csrf_exempt
def add_wishlist_flutter(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        new_bites = MyBites.objects.create(
            user=request.user,
            product=product
        )
        new_bites.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def view_wishlist_flutter(request):
    if request.method == "GET":
        wishlist_items = MyBites.objects.filter(user=request.user)
        wishlist_data = [
            {
                "model": "editbites.product",
                "pk": item.pk,
                "fields": {
                    "store": item.product.store,
                    "name": item.product.name,
                    "price": item.product.price,
                    "description": item.product.description,
                    "calories": item.product.calories,
                    "calorie_tag": item.product.calorie_tag,
                    "vegan_tag": item.product.vegan_tag,
                    "sugar_tag": item.product.sugar_tag,
                    "image": item.product.get_image_url(),
                }
            }
            for item in wishlist_items
        ]
        return JsonResponse({"wishlist": wishlist_data}, safe=False)

@csrf_exempt
def remove_flutter(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    product = get_object_or_404(Product, id=product_id)

    MyBites.objects.filter(user=request.user, product=product).delete()

    updated_wishlist_items = MyBites.objects.filter(user=request.user)

    wishlist_data = [
        {
            "model": "editbites.product",
            "pk": item.product.pk,
            "fields": {
                "store": item.product.store,
                "name": item.product.name,
                "price": item.product.price,
                "description": item.product.description,
                "calories": item.product.calories,
                "calorie_tag": item.product.calorie_tag,
                "vegan_tag": item.product.vegan_tag,
                "sugar_tag": item.product.sugar_tag,
                "image": item.product.get_image_url(),
            }
        }
        for item in updated_wishlist_items
    ]

    return JsonResponse({"wishlist": wishlist_data}, safe=False)

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