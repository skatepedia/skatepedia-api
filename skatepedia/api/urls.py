from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested.routers import NestedSimpleRouter

from django.urls import path, include

from skatepedia.api.views import (
    ClipViewSet,
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
router.register(r"clips", ClipViewSet)
router.register(r"videocategories", VideoCategoryViewSet)
router.register(r"soundtracks", SoundtrackViewSet)

# /skaters
skaters_router = NestedSimpleRouter(router, r"skaters", lookup="skater")
skaters_router.register("videos", VideoViewSet, basename="videos")
# /videos
videos_router = NestedSimpleRouter(router, r"videos", lookup="video")
videos_router.register("skaters", SkaterViewSet, basename="skaters")
videos_router.register("filmmakers", SkaterViewSet, basename="skaters")
videos_router.register("clips", ClipViewSet, basename="clips")
# /companies
companies_router = NestedSimpleRouter(router, r"companies", lookup="company")
companies_router.register(r"videos", VideoViewSet, basename="videos")
companies_router.register(r"skaters", SkaterViewSet, basename="skaters")


app_name = "api"

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(videos_router.urls)),
    path(r"", include(companies_router.urls)),
    path(r"", include(skaters_router.urls)),
    # OpenAPI schema serving and Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
]
