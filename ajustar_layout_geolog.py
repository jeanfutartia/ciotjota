import os
import re

ficheiro = os.path.join("templates", "index.html")

if not os.path.exists(ficheiro):
    print("Ficheiro templates/index.html não encontrado.")
    exit(1)

with open(ficheiro, "r", encoding="utf-8") as f:
    html = f.read()

# Novo layout moderno, alinhado em colunas (lado a lado) e com campos vazios por padrão
layout_limpo_grid = """
      <!-- FORMULÁRIO ERP COMPLETO EM GRELHA (GEOLOG CIOT V8) -->
      <style>
        .g-section { background: #0b1120; border: 1px solid #1e293b; border-radius: 8px; margin-bottom: 14px; padding: 14px; }
        .g-title { font-size: 0.85rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
        .g-grid { display: grid; gap: 10px; }
        .g-grid-2 { grid-template-columns: repeat(2, 1fr); }
        .g-grid-3 { grid-template-columns: repeat(3, 1fr); }
        .g-grid-4 { grid-template-columns: repeat(4, 1fr); }
        .g-grid-6 { grid-template-columns: repeat(6, 1fr); }
        .g-field { display: flex; flex-direction: column; gap: 3px; }
        .g-label { font-size: 0.76rem; font-weight: 600; color: #94a3b8; }
        .g-input { background: #1e293b; border: 1px solid #334155; color: #f8fafc; border-radius: 5px; padding: 5px 8px; font-size: 0.82rem; }
        .g-input:focus { border-color: #38bdf8; outline: none; }
        .g-subtitle { font-size: 0.74rem; font-weight: 700; color: #fbbf24; text-transform: uppercase; grid-column: 1 / -1; margin-top: 6px; }
      </style>

      <div class="card p-3 my-2" style="background:#060a12; border:1px solid #1e293b; border-radius:8px;">
        
        <!-- BARRA DE IMPORTAÇÃO E AÇÕES -->
        <div class="d-flex justify-content-between align-items-center mb-3 pb-2" style="border-bottom:1px solid #1e293b;">
          <h5 class="m-0 fw-bold" style="color:#00d2ff; font-size:1.05rem;">Construtor Passo a Passo de Operação de Transporte (e-Frete V8)</h5>
          <div class="d-flex align-items-center gap-2">
            <span class="small text-muted">Carregar XML NF-e:</span>
            <input type="file" id="cXmlNfe" accept=".xml" class="g-input" style="max-width:240px; padding:3px 6px;">
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="limparCamposConstrutor()">🗑️ Limpar</button>
          </div>
        </div>

        <!-- 1. CONFIGURAÇÃO EMISSOR -->
        <div class="g-section">
          <div class="g-title">🏢 1. Configuração do Emissor e Integração</div>
          <div class="g-grid g-grid-3">
            <div class="g-field">
              <label class="g-label">Hash Integrador:*</label>
              <input type="text" id="cHashIntegrador" class="g-input" value="58e47cd2-8b54-4542-ba22-6941810dd7fa" required>
            </div>
            <div class="g-field">
              <label class="g-label">CNPJ Matriz / Filial:*</label>
              <input type="text" id="cCnpjMatriz" class="g-input" placeholder="00000000000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">ID Operação no ERP:*</label>
              <input type="text" id="cIdOperacaoCliente" class="g-input" placeholder="Ex: 560000000001" required>
            </div>
          </div>
        </div>

        <!-- 2. CONTRATANTE E TRANSPORTADOR -->
        <div class="g-section">
          <div class="g-title">🤝 2. Contratante e Transportador Contratado</div>
          <div class="g-grid g-grid-4">
            <div class="g-subtitle">Contratante (Responsável pelo Pagamento)</div>
            <div class="g-field">
              <label class="g-label">CNPJ/CPF Contratante:*</label>
              <input type="text" id="cCnpjContratante" class="g-input" placeholder="00000000000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">RNTRC Contratante:*</label>
              <input type="text" id="cRntrcContratante" class="g-input" placeholder="00000000" required>
            </div>
            <div class="g-field" style="grid-column: span 2;">
              <label class="g-label">Razão Social Contratante:*</label>
              <input type="text" id="cRazaoContratante" class="g-input" placeholder="Nome empresarial" required>
            </div>
            <div class="g-field">
              <label class="g-label">CEP:*</label>
              <input type="text" id="cCepContratante" class="g-input" placeholder="00000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">Cód. IBGE Município:*</label>
              <input type="text" id="cMunContratante" class="g-input" placeholder="7 dígitos" required>
            </div>
            <div class="g-field">
              <label class="g-label">Número:*</label>
              <input type="text" id="cNumContratante" class="g-input" placeholder="Ex: 100 ou SN" required>
            </div>
            <div class="g-field">
              <label class="g-label">Logradouro / Rua:*</label>
              <input type="text" id="cRuaContratante" class="g-input" placeholder="Rua / Rodovia" required>
            </div>

            <div class="g-subtitle">Transportador Executor (Contratado)</div>
            <div class="g-field" style="grid-column: span 2;">
              <label class="g-label">CNPJ/CPF Contratado:*</label>
              <input type="text" id="cCnpjContratado" class="g-input" placeholder="00000000000000" required>
            </div>
            <div class="g-field" style="grid-column: span 2;">
              <label class="g-label">RNTRC Contratado:*</label>
              <input type="text" id="cRntrcContratado" class="g-input" placeholder="00000000" required>
            </div>
          </div>
        </div>

        <!-- 3. MOTORISTA E VEÍCULOS -->
        <div class="g-section">
          <div class="g-title">🚚 3. Motorista Condutor & Frota</div>
          <div class="g-grid g-grid-4">
            <div class="g-subtitle">Dados do Motorista</div>
            <div class="g-field">
              <label class="g-label">CPF Motorista (11 dígitos):*</label>
              <input type="text" id="cCpfMotorista" class="g-input" placeholder="00000000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">CNH do Motorista:*</label>
              <input type="text" id="cCnhMotorista" class="g-input" placeholder="Número CNH" required>
            </div>
            <div class="g-field">
              <label class="g-label">DDD:*</label>
              <input type="text" id="cDddMotorista" class="g-input" placeholder="Ex: 11" required>
            </div>
            <div class="g-field">
              <label class="g-label">Telemóvel:*</label>
              <input type="text" id="cTelMotorista" class="g-input" placeholder="Ex: 999999999" required>
            </div>

            <div class="g-subtitle">Veículos</div>
            <div class="g-field">
              <label class="g-label">Placa Cavalo (Trator):*</label>
              <input type="text" id="cPlacaCavalo" class="g-input" placeholder="ABC1D23" required>
            </div>
            <div class="g-field">
              <label class="g-label">Placa Carreta (Reboque):</label>
              <input type="text" id="cPlacaCarreta" class="g-input" placeholder="Opcional">
            </div>
            <div class="g-field" style="grid-column: span 2;">
              <label class="g-label">Composição Veicular:*</label>
              <select id="cCompVeicular" class="g-input">
                <option value="false">Não (Veículo Único)</option>
                <option value="true">Sim (Cavalo + Carreta)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 4. ROTA E NF-E -->
        <div class="g-section">
          <div class="g-title">📦 4. Viagem, Rota e Nota Fiscal Originária</div>
          <div class="g-grid g-grid-4">
            <div class="g-field">
              <label class="g-label">Início Previsto Viagem:*</label>
              <input type="datetime-local" id="cDataInicioViagem" class="g-input" required>
            </div>
            <div class="g-field">
              <label class="g-label">Fim Previsto Viagem:*</label>
              <input type="datetime-local" id="cDataFimViagem" class="g-input" required>
            </div>
            <div class="g-field">
              <label class="g-label">Distância (Km):*</label>
              <input type="number" id="cDistanciaKm" class="g-input" placeholder="Ex: 120" required>
            </div>
            <div class="g-field">
              <label class="g-label">Tipo Embalagem:*</label>
              <select id="cTipoEmbalagem" class="g-input">
                <option value="Caixa">Caixa</option>
                <option value="Palete">Palete</option>
                <option value="Granel">Granel</option>
                <option value="Unitario">Unitário</option>
              </select>
            </div>

            <div class="g-subtitle">Dados da NF-e</div>
            <div class="g-field">
              <label class="g-label">Número NF-e:*</label>
              <input type="text" id="cNfeNumero" class="g-input" placeholder="Número" required>
            </div>
            <div class="g-field">
              <label class="g-label">Série:*</label>
              <input type="text" id="cNfeSerie" class="g-input" placeholder="0" value="0" required>
            </div>
            <div class="g-field">
              <label class="g-label">CNPJ Emissor da NF-e:*</label>
              <input type="text" id="cNfeCnpjEmissor" class="g-input" placeholder="00000000000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">Data Emissão NF-e:*</label>
              <input type="datetime-local" id="cNfeDataEmissao" class="g-input" required>
            </div>
            <div class="g-field">
              <label class="g-label">NCM Predominante:*</label>
              <input type="text" id="cNcmCarga" class="g-input" placeholder="4 dígitos" required>
            </div>
            <div class="g-field">
              <label class="g-label">Peso Carga (Kg):*</label>
              <input type="number" step="0.001" id="cPesoCarga" class="g-input" placeholder="Ex: 15000" required>
            </div>
            <div class="g-field">
              <label class="g-label">Valor Total NF-e (R$):*</label>
              <input type="number" step="0.01" id="cNfeValorTotal" class="g-input" placeholder="Ex: 50000.00" required>
            </div>
            <div class="g-field">
              <label class="g-label">Descrição das Mercadorias:*</label>
              <input type="text" id="cDescMercadoria" class="g-input" placeholder="Descrição resumida" required>
            </div>
          </div>
        </div>

        <!-- 5. DESTINATÁRIO -->
        <div class="g-section">
          <div class="g-title">📍 5. Destinatário da Carga (Endereço Completo Obrigatório)</div>
          <div class="g-grid g-grid-4">
            <div class="g-field">
              <label class="g-label">CNPJ/CPF Destinatário:*</label>
              <input type="text" id="cDestCnpj" class="g-input" placeholder="00000000000000" required>
            </div>
            <div class="g-field" style="grid-column: span 3;">
              <label class="g-label">Razão Social Destinatário:*</label>
              <input type="text" id="cDestRazao" class="g-input" placeholder="Razão social completa" required>
            </div>
            <div class="g-field" style="grid-column: span 2;">
              <label class="g-label">Logradouro / Rua:*</label>
              <input type="text" id="cDestRua" class="g-input" placeholder="Rua / Avenida / Rodovia" required>
            </div>
            <div class="g-field">
              <label class="g-label">Número:*</label>
              <input type="text" id="cDestNumero" class="g-input" placeholder="Ex: 500 ou SN" required>
            </div>
            <div class="g-field">
              <label class="g-label">Bairro:*</label>
              <input type="text" id="cDestBairro" class="g-input" placeholder="Bairro" required>
            </div>
            <div class="g-field">
              <label class="g-label">CEP Destino:*</label>
              <input type="text" id="cCepDestino" class="g-input" placeholder="00000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">Cód. IBGE Destino:*</label>
              <input type="text" id="cIbgeDestino" class="g-input" placeholder="7 dígitos" required>
            </div>
            <div class="g-field">
              <label class="g-label">CEP Origem (Coleta):*</label>
              <input type="text" id="cCepOrigem" class="g-input" placeholder="00000000" required>
            </div>
            <div class="g-field">
              <label class="g-label">Cód. IBGE Origem (Coleta):*</label>
              <input type="text" id="cIbgeOrigem" class="g-input" placeholder="7 dígitos" required>
            </div>
          </div>
        </div>

        <!-- 6. VALORES, RETENÇÕES E PAGAMENTO -->
        <div class="g-section">
          <div class="g-title">💰 6. Valores do Frete, Retenções Tributárias e Dados Bancários</div>
          <div class="g-grid g-grid-5" style="grid-template-columns: repeat(5, 1fr);">
            <div class="g-field">
              <label class="g-label">Valor Bruto Frete (R$):*</label>
              <input type="number" step="0.01" id="cValorFreteBruto" class="g-input" placeholder="0.00" oninput="cCalcularLiquido()" required>
            </div>
            <div class="g-field">
              <label class="g-label">IRRF Retido (R$):</label>
              <input type="number" step="0.01" id="cImpostoIrrf" class="g-input" value="0.00" oninput="cCalcularLiquido()">
            </div>
            <div class="g-field">
              <label class="g-label">INSS Retido (R$):</label>
              <input type="number" step="0.01" id="cImpostoInss" class="g-input" value="0.00" oninput="cCalcularLiquido()">
            </div>
            <div class="g-field">
              <label class="g-label">SEST/SENAT (R$):</label>
              <input type="number" step="0.01" id="cImpostoSest" class="g-input" value="0.00" oninput="cCalcularLiquido()">
            </div>
            <div class="g-field">
              <label class="g-label" style="color:#4ade80;">Valor Líquido (R$):*</label>
              <input type="number" step="0.01" id="cValorFreteLiquido" class="g-input" style="color:#4ade80; font-weight:bold; background:#0f291e;" value="0.00" readonly>
            </div>
          </div>

          <div class="g-grid g-grid-4 mt-2">
            <div class="g-field">
              <label class="g-label">Meio de Pagamento:*</label>
              <select id="cTipoPagamento" class="g-input">
                <option value="TransferenciaBancaria" selected>Transferência Bancária</option>
                <option value="eFRETE">Saldo Conta e-Frete</option>
              </select>
            </div>
            <div class="g-field">
              <label class="g-label">Cód. Banco (COMPE):*</label>
              <input type="text" id="cBancoNum" class="g-input" placeholder="Ex: 237" required>
            </div>
            <div class="g-field">
              <label class="g-label">Agência (com dígito):*</label>
              <input type="text" id="cBancoAgencia" class="g-input" placeholder="Ex: 0001-9" required>
            </div>
            <div class="g-field">
              <label class="g-label">Conta (com dígito):*</label>
              <input type="text" id="cBancoConta" class="g-input" placeholder="Ex: 12345-6" required>
            </div>
          </div>
        </div>

        <button type="button" class="btn btn-info w-100 py-2 fw-bold text-dark text-uppercase shadow-sm" style="background:#00d2ff; border:none; letter-spacing:0.5px;" onclick="compilarEEstruturarXml()">
          COMPILAR XML E ENVIAR PARA O TRANSMISSOR
        </button>
      </div>
"""

# Substitui o bloco anterior (seja o antigo da foto 1 ou o vertical)
padrao = r'<!-- (?:FORMULÁRIO ERP COMPLETO|CONSTRUTOR ERP COMPLETO|<div[^>]*>).*?COMPILAR XML E ENVIAR PARA O TRANSMISSOR\s*</button>\s*</div>'

if "COMPILAR XML E ENVIAR PARA O TRANSMISSOR" in html:
    idx_fim_btn = html.find("COMPILAR XML E ENVIAR PARA O TRANSMISSOR")
    idx_fim = html.find("</div>", idx_fim_btn) + 6
    
    # Encontra o início da seção
    idx_inicio = html.rfind('<div class="card p-3 my-2"', 0, idx_fim_btn)
    if idx_inicio == -1:
        idx_inicio = html.rfind('<!-- FORMULÁRIO', 0, idx_fim_btn)
    if idx_inicio == -1:
        idx_inicio = html.rfind('<div class="tab-pane', 0, idx_fim_btn)
        idx_inicio = html.find('<div', idx_inicio + 20)

    html = html[:idx_inicio] + layout_limpo_grid + html[idx_fim:]
    print("✅ templates/index.html atualizado com layout em grelha limpa!")

# Garante funções JS e limpeza de campos
if "limparCamposConstrutor" not in html:
    html = html.replace("</script>", """
function limparCamposConstrutor() {
  document.querySelectorAll('#tab-construtor input').forEach(el => {
    if (el.type !== 'button' && el.type !== 'file' && el.id !== 'cHashIntegrador') el.value = '';
  });
  document.getElementById('cValorFreteLiquido').value = '0.00';
  document.getElementById('cImpostoIrrf').value = '0.00';
  document.getElementById('cImpostoInss').value = '0.00';
  document.getElementById('cImpostoSest').value = '0.00';
}
</script>""")

with open(ficheiro, "w", encoding="utf-8") as f:
    f.write(html)

print("🎉 SUCESSO! Layout atualizado com campos vazios e organizados em grelha horizontal.")
