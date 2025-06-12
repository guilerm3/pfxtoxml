from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
import xmlsec
from lxml import etree

# === CONFIGURAÇÃO ===
# Expecificar o caminho do arquivo .pfx e a senha
caminho_pfx = r"C:\Users\Fulano\Arquivo.pfx"
senha_pfx = b"Sua senha"

# === 1. Carregar chave e certificado do .pfx ===
try:
    with open(caminho_pfx, "rb") as f:
        pfx_data = f.read()

    private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
        pfx_data, senha_pfx, backend=default_backend()
    )
except Exception as e:
    print(f"Erro ao carregar o arquivo PFX: {e}")
    exit()

# === 2. Serializar para PEM (requerido por xmlsec) ===
private_key_pem = private_key.private_bytes(
    Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
)

certificate_pem = certificate.public_bytes(Encoding.PEM)

# === 3. XML COMPLETO da nota fiscal para assinar ===
xml_para_assinar = """
<GerarNfseEnvio xmlns="http://www.abrasf.org.br/nfse.xsd">
...
</GerarNfseEnvio>
"""
# Lê o XML normalmente
xml_doc = etree.fromstring(xml_para_assinar.encode("utf-8"))

# === 4. Preparar o XML para a assinatura ===
ns = {
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
}
signature_node = xml_doc.find('.//ds:Signature', namespaces=ns)

# Cria o template da assinatura
template = xmlsec.template.create(
    xml_doc,  # raiz do documento XML onde o nó será inserido
    xmlsec.Transform.EXCL_C14N,
    xmlsec.Transform.RSA_SHA256
)

# Substitui o nó Signature vazio pelo template
parent = signature_node.getparent()
parent.replace(signature_node, template)

#Adiciona a referência e transformações no template
ref = xmlsec.template.add_reference(template, xmlsec.Transform.SHA256, uri="")
xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)
xmlsec.template.add_transform(ref, xmlsec.Transform.EXCL_C14N)

# Adiciona KeyInfo e X509Data
key_info = xmlsec.template.ensure_key_info(template)
x509_data = xmlsec.template.add_x509_data(key_info)


# === 5. Assinar o documento ===
ctx = xmlsec.SignatureContext()

# Carrega a chave privada
ctx.key = xmlsec.Key.from_memory(private_key_pem, xmlsec.KeyFormat.PEM, None)

# Assina o nó da assinatura
ctx.sign(template)

# === 6. Inserir o certificado público no XML ===
cert_text = certificate_pem.decode('utf-8').replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
x509_certificate_node = x509_data.find('.//ds:X509Certificate', namespaces=ns)
if x509_certificate_node is None:
    x509_certificate_node = etree.SubElement(x509_data, etree.QName(ns['ds'], 'X509Certificate'))
x509_certificate_node.text = cert_text

# === 7. Resultado Final ===
# Imprime o XML final, assinado e pronto para ser enviado.
xml_assinado_final = etree.tostring(xml_doc, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
print(xml_assinado_final)
