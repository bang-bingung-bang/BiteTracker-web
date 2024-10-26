from venv import logger
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from TrackerBites.models import BiteTrackerModel
from TrackerBites.forms import BiteTrackerForm
from django.db.models import Sum

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

def delete_bite_entry_ajax(request, id):
    bite = BiteTrackerModel.objects.filter(pk=id)
    if not bite.exists():
        return HttpResponse({'success': False, 'error': 'Bite not found'}, status=404)
    bite.delete()

    return HttpResponse({'success': True, 'message': 'Bite deleted successfully'}, status=200)

def edit_bite_entry_ajax(request, id):
    bite = BiteTrackerModel.objects.filter(pk=id)
    if not bite.exists():
        return HttpResponse({'success': False, 'error': 'Bite not found'}, status=404)
    bite = bite.first()

    name = strip_tags(request.POST.get("name"))
    calories = strip_tags(request.POST.get("calories"))
    date = strip_tags(request.POST.get("date"))
    time = strip_tags(request.POST.get("time"))

    # Validasi input
    if not name or not calories or not date or not time:
        return HttpResponse({'success': False, 'error': 'All fields are required'}, status=400)

    # Simpan entri produk baru
    bite.bite_name = name
    bite.bite_calories = calories
    bite.bite_date = date
    bite.bite_time = time
    bite.save()

    return HttpResponse({'success': True, 'message': 'Product updated successfully'}, status=200)

def get_bite_tracker_json(request):
    data = BiteTrackerModel.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_bite_tracker_json_by_date(request):
    temp_data = BiteTrackerModel.objects.filter(user=request.user)
    data = temp_data.filter(bite_date=request.GET.get("date"))
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def calculate_total_calories(request):
    total_calories = BiteTrackerModel.objects.filter(user=request.user).filter(bite_date=request.GET.get("date")).aggregate(Sum('bite_calories'))
    total_calories_percentage = (total_calories['bite_calories__sum'] / 2500) * 100
    return HttpResponse(total_calories, total_calories_percentage, content_type="application/json")