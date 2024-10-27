import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BiteTrackerModel(models.Model):
    time_choices = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bite_date = models.DateField(null=True)
    bite_time = models.CharField(max_length=10, choices=time_choices)
    bite_name = models.CharField(max_length=100)
    bite_calories = models.IntegerField()