from rest_framework import serializers
from .models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ('id', 'nome', 'corpo', 'usuario')
        extra_kwargs = {'usuario': {'read_only': True}}

class signSerializer(serializers.Serializer):
    id = serializers.IntegerField()