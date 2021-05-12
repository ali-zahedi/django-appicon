from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from utilities import convert_pk
from utilities.contenttypes import get_content_type_from_model

"""
DataModel
"""


class DataModelQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super(DataModelQuerySet, self).__init__(*args, **kwargs)

    def active(self):
        return self.filter(
            is_active=True
        )

    def pk(self, pk):
        return self.filter(pk=convert_pk(self.model, pk))

    def pk_in(self, pk_list, pk_field=None):
        pk = 'pk'
        pk_list = map(lambda x: convert_pk(self.model, x), pk_list)
        if pk_field is not None:
            pk = pk_field
        query = Q(**{f'{pk}__in': pk_list})
        return self.filter(query)


class DataModelManager(models.Manager):
    def get_queryset(self):
        return DataModelQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class DataModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    _content_type = None

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    update_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.pk)

    @property
    def resourcetype(self):
        return self._meta.object_name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(DataModel, self).save(*args, **kwargs)

    @classmethod
    def get_content_type(cls):
        if not cls._content_type:
            cls._content_type = get_content_type_from_model(cls)
        return cls._content_type
