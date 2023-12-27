import os
from pyhanko.sign import sign_pdf
from ..models import Documento

from core.settings import BASE_DIR

cert_path = os.path.join(BASE_DIR, 'assets', 'secrets','certificate.pem')
key_path = os.path.join(BASE_DIR, 'assets', 'secrets','private_key.pem')
certificates = os.path.join(BASE_DIR, 'assets', 'certificates')

def sign_document(document_id):
    document = Documento.objects.get(id=document_id)
    sign_pdf(
        document, cert_path, key_path,
        output_path='signed.pdf',
        appearance_text='Signed by PyHanko!'
    )