from types import DynamicClassAttribute

from django.db import models
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class FileType(models.IntegerChoices):
    VOICE = 1
    IMAGE = 2
    MOVIE = 3
    PDF = 4
    PRESENTATION = 5
    SPREADSHEET = 6
    WORD = 7
    COMPRESS = 8
    TEXT = 9
    CSS = 10
    SVG = 11
    JSON = 12

    @DynamicClassAttribute
    def content_types(self) -> list:
        # TODO: complete mime type
        switcher = {
            FileType.VOICE: [],
            FileType.IMAGE: [
                'image/png',
                'image/jpeg',
                'image/jpg',
            ],
            FileType.MOVIE: [],
            FileType.PDF: [
                'application/pdf',
            ],
            FileType.PRESENTATION: [],
            FileType.SPREADSHEET: [],
            FileType.WORD: [],
            FileType.COMPRESS: [
                'application/zip',
            ],
            FileType.TEXT: [
                'text/plain',
            ],
            FileType.CSS: [
                'text/css',
            ],
            FileType.SVG: [
                'image/svg+xml',
            ],
            FileType.JSON: [
                'application/json',
            ],
        }
        return switcher.get(self, [])


class RestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: [FileType.IMAGE, FileType.COMPRESS]
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB - 104857600
            250MB - 214958080
            500MB - 429916160
    """

    def __init__(self, *args, **kwargs):
        content_types = kwargs.pop("content_types", [])
        self.content_types = []
        for ct in content_types:
            self.content_types = self.content_types + ct.content_types
        self.max_upload_size = kwargs.pop("max_upload_size", 0)

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass

        return data
