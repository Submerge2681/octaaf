from django.db import models

# Create your models here.

class Articles(models.Model):
    Title = models.CharField(max_length=200)
    Discription = models.CharField(max_length=1000)
    Link = models.URLField(max_length=1000)
    Thumbnail = models.URLField(max_length=1000)
    Tim = models.TimeField(auto_now=True)
    Sauce = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.Title   