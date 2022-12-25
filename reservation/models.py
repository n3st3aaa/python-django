from django.db import models


class Tables(models.Model):
    table_number = models.IntegerField()
    places = models.IntegerField()
    form = models.BooleanField()
    coordinates = models.CharField(max_length=7)
    size = models.CharField(max_length=7)


class Order(models.Model):
    table_number = models.ManyToManyField(Tables)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    data = models.DateField()

