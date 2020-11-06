from django.db import models

# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "options"

    def __str__(self):
        return self.name