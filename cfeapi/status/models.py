from django.db import models
from django.conf import settings

'''
JSON -- Javascript Object Notation
'''
def upload_status_image(instance, filename):
    return "status/{user}/{filename}".format(user=instance.user, filename=filename)

# Create your models here.
class StatusQuerySet(models.QuerySet):
    pass

class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)


class Status(models.Model): 
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content     = models.TextField(null=True, blank=True)
    image       = models.ImageField(upload_to=upload_status_image, null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = StatusManager()

    def __str__(self):
        if len(self.content) > 50: 
            return str(self.content)[:50] + "..."
        else:
            return str(self.content)

    class Meta: 
        # it changes the model name inside admin 
        verbose_name = "Status post"
        verbose_name_plural = "Status posts"