from typing import Any
from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    price = models.IntegerField()
    description = models.TextField()
    image_url = models.TextField()
    discount = models.TextField(null=True)
    timeid =  models.BigIntegerField()
    url = models.TextField()
    def __str__(self):
        return self.name
    
    def __int__(self):
        return self.timeid 
    
