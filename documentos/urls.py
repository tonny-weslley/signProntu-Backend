from django.urls import path, include
from .views import DocumentoViewSet
from rest_framework import routers



urlpatterns = [
    path('/', DocumentoViewSet.as_view({ 'post': 'createAndSign', 'get': 'list'})),
]