import json
from venv import logger
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from TrackerBites.models import BiteTrackerModel
from TrackerBites.forms import BiteTrackerForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import BiteTrackerModel

# Create your views here.
@login_required(login_url='/login/')
def show_tracker_bites(request):
    return render(request, 'tracker_bites.html')

def add_bite_calorie_entry(request):
    form = BiteTrackerForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        calorie_entry = form.save(commit=False)
        calorie_entry.user = request.user
        calorie_entry.save()
        return HttpResponseRedirect('/bite_tracker/')

    context = {
        'form': form
    }
    return render(request, 'add_bite_calorie_entry.html', context)

@csrf_exempt
@require_POST
def add_bite_calorie_entry_ajax(request):
    name = strip_tags(request.POST.get("bite_name"))
    calories = strip_tags(request.POST.get("bite_calories"))
    date = request.POST.get("bite_date")
    time = strip_tags(request.POST.get("bite_time"))
    user = request.user

    # Validasi input
    if not name or not calories or not date or not time:
        return HttpResponse({'success': False, 'error': 'All fields are required'}, status=400)
    

    # Simpan entri produk baru
    new_eat = BiteTrackerModel(
        user=user,
        bite_name=name,
        bite_calories=calories,
        bite_date=date,
        bite_time=time
    )
    new_eat.save()

    return HttpResponse({'success': True, 'message': 'Product created successfully'}, status=201)

@csrf_exempt
def add_bite_calorie_entry_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_bites = BiteTrackerModel.objects.create(
            user=request.user,
            bite_name=data['bite_name'],
            bite_calories=data['bite_calories'],
            bite_date=data['bite_date'],
            bite_time=data['bite_time']
        )

        new_bites.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


def delete_bite_entry_ajax(request, id):
    bite = BiteTrackerModel.objects.get(pk=id, user=request.user)
    if not bite:
        return HttpResponse({'success': False, 'error': 'Bite not found'}, status=404)
    bite.delete()

    return HttpResponse({'success': True, 'message': 'Bite deleted successfully'}, status=200)

def show_json_by_date(request, date):
    data = BiteTrackerModel.objects.filter(user=request.user, bite_date=date)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_bite_entry_ajax(request, id):
    bite = BiteTrackerModel.objects.get(pk=id, user = request.user)

    form = BiteTrackerForm(request.POST or None, instance=bite)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('TrackerBites:show_tracker_bites'))
    
    context = {
        'form': form,
    }

    return render(request, "edit_bite_calorie_entry.html", context)

def get_bite_tracker_json(request):
    data = BiteTrackerModel.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def get_bite_tracker_json_by_id(request, id):
    data = BiteTrackerModel.objects.get(pk=id, user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_bite_tracker_json_by_date(request, date):
    temp_data = BiteTrackerModel.objects.filter(user=request.user)
    data = temp_data.filter(bite_date=date)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_bite_tracker_json_by_date_and_time(request, date, time):
    time = time.capitalize()
    data = BiteTrackerModel.objects.filter(user=request.user, bite_time=time, bite_date=date)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def calculate_total_calories_by_date(request, date):
    
    total_calories = BiteTrackerModel.objects.filter(user=request.user, bite_date=date).aggregate(Sum('bite_calories'))
    total_calories_sum = total_calories['bite_calories__sum'] or 0
    total_calories_percentage = 100 if total_calories_sum > 2500 else (total_calories_sum / 2500) * 100 if total_calories_sum > 0 else 0
    total_bites = BiteTrackerModel.objects.filter(user=request.user, bite_date=date).count()

    response_data = {
        'total_bites': total_bites,
        'total_calories': total_calories_sum,
        'total_calories_percentage': total_calories_percentage
    }
    json_data = json.dumps(response_data)
    return HttpResponse(json_data, content_type="application/json")

def data_info_by_date(request, date):
    def calculate_meal_percentage(meal_count):
        return 100 if meal_count > 0 else 0

    user_bites = BiteTrackerModel.objects.filter(user=request.user, bite_date=date)
    
    total_calories = user_bites.aggregate(Sum('bite_calories'))
    total_calories_sum = total_calories['bite_calories__sum'] or 0
    
    total_bites = user_bites.count()
    
    meal_times = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    meal_counts = {meal: user_bites.filter(bite_time=meal).count() for meal in meal_times}
    meal_percentages = {meal: calculate_meal_percentage(meal_counts[meal]) for meal in meal_times}
    
    response_data = {
        'total_bites': total_bites,
        'total_calories': total_calories_sum,
        'meal_counts': meal_counts,
        'meal_percentages': meal_percentages,
    }
    
    return JsonResponse(response_data)

@csrf_exempt
def edit_bite_tracker_entry(request, id):
    if request.method == 'POST':
        # Ambil data dari request
        data = json.loads(request.body)

        bite_time = data['bite_time']
        bite_date = data['bite_date']
        bite_calories = data['bite_calories']
        bite_name = data['bite_name']
        
        # Validasi data
        if not bite_time or not bite_date or not bite_calories or not bite_name:
            return HttpResponseBadRequest("Missing required fields")
        
        try:
            bite_calories = int(bite_calories)
        except ValueError:
            return HttpResponseBadRequest("Invalid calories value")
        
        # Dapatkan entri yang akan diedit
        bite_entry = BiteTrackerModel.objects.get(pk=id, user = request.user)
        
        # Perbarui entri dengan data baru
        bite_entry.bite_name = bite_name
        bite_entry.bite_time = bite_time
        bite_entry.bite_date = bite_date
        bite_entry.bite_calories = bite_calories
        bite_entry.save()
        
        # Kembalikan respons sukses
        return JsonResponse({
            'id': bite_entry.id,
            'bite_time': bite_entry.bite_time,
            'bite_date': bite_entry.bite_date,
            'bite_calories': bite_entry.bite_calories,
            'status': 'success'
        }, status=200)
    else:
        return HttpResponseBadRequest("Invalid request method")

@csrf_exempt
def delete_bite_flutter(request, id):
    if request.method == 'POST':
        bite = BiteTrackerModel.objects.filter(pk=id, user=request.user)
        if not bite:
            return JsonResponse({'success': False, 'error': 'Bite not found'}, status=404)
        bite.delete()
        return JsonResponse({'success': True, 'message': 'Bite deleted successfully'}, status=200)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)