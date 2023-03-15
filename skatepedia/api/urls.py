from rest_framework import routers

from django.urls import path, include

from skatepedia.api.views import (
    VideoViewSet,
    SkaterViewSet,
    CompanyViewSet,
    FilmmakerViewSet,
    SoundtrackViewSet,
    VideoCategoryViewSet
)

router = routers.DefaultRouter()
router.register(r"skaters", SkaterViewSet)
router.register(r"filmmakers", FilmmakerViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"videocategories", VideoCategoryViewSet)
router.register(r"soundtracks", SoundtrackViewSet)

app_name = "api"

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"auth/", include("rest_framework.urls", namespace="rest_framework")),
]
