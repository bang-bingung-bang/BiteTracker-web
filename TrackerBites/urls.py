from django.urls import path
from TrackerBites.views import show_tracker_bites, add_bite_calorie_entry, add_bite_calorie_entry_ajax, delete_bite_entry_ajax, get_bite_tracker_json, get_bite_tracker_json_by_date, calculate_total_calories_by_date
from TrackerBites.views import get_bite_tracker_json_by_date_and_time, edit_bite_entry_ajax, add_bite_calorie_entry_flutter, show_json_by_date, data_info_by_date
from TrackerBites.views import *

app_name = 'TrackerBites'

urlpatterns = [
    path('bite_tracker/', show_tracker_bites, name='show_tracker_bites'),
    path('add_bite_calorie_entry/', add_bite_calorie_entry, name='add_bite_calorie_entry'),
    path('add_bite_calorie_entry_ajax/', add_bite_calorie_entry_ajax, name='add_bite_calorie_entry_ajax'),
    path('delete_bite_entry_ajax/<uuid:id>/', delete_bite_entry_ajax, name='delete_bite_entry_ajax'),
    path('bite_tracker/edit_bite_entry_ajax/<uuid:id>/', edit_bite_entry_ajax, name='edit_bite_entry_ajax'),
    path('get_bite_tracker_json/', get_bite_tracker_json, name='get_bite_tracker_json'),
    path('get_bite_tracker_json_by_date/<str:date>/', get_bite_tracker_json_by_date, name='get_bite_tracker_json_by_date'),
    path('get_bite_tracker_json_by_date_and_time/<str:date>/<str:time>/', get_bite_tracker_json_by_date_and_time, name='get_bite_tracker_json_by_date_and_time'),
    path('calculate_total_calories_by_date/<str:date>/', calculate_total_calories_by_date, name='calculate_total_calories_by_date'),
    path('add_bites_flutter/', add_bite_calorie_entry_flutter, name='add_bites_flutter'),
    path('show-json-by-date/<str:date>/', show_json_by_date, name='show_json_by_date'),
    path('data-info-by-date/<str:date>/', data_info_by_date, name='data_info_by_date'),
    path('edit-bite-tracker/<uuid:id>/', edit_bite_tracker_entry, name='edit_bite_tracker_entry'),
    path('delete-bite-flutter/<uuid:id>/', delete_bite_flutter, name='delete_bite_flutter')
]