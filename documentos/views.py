from requests import Response
from .models import Documento
from rest_framework import viewsets
from .serializers import DocumentoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
from base.models import CustomUser as User
from .models import Documento
from io import BytesIO


from .manager.documentManager import PDFSigner


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


class DocumentoViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    
    @action(detail=False, methods=['post'])
    def createAndSign(self, request):
        user = get_user_from_token(request)
        if not user:
            return Response(status=401)
        signed_pdf = PDFSigner(request.data, user).createAndSign()

        return HttpResponse(signed_pdf, content_type='application/pdf')
    
    @action(detail=False, methods=['get'])
    def list(self, request):
        user = get_user_from_token(request)
        if not user:
            return Response(status=401)
        documents = Documento.objects.filter(usuario=user)
        serializer = DocumentoSerializer(documents, many=True)
        response = JsonResponse(serializer.data, safe=False)
        return response


class DocumentVerifyViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    
    @action(detail=False, methods=['get'])
    def verify(self, request, hash):
        user = get_user_from_token(request)
        if not user:
            return HttpResponse(status=401)
        document = Documento.objects.filter(hash=hash)
        print(f'documento encontrado: {document}')
        if not document:
            return HttpResponse(status=404)
        document = document[0]
        if document.usuario != user:
            return Response(status=403)
        pdf = PDFSigner({
            "nome": document.nome,
            "corpo" : document.corpo}, user).generate_pdf()
        return HttpResponse(pdf, content_type='application/pdf')