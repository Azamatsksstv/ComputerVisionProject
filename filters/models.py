from django.db import models


class EnteredImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(upload_to='enteredImages/', null=True, blank=True)


class FilteredImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(upload_to='filteredImages/')
