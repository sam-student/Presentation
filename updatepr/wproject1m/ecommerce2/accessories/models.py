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
    return "accessories/{new_filename}/{final_filename}".format(new_filename=filename, final_filename=final_filename)

class AccessoriesQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter( active=True)
    def featured(self):
        return self.filter(featured=True, active=True)

class AccessoriesManager(models.Manager):
    def get_queryset(self):
        return AccessoriesQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

class Accessories(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    brand       = models.TextField()
    Reviews       = models.TextField()
    Ratings       = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)




    objects = AccessoriesManager()

    def get_absolute_url(self):
        #return "/accessories/{slug}".format(slug=self.slug)
        return  reverse("accessories:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title


def Accessories_pre_save_receiver(sender, instance , *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(Accessories_pre_save_receiver, sender=Accessories )