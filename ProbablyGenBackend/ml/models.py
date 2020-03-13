from django.db import models

# Create your models here.


class Disorder(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class HPOToDisorder(models.Model):
    id_hp = models.CharField(max_length=32)
    term = models.CharField(max_length=256)
    freq = models.IntegerField()
    disorder = models.ForeignKey(Disorder,on_delete=models.CASCADE)