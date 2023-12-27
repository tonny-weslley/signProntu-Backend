from .models import Documento
from rest_framework import viewsets
from .serializers import DocumentoSerializer, signSerializer
from .scripts import signDocument, generatePdf
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


def get_user_from_token(request):
    try:
        auth = TokenAuthentication()
        user = auth.authenticate(request)
        return user
    except AuthenticationFailed:
        return None



class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    
    # adiciona o usuario logado ao documento
    def perform_create(self, serializer):
        serializer.save(usuario=get_user_from_token(self.request))
    

class documentSignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = signSerializer

    def perform_create(self, serializer):
        serializer.save()
        signDocument(serializer.data['id'])
        
class generatePdfViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = signSerializer

    def perform_create(self, serializer):
        serializer.save()
        pdf = generatePdf(serializer.data['id'])
        # return pdf
        return HttpResponse(pdf, content_type='application/pdf')