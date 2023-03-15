from django.contrib import admin

from skatepedia.db import models

admin.site.register(models.Company)
admin.site.register(models.VideoCategory)
admin.site.register(models.Video)
admin.site.register(models.Clip)
admin.site.register(models.Skater)
admin.site.register(models.Soundtrack)
admin.site.register(models.Filmmaker)
admin.site.register(models.Track)
