import os
import re

target_file = "server.py" if os.path.exists("server.py") else "app.py"

if not os.path.exists(target_file):
    print("Ficheiro server.py ou app.py não encontrado na pasta atual.")
    exit(1)

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Novo layout completo da aba Construtor CIOT (idêntico à Foto 2 adaptado ao tema dark da Foto 1)
novo_construtor_html = '''
    <!-- ABA CONSTRUTOR CIOT COMPLETO ESTILO ERP -->
    <div class="tab-pane fade" id="tab-construtor" role="tabpanel">
      <div class="card p-3 my-2" style="background:#090d16; border:1px solid #1f2937; border-radius:8px;">
        
        <div class="d-flex justify-content-between align-items-center mb-3 pb-2" style="border-bottom:1px solid #1f2937;">
          <h5 class="m-0 text-cyan fw-bold" style="color:#00d2ff;">Construtor Passo a Passo de Operação de Transporte (e-Frete V8)</h5>
          <div class="d-flex align-items-center gap-2">
            <span class="small text-muted">Carregar XML NF-e:</span>
            <input type="file" id="construtorNfeInput" accept=".xml" class="form-control form-control-sm" style="max-width:240px; background:#111827; color:#fff; border-color:#374151;">
            <button type="button" class="btn btn-sm btn-outline-info" onclick="carregarPadraoEliferConstrutor()">⚡ Padrão Elifer</button>
          </div>
        </div>

        <!-- 1. IDENTIFICAÇÃO -->
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

        <!-- BOTÃO PRINCIPAL IDÊNTICO À FOTO 1 -->
        <button type="button" class="btn btn-info w-100 py-2 fw-bold text-dark text-uppercase shadow-sm" style="background:#00d2ff; border:none;" onclick="compilarEEstruturarXml()">
          COMPILAR XML E ENVIAR PARA O TRANSMISSOR
        </button>

      </div>
    </div>
'''

# Script JS acoplado
novo_js = '''
<script>
function cCalcularLiquido() {
  const bruto = parseFloat(document.getElementById('cValorFreteBruto').value) || 0;
  const irrf = parseFloat(document.getElementById('cImpostoIrrf').value) || 0;
  const inss = parseFloat(document.getElementById('cImpostoInss').value) || 0;
  const sest = parseFloat(document.getElementById('cImpostoSest').value) || 0;
  document.getElementById('cValorFreteLiquido').value = Math.max(0, bruto - (irrf + inss + sest)).toFixed(2);
}

document.getElementById('construtorNfeInput')?.addEventListener('change', function(e) {
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
  const extra = placa2 ? '\n        <Veiculos><Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + placa2 + '</Placa></Veiculos>' : '';

  const xmlGerado = '<?xml version="1.0" encoding="utf-8"?>\n' +
'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" \n' +
'                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" \n' +
'                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n' +
'  <SOAP-ENV:Body>\n' +
'    <AdicionarOperacaoTransporte xmlns="http://schemas.ipc.adm.br/efrete/pefV2">\n' +
'      <AdicionarOperacaoTransporteRequest xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'        <Integrador xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cHashIntegrador').value + '</Integrador>\n' +
'        <Versao xmlns="http://schemas.ipc.adm.br/efrete/objects">8</Versao>\n' +
'        \n' +
'        <TipoViagem xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">Padrao</TipoViagem>\n' +
'        <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">' + document.getElementById('cTipoPagamento').value + '</TipoPagamento>\n' +
'\n' +
'        <MatrizCNPJ>' + document.getElementById('cCnpjMatriz').value + '</MatrizCNPJ>\n' +
'        <FilialCNPJ>' + document.getElementById('cCnpjMatriz').value + '</FilialCNPJ>\n' +
'        <IdOperacaoCliente>' + document.getElementById('cIdOperacaoCliente').value + '</IdOperacaoCliente>\n' +
'\n' +
'        <DataInicioViagem>' + dIni + ':00.000Z</DataInicioViagem>\n' +
'        <DataFimViagem>' + dFim + ':00.000Z</DataFimViagem>\n' +
'        <CodigoNCMNaturezaCarga>' + document.getElementById('cNcmCarga').value + '</CodigoNCMNaturezaCarga>\n' +
'        <PesoCarga>' + peso.toFixed(5) + '</PesoCarga>\n' +
'        <TipoEmbalagem>' + document.getElementById('cTipoEmbalagem').value + '</TipoEmbalagem>\n' +
'        <CodigoTipoCarga>1</CodigoTipoCarga>\n' +
'        <AltoDesempenho>false</AltoDesempenho>\n' +
'\n' +
'        <Viagens>\n' +
'          <DocumentoViagem>' + document.getElementById('cNfeNumero').value + '</DocumentoViagem>\n' +
'          <CodigoMunicipioOrigem>' + document.getElementById('cIbgeOrigem').value + '</CodigoMunicipioOrigem>\n' +
'          <CodigoMunicipioDestino>' + document.getElementById('cIbgeDestino').value + '</CodigoMunicipioDestino>\n' +
'          <CepOrigem>' + document.getElementById('cCepOrigem').value + '</CepOrigem>\n' +
'          <CepDestino>' + document.getElementById('cCepDestino').value + '</CepDestino>\n' +
'          <DistanciaPercorrida>' + document.getElementById('cDistanciaKm').value + '</DistanciaPercorrida>\n' +
'          \n' +
'          <Valores xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">\n' +
'            <TotalOperacao>' + vBruto.toFixed(5) + '</TotalOperacao>\n' +
'            <TotalViagem>' + vBruto.toFixed(5) + '</TotalViagem>\n' +
'            <TotalDeAdiantamento>0.00000</TotalDeAdiantamento>\n' +
'            <TotalDeQuitacao>' + vBruto.toFixed(5) + '</TotalDeQuitacao>\n' +
'            <Combustivel>0.00000</Combustivel>\n' +
'            <Pedagio>0.00000</Pedagio>\n' +
'            <OutrosCreditos>0.00000</OutrosCreditos>\n' +
'            <JustificativaOutrosCreditos></JustificativaOutrosCreditos>\n' +
'            <Seguro>0.00000</Seguro>\n' +
'            <OutrosDebitos>0.00000</OutrosDebitos>\n' +
'            <JustificativaOutrosDebitos></JustificativaOutrosDebitos>\n' +
'          </Valores>\n' +
'          \n' +
'          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + document.getElementById('cTipoPagamento').value + '</TipoPagamento>\n' +
'          \n' +
'          <NotasFiscais>\n' +
'            <NotaFiscal>\n' +
'              <Numero xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('cNfeNumero').value + '</Numero>\n' +
'              <Serie xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('cNfeSerie').value + '</Serie>\n' +
'              <Data xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + dNfe + ':00.000Z</Data>\n' +
'              <ValorTotal xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + vTotal.toFixed(2) + '</ValorTotal>\n' +
'              <ValorDaMercadoriaPorUnidade xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + vUnit + '</ValorDaMercadoriaPorUnidade>\n' +
'              <CodigoNCMNaturezaCarga xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('cNcmCarga').value + '</CodigoNCMNaturezaCarga>\n' +
'              <DescricaoDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('cDescMercadoria').value + '</DescricaoDaMercadoria>\n' +
'              <UnidadeDeMedidaDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">Kg</UnidadeDeMedidaDaMercadoria>\n' +
'              <TipoDeCalculo xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">SemQuebra</TipoDeCalculo>\n' +
'              <ValorDoFretePorUnidadeDeMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte" xsi:nil="true"/>\n' +
'              <QuantidadeDaMercadoriaNoEmbarque xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + peso.toFixed(3) + '</QuantidadeDaMercadoriaNoEmbarque>\n' +
'              <ToleranciaDePerdaDeMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">\n' +
'                <Tipo>Nenhum</Tipo>\n' +
'                <Valor>0.00000</Valor>\n' +
'              </ToleranciaDePerdaDeMercadoria>\n' +
'            </NotaFiscal>\n' +
'          </NotasFiscais>\n' +
'        </Viagens>\n' +
'\n' +
'        <Impostos xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'          <IRRF xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('cImpostoIrrf').value).toFixed(5) + '</IRRF>\n' +
'          <SestSenat xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('cImpostoSest').value).toFixed(5) + '</SestSenat>\n' +
'          <INSS xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('cImpostoInss').value).toFixed(5) + '</INSS>\n' +
'          <ISSQN xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</ISSQN>\n' +
'          <OutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</OutrosImpostos>\n' +
'          <DescricaoOutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects"></DescricaoOutrosImpostos>\n' +
'        </Impostos>\n' +
'\n' +
'        <Pagamentos>\n' +
'          <IdPagamentoCliente>PAG-' + document.getElementById('cIdOperacaoCliente').value + '-1</IdPagamentoCliente>\n' +
'          <DataDeLiberacao>' + dFim + ':00.000Z</DataDeLiberacao>\n' +
'          <Valor>' + vLiquido.toFixed(5) + '</Valor>\n' +
'          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + document.getElementById('cTipoPagamento').value + '</TipoPagamento>\n' +
'          <Categoria xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">Quitacao</Categoria>\n' +
'          <Documento>' + document.getElementById('cNfeNumero').value + '</Documento>\n' +
'          <CpfCnpjCreditado>' + document.getElementById('cCnpjContratante').value + '</CpfCnpjCreditado>\n' +
'          <IndicadorPagamento>AVista</IndicadorPagamento>\n' +
'          <InformacoesBancarias xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">\n' +
'            <InstituicaoBancaria>' + document.getElementById('cBancoNum').value + '</InstituicaoBancaria>\n' +
'            <Agencia>' + document.getElementById('cBancoAgencia').value + '</Agencia>\n' +
'            <Conta>' + document.getElementById('cBancoConta').value + '</Conta>\n' +
'            <TipoConta>' + document.getElementById('cTipoConta').value + '</TipoConta>\n' +
'          </InformacoesBancarias>\n' +
'        </Pagamentos>\n' +
'\n' +
'        <Contratado>\n' +
'          <CpfOuCnpj>' + document.getElementById('cCnpjContratado').value + '</CpfOuCnpj>\n' +
'          <RNTRC>' + document.getElementById('cRntrcContratado').value + '</RNTRC>\n' +
'        </Contratado>\n' +
'\n' +
'        <Motorista>\n' +
'          <CpfOuCnpj>' + document.getElementById('cCpfMotorista').value + '</CpfOuCnpj>\n' +
'          <CNH>' + document.getElementById('cCnhMotorista').value + '</CNH>\n' +
'          <Celular xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'            <DDD xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cDddMotorista').value + '</DDD>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cTelMotorista').value + '</Numero>\n' +
'          </Celular>\n' +
'        </Motorista>\n' +
'\n' +
'        <Destinatario xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cDestRazao').value + '</NomeOuRazaoSocial>\n' +
'          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cDestCnpj').value + '</CpfOuCnpj>\n' +
'          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cDestBairro').value + '</Bairro>\n' +
'            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cDestRua').value + '</Rua>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cDestNumero').value + '</Numero>\n' +
'            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>\n' +
'            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cCepDestino').value + '</CEP>\n' +
'            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cIbgeDestino').value + '</CodigoMunicipio>\n' +
'          </Endereco>\n' +
'          <EMail xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cDestEmail').value + '</EMail>\n' +
'          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">false</ResponsavelPeloPagamento>\n' +
'        </Destinatario>\n' +
'\n' +
'        <Contratante xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cRazaoContratante').value + '</NomeOuRazaoSocial>\n' +
'          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cCnpjContratante').value + '</CpfOuCnpj>\n' +
'          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">ITAPIRU</Bairro>\n' +
'            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cRuaContratante').value + '</Rua>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cNumContratante').value + '</Numero>\n' +
'            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>\n' +
'            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cCepContratante').value + '</CEP>\n' +
'            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cMunContratante').value + '</CodigoMunicipio>\n' +
'          </Endereco>\n' +
'          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">true</ResponsavelPeloPagamento>\n' +
'          <RNTRC>' + document.getElementById('cRntrcContratante').value + '</RNTRC>\n' +
'        </Contratante>\n' +
'\n' +
'        <Veiculos>\n' +
'          <Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('cPlacaCavalo').value + '</Placa>\n' +
'        </Veiculos>' + extra + '\n' +
'\n' +
'        <ComposicaoVeicular>' + document.getElementById('cCompVeicular').value + '</ComposicaoVeicular>\n' +
'        <RetornoVazio>false</RetornoVazio>\n' +
'      </AdicionarOperacaoTransporteRequest>\n' +
'    </AdicionarOperacaoTransporte>\n' +
'  </SOAP-ENV:Body>\n' +
'</SOAP-ENV:Envelope>';

  // Transfere para o textarea do Transmissor XML
  const tx = document.querySelector('textarea');
  if (tx) tx.value = xmlGerado;

  // Clica automaticamente na aba Transmissor XML
  const tabBtn = document.querySelector('button[data-bs-target*="transmissor"], button[data-bs-target*="envio"], button:first-child');
  if (tabBtn) tabBtn.click();

  alert('🚀 XML V8 gerado com sucesso e injetado no Transmissor XML!');
}

function carregarPadraoEliferConstrutor() {
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
'''

# Substitui a div da aba construtor existente
if 'id="tab-construtor"' in content or 'Construtor Passo a Passo' in content:
    # Substituição por regex abrangendo o bloco antigo da aba construtor
    pattern = r'<div class="tab-pane[^"]*" id="tab-construtor"[^>]*>.*?</div>\s*</div>\s*</div>'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, novo_construtor_html, content, flags=re.DOTALL)
    else:
        # Se for estrutura simples, substitui até o fechamento da tab-pane
        content = re.sub(r'<div class="tab-pane[^"]*" id="tab-construtor"[^>]*>.*?</div>\s*</div>', novo_construtor_html, content, flags=re.DOTALL)

# Injeta os scripts JS antes do </body>
if 'compilarEEstruturarXml' not in content:
    content = content.replace('</body>', novo_js + '\n</body>')

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Sucesso! Aba Construtor CIOT atualizada com o formulário completo no ficheiro {target_file}.")
