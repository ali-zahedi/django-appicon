from django.utils.translation import gettext_lazy as _

from appicons.utils import get_archive_path, get_file_path
from utilities.db import DataModel, DataModelManager, DataModelQuerySet, FileType, RestrictedFileField


class AppIconQuerySet(DataModelQuerySet):
    def __init__(self, *args, **kwargs):
        super(AppIconQuerySet, self).__init__(*args, **kwargs)


class AppIconManager(DataModelManager):
    def get_queryset(self):
        return AppIconQuerySet(self.model, using=self._db)

# TODO: remove archive file after one day
class AppIcon(DataModel):
    file = RestrictedFileField(
        content_types=[FileType.IMAGE, ],
        upload_to=get_file_path,
        max_upload_size=5242880,
        blank=False,
        null=False,
        verbose_name=_('File'),
    )
    archive = RestrictedFileField(
        content_types=[FileType.COMPRESS, ],
        upload_to=get_archive_path,
        max_upload_size=10485760,
        blank=True,
        null=True,
        verbose_name=_('Archive'),
    )

    objects = AppIconManager()

    class Meta:
        verbose_name = _('App icon')
        verbose_name_plural = _('App icons')

