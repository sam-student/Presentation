from django.db import models


# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return ("%s , %s" % (self.item.name,  self.time))
