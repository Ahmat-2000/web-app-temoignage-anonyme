from django.db import models
from custom_user.models import User

# Create your models here.
class TemoignesModel(models.Model):
    agresseur = models.CharField(verbose_name="Agresseur",max_length=250)
    message = models.CharField(verbose_name="Message", max_length=600)
    victime = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Témoignage")
        verbose_name_plural = ("Témoignages")
        db_table = 'temoignages'
    def __str__(self):
        return self.victime.get_username()
