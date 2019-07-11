import random
import os
from django.db import models
from django.urls import reverse

# Create your models here.
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator

def get_filename_ext(filename):
    base_name=os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    return name,ext

def upload_image_path(instance,filename):
    print(instance)
    print(filename)
    new_filename=random.randint(1,39321457854)
    name,ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=filename, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter( active=True)
    def featured(self):
        return self.filter(featured=True, active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

class Products(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    description = models.TextField()
    sound       = models.TextField(default="good speakers")
    memory      = models.TextField(default="2GB")
    camera      = models.TextField(default="8MP")
    connectivity= models.TextField(default="None")
    other_features= models.TextField(default="None")
    diplay      = models.TextField(default=5.6)
    processor   = models.TextField(default=2.0)
    image       = models.ImageField(upload_to=upload_image_path, null=True , blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}".format(slug=self.slug)
        return  reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance , *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Products )