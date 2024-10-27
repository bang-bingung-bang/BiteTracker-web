from django.urls import path
from TrackerBites.views import show_tracker_bites, add_bite_calorie_entry, add_bite_calorie_entry_ajax, delete_bite_entry_ajax, get_bite_tracker_json, get_bite_tracker_json_by_date, calculate_total_calories_by_date
from TrackerBites.views import get_bite_tracker_json_by_date_and_time, edit_bite_entry_ajax

app_name = 'TrackerBites'

urlpatterns = [
    path('bite_tracker/', show_tracker_bites, name='show_tracker_bites'),
    path('add_bite_calorie_entry/', add_bite_calorie_entry, name='add_bite_calorie_entry'),
    path('add_bite_calorie_entry_ajax/', add_bite_calorie_entry_ajax, name='add_bite_calorie_entry_ajax'),
    path('delete_bite_entry_ajax/<uuid:id>/', delete_bite_entry_ajax, name='delete_bite_entry_ajax'),
    path('edit_bite_entry_ajax/<uuid:id>/', edit_bite_entry_ajax, name='edit_bite_entry_ajax'),
    path('get_bite_tracker_json/', get_bite_tracker_json, name='get_bite_tracker_json'),
    path('get_bite_tracker_json_by_date/<str:date>/', get_bite_tracker_json_by_date, name='get_bite_tracker_json_by_date'),
    path('get_bite_tracker_json_by_date_and_time/<str:date>/<str:time>/', get_bite_tracker_json_by_date_and_time, name='get_bite_tracker_json_by_date_and_time'),
    path('calculate_total_calories_by_date/<str:date>/', calculate_total_calories_by_date, name='calculate_total_calories_by_date'),
]