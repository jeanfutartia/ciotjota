import os

target_file = "server.py" if os.path.exists("server.py") else "app.py"

if not os.path.exists(target_file):
    print("Arquivo server.py/app.py não encontrado na pasta atual.")
    exit(1)

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Injetar o botão da nova aba no cabeçalho nav-tabs
nav_marker = '<li class="nav-item">'
new_nav_btn = '''
        <li class="nav-item">
          <button class="nav-link" id="erp-tab" data-bs-toggle="tab" data-bs-target="#tab-erp" type="button">
            📝 Formulário ERP CIOT (V8)
          </button>
        </li>'''

# 2. Conteúdo HTML da aba ERP
erp_html_tab = '''
      <!-- ABA FORMULÁRIO ERP CIOT -->
      <div class="tab-pane fade" id="tab-erp" role="tabpanel">
        <div class="p-3 bg-white border border-top-0 rounded-bottom">
          <div class="card bg-light border-primary mb-3">
            <div class="card-body p-2 d-flex flex-wrap align-items-center justify-content-between gap-2">
              <div class="d-flex align-items-center gap-2">
                <label class="form-label m-0 text-primary fw-bold">📄 Carregar XML da NF-e:</label>
                <input type="file" id="erpNfeXmlInput" accept=".xml" class="form-control form-control-sm" style="max-width: 320px;">
              </div>
              <div class="d-flex gap-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" onclick="preencherPadraoEliferERP()">⚡ Carregar Dados Elifer</button>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="limparCamposERP()">🗑️ Limpar</button>
              </div>
            </div>
          </div>

          <div class="card mb-3">
            <div class="card-header fw-bold text-primary">🏢 1. Configuração do Emissor e Integração</div>
            <div class="card-body">
              <div class="row g-2">
                <div class="col-md-4">
                  <label class="form-label">Hash Integrador (A3 Soft):*</label>
                  <input type="text" id="erpHashIntegrador" class="form-control" value="58e47cd2-8b54-4542-ba22-6941810dd7fa" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">CNPJ Matriz / Filial:*</label>
                  <input type="text" id="erpCnpjMatriz" class="form-control" value="11722820000103" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">ID Operação no ERP:*</label>
                  <input type="text" id="erpIdOperacao" class="form-control" value="560000549800" required>
                </div>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6">
              <div class="card mb-3 h-100">
                <div class="card-header fw-bold">🏢 2. Contratante & Transportador Contratado</div>
                <div class="card-body">
                  <div class="text-muted fw-bold mb-2 small text-uppercase">Contratante</div>
                  <div class="row g-2 mb-3">
                    <div class="col-md-6">
                      <label class="form-label">CNPJ/CPF Contratante:*</label>
                      <input type="text" id="erpCnpjContratante" class="form-control" value="11722820000103" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">RNTRC Contratante:*</label>
                      <input type="text" id="erpRntrcContratante" class="form-control" value="49919644" required>
                    </div>
                    <div class="col-md-12">
                      <label class="form-label">Razão Social Contratante:*</label>
                      <input type="text" id="erpRazaoContratante" class="form-control" value="ELIFER COMERCIO DE SUCATAS E RESIDUOS TRANSPORTES E SERVICOS" required>
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">CEP:*</label>
                      <input type="text" id="erpCepContratante" class="form-control" value="13400970" required>
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">IBGE Município:*</label>
                      <input type="text" id="erpMunContratante" class="form-control" value="3538709" required>
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Número:*</label>
                      <input type="text" id="erpNumContratante" class="form-control" value="SN" required>
                    </div>
                    <div class="col-md-12">
                      <label class="form-label">Logradouro / Rua:*</label>
                      <input type="text" id="erpRuaContratante" class="form-control" value="ROD SP 304, KM 172 5" required>
                    </div>
                  </div>
                  <div class="text-muted fw-bold mb-2 small text-uppercase">Transportador (Executor)</div>
                  <div class="row g-2">
                    <div class="col-md-6">
                      <label class="form-label">CNPJ/CPF Contratado:*</label>
                      <input type="text" id="erpCnpjContratado" class="form-control" value="11722820000103" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">RNTRC Contratado:*</label>
                      <input type="text" id="erpRntrcContratado" class="form-control" value="49919644" required>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <div class="card mb-3 h-100">
                <div class="card-header fw-bold">🚛 3. Motorista Condutor & Veículos</div>
                <div class="card-body">
                  <div class="text-muted fw-bold mb-2 small text-uppercase">Dados do Motorista</div>
                  <div class="row g-2 mb-3">
                    <div class="col-md-6">
                      <label class="form-label">CPF Motorista (11 dígitos):*</label>
                      <input type="text" id="erpCpfMotorista" class="form-control" value="60937378291" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">CNH do Motorista:*</label>
                      <input type="text" id="erpCnhMotorista" class="form-control" value="1466825624" required>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label">DDD:*</label>
                      <input type="text" id="erpDddMotorista" class="form-control" value="19" required>
                    </div>
                    <div class="col-md-9">
                      <label class="form-label">Celular Motorista:*</label>
                      <input type="text" id="erpTelMotorista" class="form-control" value="974098553" required>
                    </div>
                  </div>
                  <div class="text-muted fw-bold mb-2 small text-uppercase">Veículos</div>
                  <div class="row g-2">
                    <div class="col-md-4">
                      <label class="form-label">Placa Cavalo (Trator):*</label>
                      <input type="text" id="erpPlacaCavalo" class="form-control" value="GXS4F23" required>
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Placa Carreta (Reboque):</label>
                      <input type="text" id="erpPlacaCarreta" class="form-control" value="ADN8I23">
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Composição Veicular:*</label>
                      <select id="erpCompVeicular" class="form-select">
                        <option value="true" selected>Sim (Conjunto)</option>
                        <option value="false">Não (Veículo Único)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card mb-3">
            <div class="card-header fw-bold">📦 4. Dados da Viagem, Rota e NF-e</div>
            <div class="card-body">
              <div class="row g-2 mb-3">
                <div class="col-md-3">
                  <label class="form-label">Início da Viagem:*</label>
                  <input type="datetime-local" id="erpDataInicioViagem" class="form-control" value="2026-09-30T14:00" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Fim da Viagem:*</label>
                  <input type="datetime-local" id="erpDataFimViagem" class="form-control" value="2026-10-01T18:00" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Distância (Km):*</label>
                  <input type="number" id="erpDistanciaKm" class="form-control" value="45" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">NCM Carga:*</label>
                  <input type="text" id="erpNcmCarga" class="form-control" value="3402" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Tipo Embalagem:*</label>
                  <select id="erpTipoEmbalagem" class="form-select">
                    <option value="Caixa" selected>Caixa</option>
                    <option value="Palete">Palete</option>
                    <option value="Granel">Granel</option>
                    <option value="Unitario">Unitário</option>
                  </select>
                </div>
              </div>
              <div class="row g-2">
                <div class="col-md-2">
                  <label class="form-label">Número NF-e:*</label>
                  <input type="text" id="erpNfeNumero" class="form-control" value="15584" required>
                </div>
                <div class="col-md-1">
                  <label class="form-label">Série:*</label>
                  <input type="text" id="erpNfeSerie" class="form-control" value="0" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">CNPJ Emissor da NF-e:*</label>
                  <input type="text" id="erpNfeCnpjEmissor" class="form-control" value="60881299000839" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Data Emissão NF-e:*</label>
                  <input type="datetime-local" id="erpNfeDataEmissao" class="form-control" value="2026-08-31T20:23" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Peso Bruto (Kg):*</label>
                  <input type="number" step="0.001" id="erpPesoCarga" class="form-control" value="2625.200" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Valor Total NF-e (R$):*</label>
                  <input type="number" step="0.01" id="erpNfeValorTotal" class="form-control" value="154585.18" required>
                </div>
                <div class="col-md-12">
                  <label class="form-label">Descrição da Carga:*</label>
                  <input type="text" id="erpDescMercadoria" class="form-control" value="ESSENCIAS E PRODUTOS DE LIMPEZA COALA" required>
                </div>
              </div>
            </div>
          </div>

          <div class="card mb-3">
            <div class="card-header fw-bold">📍 5. Destinatário da Carga</div>
            <div class="card-body">
              <div class="row g-2">
                <div class="col-md-4">
                  <label class="form-label">CNPJ/CPF Destinatário:*</label>
                  <input type="text" id="erpDestCnpj" class="form-control" value="23637077001659" required>
                </div>
                <div class="col-md-8">
                  <label class="form-label">Razão Social Destinatário:*</label>
                  <input type="text" id="erpDestRazao" class="form-control" value="P.SEVERINI NETO COMERCIAL LTDA" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Logradouro / Rodovia:*</label>
                  <input type="text" id="erpDestRua" class="form-control" value="RODOVIA RODOVIA DOM PEDRO I" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Número / KM:*</label>
                  <input type="text" id="erpDestNumero" class="form-control" value="SN" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Bairro:*</label>
                  <input type="text" id="erpDestBairro" class="form-control" value="COLONIA FAZENDA SANTA ELISA" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">CEP Destino:*</label>
                  <input type="text" id="erpCepDestino" class="form-control" value="13069300" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">IBGE Destino:*</label>
                  <input type="text" id="erpIbgeDestino" class="form-control" value="3509502" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">CEP Origem (Coleta):*</label>
                  <input type="text" id="erpCepOrigem" class="form-control" value="13474789" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">IBGE Origem (Coleta):*</label>
                  <input type="text" id="erpIbgeOrigem" class="form-control" value="3501608" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">E-mail Destinatário:</label>
                  <input type="email" id="erpDestEmail" class="form-control" value="munique.sances@vilanova.com.br">
                </div>
              </div>
            </div>
          </div>

          <div class="card mb-3">
            <div class="card-header fw-bold">💰 6. Valores do Frete, Retenções Tributárias e Conta Bancária</div>
            <div class="card-body">
              <div class="row g-2 mb-3">
                <div class="col-md-3">
                  <label class="form-label">Valor Bruto Frete (R$):*</label>
                  <input type="number" step="0.01" id="erpValorFreteBruto" class="form-control" value="3850.00" oninput="erpCalcularLiquido()" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">IRRF Retido (R$):</label>
                  <input type="number" step="0.01" id="erpImpostoIrrf" class="form-control" value="0.00" oninput="erpCalcularLiquido()">
                </div>
                <div class="col-md-2">
                  <label class="form-label">INSS Retido (R$):</label>
                  <input type="number" step="0.01" id="erpImpostoInss" class="form-control" value="0.00" oninput="erpCalcularLiquido()">
                </div>
                <div class="col-md-2">
                  <label class="form-label">SEST/SENAT (R$):</label>
                  <input type="number" step="0.01" id="erpImpostoSest" class="form-control" value="0.00" oninput="erpCalcularLiquido()">
                </div>
                <div class="col-md-3">
                  <label class="form-label fw-bold text-success">Líquido a Pagar (R$):*</label>
                  <input type="number" step="0.01" id="erpValorFreteLiquido" class="form-control bg-light fw-bold" value="3850.00" readonly>
                </div>
              </div>
              <div class="row g-2">
                <div class="col-md-3">
                  <label class="form-label">Meio de Pagamento:*</label>
                  <select id="erpTipoPagamento" class="form-select">
                    <option value="TransferenciaBancaria" selected>Transferência Bancária</option>
                    <option value="eFRETE">Saldo Conta e-Frete</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Banco (COMPE):*</label>
                  <input type="text" id="erpBancoNum" class="form-control" value="237" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Agência:*</label>
                  <input type="text" id="erpBancoAgencia" class="form-control" value="2825" required>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Conta Corrente:*</label>
                  <input type="text" id="erpBancoConta" class="form-control" value="29856-8" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Tipo de Conta:*</label>
                  <select id="erpTipoConta" class="form-select">
                    <option value="ContaCorrente" selected>Conta Corrente</option>
                    <option value="ContaPoupanca">Conta Poupança</option>
                    <option value="ContaPagamento">Conta Pagamento</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex gap-2 justify-content-end mb-3">
            <button type="button" class="btn btn-outline-secondary px-4 fw-bold" onclick="erpCopiarXml()">📋 Copiar XML</button>
            <button type="button" class="btn btn-primary px-4 fw-bold" onclick="erpTransferirParaEmissor()">🚀 Gerar & Injetar no Transmissor</button>
          </div>
        </div>
      </div>
'''

# 3. Bloco JS para controle e montagem
erp_js = '''
<script>
function erpCalcularLiquido() {
  const bruto = parseFloat(document.getElementById('erpValorFreteBruto').value) || 0;
  const irrf = parseFloat(document.getElementById('erpImpostoIrrf').value) || 0;
  const inss = parseFloat(document.getElementById('erpImpostoInss').value) || 0;
  const sest = parseFloat(document.getElementById('erpImpostoSest').value) || 0;
  document.getElementById('erpValorFreteLiquido').value = Math.max(0, bruto - (irrf + inss + sest)).toFixed(2);
}

document.getElementById('erpNfeXmlInput')?.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const parser = new DOMParser();
      const xml = parser.parseFromString(evt.target.result, "application/xml");
      const getVal = (tag) => xml.getElementsByTagName(tag)[0]?.textContent?.trim() || '';

      if (getVal('nNF')) document.getElementById('erpNfeNumero').value = getVal('nNF');
      if (getVal('serie')) document.getElementById('erpNfeSerie').value = getVal('serie');
      if (getVal('vNF')) document.getElementById('erpNfeValorTotal').value = getVal('vNF');
      if (getVal('pesoB') || getVal('pesoL')) document.getElementById('erpPesoCarga').value = getVal('pesoB') || getVal('pesoL');
      if (getVal('NCM')) document.getElementById('erpNcmCarga').value = getVal('NCM').substring(0, 4);
      if (getVal('xProd')) document.getElementById('erpDescMercadoria').value = getVal('xProd');

      const dhEmi = getVal('dhEmi');
      if (dhEmi && dhEmi.length >= 16) document.getElementById('erpNfeDataEmissao').value = dhEmi.substring(0, 16);

      const emit = xml.getElementsByTagName('emit')[0];
      if (emit) {
        document.getElementById('erpNfeCnpjEmissor').value = emit.getElementsByTagName('CNPJ')[0]?.textContent || '';
        document.getElementById('erpIbgeOrigem').value = emit.getElementsByTagName('cMun')[0]?.textContent || '';
        document.getElementById('erpCepOrigem').value = emit.getElementsByTagName('CEP')[0]?.textContent || '';
      }

      const dest = xml.getElementsByTagName('dest')[0];
      if (dest) {
        document.getElementById('erpDestCnpj').value = dest.getElementsByTagName('CNPJ')[0]?.textContent || '';
        document.getElementById('erpDestRazao').value = dest.getElementsByTagName('xNome')[0]?.textContent || '';
        document.getElementById('erpDestRua').value = dest.getElementsByTagName('xLgr')[0]?.textContent || '';
        document.getElementById('erpDestNumero').value = dest.getElementsByTagName('nro')[0]?.textContent || 'SN';
        document.getElementById('erpDestBairro').value = dest.getElementsByTagName('xBairro')[0]?.textContent || '';
        document.getElementById('erpCepDestino').value = dest.getElementsByTagName('CEP')[0]?.textContent || '';
        document.getElementById('erpIbgeDestino').value = dest.getElementsByTagName('cMun')[0]?.textContent || '';
        document.getElementById('erpDestEmail').value = dest.getElementsByTagName('email')[0]?.textContent || '';
      }
      erpCalcularLiquido();
      alert('✅ NF-e carregada com sucesso!');
    } catch (err) {
      alert('Erro ao ler XML: ' + err.message);
    }
  };
  reader.readAsText(file);
});

function montarEnvelopeXmlERP() {
  erpCalcularLiquido();
  const peso = parseFloat(document.getElementById('erpPesoCarga').value) || 1;
  const vTotal = parseFloat(document.getElementById('erpNfeValorTotal').value) || 1;
  const vUnit = (vTotal / peso).toFixed(5);
  const vLiquido = parseFloat(document.getElementById('erpValorFreteLiquido').value) || 0;
  const vBruto = parseFloat(document.getElementById('erpValorFreteBruto').value) || 0;
  const dIni = document.getElementById('erpDataInicioViagem').value;
  const dFim = document.getElementById('erpDataFimViagem').value;
  const dNfe = document.getElementById('erpNfeDataEmissao').value;
  const placa2 = document.getElementById('erpPlacaCarreta').value.trim();
  const extra = placa2 ? '\\n        <Veiculos><Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + placa2 + '</Placa></Veiculos>' : '';

  return `<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <AdicionarOperacaoTransporte xmlns="http://schemas.ipc.adm.br/efrete/pefV2">
      <AdicionarOperacaoTransporteRequest xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
        <Integrador xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpHashIntegrador').value}</Integrador>
        <Versao xmlns="http://schemas.ipc.adm.br/efrete/objects">8</Versao>
        
        <TipoViagem xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">Padrao</TipoViagem>
        <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">${document.getElementById('erpTipoPagamento').value}</TipoPagamento>

        <MatrizCNPJ>${document.getElementById('erpCnpjMatriz').value}</MatrizCNPJ>
        <FilialCNPJ>${document.getElementById('erpCnpjMatriz').value}</FilialCNPJ>
        <IdOperacaoCliente>${document.getElementById('erpIdOperacao').value}</IdOperacaoCliente>

        <DataInicioViagem>${dIni}:00.000Z</DataInicioViagem>
        <DataFimViagem>${dFim}:00.000Z</DataFimViagem>
        <CodigoNCMNaturezaCarga>${document.getElementById('erpNcmCarga').value}</CodigoNCMNaturezaCarga>
        <PesoCarga>${peso.toFixed(5)}</PesoCarga>
        <TipoEmbalagem>${document.getElementById('erpTipoEmbalagem').value}</TipoEmbalagem>
        <CodigoTipoCarga>1</CodigoTipoCarga>
        <AltoDesempenho>false</AltoDesempenho>

        <Viagens>
          <DocumentoViagem>${document.getElementById('erpNfeNumero').value}</DocumentoViagem>
          <CodigoMunicipioOrigem>${document.getElementById('erpIbgeOrigem').value}</CodigoMunicipioOrigem>
          <CodigoMunicipioDestino>${document.getElementById('erpIbgeDestino').value}</CodigoMunicipioDestino>
          <CepOrigem>${document.getElementById('erpCepOrigem').value}</CepOrigem>
          <CepDestino>${document.getElementById('erpCepDestino').value}</CepDestino>
          <DistanciaPercorrida>${document.getElementById('erpDistanciaKm').value}</DistanciaPercorrida>
          
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
          
          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${document.getElementById('erpTipoPagamento').value}</TipoPagamento>
          
          <NotasFiscais>
            <NotaFiscal>
              <Numero xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('erpNfeNumero').value}</Numero>
              <Serie xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('erpNfeSerie').value}</Serie>
              <Data xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${dNfe}:00.000Z</Data>
              <ValorTotal xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${vTotal.toFixed(2)}</ValorTotal>
              <ValorDaMercadoriaPorUnidade xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${vUnit}</ValorDaMercadoriaPorUnidade>
              <CodigoNCMNaturezaCarga xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('erpNcmCarga').value}</CodigoNCMNaturezaCarga>
              <DescricaoDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('erpDescMercadoria').value}</DescricaoDaMercadoria>
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
          <IRRF xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('erpImpostoIrrf').value).toFixed(5)}</IRRF>
          <SestSenat xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('erpImpostoSest').value).toFixed(5)}</SestSenat>
          <INSS xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${parseFloat(document.getElementById('erpImpostoInss').value).toFixed(5)}</INSS>
          <ISSQN xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</ISSQN>
          <OutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</OutrosImpostos>
          <DescricaoOutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects"></DescricaoOutrosImpostos>
        </Impostos>

        <Pagamentos>
          <IdPagamentoCliente>PAG-${document.getElementById('erpIdOperacao').value}-1</IdPagamentoCliente>
          <DataDeLiberacao>${dFim}:00.000Z</DataDeLiberacao>
          <Valor>${vLiquido.toFixed(5)}</Valor>
          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">${document.getElementById('erpTipoPagamento').value}</TipoPagamento>
          <Categoria xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">Quitacao</Categoria>
          <Documento>${document.getElementById('erpNfeNumero').value}</Documento>
          <CpfCnpjCreditado>${document.getElementById('erpCnpjContratante').value}</CpfCnpjCreditado>
          <IndicadorPagamento>AVista</IndicadorPagamento>
          <InformacoesBancarias xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">
            <InstituicaoBancaria>${document.getElementById('erpBancoNum').value}</InstituicaoBancaria>
            <Agencia>${document.getElementById('erpBancoAgencia').value}</Agencia>
            <Conta>${document.getElementById('erpBancoConta').value}</Conta>
            <TipoConta>${document.getElementById('erpTipoConta').value}</TipoConta>
          </InformacoesBancarias>
        </Pagamentos>

        <Contratado>
          <CpfOuCnpj>${document.getElementById('erpCnpjContratado').value}</CpfOuCnpj>
          <RNTRC>${document.getElementById('erpRntrcContratado').value}</RNTRC>
        </Contratado>

        <Motorista>
          <CpfOuCnpj>${document.getElementById('erpCpfMotorista').value}</CpfOuCnpj>
          <CNH>${document.getElementById('erpCnhMotorista').value}</CNH>
          <Celular xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
            <DDD xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpDddMotorista').value}</DDD>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpTelMotorista').value}</Numero>
          </Celular>
        </Motorista>

        <Destinatario xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('erpDestRazao').value}</NomeOuRazaoSocial>
          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('erpDestCnpj').value}</CpfOuCnpj>
          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpDestBairro').value}</Bairro>
            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpDestRua').value}</Rua>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpDestNumero').value}</Numero>
            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>
            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpCepDestino').value}</CEP>
            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpIbgeDestino').value}</CodigoMunicipio>
          </Endereco>
          <EMail xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('erpDestEmail').value}</EMail>
          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">false</ResponsavelPeloPagamento>
        </Destinatario>

        <Contratante xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">
          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('erpRazaoContratante').value}</NomeOuRazaoSocial>
          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">${document.getElementById('erpCnpjContratante').value}</CpfOuCnpj>
          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">
            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">ITAPIRU</Bairro>
            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpRuaContratante').value}</Rua>
            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpNumContratante').value}</Numero>
            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>
            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpCepContratante').value}</CEP>
            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">${document.getElementById('erpMunContratante').value}</CodigoMunicipio>
          </Endereco>
          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">true</ResponsavelPeloPagamento>
          <RNTRC>${document.getElementById('erpRntrcContratante').value}</RNTRC>
        </Contratante>

        <Veiculos>
          <Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">${document.getElementById('erpPlacaCavalo').value}</Placa>
        </Veiculos>${extra}

        <ComposicaoVeicular>${document.getElementById('erpCompVeicular').value}</ComposicaoVeicular>
        <RetornoVazio>false</RetornoVazio>
      </AdicionarOperacaoTransporteRequest>
    </AdicionarOperacaoTransporte>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>`;
}

function erpTransferirParaEmissor() {
  const xml = montarEnvelopeXmlERP();
  const tx = document.querySelector('#envelopeXml, textarea[name="envelopeXml"], textarea');
  if (tx) tx.value = xml;
  const tabEmissao = document.querySelector('button[data-bs-target="#tab-emissao"], #emissao-tab, button[data-bs-target*="emissao"]');
  if (tabEmissao) tabEmissao.click();
  alert('🚀 XML V8 gerado e injetado no Transmissor!');
}

function erpCopiarXml() {
  const xml = montarEnvelopeXmlERP();
  navigator.clipboard.writeText(xml).then(() => alert('📋 XML copiado com sucesso!'));
}

function preencherPadraoEliferERP() {
  document.getElementById('erpCnpjMatriz').value = '11722820000103';
  document.getElementById('erpCnpjContratante').value = '11722820000103';
  document.getElementById('erpRntrcContratante').value = '49919644';
  document.getElementById('erpCnpjContratado').value = '11722820000103';
  document.getElementById('erpRntrcContratado').value = '49919644';
  document.getElementById('erpCpfMotorista').value = '60937378291';
  document.getElementById('erpCnhMotorista').value = '1466825624';
  document.getElementById('erpPlacaCavalo').value = 'GXS4F23';
  document.getElementById('erpPlacaCarreta').value = 'ADN8I23';
}

function limparCamposERP() {
  if (confirm('Limpar todos os campos?')) {
    document.querySelectorAll('#tab-erp input').forEach(i => { if (i.type !== 'button' && i.type !== 'file') i.value = ''; });
  }
}
</script>
'''

if "tab-erp" in content:
    print("A aba ERP já está presente no arquivo.")
else:
    # Insere o botão da aba no primeiro nav-item encontrado
    content = content.replace(nav_marker, new_nav_btn + "\n        " + nav_marker, 1)
    
    # Insere a aba antes do fechamento do tab-content
    if '</div><!-- /tab-content -->' in content:
        content = content.replace('</div><!-- /tab-content -->', erp_html_tab + '\n      </div><!-- /tab-content -->')
    elif '</div>\n  </div>' in content:
        content = content.replace('</div>\n  </div>', erp_html_tab + '\n    </div>\n  </div>', 1)
    else:
        content = content.replace('</body>', erp_html_tab + '\n</body>')

    # Insere o script JS antes do </body>
    content = content.replace('</body>', erp_js + '\n</body>')

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sucesso! Aba ERP integrada ao {target_file}.")
