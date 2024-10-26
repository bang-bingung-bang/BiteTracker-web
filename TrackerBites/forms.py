from django.forms import ModelForm
from TrackerBites.models import BiteTrackerModel
from django.utils.html import strip_tags

class BiteTrackerForm(ModelForm):
    class Meta:
        model = BiteTrackerModel
        fields = ["bite_name", "bite_date", "bite_calories", "bite_time"]

