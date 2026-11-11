from django.db import models

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'communities'

    def __str__(self):
        return self.name