import uuid
from django.db import models
from django.contrib.auth.models import User

class ShareBites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Nutritional tags
    CALORIE_CHOICES = [
        ('low', 'Low Calorie'),
        ('high', 'High Calorie'),
    ]
    SUGAR_CHOICES = [
        ('low', 'Low Sugar'),
        ('high', 'High Sugar'),
    ]
    DIET_CHOICES = [
        ('vegan', 'Vegan'),
        ('non_vegan', 'Non-Vegan'),
    ]

    calorie_content = models.CharField(max_length=4, choices=CALORIE_CHOICES, default='low')
    sugar_content = models.CharField(max_length=4, choices=SUGAR_CHOICES, default='low')
    diet_type = models.CharField(max_length=10, choices=DIET_CHOICES, default='non_vegan')
    
    def __str__(self) :
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(ShareBites, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username}'

class Like(models.Model):
    post = models.ForeignKey(ShareBites, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like by {self.user.username}'

    
