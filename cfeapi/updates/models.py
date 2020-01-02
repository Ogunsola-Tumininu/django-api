from django.db import models
from django.conf import settings
from django.core.serializers import serialize

import json

def upload_update_image(instance, filename):
    return "updates/{user}/{filename}"

# Create your models here.
class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     return serialize('json', qs, fields=('user', 'content', 'image'))

    # def serialize(self):
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         struct = json.loads(obj.serialize()) # convert to dictionary
    #         final_array.append(struct)
    #     return json.dumps(final_array)

    def serialize(self):
        list_values = list(self.values("id", "user", "content", "image"))
        return json.dumps(list_values)



class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, using=self._db)


class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UpdateManager()

    def __str__(self):
        return self.content or "" 

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""
        
        data = {
            "id": self.pk,
            "content": self.content,
            "user" : self.user.id,
            "image": image
        }
        data = json.dumps(data) # convert to json
        return data