from rest_framework import serializers

from utilities.db.models import DataModel

# DataModel
class DataModelSummarySerializer(serializers.ModelSerializer):
    i_content_type_id = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        model = DataModel
        fields = [
            'pk',
            'resourcetype',
            'i_content_type_id',
            'created_at',
            'is_active',
        ]

        read_only_fields = [
            'pk',
            'resourcetype',
            'created_at',
            'is_active',
            'i_content_type_id',
        ]

    def get_i_content_type_id(self, obj):
        return obj.get_content_type().pk


class DataModelDetailSerializer(DataModelSummarySerializer):

    class Meta:
        abstract = True
        model = DataModel
        fields = DataModelSummarySerializer.Meta.fields + [
        ]

        read_only_fields = DataModelSummarySerializer.Meta.fields + [
        ]
