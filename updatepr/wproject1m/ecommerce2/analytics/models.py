from django.conf import settings
from product.models import Product
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from accounts.signals import user_logged_in

from django.db.models.signals import post_save,pre_save
from .signals import object_viewed_signal

from .utils import get_client_ip
# Create your models here.


User = settings.AUTH_USER_MODEL


FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class):
        c_type = ContentType.objects.get_for_model(model_class)
        return self.filter(content_type=c_type)

class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self.db)

    def by_model(self, model_class):
        return self.get_queryset().by_model(model_class)

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)
    # product         = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)

    objects = ObjectViewedManager()

    def __str__(self, ):
        return "%d :%s viewed: %s" % (self.object_id,self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)

    new_view_obj = ObjectViewed.objects.create(
                user = request.user,
                content_type=c_type,
                object_id = instance.id,
                ip_address = get_client_ip(request)


    )

object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    session_key     = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended           = models.BooleanField(default=False)


    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession )


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_session_receiver, sender=UserSession )


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    # print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key=request.session.session_key
    UserSession.objects.create(
            user=user,
            ip_address=ip_address,
            session_key=session_key
    )

user_logged_in.connect(user_logged_in_receiver)