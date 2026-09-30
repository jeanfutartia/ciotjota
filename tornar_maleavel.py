import os

# 1. ATUALIZAR SERVER.PY
with open("server.py", "r", encoding="utf-8") as f:
    server_code = f.read()

novo_helper_pfx = """
import re
import cryptography.hazmat.primitives.serialization.pkcs12 as pkcs12_lib
import cryptography.x509.oid as x509_oid

def extrair_dados_pfx(pfx_bytes: bytes, password: str):
    try:
        senha_bytes = password.encode("utf-8") if isinstance(password, str) else password
        _, cert, _ = pkcs12_lib.load_key_and_certificates(pfx_bytes, senha_bytes)
        if not cert:
            return None, None
        
        # Extrai CNPJ (OID ICP-Brasil 2.16.76.1.3.3) ou do Common Name
        cnpj = None
        for ext in cert.extensions:
            if ext.oid.dotted_string == "2.5.29.17": # Subject Alternative Name
                for name in ext.value:
                    val_str = str(name.value)
                    m = re.search(r"\\b(\\d{14})\\b", val_str)
                    if m:
                        cnpj = m.group(1)
                        break
        
        common_name = ""
        for attr in cert.subject:
            if attr.oid == x509_oid.NameOID.COMMON_NAME:
                common_name = attr.value
                if not cnpj:
                    m = re.search(r"\\b(\\d{14})\\b", common_name)
                    if m:
                        cnpj = m.group(1)

        return cnpj, common_name
    except Exception:
        return None, None

@app.post("/api/inspecionar_pfx")
async def api_inspecionar_pfx(
    pfxFile: UploadFile = File(...),
    pfxPassword: str = Form("")
):
    try:
        pfx_bytes = await pfxFile.read()
        cnpj, nome = extrair_dados_pfx(pfx_bytes, pfxPassword)
        if not cnpj:
            return {"sucesso": False, "erro": "Senha incorreta ou CNPJ não localizado no certificado."}
        
        return {
            "sucesso": True,
            "cnpj": cnpj,
            "razao_social": nome
        }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}
"""

if "/api/inspecionar_pfx" not in server_code:
    # Insere antes da rota /api/transmitir
    pos = server_code.find("@app.post(\"/api/transmitir\")")
    if pos != -1:
        server_code = server_code[:pos] + novo_helper_pfx + "\n" + server_code[pos:]
        
        # Ajusta a rota /api/transmitir para autoinjetar o CNPJ do PFX no XML
        old_transmitir = 'response = pkcs12_post('
        new_transmitir = '''# Auto-alinha o CNPJ do XML com o CNPJ titular do certificado PFX
        cnpj_pfx, _ = extrair_dados_pfx(pfx_bytes, pfxPassword)
        if cnpj_pfx:
            xmlPayload = re.sub(r"<MatrizCNPJ>.*?</MatrizCNPJ>", f"<MatrizCNPJ>{cnpj_pfx}</MatrizCNPJ>", xmlPayload)
            xmlPayload = re.sub(r"<FilialCNPJ>.*?</FilialCNPJ>", f"<FilialCNPJ>{cnpj_pfx}</FilialCNPJ>", xmlPayload)

        response = pkcs12_post('''
        server_code = server_code.replace(old_transmitir, new_transmitir, 1)

        with open("server.py", "w", encoding="utf-8") as f:
            f.write(server_code)
        print("[OK] server.py atualizado com extrator dinamico de PFX!")

# 2. ATUALIZAR INDEX.HTML COM LEITOR DINÂMICO
html_file = os.path.join("templates", "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    html_code = f.read()

# Substitui o campo de CNPJ do construtor para permitir edicao livre
html_code = html_code.replace('readonly style="color: #38bdf8; font-weight: bold;"', 'style="color: #38bdf8; font-weight: bold;"')

# Adiciona o script de inspecao automatica ao selecionar PFX e senha
script_inspecao = """
    // Leitura dinamica do PFX
    async function checarCertificadoDinamico() {
      const fileInput = document.getElementById('ciotPfxInput');
      const password = document.getElementById('ciotPfxPassword').value;
      if (!fileInput.files || fileInput.files.length === 0 || !password) return;

      const formData = new FormData();
      formData.append('pfxFile', fileInput.files[0]);
      formData.append('pfxPassword', password);

      try {
        const resp = await fetch('/api/inspecionar_pfx', { method: 'POST', body: formData });
        const data = await resp.json();
        if (data.sucesso) {
          const badge = document.getElementById('badgeEmitenteDinamico');
          if (badge) {
            badge.innerText = `EMITENTE: ${data.razao_social} (${data.cnpj})`;
            badge.style.color = '#34d399';
          }
          document.getElementById('f_cnpjContratante').value = data.cnpj;
          compilarFormularioParaXml();
        }
      } catch (e) {
        console.warn('Erro ao inspecionar PFX:', e);
      }
    }

    document.getElementById('ciotPfxPassword').addEventListener('blur', checarCertificadoDinamico);
    document.getElementById('ciotPfxInput').addEventListener('change', checarCertificadoDinamico);
"""

if "checarCertificadoDinamico" not in html_code:
    html_code = html_code.replace("function compilarFormularioParaXml() {", script_inspecao + "\n    function compilarFormularioParaXml() {")
    html_code = html_code.replace("EMITENTE: IPATINGASES COMÉRCIO E TRANSPORTES (09.278.583/0001-91)", '<span id="badgeEmitenteDinamico">EMITENTE: Selecione o certificado .PFX</span>')

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_code)
    print("[OK] templates/index.html atualizado com deteccao multiempresa!")
