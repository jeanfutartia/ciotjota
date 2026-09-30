import os
import re

ficheiro = os.path.join("templates", "index.html")

if not os.path.exists(ficheiro):
    print("Ficheiro templates/index.html não encontrado.")
    exit(1)

with open(ficheiro, "r", encoding="utf-8") as f:
    html = f.read()

# Novo formulário ERP completo com tema Dark do GEOLOG TMS
novo_formulario = """
      <!-- FORMULÁRIO ERP COMPLETO (GEOLOG CIOT V8) -->
      <div class="card p-3 my-2" style="background:#090d16; border:1px solid #1f2937; border-radius:8px;">
        <div class="d-flex justify-content-between align-items-center mb-3 pb-2" style="border-bottom:1px solid #1f2937;">
          <h5 class="m-0 fw-bold" style="color:#00d2ff;">Construtor Passo a Passo de Operação de Transporte (e-Frete V8)</h5>
          <div class="d-flex align-items-center gap-2">
            <span class="small text-muted">Importar XML NF-e:</span>
            <input type="file" id="cXmlNfe" accept=".xml" class="form-control form-control-sm" style="max-width:260px; background:#111827; color:#fff; border-color:#374151;">
            <button type="button" class="btn btn-sm btn-outline-info" onclick="cCarregarPadraoElifer()">⚡ Padrão Elifer</button>
          </div>
        </div>

        <!-- 1. CONFIGURAÇÃO EMISSOR -->
        <div class="card mb-3" style="background:#111827; border:1px solid #1f2937;">
          <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">🏢 1. Configuração do Emissor e Integração</div>
          <div class="card-body p-2">
            <div class="row g-2">
              <div class="col-md-4">
                <label class="form-label small text-muted">Hash Integrador A3 Soft:*</label>
                <input type="text" id="cHashIntegrador" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="58e47cd2-8b54-4542-ba22-6941810dd7fa" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small text-muted">CNPJ Matriz / Filial (Elifer):*</label>
                <input type="text" id="cCnpjMatriz" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="11722820000103" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small text-muted">ID Único da Operação no ERP:*</label>
                <input type="text" id="cIdOperacaoCliente" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="560000549800" required>
              </div>
            </div>
          </div>
        </div>

        <div class="row g-2 mb-3">
          <!-- 2. CONTRATANTE E TRANSPORTADOR -->
          <div class="col-md-6">
            <div class="card h-100" style="background:#111827; border:1px solid #1f2937;">
              <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">🤝 2. Contratante e Transportador Contratado</div>
              <div class="card-body p-2">
                <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Contratante (Responsável pelo Pagamento)</div>
                <div class="row g-2 mb-2">
                  <div class="col-md-6">
                    <label class="form-label small text-muted">CNPJ/CPF Contratante:*</label>
                    <input type="text" id="cCnpjContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="11722820000103" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small text-muted">RNTRC Contratante:*</label>
                    <input type="text" id="cRntrcContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="49919644" required>
                  </div>
                  <div class="col-md-12">
                    <label class="form-label small text-muted">Razão Social Contratante:*</label>
                    <input type="text" id="cRazaoContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="ELIFER COMERCIO DE SUCATAS E RESIDUOS TRANSPORTES E SERVICOS" required>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label small text-muted">CEP:*</label>
                    <input type="text" id="cCepContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="13400970" required>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label small text-muted">Cód. IBGE Município:*</label>
                    <input type="text" id="cMunContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="3538709" required>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label small text-muted">Número:*</label>
                    <input type="text" id="cNumContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="SN" required>
                  </div>
                  <div class="col-md-12">
                    <label class="form-label small text-muted">Logradouro / Rua:*</label>
                    <input type="text" id="cRuaContratante" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="ROD SP 304, KM 172 5" required>
                  </div>
                </div>

                <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Contratado (Proprietário / Executor)</div>
                <div class="row g-2">
                  <div class="col-md-6">
                    <label class="form-label small text-muted">CNPJ/CPF Contratado:*</label>
                    <input type="text" id="cCnpjContratado" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="11722820000103" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small text-muted">RNTRC Contratado:*</label>
                    <input type="text" id="cRntrcContratado" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="49919644" required>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. MOTORISTA E VEÍCULOS -->
          <div class="col-md-6">
            <div class="card h-100" style="background:#111827; border:1px solid #1f2937;">
              <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">🚚 3. Motorista Condutor & Frota</div>
              <div class="card-body p-2">
                <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Dados do Condutor</div>
                <div class="row g-2 mb-2">
                  <div class="col-md-6">
                    <label class="form-label small text-muted">CPF Motorista (11 dígitos):*</label>
                    <input type="text" id="cCpfMotorista" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="60937378291" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small text-muted">CNH do Motorista:*</label>
                    <input type="text" id="cCnhMotorista" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="1466825624" required>
                  </div>
                  <div class="col-md-3">
                    <label class="form-label small text-muted">DDD:*</label>
                    <input type="text" id="cDddMotorista" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="19" required>
                  </div>
                  <div class="col-md-9">
                    <label class="form-label small text-muted">Telemóvel Motorista:*</label>
                    <input type="text" id="cTelMotorista" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="974098553" required>
                  </div>
                </div>

                <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Veículos da Viagem</div>
                <div class="row g-2">
                  <div class="col-md-4">
                    <label class="form-label small text-muted">Placa Trator (Cavalo):*</label>
                    <input type="text" id="cPlacaCavalo" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="GXS4F23" required>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label small text-muted">Placa Reboque (Carreta):</label>
                    <input type="text" id="cPlacaCarreta" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="ADN8I23">
                  </div>
                  <div class="col-md-4">
                    <label class="form-label small text-muted">Composição Veicular:*</label>
                    <select id="cCompVeicular" class="form-select form-select-sm text-white" style="background:#1f2937; border-color:#374151;">
                      <option value="true" selected>Sim (Conjunto)</option>
                      <option value="false">Não (Veículo Único)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. VIAGEM E NF-E -->
        <div class="card mb-3" style="background:#111827; border:1px solid #1f2937;">
          <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">📦 4. Viagem, Rota e Nota Fiscal Originária</div>
          <div class="card-body p-2">
            <div class="row g-2 mb-2">
              <div class="col-md-3">
                <label class="form-label small text-muted">Início Previsto Viagem:*</label>
                <input type="datetime-local" id="cDataInicioViagem" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="2026-09-30T14:00" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">Fim Previsto Viagem:*</label>
                <input type="datetime-local" id="cDataFimViagem" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="2026-10-01T18:00" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Distância (Km):*</label>
                <input type="number" id="cDistanciaKm" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="45" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">NCM Predominante:*</label>
                <input type="text" id="cNcmCarga" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="3402" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Tipo Embalagem:*</label>
                <select id="cTipoEmbalagem" class="form-select form-select-sm text-white" style="background:#1f2937; border-color:#374151;">
                  <option value="Caixa" selected>Caixa</option>
                  <option value="Palete">Palete</option>
                  <option value="Granel">Granel</option>
                  <option value="Unitario">Unitário</option>
                </select>
              </div>
            </div>

            <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Dados da Nota Fiscal Originária</div>
            <div class="row g-2">
              <div class="col-md-2">
                <label class="form-label small text-muted">Número NF-e:*</label>
                <input type="text" id="cNfeNumero" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="15584" required>
              </div>
              <div class="col-md-1">
                <label class="form-label small text-muted">Série:*</label>
                <input type="text" id="cNfeSerie" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="0" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">CNPJ Emissor da NF-e:*</label>
                <input type="text" id="cNfeCnpjEmissor" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="60881299000839" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Data Emissão NF-e:*</label>
                <input type="datetime-local" id="cNfeDataEmissao" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="2026-08-31T20:23" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Peso Carga (Kg):*</label>
                <input type="number" step="0.001" id="cPesoCarga" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="2625.200" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Valor Total NF-e (R$):*</label>
                <input type="number" step="0.01" id="cNfeValorTotal" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="154585.18" required>
              </div>
              <div class="col-md-12">
                <label class="form-label small text-muted">Descrição das Mercadorias:*</label>
                <input type="text" id="cDescMercadoria" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="ESSENCIAS E PRODUTOS DE LIMPEZA COALA" required>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. DESTINATÁRIO -->
        <div class="card mb-3" style="background:#111827; border:1px solid #1f2937;">
          <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">📍 5. Destinatário da Carga (Endereço Completo Obrigatório)</div>
          <div class="card-body p-2">
            <div class="row g-2">
              <div class="col-md-4">
                <label class="form-label small text-muted">CNPJ/CPF Destinatário:*</label>
                <input type="text" id="cDestCnpj" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="23637077001659" required>
              </div>
              <div class="col-md-8">
                <label class="form-label small text-muted">Razão Social Destinatário:*</label>
                <input type="text" id="cDestRazao" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="P.SEVERINI NETO COMERCIAL LTDA" required>
              </div>
              <div class="col-md-4">
                <label class="form-label small text-muted">Logradouro / Rodovia:*</label>
                <input type="text" id="cDestRua" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="RODOVIA RODOVIA DOM PEDRO I" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Número / KM:*</label>
                <input type="text" id="cDestNumero" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="SN" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">Bairro:*</label>
                <input type="text" id="cDestBairro" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="COLONIA FAZENDA SANTA ELISA" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">CEP Destino:*</label>
                <input type="text" id="cCepDestino" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="13069300" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">Cód. IBGE Destino:*</label>
                <input type="text" id="cIbgeDestino" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="3509502" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">CEP Origem (Coleta):*</label>
                <input type="text" id="cCepOrigem" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="13474789" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">Cód. IBGE Origem (Coleta):*</label>
                <input type="text" id="cIbgeOrigem" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="3501608" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">E-mail Notificação:</label>
                <input type="email" id="cDestEmail" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="munique.sances@vilanova.com.br">
              </div>
            </div>
          </div>
        </div>

        <!-- 6. VALORES, RETENÇÕES E BANCO -->
        <div class="card mb-3" style="background:#111827; border:1px solid #1f2937;">
          <div class="card-header py-2 fw-bold text-info" style="background:#161f30; font-size:0.85rem;">💰 6. Valores do Frete, Retenções Tributárias e Dados Bancários</div>
          <div class="card-body p-2">
            <div class="row g-2 mb-2">
              <div class="col-md-3">
                <label class="form-label small text-muted">Valor Bruto do Frete (R$):*</label>
                <input type="number" step="0.01" id="cValorFreteBruto" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="3850.00" oninput="cCalcularLiquido()" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">IRRF Retido (R$):</label>
                <input type="number" step="0.01" id="cImpostoIrrf" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="0.00" oninput="cCalcularLiquido()">
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">INSS Retido (R$):</label>
                <input type="number" step="0.01" id="cImpostoInss" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="0.00" oninput="cCalcularLiquido()">
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">SEST/SENAT (R$):</label>
                <input type="number" step="0.01" id="cImpostoSest" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="0.00" oninput="cCalcularLiquido()">
              </div>
              <div class="col-md-3">
                <label class="form-label small fw-bold text-success">Valor Líquido a Pagar (R$):*</label>
                <input type="number" step="0.01" id="cValorFreteLiquido" class="form-control form-control-sm text-success fw-bold" style="background:#1f2937; border-color:#374151;" value="3850.00" readonly>
              </div>
            </div>

            <div class="text-uppercase small fw-bold text-warning mb-1" style="font-size:0.75rem;">Dados do Depósito / Transferência Bancária</div>
            <div class="row g-2">
              <div class="col-md-3">
                <label class="form-label small text-muted">Meio de Pagamento:*</label>
                <select id="cTipoPagamento" class="form-select form-select-sm text-white" style="background:#1f2937; border-color:#374151;">
                  <option value="TransferenciaBancaria" selected>Transferência Bancária</option>
                  <option value="eFRETE">Saldo Conta e-Frete</option>
                </select>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Cód. Banco (COMPE):*</label>
                <input type="text" id="cBancoNum" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="237" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Agência (com dígito):*</label>
                <input type="text" id="cBancoAgencia" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="2825" required>
              </div>
              <div class="col-md-2">
                <label class="form-label small text-muted">Conta (com dígito):*</label>
                <input type="text" id="cBancoConta" class="form-control form-control-sm text-white" style="background:#1f2937; border-color:#374151;" value="29856-8" required>
              </div>
              <div class="col-md-3">
                <label class="form-label small text-muted">Tipo de Conta:*</label>
                <select id="cTipoConta" class="form-select form-select-sm text-white" style="background:#1f2937; border-color:#374151;">
                  <option value="ContaCorrente" selected>Conta Corrente</option>
                  <option value="ContaPoupanca">Conta Poupança</option>
                  <option value="ContaPagamento">Conta Pagamento</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <button type="button" class="btn btn-info w-100 py-2 fw-bold text-dark text-uppercase shadow-sm" style="background:#00d2ff; border:none;" onclick="compilarEEstruturarXml()">
          COMPILAR XML E ENVIAR PARA O TRANSMISSOR
        </button>
      </div>
"""

# Expressão para localizar e substituir o bloco antigo da Foto 1
alvo_re = r'<div[^>]*>\s*<h\d[^>]*>Construtor Passo a Passo de Operação de Transporte</h\d>.*?COMPILAR XML E ENVIAR PARA O TRANSMISSOR\s*</button>\s*</div>'

if re.search(alvo_re, html, re.DOTALL):
    html = re.sub(alvo_re, novo_formulario, html, flags=re.DOTALL)
    print("✅ Bloco do formulário substituído com sucesso em templates/index.html!")
else:
    idx_inicio = html.find("Construtor Passo a Passo de Operação de Transporte")
    if idx_inicio != -1:
        idx_div = html.rfind("<div", 0, idx_inicio)
        idx_fim_btn = html.find("COMPILAR XML E ENVIAR PARA O TRANSMISSOR", idx_inicio)
        idx_fim = html.find("</div>", idx_fim_btn) + 6
        html = html[:idx_div] + novo_formulario + html[idx_fim:]
        print("✅ Bloco localizado por âncoras e substituído com sucesso!")
    else:
        print("⚠️ Não foi possível encontrar a âncora em templates/index.html.")
        exit(1)

# Inserção das funções JavaScript se ainda não estiverem no ficheiro
if "compilarEEstruturarXml" not in html:
    html = html.replace("</body>", """
<script>
function cCalcularLiquido() {
  const bruto = parseFloat(document.getElementById('cValorFreteBruto').value) || 0;
  const irrf = parseFloat(document.getElementById('cImpostoIrrf').value) || 0;
  const inss = parseFloat(document.getElementById('cImpostoInss').value) || 0;
  const sest = parseFloat(document.getElementById('cImpostoSest').value) || 0;
  document.getElementById('cValorFreteLiquido').value = Math.max(0, bruto - (irrf + inss + sest)).toFixed(2);
}

document.getElementById('cXmlNfe')?.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const parser = new DOMParser();
      const xml = parser.parseFromString(evt.target.result, "application/xml");
      const getVal = (tag) => xml.getElementsByTagName(tag)[0]?.textContent?.trim() || '';

      if (getVal('nNF')) document.getElementById('cNfeNumero').value = getVal('nNF');
      if (getVal('serie')) document.getElementById('cNfeSerie').value = getVal('serie');
      if (getVal('vNF')) document.getElementById('cNfeValorTotal').value = getVal('vNF');
      if (getVal('pesoB') || getVal('pesoL')) document.getElementById('cPesoCarga').value = getVal('pesoB') || getVal('pesoL');
      if (getVal('NCM')) document.getElementById('cNcmCarga').value = getVal('NCM').substring(0, 4);
      if (getVal('xProd')) document.getElementById('cDescMercadoria').value = getVal('xProd');

      const dhEmi = getVal('dhEmi');
      if (dhEmi && dhEmi.length >= 16) document.getElementById('cNfeDataEmissao').value = dhEmi.substring(0, 16);

      const emit = xml.getElementsByTagName('emit')[0];
      if (emit) {
        document.getElementById('cNfeCnpjEmissor').value = emit.getElementsByTagName('CNPJ')[0]?.textContent || '';
        document.getElementById('cIbgeOrigem').value = emit.getElementsByTagName('cMun')[0]?.textContent || '';
        document.getElementById('cCepOrigem').value = emit.getElementsByTagName('CEP')[0]?.textContent || '';
      }

      const dest = xml.getElementsByTagName('dest')[0];
      if (dest) {
        document.getElementById('cDestCnpj').value = dest.getElementsByTagName('CNPJ')[0]?.textContent || '';
        document.getElementById('cDestRazao').value = dest.getElementsByTagName('xNome')[0]?.textContent || '';
        document.getElementById('cDestRua').value = dest.getElementsByTagName('xLgr')[0]?.textContent || '';
        document.getElementById('cDestNumero').value = dest.getElementsByTagName('nro')[0]?.textContent || 'SN';
        document.getElementById('cDestBairro').value = dest.getElementsByTagName('xBairro')[0]?.textContent || '';
        document.getElementById('cCepDestino').value = dest.getElementsByTagName('CEP')[0]?.textContent || '';
        document.getElementById('cIbgeDestino').value = dest.getElementsByTagName('cMun')[0]?.textContent || '';
        document.getElementById('cDestEmail').value = dest.getElementsByTagName('email')[0]?.textContent || '';
      }
      cCalcularLiquido();
      alert('✅ Dados da NF-e ' + document.getElementById('cNfeNumero').value + ' carregados com sucesso!');
    } catch (err) {
      alert('Erro ao ler XML da NF-e: ' + err.message);
    }
  };
  reader.readAsText(file);
});

function compilarEEstruturarXml() {
  cCalcularLiquido();
  const peso = parseFloat(document.getElementById('cPesoCarga').value) || 1;
  const vTotal = parseFloat(document.getElementById('cNfeValorTotal').value) || 1;
  const vUnit = (vTotal / peso).toFixed(5);
  const vLiquido = parseFloat(document.getElementById('cValorFreteLiquido').value) || 0;
  const vBruto = parseFloat(document.getElementById('cValorFreteBruto').value) || 0;

  const dIni = document.getElementById('cDataInicioViagem').value;
  const dFim = document.getElementById('cDataFimViagem').value;
  const dNfe = document.getElementById('cNfeDataEmissao').value;

  const placa2 = document.getElementById('cPlacaCarreta').value.trim();
  const extra = placa2 ? '\\n        <Veiculos><Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + placa2 + '</Placa></Veiculos>' : '';

  const xmlGerado = `<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <AdicionarOperacaoTransporte xmlns="http://schemas.ipc.adm.br/efrete/pefV2">
      <AdicionarOperacaoTransporteRequest xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
        <Integrador xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cHashIntegrador').value}</Integrador>
        <Versao xmlns="http://schemas.ipc.adm.br/efrete/objects">8</Versao>
        
        <TipoViagem xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">Padrao</TipoViagem>
        <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">${document.getElementById('cTipoPagamento').value}</TipoPagamento>

        <MatrizCNPJ>${document.getElementById('cCnpjMatriz').value}</MatrizCNPJ>
        <FilialCNPJ>${document.getElementById('cCnpjMatriz').value}</FilialCNPJ>
        <IdOperacaoCliente>${document.getElementById('cIdOperacaoCliente').value}</IdOperacaoCliente>

        <DataInicioViagem>${dIni}:00.000Z</DataInicioViagem>
        <DataFimViagem>${dFim}:00.000Z</DataFimViagem>
        <CodigoNCMNaturezaCarga>${document.getElementById('cNcmCarga').value}</CodigoNCMNaturezaCarga>
        <PesoCarga>${peso.toFixed(5)}</PesoCarga>
        <TipoEmbalagem>${document.getElementById('cTipoEmbalagem').value}</TipoEmbalagem>
        <CodigoTipoCarga>1</CodigoTipoCarga>
        <AltoDesempenho>false</AltoDesempenho>

        <Viagens>
          <DocumentoViagem>${document.getElementById('cNfeNumero').value}</DocumentoViagem>
          <CodigoMunicipioOrigem>${document.getElementById('cIbgeOrigem').value}</CodigoMunicipioOrigem>
          <CodigoMunicipioDestino>${document.getElementById('cIbgeDestino').value}</CodigoMunicipioDestino>
          <CepOrigem>${document.getElementById('cCepOrigem').value}</CepOrigem>
          <CepDestino>${document.getElementById('cCepDestino').value}</CepDestino>
          <DistanciaPercorrida>${document.getElementById('cDistanciaKm').value}</DistanciaPercorrida>
          
          <Valores xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">
            <TotalOperacao>${vBruto.toFixed(5)}</TotalOperacao>
            <TotalViagem>${vBruto.toFixed(5)}</TotalViagem>
            <TotalDeAdiantamento>0.00000</TotalDeAdiantamento>
            <TotalDeQuitacao>${vBruto.toFixed(5)}</TotalDeQuitacao>
            <Combustivel>0.00000</Combustivel>
            <Pedagio>0.00000</Pedagio>
            <OutrosCreditos>0.00000</OutrosCreditos>
            <JustificativaOutrosCreditos></JustificativaOutrosCreditos>
            <Seguro>0.00000</Seguro>
            <OutrosDebitos>0.00000</OutrosDebitos>
            <JustificativaOutrosDebitos></JustificativaOutrosDebitos>
          </Valores>
          
          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${document.getElementById('cTipoPagamento').value}</TipoPagamento>
          
          <NotasFiscais>
            <NotaFiscal>
              <Numero xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('cNfeNumero').value}</Numero>
              <Serie xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('cNfeSerie').value}</Serie>
              <Data xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${dNfe}:00.000Z</Data>
              <ValorTotal xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${vTotal.toFixed(2)}</ValorTotal>
              <ValorDaMercadoriaPorUnidade xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${vUnit}</ValorDaMercadoriaPorUnidade>
              <CodigoNCMNaturezaCarga xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('cNcmCarga').value}</CodigoNCMNaturezaCarga>
              <DescricaoDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('cDescMercadoria').value}</DescricaoDaMercadoria>
              <UnidadeDeMedidaDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">Kg</UnidadeDeMedidaDaMercadoria>
              <TipoDeCalculo xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">SemQuebra</TipoDeCalculo>
              <ValorDoFretePorUnidadeDeMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte" xsi:nil="true"/>
              <QuantidadeDaMercadoriaNoEmbarque xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${peso.toFixed(3)}</QuantidadeDaMercadoriaNoEmbarque>
              <ToleranciaDePerdaDeMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">
                <Tipo>Nenhum</Tipo>
                <Valor>0.00000</Valor>
              </ToleranciaDePerdaDeMercadoria>
            </NotaFiscal>
          </NotasFiscais>
        </Viagens>

        <Impostos xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
          <IRRF xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('cImpostoIrrf').value).toFixed(5)}</IRRF>
          <SestSenat xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('cImpostoSest').value).toFixed(5)}</SestSenat>
          <INSS xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('cImpostoInss').value).toFixed(5)}</INSS>
          <ISSQN xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</ISSQN>
          <OutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</OutrosImpostos>
          <DescricaoOutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects"></DescricaoOutrosImpostos>
        </Impostos>

        <Pagamentos>
          <IdPagamentoCliente>PAG-${document.getElementById('cIdOperacaoCliente').value}-1</IdPagamentoCliente>
          <DataDeLiberacao>${dFim}:00.000Z</DataDeLiberacao>
          <Valor>${vLiquido.toFixed(5)}</Valor>
          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${document.getElementById('cTipoPagamento').value}</TipoPagamento>
          <Categoria xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">Quitacao</Categoria>
          <Documento>${document.getElementById('cNfeNumero').value}</Documento>
          <CpfCnpjCreditado>${document.getElementById('cCnpjContratante').value}</CpfCnpjCreditado>
          <IndicadorPagamento>AVista</IndicadorPagamento>
          <InformacoesBancarias xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">
            <InstituicaoBancaria>${document.getElementById('cBancoNum').value}</InstituicaoBancaria>
            <Agencia>${document.getElementById('cBancoAgencia').value}</Agencia>
            <Conta>${document.getElementById('cBancoConta').value}</Conta>
            <TipoConta>${document.getElementById('cTipoConta').value}</TipoConta>
          </InformacoesBancarias>
        </Pagamentos>

        <Contratado>
          <CpfOuCnpj>${document.getElementById('cCnpjContratado').value}</CpfOuCnpj>
          <RNTRC>${document.getElementById('cRntrcContratado').value}</RNTRC>
        </Contratado>

        <Motorista>
          <CpfOuCnpj>${document.getElementById('cCpfMotorista').value}</CpfOuCnpj>
          <CNH>${document.getElementById('cCnhMotorista').value}</CNH>
          <Celular xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
            <DDD xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cDddMotorista').value}</DDD>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cTelMotorista').value}</Numero>
          </Celular>
        </Motorista>

        <Destinatario xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('cDestRazao').value}</NomeOuRazaoSocial>
          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('cDestCnpj').value}</CpfOuCnpj>
          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cDestBairro').value}</Bairro>
            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cDestRua').value}</Rua>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cDestNumero').value}</Numero>
            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>
            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cCepDestino').value}</CEP>
            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cIbgeDestino').value}</CodigoMunicipio>
          </Endereco>
          <EMail xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('cDestEmail').value}</EMail>
          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">false</ResponsavelPeloPagamento>
        </Destinatario>

        <Contratante xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('cRazaoContratante').value}</NomeOuRazaoSocial>
          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('cCnpjContratante').value}</CpfOuCnpj>
          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">ITAPIRU</Bairro>
            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cRuaContratante').value}</Rua>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cNumContratante').value}</Numero>
            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>
            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cCepContratante').value}</CEP>
            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('cMunContratante').value}</CodigoMunicipio>
          </Endereco>
          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">true</ResponsavelPeloPagamento>
          <RNTRC>${document.getElementById('cRntrcContratante').value}</RNTRC>
        </Contratante>

        <Veiculos>
          <Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('cPlacaCavalo').value}</Placa>
        </Veiculos>${extra}

        <ComposicaoVeicular>${document.getElementById('cCompVeicular').value}</ComposicaoVeicular>
        <RetornoVazio>false</RetornoVazio>
      </AdicionarOperacaoTransporteRequest>
    </AdicionarOperacaoTransporte>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>`;

  const tx = document.querySelector('textarea');
  if (tx) tx.value = xmlGerado;

  const btnTransmissor = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Transmissor XML'));
  if (btnTransmissor) btnTransmissor.click();

  alert('🚀 XML V8 Oficial compilado e inserido no Transmissor XML!');
}

function cCarregarPadraoElifer() {
  document.getElementById('cCnpjMatriz').value = '11722820000103';
  document.getElementById('cCnpjContratante').value = '11722820000103';
  document.getElementById('cRntrcContratante').value = '49919644';
  document.getElementById('cCnpjContratado').value = '11722820000103';
  document.getElementById('cRntrcContratado').value = '49919644';
  document.getElementById('cCpfMotorista').value = '60937378291';
  document.getElementById('cCnhMotorista').value = '1466825624';
  document.getElementById('cPlacaCavalo').value = 'GXS4F23';
  document.getElementById('cPlacaCarreta').value = 'ADN8I23';
  cCalcularLiquido();
}
</script>
</body>
""")

with open(ficheiro, "w", encoding="utf-8") as f:
    f.write(html)

print("🎉 SUCESSO! templates/index.html atualizado diretamente!")
