from django.contrib import admin

from .models import Status
from .forms import StatusForm

class StatusAdmin(admin.ModelAdmin):
    # it specify fields to show on admin site
    list_display = ['user', '__str__', 'image']
    form = StatusForm
    # class Meta:
    #     model: StatusForm

# Register your models here.
admin.site.register(Status, StatusAdmin )
 