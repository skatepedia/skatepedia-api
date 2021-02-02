from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

from skatepedia.api.views import (
    SkaterViewSet,
    BrandViewSet,
    VideoViewSet,
    SoundtrackViewSet,
)

router = routers.DefaultRouter()
router.register(r'skaters', SkaterViewSet)
router.register(r'companies', BrandViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'soundtracks', SoundtrackViewSet)

app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
