from django.db import models
from django.utils.translation import gettext_lazy as _

from appicons.utils import get_document_path
from utilities.db import DataModel, DataModelManager, DataModelQuerySet, FileType, RestrictedFileField


class AppIconQuerySet(DataModelQuerySet):
    def __init__(self, *args, **kwargs):
        super(AppIconQuerySet, self).__init__(*args, **kwargs)


class AppIconManager(DataModelManager):
    def get_queryset(self):
        return AppIconQuerySet(self.model, using=self._db)


class AppIcon(DataModel):
    file = RestrictedFileField(
        content_types=[FileType.IMAGE, ],
        upload_to=get_document_path,
        max_upload_size=5242880,
        blank=False,
        null=False,
        verbose_name=_('File'),
    )

    objects = AppIconManager()

    class Meta:
        verbose_name = _('App icon')
        verbose_name_plural = _('App icons')

