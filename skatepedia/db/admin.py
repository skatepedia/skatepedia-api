from django.contrib import admin

from skatepedia.db import models


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SkaterAdmin(admin.ModelAdmin):
    list_filter = ("stance", "gender", "country", "year_of_birth")
    search_fields = ("name",)


class VideoAdmin(admin.ModelAdmin):
    list_filter = ("year", "is_active")


class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "website")


admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.VideoCategory)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.Clip)
admin.site.register(models.Skater, SkaterAdmin)
admin.site.register(models.Soundtrack)
admin.site.register(models.Filmmaker)
admin.site.register(models.Track)
