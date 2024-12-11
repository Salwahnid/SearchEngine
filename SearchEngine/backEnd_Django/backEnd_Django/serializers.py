# backEnd_Django/serializers.py
from rest_framework import serializers

class SearchResultSerializer(serializers.Serializer):
    doc_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
