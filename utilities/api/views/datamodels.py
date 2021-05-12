from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..serializers import DataModelDetailSerializer
from ... import convert_pk

"""
Data Model
"""


class DataModelViewSet(ModelViewSet):
    serializers = {
        'default': DataModelDetailSerializer,
    }
    permission_classes_by_action = {
    }

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset_ids lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: convert_pk(self.model, self.kwargs[lookup_url_kwarg])}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        permissions = self.get_permission_classes_by_action()
        act = self.action
        result = [
            permission() for permission in permissions.get(
                act, permissions['default']
            )
        ]
        return result

    @classmethod
    def get_permission_classes_by_action(cls):
        permissions = {
            'default': [IsAuthenticated, ],
            'list': [AllowAny, ],
            'retrieve': [AllowAny, ],
            'create': [IsAdminUser, ],
            'update': [IsAdminUser, ],
            'partial_update': [IsAdminUser, ],
            'filter': [AllowAny, ],
            'destroy': [IsAdminUser, ],
        }

        permissions.update(cls.permission_classes_by_action)
        return permissions

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)

    def get_queryset(self):
        return self.model.objects.active()

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            error = []
            for item in e.protected_objects.all():
                error.append(
                    _('Deleting this item depends on the %(verbose_name)s with ID %(id)s. (%(title)s)') % {
                        'verbose_name': item._meta.verbose_name,
                        'id': str(item.pk),
                        'title': str(item),
                    }
                )
            return Response({'non_field_errors': error}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset_filter(self, request):
        queryset = self.get_queryset()
        pk_list = request.data.get('pk_list', [])
        if len(pk_list) > 0:
            queryset = queryset.pk_in(pk_list)
        return queryset.distinct()

    @action(methods=['post'], detail=False)
    def filter(self, request):
        queryset = self.get_queryset_filter(request)
        serializer = self.get_serializer(
            queryset,
            many=True,
            read_only=True,
            context={'request': request}
        ).data
        return Response(serializer, status=status.HTTP_200_OK)
