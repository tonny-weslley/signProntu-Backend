from requests import Response
from .models import Documento
from rest_framework import viewsets
from .serializers import DocumentoSerializer, signSerializer
from .scripts import generate_pdf, sign_document
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import FileResponse


def get_user_from_token(request):
    try:
        auth = JWTAuthentication()
        user, _ = auth.authenticate(request)
        if user and user.is_authenticated:
            return user
    except AuthenticationFailed:
        pass
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
        sign_document(serializer.data['id'])
        
class GeneratePdfViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = signSerializer

    @action(detail=True, methods=['get'], url_path='generatePdf')
    def generatePdf(self, request, pk=None):
        try:
            document = get_object_or_404(Documento, id=pk)
            print(f'document : {document} documento id: {document.id}')
            pdf = generate_pdf(document.id)
            print(f'olha o pdf: {pdf}')
            # Retorne o PDF como uma resposta HTTP
            response = FileResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{document.nome}.pdf"'
            return response
        except Documento.DoesNotExist:
            # Se o documento não for encontrado, retorne uma resposta adequada (por exemplo, 404 Not Found)
            return Response({'detail': 'Documento não encontrado'}, status=404)