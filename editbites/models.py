from django.db import models

# Create your models here.

class Snack(models.Model):

    id = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=13)
    BookTitle = models.CharField(max_length=255)
    BookAuthor = models.CharField(max_length=255)
    Year_Of_Publication = models.PositiveIntegerField()
    Publisher = models.CharField(max_length=255)
    Image = models.URLField()