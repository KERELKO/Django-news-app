from rest_framework import serializers

from backend.apps.content.models import Content


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    content = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['content', 'object_id']
