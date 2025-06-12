# 📄 NFSeSigner

NFSeSigner é uma aplicação em Python para assinatura digital de arquivos XML de **Nota Fiscal de Serviço Eletrônica (NFS-e)**, compatível com o padrão **ABRASF**, utilizando certificados digitais no formato **.pfx (PKCS#12)**.

## 🔐 Funcionalidades

- Leitura de certificados digitais `.pfx` com senha  
- Extração de chave privada e certificado público  
- Conversão para formato PEM compatível com xmlsec  
- Criação de assinatura digital `XML Digital Signature` (`ds:Signature`)  
- Inclusão do certificado X.509 no XML  
- Geração do XML assinado, pronto para envio à prefeitura  

## 🧰 Tecnologias e Bibliotecas

- [Python 3.8+](https://www.python.org)
- [xmlsec](https://github.com/mehcode/python-xmlsec)
- [cryptography](https://cryptography.io)
- [lxml](https://lxml.de)

## 🛠️ Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/guilerm3/pfxtoxml.git
   cd pfxtoxml
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/macOS
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

### Exemplo do arquivo `requirements.txt`:

```
cryptography
lxml
xmlsec
```

## 🚀 Como Usar

1. Altere o caminho e a senha do seu certificado `.pfx` nas variáveis:

```python
caminho_pfx = r"C:\caminho\para\seu_certificado.pfx"
senha_pfx = b"SuaSenhaAqui"
```

2. Insira seu XML conforme o layout da ABRASF dentro da variável `xml_para_assinar`.

3. Execute o script:

```bash
python pfxtoxml.py
```

4. O XML assinado será exibido no terminal. Você pode salvar em arquivo, se desejar:

```python
with open("nfse_assinada.xml", "w", encoding="utf-8") as f:
    f.write(xml_assinado_final)
```

## 📂 Estrutura do Projeto

```
NFSeSigner/
│
├── assinar_nfse.py         # Script principal de assinatura
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## 🧪 Testado com

- Certificado A1 em formato `.pfx`
- XML padrão ABRASF para NFSe

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

> Feito com 💻 e paciência por Guilherme.
