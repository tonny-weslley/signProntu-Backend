import base64
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
from django.http import FileResponse, HttpResponse
from base.models import CustomUser as User


def get_user_from_token(request):
    try:
        auth = JWTAuthentication()
        user, _ = auth.authenticate(request)
        if user and user.is_authenticated:
            # pega o usuario do banco de dados
            db_user = User.objects.get(id=user.id)
            return db_user
    except AuthenticationFailed:
        pass
    return None


class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    
    def createAndSign(self, request, *args, **kwargs):
        data = request.data
        user = get_user_from_token(self.request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=get_user_from_token(self.request))
        pdf = generate_pdf(serializer.data['id'])
        signed_pdf = sign_document(pdf)
        print(signed_pdf)
        
    

class documentSignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = signSerializer
    

class GeneratePdfViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = signSerializer

    @action(detail=True, methods=['get'], url_path='generatePdf')
    def generatePdf(self, request, pk=None):
        try:
            document = get_object_or_404(Documento, id=pk)
          
            pdf = generate_pdf(document.id)

            output_pdf_file = "output.pdf"

           
                
            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=output.pdf"
            return response
        except Documento.DoesNotExist:
            return Response({'detail': 'Documento não encontrado'}, status=404)