from rest_framework import serializers
from .models import ErrorReport

# Serializer para el estado del servidor
class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()

# Serializer para el modelo ErrorReport
class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ['code', 'description', 'date']
