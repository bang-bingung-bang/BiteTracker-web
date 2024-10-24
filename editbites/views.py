from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from .models import Product
from .forms import ProductForm, LoginForm, RegisterForm

def main(request):
    products = Product.objects.all()
    return render(request, 'editbites/main.html', {'products': products})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('editbites:main')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('editbites:main')
    else:
        form = RegisterForm()
    return render(request, 'editbites/auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('editbites:main')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'editbites:main')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'editbites/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('editbites:login')

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    print(f"User: {request.user.username}, is_staff: {request.user.is_staff}")
    products = Product.objects.all()
    return render(request, 'editbites/admin_dashboard.html', {
        'products': products
    })

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('editbites:admin_dashboard')
        else:
            messages.error(request, 'Error adding product. Please check the form.')
    else:
        form = ProductForm()
    return render(request, 'editbites/product_form.html', {
        'form': form,
        'action': 'Add'
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
            return redirect('editbites:admin_dashboard')
        else:
            messages.error(request, 'Error updating product. Please check the form.')
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
            'image_url': product.get_image_url()
        })
    return JsonResponse(data, safe=False)