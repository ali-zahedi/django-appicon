from rest_framework import routers
from appicons.api.views import AppIconViewSet


router = routers.DefaultRouter()
router.register(r'icons', AppIconViewSet)


api_url = router.urls
