import math
import re
import sys
import unicodedata
import requests
from geopy.distance import geodesic
from shapely.geometry import shape
from shapely.ops import nearest_points


def normalizar(texto: str) -> str:
    """Remove acentos e espaços extras, deixando em minúsculas."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()


def extrair_uf(m: dict) -> str:
    """Extrai a UF do payload do IBGE de forma segura contra nós nulos."""
    try:
        return m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("sigla", "").upper()
    except (AttributeError, TypeError):
        pass

    try:
        return m.get("regiao-imediata", {}).get("regiao-intermediaria", {}).get("UF", {}).get("sigla", "").upper()
    except (AttributeError, TypeError):
        pass

    # Pelo código IBGE (os dois primeiros dígitos representam o código da UF)
    codigos_uf = {
        "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
        "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL",
        "28": "SE", "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP", "41": "PR",
        "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"
    }
    return codigos_uf.get(str(m.get("id", ""))[:2], "BR")


class CalculadorDivisasMonitor:
    def __init__(self):
        self.headers = {"User-Agent": "CalculadorDistanciaDivisas/2.0"}
        self.municipios_base = []
        self.carregar_base_ibge()

    def carregar_base_ibge(self):
        print("Carregando base de dados oficial de municípios do IBGE...", end=" ", flush=True)
        try:
            url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
            resp = requests.get(url, headers=self.headers, timeout=20)
            resp.raise_for_status()
            dados = resp.json()
            self.municipios_base = [
                {
                    "id": str(m["id"]),
                    "nome": m["nome"],
                    "uf": extrair_uf(m),
                    "busca": normalizar(m["nome"])
                }
                for m in dados
            ]
            print(f"OK! ({len(self.municipios_base)} municípios prontos)\n")
        except Exception as e:
            print(f"\n[ERRO] Falha ao carregar IBGE: {e}")
            sys.exit(1)

    def selecionar_municipio(self, rotulo: str, default_nome: str) -> dict:
        while True:
            entrada = input(f"{rotulo} [padrão: {default_nome}]: ").strip()
            if not entrada:
                entrada = default_nome

            if entrada.lower() in ["sair", "exit", "quit"]:
                raise KeyboardInterrupt

            busca = normalizar(entrada)

            # Prioriza correspondência exata de nome
            candidatos = [m for m in self.municipios_base if m["busca"] == busca]

            # Se não achar exato, busca parcial
            if not candidatos:
                candidatos = [m for m in self.municipios_base if busca in m["busca"]]

            if not candidatos:
                print(f" -> Nenhum município encontrado para '{entrada}'. Tente novamente.")
                continue

            if len(candidatos) == 1:
                escolhido = candidatos[0]
                print(f" -> Selecionado: {escolhido['nome']} / {escolhido['uf']} (IBGE: {escolhido['id']})")
                return escolhido

            # Caso com nomes iguais (homônimos) ou múltiplos resultados parciais
            print(f"\nForam encontrados {len(candidatos)} municípios com esse nome. Selecione:")
            for idx, c in enumerate(candidatos, start=1):
                print(f"  [{idx}] {c['nome']} - {c['uf']} (Código IBGE: {c['id']})")

            while True:
                escolha = input(f"Digite o número desejado (1-{len(candidatos)}): ").strip()
                if escolha.isdigit() and 1 <= int(escolha) <= len(candidatos):
                    escolhido = candidatos[int(escolha) - 1]
                    print(f" -> Selecionado: {escolhido['nome']} / {escolhido['uf']}\n")
                    return escolhido
                print("Opção inválida. Tente novamente.")

    def obter_poligono_municipio(self, id_ibge: str):
        url = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{id_ibge}?formato=application/vnd.geo+json"
        resp = requests.get(url, headers=self.headers, timeout=20)
        resp.raise_for_status()
        geojson = resp.json()

        features = geojson.get("features", [])
        if not features:
            raise ValueError(f"Não foi possível obter a malha geográfica do IBGE {id_ibge}.")

        return shape(features[0]["geometry"])

    def buscar_cep_especifico(self, lat: float, lon: float):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1,
            "zoom": 17,
        }
        try:
            r = requests.get(url, params=params, headers=self.headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            address = data.get("address", {})

            postcode = address.get("postcode", "Não identificado")
            rua = (
                address.get("road")
                or address.get("suburb")
                or address.get("village")
                or "Ponto de divisa / Estrada rural"
            )

            cep_limpo = re.sub(r"\D", "", postcode)
            if len(cep_limpo) == 8 and not cep_limpo.endswith("000"):
                return {"cep": f"{cep_limpo[:5]}-{cep_limpo[5:]}", "logradouro": rua, "generico": False}
            elif len(cep_limpo) == 8:
                return {"cep": f"{cep_limpo[:5]}-{cep_limpo[5:]} (Base distrital)", "logradouro": rua, "generico": True}
            return {"cep": postcode, "logradouro": rua, "generico": True}
        except Exception:
            return {"cep": "Indisponível", "logradouro": "Região de fronteira municipal", "generico": True}

    def processar(self, m1: dict, m2: dict):
        print("\n[Calculando] Baixando malhas cartográficas e calculando menor distância...")
        poly1 = self.obter_poligono_municipio(m1["id"])
        poly2 = self.obter_poligono_municipio(m2["id"])

        ponto1, ponto2 = nearest_points(poly1, poly2)
        coord1 = (ponto1.y, ponto1.x)
        coord2 = (ponto2.y, ponto2.x)

        distancia_km = geodesic(coord1, coord2).kilometers
        faz_divisa = poly1.touches(poly2) or math.isclose(distancia_km, 0.0, abs_tol=0.05)

        print("[Calculando] Identificando CEPs e logradouros nas divisas...")
        end1 = self.buscar_cep_especifico(coord1[0], coord1[1])
        end2 = self.buscar_cep_especifico(coord2[0], coord2[1])

        print("\n" + "=" * 65)
        print(f"ANÁLISE: {m1['nome']}/{m1['uf']} ({m1['id']}) x {m2['nome']}/{m2['uf']} ({m2['id']})")
        print("=" * 65)

        if faz_divisa:
            print("STATUS: FAZEM DIVISA TERRITORIAL DIRETA (Distância na fronteira: 0.00 km)")
        else:
            print(f"STATUS: DISTÂNCIA MÍNIMA ENTRE DIVISAS: {distancia_km:.2f} km")

        print(f"\n--- Ponto Extremo em {m1['nome']} ---")
        print(f"Logradouro:  {end1['logradouro']}")
        print(f"CEP Divisa:  {end1['cep']}")
        print(f"Coordenadas: Lat {coord1[0]:.6f}, Lon {coord1[1]:.6f}")

        print(f"\n--- Ponto Extremo em {m2['nome']} ---")
        print(f"Logradouro:  {end2['logradouro']}")
        print(f"CEP Divisa:  {end2['cep']}")
        print(f"Coordenadas: Lat {coord2[0]:.6f}, Lon {coord2[1]:.6f}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    print("=" * 65)
    print(" MONITOR DE DIVISAS E MENOR DISTÂNCIA (IBGE)")
    print(" (Digite 'sair' a qualquer momento para fechar)")
    print("=" * 65)

    app = CalculadorDivisasMonitor()

    while True:
        try:
            m1 = app.selecionar_municipio("Cidade 1", "Piracicaba")
            m2 = app.selecionar_municipio("Cidade 2", "Saltinho")
            app.processar(m1, m2)
        except KeyboardInterrupt:
            print("\nEncerrando monitor...")
            break
        except Exception as e:
            print(f"\n[AVISO] Não foi possível calcular o par de cidades: {e}\n")
