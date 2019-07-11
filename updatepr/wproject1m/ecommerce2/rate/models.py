from django.db import models
import numpy as np
from product.models import Product

class Review(models.Model):
    wine = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             )
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
