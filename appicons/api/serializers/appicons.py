import re

import requests
from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import serializers

from appicons.models import AppIcon
from utilities.api.serializers import DataModelSummarySerializer, DataModelDetailSerializer


class AppIconSummarySerializer(DataModelSummarySerializer):
    link_logo = serializers.SerializerMethodField()
    link_archive = serializers.SerializerMethodField()

    class Meta:
        model = AppIcon
        fields = DataModelSummarySerializer.Meta.fields + [
            'link_logo',
            'link_archive',
        ]

        read_only_fields = DataModelSummarySerializer.Meta.read_only_fields + [
            'link_logo',
            'link_archive',
        ]

    def get_link_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.file.url)

    def get_link_archive(self, obj):
        if obj.archive and hasattr(obj.archive, 'url'):
            return self.context['request'].build_absolute_uri(obj.archive.url)
        return None


class AppIconDetailSerializer(AppIconSummarySerializer, DataModelDetailSerializer):
    file = serializers.FileField(required=False, write_only=True)
    file_link = serializers.URLField(required=False, write_only=True)
    _file = None

    class Meta:
        model = AppIcon
        fields = DataModelDetailSerializer.Meta.fields + AppIconSummarySerializer.Meta.fields + [
            'file',
            'file_link',
        ]

        read_only_fields = DataModelDetailSerializer.Meta.read_only_fields + AppIconSummarySerializer.Meta.read_only_fields + [
        ]

    def validate_file_link(self, value):
        if not value:
            return
        r = requests.head(value, allow_redirects=True)
        headers = r.headers
        mime_type = headers.get('content-type')
        file_size = headers.get('content-length')

        file_name = None
        if "Content-Disposition" in r.headers.keys():
            file_name_list = re.findall("filename=(.+)", r.headers["Content-Disposition"])
            if len(file_name_list) > 0:
                file_name = file_name_list[0]

        if not file_name:
            file_name = value.split("/")[-1]

        tf = TemporaryUploadedFile(
            file_name,
            mime_type,
            file_size,
            'utf-8'
        )
        r = requests.get(value, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

        tf.seek(0)
        self._file = tf

    def update(self, instance, validated_data):
        try:
            validated_data.pop('file_link')
        except:
            pass
        if self._file:
            validated_data['file'] = self._file
        return super(AppIconDetailSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        try:
            validated_data.pop('file_link')
        except:
            pass
        if self._file:
            validated_data['file'] = self._file
        return super(AppIconDetailSerializer, self).create(validated_data)
