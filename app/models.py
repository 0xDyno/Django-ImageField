from django.db import models

# Create your models here.
folder = "images/"


class SaveModel(models.Model):
    img = models.ImageField(upload_to="app/static/" + folder)