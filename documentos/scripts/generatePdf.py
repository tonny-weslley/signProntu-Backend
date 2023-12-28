import os
import pdfkit
from documentos.models import Documento
from django.template.response import get_template
from core.settings import BASE_DIR

pdf_path = os.path.join(BASE_DIR, 'documentos', 'tmp')

def generate_pdf(document_id):
    document = Documento.objects.get(id=document_id)
    template = get_template('template.html')
    html = template.render({'nome' : document.nome, 'corpo' : document.corpo})
    pdf = pdfkit.from_string(html, False, options={"enable-local-file-access": ""})
    pdf_name = document.nome.strip().replace(' ', '_') + '.pdf'
    pdf_file = os.path.join(pdf_path, pdf_name)

    with open(pdf_file, 'wb') as f:
        f.write(pdf)  
    
    return pdf_file
    