import pdfkit
from documentos.models import Documento

def main(document_id):
    document = Documento.objects.get(id=document_id)
    pdf = pdfkit.from_string(document.corpo)
    return pdf
