from OpenSSL import crypto
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates a certificate for the user'

    def handle(self, *args, **options):
        try:
            # Cria uma chave privada
            key = crypto.PKey()
            key.generate_key(crypto.TYPE_RSA, 2048)

            # Cria um certificado
            cert = crypto.X509()
            cert.get_subject().C = "BR"
            cert.get_subject().ST = "Estado"
            cert.get_subject().L = "Cidade"
            cert.get_subject().O = "Organizacao"
            cert.get_subject().OU = "Unidade Organizacional"
            cert.get_subject().CN = "Nome Comum"
            cert.set_serial_number(1000)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(365*24*60*60)  # Certificado válido por 1 ano
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(key)
            cert.sign(key, 'sha256')

            # Salva a chave privada e o certificado em arquivos
            with open("core/assets/secrets/private_key.pem", "wb") as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

            with open("core/assets/secrets/certificate.pem", "wb") as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                
            self.stdout.write(self.style.SUCCESS('Certificado gerado com sucesso'))
        
        except Exception as e:
            print(e)
            self.stdout.write(self.style.ERROR('Erro ao gerar certificado'))
            return
