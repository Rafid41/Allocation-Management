from django.db import models

# Create your models here.
class PBS(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name