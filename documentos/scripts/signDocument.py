import os
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers

from core.settings import BASE_DIR

cert_path = os.path.join(BASE_DIR, 'core', 'assets', 'secrets','certificate.pem')
key_path = os.path.join(BASE_DIR, 'core', 'assets', 'secrets','private_key.pem')
certificates = os.path.join(BASE_DIR, 'core',  'assets', 'certificates')


cms_signer = signers.SimpleSigner.load(
    key_path, cert_path)

def sign_document(document):
    with open(document, 'rb') as doc:
        w = IncrementalPdfFileWriter(doc)
        out = signers.sign_pdf(
            w, signers.PdfSignatureMetadata(field_name='Signature1'),
            signer=cms_signer,
        )
        
        print(f'Assinatura realizada com sucesso: {out}')

    

