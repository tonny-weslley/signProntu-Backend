from .models import Documento
from rest_framework import viewsets
from .serializers import DocumentoSerializer, signSerializer
from .scripts import signDocument


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class documentSignViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = signSerializer

    def perform_create(self, serializer):
        serializer.save()
        signDocument(serializer.data['documento'], serializer.data['id'])