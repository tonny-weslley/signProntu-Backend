import pdfkit
from documentos.models import Documento

def generate_pdf(document_id):
    document = Documento.objects.get(id=document_id)
    print(f'Dentro do bgl document : {document} documento id: {document.id}, corpo: {document.corpo}')
    pdf = pdfkit.from_string(document.corpo, False)
    return pdf