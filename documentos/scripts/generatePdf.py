import os
import pdfkit
from documentos.models import Documento
from django.template.response import get_template
from core.settings import BASE_DIR

def generate_pdf(document_id):
    

    
    document = Documento.objects.get(id=document_id)
    template = get_template('template.html')
    html = template.render({'nome' : document.nome, 'corpo' : document.corpo})
    pdf = pdfkit.from_string(html, False, options={"enable-local-file-access": ""})
    print(pdf)
    return pdf