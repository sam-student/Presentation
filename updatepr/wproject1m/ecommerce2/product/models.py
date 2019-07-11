import random
import os
import numpy as np
from django.conf import settings

from django.db import models
from django.urls import reverse

# Create your models here.
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator

from accounts.models import GuestEmail
User = settings.AUTH_USER_MODEL

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
    return "product/{new_filename}/{final_filename}".format(new_filename=filename, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter( active=True)
    def category(self):
        return self.filter(category=True)
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

class Product(models.Model):
    title = models.CharField(max_length=120)
    brand = models.CharField(max_length=120,default="None")
    model = models.CharField(max_length=120,default="None")
    slug = models.SlugField(blank=True, unique=True)
    category = models.CharField(max_length=120 , default="Phone")
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    Charging = models.TextField(default="26000mAh")
    Torch = models.TextField(default="Yes")
    Games = models.TextField(default="built-in + downloadable")
    Messaging = models.TextField(default=", SMS (threaded view), MMS, Email, Push Email")
    Browser = models.TextField(default="HTML5")
    Audio = models.TextField(default="3.5mm audio jack, MP4/WMV/H.264 player")
    Data = models.TextField(default="GPRS, Edge, 3G (HSPA 42.2/5.76 Mbps), 4G (LTE-A (2CA) Cat6 300/50 Mbps")
    NFC = models.TextField(default="Yes")
    USB = models.TextField(default="microUSB 2.0")
    GPS = models.TextField(default="Yes + A-GPS support & Glonass, BDS, GALILEO")
    Bluetooth = models.TextField(default="None")
    Wifi = models.TextField(default="Wi-Fi 802.11 a/b/g/n/ac, dual-band, hotspot")
    Front = models.TextField()
    Main = models.TextField()
    card = models.TextField(default="Yes")
    BuiltIn = models.TextField(default="16GB Built-in")
    Features = models.TextField(default="None")
    Protection = models.TextField(default="Yes")
    Resolution = models.TextField(default="720 x 1280 Pixels (~282 PPI) ")
    Size = models.TextField(default="5.5 inches")
    Technology = models.TextField(default="None")
    GPU = models.TextField(default="Mali-T830MP2 ")
    Chipset = models.TextField(default="None")
    CPU = models.TextField(default="None")
    FourGBand = models.TextField(default="LTE")
    ThreeGBand = models.TextField(default="HSDPA 850 / 900 / 1700(AWS) / 1900 / 2100 ")
    TwoGBand = models.TextField(default="SIM1: GSM 850 / 900 / 1800 / 1900 SIM2: GSM 850 / 900 / 1800 / 1900  ")
    Color = models.TextField(max_length=120)
    SIM = models.TextField(default="Single SIM (Nano-SIM)  ")
    Weight = models.TextField(default="148g")
    Dimension = models.TextField(default="146.2 x 71.3 x 8 mm")
    UIBuild = models.TextField(default="TouchWiz UI")
    OperatingSystem = models.TextField(default="Android v7.1 Nougat")
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image1 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image2 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    Review_count = models.TextField(default="90")
    Average_Rating = models.TextField(default=" 4")
    Reviews = models.TextField(default="None")
    Ram = models.TextField(null=True)
    Populrity_Score = models.FloatField(default=0.0)
    Knowledge_Score = models.FloatField(default=0.0)
    R_C = models.IntegerField(default=0)
    A_R = models.FloatField(default=0.0)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/product/{slug}".format(slug=self.slug)
        return  reverse("product:detail", kwargs={"slug": self.slug})

    def get_acc_absolute_url(self):
        #return "/product/{slug}".format(slug=self.slug)
        return  reverse("product:adetail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance , *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product )



class Comments(models.Model):
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    reviews =  models.TextField(default="None")
    rating  = models.TextField(default="None")

    # def __str__(self, ):
    #     return "%d :%s %s viewed: %s" % (self.user_id,self.product_id,self.reviews, self.rating)

    def __unicode__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    pub_date = models.DateTimeField('date published')
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.reviews.all())
        return np.mean(all_ratings)