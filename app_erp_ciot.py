import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>A3 Soft | Painel ERP Emissor CIOT (e-Frete V8)</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f1f4f8; font-size: 0.88rem; }
    .card { border-radius: 8px; border: 1px solid #dcdfe4; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .card-header { font-weight: 700; background-color: #ffffff; border-bottom: 1px solid #e2e5e9; color: #1e3a8a; }
    .form-label { font-weight: 600; font-size: 0.8rem; color: #374151; margin-bottom: 2px; }
    .form-control, .form-select { font-size: 0.84rem; padding: 0.35rem 0.55rem; }
    .section-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #6b7280; margin-bottom: 6px; }
    pre { background: #111827; color: #34d399; padding: 14px; border-radius: 6px; max-height: 420px; font-size: 0.8rem; overflow: auto; }
  </style>
</head>
<body class="p-3">
  <div class="container-fluid" style="max-width: 1300px;">
    
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <h4 class="m-0 text-primary fw-bold">🚛 A3 Soft | Gerador ERP de CIOT (e-Frete V8 / Lotação)</h4>
        <small class="text-muted">Preenchimento manual assistido com suporte à importação de XML de NF-e</small>
      </div>
      <span class="badge bg-success p-2">Layout Homologado V8</span>
    </div>

    <!-- CARREGADOR DE XML DE NF-E OPCIONAL -->
    <div class="card bg-white border-primary mb-3">
      <div class="card-body p-2 d-flex flex-wrap align-items-center justify-content-between gap-2">
        <div class="d-flex align-items-center gap-2">
          <label class="form-label m-0 text-primary">📄 Importar XML da NF-e (Opcional):</label>
          <input type="file" id="nfeXmlInput" accept=".xml" class="form-control form-control-sm" style="max-width: 320px;">
        </div>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-sm btn-outline-secondary" onclick="preencherPadraoElifer()">⚡ Repor Dados Padrão (Elifer)</button>
          <button type="button" class="btn btn-sm btn-outline-danger" onclick="limparTudo()">🗑️ Limpar Campos</button>
        </div>
      </div>
    </div>

    <form id="erpForm">
      <!-- 1. IDENTIFICAÇÃO E INTEGRADOR -->
      <div class="card">
        <div class="card-header">🏢 1. Configuração do Emissor e Integração</div>
        <div class="card-body">
          <div class="row g-2">
            <div class="col-md-4">
              <label class="form-label">Hash Integrador A3 Soft:*</label>
              <input type="text" id="hashIntegrador" class="form-control" value="58e47cd2-8b54-4542-ba22-6941810dd7fa" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">CNPJ Matriz / Filial (Elifer):*</label>
              <input type="text" id="cnpjMatriz" class="form-control" value="11722820000103" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">ID Único da Operação no ERP:*</label>
              <input type="text" id="idOperacaoCliente" class="form-control" value="560000549800" required>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- 2. CONTRATANTE E TRANSPORTADOR EXECUTOR -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">🤝 2. Contratante e Transportador Contratado</div>
            <div class="card-body">
              <div class="section-title">Contratante (Responsável pelo Pagamento)</div>
              <div class="row g-2 mb-3">
                <div class="col-md-6">
                  <label class="form-label">CNPJ/CPF Contratante:*</label>
                  <input type="text" id="cnpjContratante" class="form-control" value="11722820000103" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">RNTRC Contratante:*</label>
                  <input type="text" id="rntrcContratante" class="form-control" value="49919644" required>
                </div>
                <div class="col-md-12">
                  <label class="form-label">Razão Social Contratante:*</label>
                  <input type="text" id="razaoContratante" class="form-control" value="ELIFER COMERCIO DE SUCATAS E RESIDUOS TRANSPORTES E SERVICOS" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">CEP:*</label>
                  <input type="text" id="cepContratante" class="form-control" value="13400970" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Cód. IBGE Município:*</label>
                  <input type="text" id="munContratante" class="form-control" value="3538709" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Número:*</label>
                  <input type="text" id="numContratante" class="form-control" value="SN" required>
                </div>
                <div class="col-md-12">
                  <label class="form-label">Logradouro / Rua:*</label>
                  <input type="text" id="ruaContratante" class="form-control" value="ROD SP 304, KM 172 5" required>
                </div>
              </div>

              <div class="section-title">Contratado (Proprietário / Executor)</div>
              <div class="row g-2">
                <div class="col-md-6">
                  <label class="form-label">CNPJ/CPF Contratado:*</label>
                  <input type="text" id="cnpjContratado" class="form-control" value="11722820000103" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">RNTRC Contratado:*</label>
                  <input type="text" id="rntrcContratado" class="form-control" value="49919644" required>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. MOTORISTA E VEÍCULOS -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">🚚 3. Motorista Condutor & Frota</div>
            <div class="card-body">
              <div class="section-title">Dados do Condutor</div>
              <div class="row g-2 mb-3">
                <div class="col-md-6">
                  <label class="form-label">CPF Motorista (11 dígitos):*</label>
                  <input type="text" id="cpfMotorista" class="form-control" value="60937378291" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">CNH do Motorista:*</label>
                  <input type="text" id="cnhMotorista" class="form-control" value="1466825624" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">DDD:*</label>
                  <input type="text" id="dddMotorista" class="form-control" value="19" required>
                </div>
                <div class="col-md-9">
                  <label class="form-label">Telemóvel Motorista:*</label>
                  <input type="text" id="telMotorista" class="form-control" value="974098553" required>
                </div>
              </div>

              <div class="section-title">Veículos da Viagem</div>
              <div class="row g-2">
                <div class="col-md-4">
                  <label class="form-label">Placa Trator (Cavalo):*</label>
                  <input type="text" id="placaCavalo" class="form-control" value="GXS4F23" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Placa Reboque (Carreta):</label>
                  <input type="text" id="placaCarreta" class="form-control" value="ADN8I23">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Composição Veicular:*</label>
                  <select id="compVeicular" class="form-select">
                    <option value="true" selected>Sim (Conjunto)</option>
                    <option value="false">Não (Veículo Único)</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. VIAGEM E DOCUMENTO FISCAL (NF-E) -->
      <div class="card">
        <div class="card-header">📦 4. Viagem, Rota e Nota Fiscal Originária</div>
        <div class="card-body">
          <div class="row g-2 mb-3">
            <div class="col-md-3">
              <label class="form-label">Início Previsto Viagem:*</label>
              <input type="datetime-local" id="dataInicioViagem" class="form-control" value="2026-09-30T14:00" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">Fim Previsto Viagem:*</label>
              <input type="datetime-local" id="dataFimViagem" class="form-control" value="2026-10-01T18:00" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Distância Percorrida (Km):*</label>
              <input type="number" id="distanciaKm" class="form-control" value="45" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">NCM Predominante:*</label>
              <input type="text" id="ncmCarga" class="form-control" value="3402" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Tipo Embalagem:*</label>
              <select id="tipoEmbalagem" class="form-select">
                <option value="Caixa" selected>Caixa</option>
                <option value="Palete">Palete</option>
                <option value="Granel">Granel</option>
                <option value="Unitario">Unitário</option>
              </select>
            </div>
          </div>

          <div class="section-title">Dados da Nota Fiscal Originária</div>
          <div class="row g-2">
            <div class="col-md-2">
              <label class="form-label">Número NF-e:*</label>
              <input type="text" id="nfeNumero" class="form-control" value="15584" required>
            </div>
            <div class="col-md-1">
              <label class="form-label">Série:*</label>
              <input type="text" id="nfeSerie" class="form-control" value="0" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">CNPJ Emissor da NF-e:*</label>
              <input type="text" id="nfeCnpjEmissor" class="form-control" value="60881299000839" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Data Emissão NF-e:*</label>
              <input type="datetime-local" id="nfeDataEmissao" class="form-control" value="2026-08-31T20:23" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Peso da Carga (Kg):*</label>
              <input type="number" step="0.001" id="pesoCarga" class="form-control" value="2625.200" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Valor Total NF-e (R$):*</label>
              <input type="number" step="0.01" id="nfeValorTotal" class="form-control" value="154585.18" required>
            </div>
            <div class="col-md-12">
              <label class="form-label">Descrição das Mercadorias:*</label>
              <input type="text" id="descMercadoria" class="form-control" value="ESSENCIAS E PRODUTOS DE LIMPEZA COALA" required>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. DESTINATÁRIO -->
      <div class="card">
        <div class="card-header">📍 5. Destinatário da Carga (Endereço Completo Obrigatório)</div>
        <div class="card-body">
          <div class="row g-2">
            <div class="col-md-4">
              <label class="form-label">CNPJ/CPF Destinatário:*</label>
              <input type="text" id="destCnpj" class="form-control" value="23637077001659" required>
            </div>
            <div class="col-md-8">
              <label class="form-label">Razão Social Destinatário:*</label>
              <input type="text" id="destRazao" class="form-control" value="P.SEVERINI NETO COMERCIAL LTDA" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Logradouro / Rodovia:*</label>
              <input type="text" id="destRua" class="form-control" value="RODOVIA RODOVIA DOM PEDRO I" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Número / KM:*</label>
              <input type="text" id="destNumero" class="form-control" value="SN" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">Bairro:*</label>
              <input type="text" id="destBairro" class="form-control" value="COLONIA FAZENDA SANTA ELISA" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">CEP Destino:*</label>
              <input type="text" id="cepDestino" class="form-control" value="13069300" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">Cód. IBGE Destino:*</label>
              <input type="text" id="ibgeDestino" class="form-control" value="3509502" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">CEP Origem (Coleta):*</label>
              <input type="text" id="cepOrigem" class="form-control" value="13474789" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">Cód. IBGE Origem (Coleta):*</label>
              <input type="text" id="ibgeOrigem" class="form-control" value="3501608" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">E-mail Destinatário:</label>
              <input type="email" id="destEmail" class="form-control" value="munique.sances@vilanova.com.br">
            </div>
          </div>
        </div>
      </div>

      <!-- 6. VALORES, RETENÇÕES E PAGAMENTO -->
      <div class="card">
        <div class="card-header">💰 6. Valores do Frete, Retenções Tributárias e Dados Bancários</div>
        <div class="card-body">
          <div class="row g-2 mb-3">
            <div class="col-md-3">
              <label class="form-label">Valor Bruto do Frete (R$):*</label>
              <input type="number" step="0.01" id="valorFreteBruto" class="form-control" value="3850.00" oninput="calcularLiquido()" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">IRRF Retido (R$):</label>
              <input type="number" step="0.01" id="impostoIrrf" class="form-control" value="0.00" oninput="calcularLiquido()">
            </div>
            <div class="col-md-2">
              <label class="form-label">INSS Retido (R$):</label>
              <input type="number" step="0.01" id="impostoInss" class="form-control" value="0.00" oninput="calcularLiquido()">
            </div>
            <div class="col-md-2">
              <label class="form-label">SEST/SENAT (R$):</label>
              <input type="number" step="0.01" id="impostoSest" class="form-control" value="0.00" oninput="calcularLiquido()">
            </div>
            <div class="col-md-3">
              <label class="form-label fw-bold text-success">Valor Líquido a Pagar (R$):*</label>
              <input type="number" step="0.01" id="valorFreteLiquido" class="form-control bg-light fw-bold" value="3850.00" readonly>
            </div>
          </div>

          <div class="section-title">Dados do Depósito / Transferência Bancária</div>
          <div class="row g-2">
            <div class="col-md-3">
              <label class="form-label">Meio de Pagamento:*</label>
              <select id="tipoPagamento" class="form-select">
                <option value="TransferenciaBancaria" selected>Transferência Bancária</option>
                <option value="eFRETE">Saldo Conta e-Frete</option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label">Código Banco (COMPE):*</label>
              <input type="text" id="bancoNum" class="form-control" value="237" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Agência (com dígito):*</label>
              <input type="text" id="bancoAgencia" class="form-control" value="2825" required>
            </div>
            <div class="col-md-2">
              <label class="form-label">Conta (com dígito):*</label>
              <input type="text" id="bancoConta" class="form-control" value="29856-8" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">Tipo de Conta:*</label>
              <select id="tipoConta" class="form-select">
                <option value="ContaCorrente" selected>Conta Corrente</option>
                <option value="ContaPoupanca">Conta Poupança</option>
                <option value="ContaPagamento">Conta Pagamento</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- BOTÕES DE AÇÃO -->
      <div class="d-flex gap-2 justify-content-end mb-4">
        <button type="button" class="btn btn-outline-primary px-4 fw-bold" onclick="gerarXml()">⚙️ Gerar Arquivo XML SOAP</button>
        <button type="button" class="btn btn-success px-4 fw-bold" onclick="copiarXml()">📋 Copiar XML para Área de Transferência</button>
      </div>
    </form>

    <!-- ÁREA DE VISUALIZAÇÃO DO XML GERADO -->
    <div class="card">
      <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
        <span>📄 XML SOAP V8 Oficial Pronto para Envio</span>
        <span class="badge bg-secondary" id="xmlStatusBadge">Aguardando geração</span>
      </div>
      <div class="card-body p-2">
        <textarea id="xmlResultArea" class="form-control font-monospace" style="height: 380px; font-size: 0.82rem; background: #0f172a; color: #10b981;" placeholder="O XML gerado aparecerá aqui..."></textarea>
      </div>
    </div>
  </div>

  <script>
    function calcularLiquido() {
      const bruto = parseFloat(document.getElementById('valorFreteBruto').value) || 0;
      const irrf = parseFloat(document.getElementById('impostoIrrf').value) || 0;
      const inss = parseFloat(document.getElementById('impostoInss').value) || 0;
      const sest = parseFloat(document.getElementById('impostoSest').value) || 0;
      const liquido = Math.max(0, bruto - (irrf + inss + sest));
      document.getElementById('valorFreteLiquido').value = liquido.toFixed(2);
    }

    // Leitor de XML de NF-e
    document.getElementById('nfeXmlInput').addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(evt) {
        try {
          const parser = new DOMParser();
          const xml = parser.parseFromString(evt.target.result, "application/xml");
          const getVal = (tag) => {
            const el = xml.getElementsByTagName(tag)[0];
            return el ? el.textContent.trim() : '';
          };

          if (getVal('nNF')) document.getElementById('nfeNumero').value = getVal('nNF');
          if (getVal('serie')) document.getElementById('nfeSerie').value = getVal('serie');
          if (getVal('vNF')) document.getElementById('nfeValorTotal').value = getVal('vNF');
          if (getVal('pesoB') || getVal('pesoL')) document.getElementById('pesoCarga').value = getVal('pesoB') || getVal('pesoL');
          if (getVal('NCM')) document.getElementById('ncmCarga').value = getVal('NCM').substring(0, 4);
          if (getVal('xProd')) document.getElementById('descMercadoria').value = getVal('xProd');

          const dhEmi = getVal('dhEmi');
          if (dhEmi && dhEmi.length >= 16) document.getElementById('nfeDataEmissao').value = dhEmi.substring(0, 16);

          const emit = xml.getElementsByTagName('emit')[0];
          if (emit) {
            document.getElementById('nfeCnpjEmissor').value = emit.getElementsByTagName('CNPJ')[0]?.textContent || '';
            document.getElementById('ibgeOrigem').value = emit.getElementsByTagName('cMun')[0]?.textContent || '';
            document.getElementById('cepOrigem').value = emit.getElementsByTagName('CEP')[0]?.textContent || '';
          }

          const dest = xml.getElementsByTagName('dest')[0];
          if (dest) {
            document.getElementById('destCnpj').value = dest.getElementsByTagName('CNPJ')[0]?.textContent || '';
            document.getElementById('destRazao').value = dest.getElementsByTagName('xNome')[0]?.textContent || '';
            document.getElementById('destRua').value = dest.getElementsByTagName('xLgr')[0]?.textContent || '';
            document.getElementById('destNumero').value = dest.getElementsByTagName('nro')[0]?.textContent || 'SN';
            document.getElementById('destBairro').value = dest.getElementsByTagName('xBairro')[0]?.textContent || '';
            document.getElementById('cepDestino').value = dest.getElementsByTagName('CEP')[0]?.textContent || '';
            document.getElementById('ibgeDestino').value = dest.getElementsByTagName('cMun')[0]?.textContent || '';
            document.getElementById('destEmail').value = dest.getElementsByTagName('email')[0]?.textContent || '';
          }

          calcularLiquido();
          gerarXml();
          alert('✅ Dados da NF-e ' + document.getElementById('nfeNumero').value + ' carregados com sucesso no formulário!');
        } catch (err) {
          alert('Falha ao processar arquivo XML: ' + err.message);
        }
      };
      reader.readAsText(file);
    });

    function gerarXml() {
      calcularLiquido();

      const peso = parseFloat(document.getElementById('pesoCarga').value) || 1;
      const vTotal = parseFloat(document.getElementById('nfeValorTotal').value) || 1;
      const vUnit = (vTotal / peso).toFixed(5);
      const vLiquido = parseFloat(document.getElementById('valorFreteLiquido').value) || 0;
      const vBruto = parseFloat(document.getElementById('valorFreteBruto').value) || 0;

      const dIni = document.getElementById('dataInicioViagem').value;
      const dFim = document.getElementById('dataFimViagem').value;
      const dNfe = document.getElementById('nfeDataEmissao').value;

      const placa2 = document.getElementById('placaCarreta').value.trim();
      let veiculoExtra = '';
      if (placa2) {
        veiculoExtra = '\n        <Veiculos><Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + placa2 + '</Placa></Veiculos>';
      }

      const xml = '<?xml version="1.0" encoding="utf-8"?>\n' +
'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" \n' +
'                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" \n' +
'                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n' +
'  <SOAP-ENV:Body>\n' +
'    <AdicionarOperacaoTransporte xmlns="http://schemas.ipc.adm.br/efrete/pefV2">\n' +
'      <AdicionarOperacaoTransporteRequest xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'        <Integrador xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('hashIntegrador').value + '</Integrador>\n' +
'        <Versao xmlns="http://schemas.ipc.adm.br/efrete/objects">8</Versao>\n' +
'        \n' +
'        <TipoViagem xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">Padrao</TipoViagem>\n' +
'        <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">' + document.getElementById('tipoPagamento').value + '</TipoPagamento>\n' +
'\n' +
'        <MatrizCNPJ>' + document.getElementById('cnpjMatriz').value + '</MatrizCNPJ>\n' +
'        <FilialCNPJ>' + document.getElementById('cnpjMatriz').value + '</FilialCNPJ>\n' +
'        <IdOperacaoCliente>' + document.getElementById('idOperacaoCliente').value + '</IdOperacaoCliente>\n' +
'\n' +
'        <DataInicioViagem>' + dIni + ':00.000Z</DataInicioViagem>\n' +
'        <DataFimViagem>' + dFim + ':00.000Z</DataFimViagem>\n' +
'        <CodigoNCMNaturezaCarga>' + document.getElementById('ncmCarga').value + '</CodigoNCMNaturezaCarga>\n' +
'        <PesoCarga>' + peso.toFixed(5) + '</PesoCarga>\n' +
'        <TipoEmbalagem>' + document.getElementById('tipoEmbalagem').value + '</TipoEmbalagem>\n' +
'        <CodigoTipoCarga>1</CodigoTipoCarga>\n' +
'        <AltoDesempenho>false</AltoDesempenho>\n' +
'\n' +
'        <Viagens>\n' +
'          <DocumentoViagem>' + document.getElementById('nfeNumero').value + '</DocumentoViagem>\n' +
'          <CodigoMunicipioOrigem>' + document.getElementById('ibgeOrigem').value + '</CodigoMunicipioOrigem>\n' +
'          <CodigoMunicipioDestino>' + document.getElementById('ibgeDestino').value + '</CodigoMunicipioDestino>\n' +
'          <CepOrigem>' + document.getElementById('cepOrigem').value + '</CepOrigem>\n' +
'          <CepDestino>' + document.getElementById('cepDestino').value + '</CepDestino>\n' +
'          <DistanciaPercorrida>' + document.getElementById('distanciaKm').value + '</DistanciaPercorrida>\n' +
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
'          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + document.getElementById('tipoPagamento').value + '</TipoPagamento>\n' +
'          \n' +
'          <NotasFiscais>\n' +
'            <NotaFiscal>\n' +
'              <Numero xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('nfeNumero').value + '</Numero>\n' +
'              <Serie xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('nfeSerie').value + '</Serie>\n' +
'              <Data xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + dNfe + ':00.000Z</Data>\n' +
'              <ValorTotal xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + vTotal.toFixed(2) + '</ValorTotal>\n' +
'              <ValorDaMercadoriaPorUnidade xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + vUnit + '</ValorDaMercadoriaPorUnidade>\n' +
'              <CodigoNCMNaturezaCarga xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('ncmCarga').value + '</CodigoNCMNaturezaCarga>\n' +
'              <DescricaoDaMercadoria xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('descMercadoria').value + '</DescricaoDaMercadoria>\n' +
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
'          <IRRF xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('impostoIrrf').value).toFixed(5) + '</IRRF>\n' +
'          <SestSenat xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('impostoSest').value).toFixed(5) + '</SestSenat>\n' +
'          <INSS xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + parseFloat(document.getElementById('impostoInss').value).toFixed(5) + '</INSS>\n' +
'          <ISSQN xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</ISSQN>\n' +
'          <OutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">0.00000</OutrosImpostos>\n' +
'          <DescricaoOutrosImpostos xmlns="http://schemas.ipc.adm.br/efrete/pef/objects"></DescricaoOutrosImpostos>\n' +
'        </Impostos>\n' +
'\n' +
'        <Pagamentos>\n' +
'          <IdPagamentoCliente>PAG-' + document.getElementById('idOperacaoCliente').value + '-1</IdPagamentoCliente>\n' +
'          <DataDeLiberacao>' + dFim + ':00.000Z</DataDeLiberacao>\n' +
'          <Valor>' + vLiquido.toFixed(5) + '</Valor>\n' +
'          <TipoPagamento xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">' + document.getElementById('tipoPagamento').value + '</TipoPagamento>\n' +
'          <Categoria xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">Quitacao</Categoria>\n' +
'          <Documento>' + document.getElementById('nfeNumero').value + '</Documento>\n' +
'          <CpfCnpjCreditado>' + document.getElementById('cnpjContratante').value + '</CpfCnpjCreditado>\n' +
'          <IndicadorPagamento>AVista</IndicadorPagamento>\n' +
'          <InformacoesBancarias xmlns="http://schemas.ipc.adm.br/efrete/pef/objects">\n' +
'            <InstituicaoBancaria>' + document.getElementById('bancoNum').value + '</InstituicaoBancaria>\n' +
'            <Agencia>' + document.getElementById('bancoAgencia').value + '</Agencia>\n' +
'            <Conta>' + document.getElementById('bancoConta').value + '</Conta>\n' +
'            <TipoConta>' + document.getElementById('tipoConta').value + '</TipoConta>\n' +
'          </InformacoesBancarias>\n' +
'        </Pagamentos>\n' +
'\n' +
'        <Contratado>\n' +
'          <CpfOuCnpj>' + document.getElementById('cnpjContratado').value + '</CpfOuCnpj>\n' +
'          <RNTRC>' + document.getElementById('rntrcContratado').value + '</RNTRC>\n' +
'        </Contratado>\n' +
'\n' +
'        <Motorista>\n' +
'          <CpfOuCnpj>' + document.getElementById('cpfMotorista').value + '</CpfOuCnpj>\n' +
'          <CNH>' + document.getElementById('cnhMotorista').value + '</CNH>\n' +
'          <Celular xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'            <DDD xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('dddMotorista').value + '</DDD>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('telMotorista').value + '</Numero>\n' +
'          </Celular>\n' +
'        </Motorista>\n' +
'\n' +
'        <Destinatario xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('destRazao').value + '</NomeOuRazaoSocial>\n' +
'          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('destCnpj').value + '</CpfOuCnpj>\n' +
'          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('destBairro').value + '</Bairro>\n' +
'            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('destRua').value + '</Rua>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('destNumero').value + '</Numero>\n' +
'            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>\n' +
'            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cepDestino').value + '</CEP>\n' +
'            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('ibgeDestino').value + '</CodigoMunicipio>\n' +
'          </Endereco>\n' +
'          <EMail xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('destEmail').value + '</EMail>\n' +
'          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">false</ResponsavelPeloPagamento>\n' +
'        </Destinatario>\n' +
'\n' +
'        <Contratante xmlns="http://schemas.ipc.adm.br/efrete/pefV2/objects">\n' +
'          <NomeOuRazaoSocial xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('razaoContratante').value + '</NomeOuRazaoSocial>\n' +
'          <CpfOuCnpj xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">' + document.getElementById('cnpjContratante').value + '</CpfOuCnpj>\n' +
'          <Endereco xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">\n' +
'            <Bairro xmlns="http://schemas.ipc.adm.br/efrete/objects">ITAPIRU</Bairro>\n' +
'            <Rua xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('ruaContratante').value + '</Rua>\n' +
'            <Numero xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('numContratante').value + '</Numero>\n' +
'            <Complemento xmlns="http://schemas.ipc.adm.br/efrete/objects"></Complemento>\n' +
'            <CEP xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('cepContratante').value + '</CEP>\n' +
'            <CodigoMunicipio xmlns="http://schemas.ipc.adm.br/efrete/objects">' + document.getElementById('munContratante').value + '</CodigoMunicipio>\n' +
'          </Endereco>\n' +
'          <ResponsavelPeloPagamento xmlns="http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte">true</ResponsavelPeloPagamento>\n' +
'          <RNTRC>' + document.getElementById('rntrcContratante').value + '</RNTRC>\n' +
'        </Contratante>\n' +
'\n' +
'        <Veiculos>\n' +
'          <Placa xmlns="http://schemas.ipc.adm.br/efrete/pef/AdicionarOperacaoTransporte">' + document.getElementById('placaCavalo').value + '</Placa>\n' +
'        </Veiculos>' + veiculoExtra + '\n' +
'\n' +
'        <ComposicaoVeicular>' + document.getElementById('compVeicular').value + '</ComposicaoVeicular>\n' +
'        <RetornoVazio>false</RetornoVazio>\n' +
'      </AdicionarOperacaoTransporteRequest>\n' +
'    </AdicionarOperacaoTransporte>\n' +
'  </SOAP-ENV:Body>\n' +
'</SOAP-ENV:Envelope>';

      document.getElementById('xmlResultArea').value = xml;
      document.getElementById('xmlStatusBadge').className = 'badge bg-success';
      document.getElementById('xmlStatusBadge').textContent = 'XML V8 Gerado com Sucesso!';
    }

    function copiarXml() {
      const ta = document.getElementById('xmlResultArea');
      if (!ta.value) gerarXml();
      ta.select();
      document.execCommand('copy');
      alert('📋 XML copiado para a Área de Transferência com sucesso!');
    }

    function preencherPadraoElifer() {
      document.getElementById('cnpjMatriz').value = '11722820000103';
      document.getElementById('cnpjContratante').value = '11722820000103';
      document.getElementById('rntrcContratante').value = '49919644';
      document.getElementById('cnpjContratado').value = '11722820000103';
      document.getElementById('rntrcContratado').value = '49919644';
      document.getElementById('cpfMotorista').value = '60937378291';
      document.getElementById('cnhMotorista').value = '1466825624';
      document.getElementById('placaCavalo').value = 'GXS4F23';
      document.getElementById('placaCarreta').value = 'ADN8I23';
      gerarXml();
    }

    function limparTudo() {
      if (confirm('Deseja limpar todos os campos do formulário?')) {
        document.getElementById('erpForm').reset();
        document.getElementById('xmlResultArea').value = '';
      }
    }

    // Inicializa a geração no carregamento da página
    window.onload = function() {
      gerarXml();
    };
  </script>
</body>
</html>
"""

class SimpleERPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

def run():
    port = 8080
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleERPHandler)
    url = f"http://localhost:{port}"
    print(f"\n========================================================")
    print(f"🚀 PAINEL ERP EMISSOR DE CIOT INICIADO COM SUCESSO!")
    print(f"🌐 Abra no seu navegador: {url}")
    print(f"========================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo utilizador.")
        httpd.server_close()

if __name__ == "__main__":
    run()