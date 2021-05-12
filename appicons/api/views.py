import os
import tempfile

from appicon import icon_generate
from django.core.files import File
from rest_framework.permissions import AllowAny, IsAdminUser

from utilities.api.views import DataModelViewSet
from .serializers import AppIconSummarySerializer, AppIconDetailSerializer
# ViewSets define the view behavior.
from ..models import AppIcon

"""
AppIcon
"""


class AppIconViewSet(DataModelViewSet):
    queryset = AppIcon.objects.none()
    model = AppIcon

    serializers = {
        'default': AppIconSummarySerializer,
        'create': AppIconDetailSerializer,
        'update': AppIconDetailSerializer,
    }
    permission_classes_by_action = {
        'default': [IsAdminUser, ],
        'retrieve': [AllowAny, ],
        'list': [IsAdminUser, ],
        'create': [AllowAny, ],
        'update': [IsAdminUser, ],
    }

    def create(self, request, *args, **kwargs):
        response = super(AppIconViewSet, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            instance = response.data.serializer.instance
            with tempfile.TemporaryDirectory() as tmpdirname:
                dir_des = os.path.join(tmpdirname, 'icons')
                os.makedirs(dir_des)
                dd = icon_generate(logo_path=instance.file.path, destination_directory=dir_des, is_zip=True)
                local_file = open(dd, "rb")
                f = File(local_file)
                instance.archive.save('new', f)
                local_file.close()
                response.data = AppIconDetailSerializer(instance, many=False, read_only=True, context={'request': request}).data
        return response
