import os
import json
import time
import datetime
import math
import re
import unicodedata
import requests
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from geopy.distance import geodesic
from shapely.geometry import shape
from shapely.ops import nearest_points
from requests_pkcs12 import post as pkcs12_post

app = FastAPI(title="GeoLog TMS & JCIOT Hub Enterprise", docs_url=None, redoc_url=None)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
MUNICIPIOS_CACHE = []
MALHAS_CACHE = {}

DATA_HORA_SYNC = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

CATALOGO_PRACAS_PEDAGIO = [
    {"nome": "Pedágio Boituva Leste (SP-280)", "lat": -23.3284, "lon": -47.6612, "tarifa_eixo": 14.50, "rodovia": "SP-280 Castello Branco"},
    {"nome": "Pedágio Itu Leste (SP-280)", "lat": -23.3989, "lon": -47.2625, "tarifa_eixo": 13.20, "rodovia": "SP-280 Castello Branco"},
    {"nome": "Pedágio Barueri I Leste (SP-280)", "lat": -23.5042, "lon": -46.8524, "tarifa_eixo": 4.20, "rodovia": "SP-280 Castello Branco"},
    {"nome": "Pedágio Osasco (SP-280)", "lat": -23.5180, "lon": -46.7820, "tarifa_eixo": 4.20, "rodovia": "SP-280 Castello Branco"},
    {"nome": "Pedágio Itaquaquecetuba Leste (SP-070)", "lat": -23.4735, "lon": -46.3312, "tarifa_eixo": 6.10, "rodovia": "SP-070 Ayrton Senna"},
    {"nome": "Pedágio Guararema Leste (SP-070)", "lat": -23.3854, "lon": -46.0821, "tarifa_eixo": 5.70, "rodovia": "SP-070 Carvalho Pinto"},
    {"nome": "Pedágio São José dos Campos Leste (SP-070)", "lat": -23.2381, "lon": -45.8920, "tarifa_eixo": 5.70, "rodovia": "SP-070 Carvalho Pinto"},
    {"nome": "Pedágio Caçapava Leste (SP-070)", "lat": -23.1092, "lon": -45.6980, "tarifa_eixo": 5.80, "rodovia": "SP-070 Carvalho Pinto"},
    {"nome": "Pedágio P6 Moreira César Norte (BR-116)", "lat": -22.9512, "lon": -45.3621, "tarifa_eixo": 17.10, "rodovia": "BR-116 Presidente Dutra"},
    {"nome": "Pedágio P7 Itatiaia Norte (BR-116)", "lat": -22.5184, "lon": -44.5710, "tarifa_eixo": 14.70, "rodovia": "BR-116 Presidente Dutra"},
    {"nome": "Pedágio P04 Viúva Graça Norte (BR-116)", "lat": -22.7145, "lon": -43.7621, "tarifa_eixo": 17.20, "rodovia": "BR-116 Presidente Dutra"},
    {"nome": "Pedágio P1 Xerém Norte (BR-040)", "lat": -22.5812, "lon": -43.2985, "tarifa_eixo": 21.00, "rodovia": "BR-040 Rio-Petrópolis"},
    {"nome": "Pedágio Arujá (BR-116)", "lat": -23.3812, "lon": -46.3210, "tarifa_eixo": 4.10, "rodovia": "BR-116 Dutra"},
    {"nome": "Pedágio Jacareí (BR-116)", "lat": -23.3105, "lon": -45.9620, "tarifa_eixo": 7.30, "rodovia": "BR-116 Dutra"},
    {"nome": "Pedágio Parateí (SP-065)", "lat": -23.2841, "lon": -46.0910, "tarifa_eixo": 6.80, "rodovia": "SP-065 Dom Pedro I"},
    {"nome": "Pedágio Igaratá (SP-065)", "lat": -23.1950, "lon": -46.1520, "tarifa_eixo": 6.80, "rodovia": "SP-065 Dom Pedro I"},
    {"nome": "Pedágio Atibaia (SP-065)", "lat": -23.1310, "lon": -46.5210, "tarifa_eixo": 7.20, "rodovia": "SP-065 Dom Pedro I"},
    {"nome": "Pedágio Perus (SP-348)", "lat": -23.4110, "lon": -46.7820, "tarifa_eixo": 9.40, "rodovia": "SP-348 Bandeirantes"},
    {"nome": "Pedágio Campo Limpo (SP-348)", "lat": -23.2105, "lon": -46.9120, "tarifa_eixo": 9.40, "rodovia": "SP-348 Bandeirantes"},
    {"nome": "Pedágio Itupeva (SP-348)", "lat": -23.0820, "lon": -47.0510, "tarifa_eixo": 9.40, "rodovia": "SP-348 Bandeirantes"},
    {"nome": "Pedágio Sumaré (SP-330)", "lat": -22.8410, "lon": -47.2210, "tarifa_eixo": 8.90, "rodovia": "SP-330 Anhanguera"},
    {"nome": "Pedágio Limeira (SP-330)", "lat": -22.6105, "lon": -47.3820, "tarifa_eixo": 8.20, "rodovia": "SP-330 Anhanguera"},
    {"nome": "Pedágio Rio Claro (SP-310)", "lat": -22.4210, "lon": -47.5810, "tarifa_eixo": 7.90, "rodovia": "SP-310 Washington Luís"}
]

COEFICIENTES_ANTT_2026 = {
    "geral": {
        2: {"tab_a": {"ccd": 3.8812, "cc": 358.46}, "tab_b": {"ccd": 3.4860, "cc": 324.91}, "tab_c": {"ccd": 3.5950, "cc": 234.36}, "tab_d": {"ccd": 3.2490, "cc": 206.88}},
        3: {"tab_a": {"ccd": 4.6908, "cc": 414.56}, "tab_b": {"ccd": 4.2064, "cc": 377.78}, "tab_c": {"ccd": 4.3518, "cc": 269.76}, "tab_d": {"ccd": 3.9372, "cc": 241.32}},
        4: {"tab_a": {"ccd": 5.5410, "cc": 495.22}, "tab_b": {"ccd": 4.9840, "cc": 449.23}, "tab_c": {"ccd": 5.1386, "cc": 322.08}, "tab_d": {"ccd": 4.6334, "cc": 288.24}},
        5: {"tab_a": {"ccd": 6.4715, "cc": 583.18}, "tab_b": {"ccd": 5.8212, "cc": 528.87}, "tab_c": {"ccd": 6.0052, "cc": 378.72}, "tab_d": {"ccd": 5.4196, "cc": 338.88}},
        6: {"tab_a": {"ccd": 7.3547, "cc": 671.93}, "tab_b": {"ccd": 6.6063, "cc": 608.99}, "tab_c": {"ccd": 6.8228, "cc": 435.36}, "tab_d": {"ccd": 6.1578, "cc": 390.12}},
        7: {"tab_a": {"ccd": 8.1418, "cc": 760.14}, "tab_b": {"ccd": 7.3228, "cc": 689.30}, "tab_c": {"ccd": 7.5532, "cc": 492.60}, "tab_d": {"ccd": 6.8252, "cc": 441.84}},
        9: {"tab_a": {"ccd": 9.7082, "cc": 936.42}, "tab_b": {"ccd": 8.7420, "cc": 850.15}, "tab_c": {"ccd": 9.0048, "cc": 607.44}, "tab_d": {"ccd": 8.1384, "cc": 544.92}}
    },
    "granel_solido": {
        2: {"tab_a": {"ccd": 4.1102, "cc": 382.20}, "tab_b": {"ccd": 3.6901, "cc": 346.22}, "tab_c": {"ccd": 3.8090, "cc": 249.72}, "tab_d": {"ccd": 3.4390, "cc": 221.04}},
        3: {"tab_a": {"ccd": 4.9664, "cc": 442.44}, "tab_b": {"ccd": 4.4552, "cc": 402.82}, "tab_c": {"ccd": 4.6080, "cc": 288.24}, "tab_d": {"ccd": 4.1696, "cc": 257.16}},
        4: {"tab_a": {"ccd": 5.8684, "cc": 529.74}, "tab_b": {"ccd": 5.2768, "cc": 480.98}, "tab_c": {"ccd": 5.4426, "cc": 345.00}, "tab_d": {"ccd": 4.9070, "cc": 307.32}},
        5: {"tab_a": {"ccd": 6.8546, "cc": 624.22}, "tab_b": {"ccd": 6.1636, "cc": 565.86}, "tab_c": {"ccd": 6.3596, "cc": 406.08}, "tab_d": {"ccd": 5.7388, "cc": 362.64}},
        6: {"tab_a": {"ccd": 7.7918, "cc": 718.98}, "tab_b": {"ccd": 7.0062, "cc": 651.90}, "tab_c": {"ccd": 7.2282, "cc": 467.04}, "tab_d": {"ccd": 6.5244, "cc": 417.72}},
        7: {"tab_a": {"ccd": 8.6252, "cc": 813.44}, "tab_b": {"ccd": 7.7656, "cc": 737.94}, "tab_c": {"ccd": 8.0034, "cc": 528.12}, "tab_d": {"ccd": 7.2274, "cc": 473.16}},
        9: {"tab_a": {"ccd": 10.2912, "cc": 1002.66}, "tab_b": {"ccd": 9.2554, "cc": 909.78}, "tab_c": {"ccd": 9.5470, "cc": 651.36}, "tab_d": {"ccd": 8.6234, "cc": 583.44}}
    },
    "granel_liquido": {
        2: {"tab_a": {"ccd": 4.3418, "cc": 406.46}, "tab_b": {"ccd": 3.8980, "cc": 369.18}, "tab_c": {"ccd": 4.0242, "cc": 265.68}, "tab_d": {"ccd": 3.6330, "cc": 235.68}},
        3: {"tab_a": {"ccd": 5.2460, "cc": 470.90}, "tab_b": {"ccd": 4.7092, "cc": 428.44}, "tab_c": {"ccd": 4.8678, "cc": 307.32}, "tab_d": {"ccd": 4.4038, "cc": 273.96}},
        4: {"tab_a": {"ccd": 6.1962, "cc": 564.18}, "tab_b": {"ccd": 5.5724, "cc": 512.50}, "tab_c": {"ccd": 5.7468, "cc": 367.68}, "tab_d": {"ccd": 5.1824, "cc": 327.84}},
        5: {"tab_a": {"ccd": 7.2396, "cc": 664.54}, "tab_b": {"ccd": 6.5110, "cc": 602.82}, "tab_c": {"ccd": 6.7168, "cc": 433.44}, "tab_d": {"ccd": 6.0614, "cc": 386.88}},
        6: {"tab_a": {"ccd": 8.2308, "cc": 765.92}, "tab_b": {"ccd": 7.4046, "cc": 694.22}, "tab_c": {"ccd": 7.6382, "cc": 498.96}, "tab_d": {"ccd": 6.8968, "cc": 445.44}},
        7: {"tab_a": {"ccd": 9.1124, "cc": 866.40}, "tab_b": {"ccd": 8.2072, "cc": 786.12}, "tab_c": {"ccd": 8.4574, "cc": 564.24}, "tab_d": {"ccd": 7.6398, "cc": 504.60}},
        9: {"tab_a": {"ccd": 10.8748, "cc": 1067.84}, "tab_b": {"ccd": 9.7892, "cc": 969.24}, "tab_c": {"ccd": 10.0894, "cc": 695.28}, "tab_d": {"ccd": 9.1136, "cc": 622.92}}
    },
    "frigorificada": {
        2: {"tab_a": {"ccd": 4.7630, "cc": 450.50}, "tab_b": {"ccd": 4.2758, "cc": 409.64}, "tab_c": {"ccd": 4.4150, "cc": 294.36}, "tab_d": {"ccd": 3.9852, "cc": 261.72}},
        3: {"tab_a": {"ccd": 5.7550, "cc": 522.64}, "tab_b": {"ccd": 5.1680, "cc": 475.12}, "tab_c": {"ccd": 5.3402, "cc": 341.40}, "tab_d": {"ccd": 4.8322, "cc": 304.08}},
        4: {"tab_a": {"ccd": 6.8004, "cc": 626.58}, "tab_b": {"ccd": 6.1156, "cc": 568.96}, "tab_c": {"ccd": 6.3072, "cc": 408.96}, "tab_d": {"ccd": 5.6890, "cc": 364.20}},
        5: {"tab_a": {"ccd": 7.9460, "cc": 738.38}, "tab_b": {"ccd": 7.1466, "cc": 670.18}, "tab_c": {"ccd": 7.3732, "cc": 481.80}, "tab_d": {"ccd": 6.6570, "cc": 429.72}},
        6: {"tab_a": {"ccd": 9.0354, "cc": 851.20}, "tab_b": {"ccd": 8.1286, "cc": 771.84}, "tab_c": {"ccd": 8.3854, "cc": 555.00}, "tab_d": {"ccd": 7.5708, "cc": 494.76}},
        7: {"tab_a": {"ccd": 10.0038, "cc": 962.88}, "tab_b": {"ccd": 9.0050, "cc": 874.20}, "tab_c": {"ccd": 9.2838, "cc": 628.08}, "tab_d": {"ccd": 8.3854, "cc": 560.52}},
        9: {"tab_a": {"ccd": 11.9392, "cc": 1186.82}, "tab_b": {"ccd": 10.7490, "cc": 1077.58}, "tab_c": {"ccd": 11.0772, "cc": 774.24}, "tab_d": {"ccd": 10.0050, "cc": 692.16}}
    },
    "perigosa": {
        2: {"tab_a": {"ccd": 5.1718, "cc": 495.40}, "tab_b": {"ccd": 4.6460, "cc": 450.36}, "tab_c": {"ccd": 4.7972, "cc": 323.76}, "tab_d": {"ccd": 4.3300, "cc": 287.76}},
        3: {"tab_a": {"ccd": 6.2508, "cc": 574.76}, "tab_b": {"ccd": 5.6186, "cc": 522.50}, "tab_c": {"ccd": 5.8010, "cc": 375.72}, "tab_d": {"ccd": 5.2492, "cc": 334.68}},
        4: {"tab_a": {"ccd": 7.3872, "cc": 689.36}, "tab_b": {"ccd": 6.6454, "cc": 626.06}, "tab_c": {"ccd": 6.8516, "cc": 450.24}, "tab_d": {"ccd": 6.1818, "cc": 400.92}},
        5: {"tab_a": {"ccd": 8.6322, "cc": 812.72}, "tab_b": {"ccd": 7.7644, "cc": 737.84}, "tab_c": {"ccd": 8.0098, "cc": 530.52}, "tab_d": {"ccd": 7.2336, "cc": 473.04}},
        6: {"tab_a": {"ccd": 9.8138, "cc": 936.80}, "tab_b": {"ccd": 8.8288, "cc": 849.70}, "tab_c": {"ccd": 9.1074, "cc": 611.04}, "tab_d": {"ccd": 8.2238, "cc": 544.80}},
        7: {"tab_a": {"ccd": 10.8654, "cc": 1059.78}, "tab_b": {"ccd": 9.7802, "cc": 962.34}, "tab_c": {"ccd": 10.0848, "cc": 691.68}, "tab_d": {"ccd": 9.1082, "cc": 617.04}},
        9: {"tab_a": {"ccd": 12.9678, "cc": 1306.40}, "tab_b": {"ccd": 11.6748, "cc": 1186.22}, "tab_c": {"ccd": 12.0354, "cc": 852.96}, "tab_d": {"ccd": 10.8710, "cc": 762.00}}
    },
    "neogranel": {
        2: {"tab_a": {"ccd": 4.0388, "cc": 370.20}, "tab_b": {"ccd": 3.6276, "cc": 335.58}, "tab_c": {"ccd": 3.7418, "cc": 242.04}, "tab_d": {"ccd": 3.3812, "cc": 214.20}},
        3: {"tab_a": {"ccd": 4.8814, "cc": 428.38}, "tab_b": {"ccd": 4.3792, "cc": 390.40}, "tab_c": {"ccd": 4.5298, "cc": 279.00}, "tab_d": {"ccd": 4.0990, "cc": 249.36}},
        4: {"tab_a": {"ccd": 5.7656, "cc": 512.86}, "tab_b": {"ccd": 5.1864, "cc": 465.80}, "tab_c": {"ccd": 5.3496, "cc": 333.36}, "tab_d": {"ccd": 4.8236, "cc": 298.08}},
        5: {"tab_a": {"ccd": 6.7348, "cc": 604.56}, "tab_b": {"ccd": 6.0578, "cc": 548.06}, "tab_c": {"ccd": 6.2486, "cc": 392.40}, "tab_d": {"ccd": 5.5418, "cc": 351.48}},
        6: {"tab_a": {"ccd": 7.6552, "cc": 696.34}, "tab_b": {"ccd": 6.8858, "cc": 631.42}, "tab_c": {"ccd": 7.1018, "cc": 451.80}, "tab_d": {"ccd": 6.4136, "cc": 404.28}},
        7: {"tab_a": {"ccd": 8.4746, "cc": 787.82}, "tab_b": {"ccd": 7.6324, "cc": 714.78}, "tab_c": {"ccd": 7.8632, "cc": 510.96}, "tab_d": {"ccd": 7.1042, "cc": 457.92}},
        9: {"tab_a": {"ccd": 10.1118, "cc": 971.04}, "tab_b": {"ccd": 9.0968, "cc": 881.56}, "tab_c": {"ccd": 9.3804, "cc": 630.12}, "tab_d": {"ccd": 8.4764, "cc": 564.84}}
    }
}

def normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()

def extrair_uf(m: dict) -> str:
    try:
        return m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("sigla", "").upper()
    except:
        pass
    try:
        return m.get("regiao-imediata", {}).get("regiao-intermediaria", {}).get("UF", {}).get("sigla", "").upper()
    except:
        pass
    codigos_uf = {
        "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
        "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL",
        "28": "SE", "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP", "41": "PR",
        "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"
    }
    return codigos_uf.get(str(m.get("id", ""))[:2], "BR")

ARQUIVO_CACHE_IBGE = os.path.join(os.path.dirname(__file__), "municipios_ibge.json")

def carregar_base():
    global MUNICIPIOS_CACHE
    if MUNICIPIOS_CACHE:
        return

    # 1. Tenta carregar do cache local
    if os.path.exists(ARQUIVO_CACHE_IBGE):
        try:
            with open(ARQUIVO_CACHE_IBGE, "r", encoding="utf-8") as f:
                MUNICIPIOS_CACHE = json.load(f)
                if MUNICIPIOS_CACHE:
                    print(f"[*] Base territorial carregada do cache local: {len(MUNICIPIOS_CACHE)} municipios.")
                    return
        except Exception as e:
            print(f"[!] Erro ao ler cache local de municipios: {e}")

    # 2. Se nao existir cache, tenta baixar com 3 tentativas e timeout aumentado
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    for tentativa in range(1, 4):
        try:
            print(f"[*] Sincronizando municipios com o IBGE (Tentativa {tentativa}/3)...")
            r = requests.get(url, headers=HEADERS, timeout=25)
            r.raise_for_status()
            MUNICIPIOS_CACHE = [
                {"id": str(m["id"]), "nome": m["nome"], "uf": extrair_uf(m), "busca": normalizar(m["nome"])}
                for m in r.json()
            ]
            with open(ARQUIVO_CACHE_IBGE, "w", encoding="utf-8") as f:
                json.dump(MUNICIPIOS_CACHE, f, ensure_ascii=False)
            print(f"[*] Base salva com sucesso em '{ARQUIVO_CACHE_IBGE}'!")
            return
        except Exception as e:
            print(f"[!] Falha na tentativa {tentativa}: {e}")
            time.sleep(2)

    # 3. Fallback de contingencia caso o IBGE continue fora do ar
    if not MUNICIPIOS_CACHE:
        print("[!] AVISO: IBGE indisponivel no momento. Carregando cidades base...")
        MUNICIPIOS_CACHE = [
            {"id": "3537503", "nome": "Pereiras", "uf": "SP", "busca": "pereiras"},
            {"id": "3303906", "nome": "Petrópolis", "uf": "RJ", "busca": "petropolis"},
            {"id": "4104808", "nome": "Cascavel", "uf": "PR", "busca": "cascavel"},
            {"id": "3543907", "nome": "Rio das Pedras", "uf": "SP", "busca": "rio das pedras"},
            {"id": "3550308", "nome": "São Paulo", "uf": "SP", "busca": "sao paulo"},
            {"id": "3304557", "nome": "Rio de Janeiro", "uf": "RJ", "busca": "rio de janeiro"}
        ]
carregar_base()

def buscar_municipios(termo: str):
    if not MUNICIPIOS_CACHE:
        carregar_base()
    termo_str = str(termo).strip()
    if termo_str.isdigit():
        for m in MUNICIPIOS_CACHE:
            if m["id"] == termo_str:
                return [m]
    b = normalizar(termo_str)
    exatos = [m for m in MUNICIPIOS_CACHE if m["busca"] == b]
    if exatos:
        return exatos
    return [m for m in MUNICIPIOS_CACHE if b in m["busca"]]

def obter_poligono(id_ibge: str):
    if id_ibge in MALHAS_CACHE:
        return MALHAS_CACHE[id_ibge]
    url = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{id_ibge}?formato=application/vnd.geo+json&qualidade=minima"
    r = requests.get(url, headers=HEADERS, timeout=6)
    r.raise_for_status()
    geojson = r.json()
    features = geojson.get("features", [])
    if not features:
        raise ValueError("Malha nao localizada.")
    geom = shape(features[0]["geometry"])
    MALHAS_CACHE[id_ibge] = (geom, features[0]["geometry"])
    return MALHAS_CACHE[id_ibge]

def identificar_municipio_por_coordenada(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=10"
    try:
        r = requests.get(url, headers=HEADERS, timeout=3)
        if r.status_code == 200:
            addr = r.json().get("address", {})
            cidade = addr.get("city") or addr.get("town") or addr.get("municipality") or addr.get("village") or ""
            uf = addr.get("state_code", "").upper()
            if cidade:
                cands = buscar_municipios(cidade)
                if uf:
                    cands_uf = [c for c in cands if c["uf"] == uf]
                    if cands_uf:
                        return cands_uf[0]
                if cands:
                    return cands[0]
    except Exception:
        pass
    return None

def buscar_cep_e_coordenadas(lat: float, lon: float, nome_cidade: str, uf: str):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=17"
        r = requests.get(url, headers=HEADERS, timeout=2.5)
        if r.status_code == 200:
            d = r.json()
            postcode = re.sub(r"\D", "", d.get("address", {}).get("postcode", ""))
            if len(postcode) == 8 and not postcode.endswith("000"):
                rua = d.get("address", {}).get("road") or "Via Urbana"
                return {
                    "cep": f"{postcode[:5]}-{postcode[5:]}",
                    "logradouro": rua,
                    "lat": round(float(lat), 6),
                    "lon": round(float(lon), 6)
                }
    except Exception:
        pass

    try:
        url = f"https://viacep.com.br/ws/{uf}/{requests.utils.quote(nome_cidade)}/Rua/json/"
        r = requests.get(url, headers=HEADERS, timeout=2.5)
        if r.status_code == 200:
            itens = r.json()
            if isinstance(itens, list):
                for item in itens:
                    cep_limpo = re.sub(r"\D", "", item.get("cep", ""))
                    if len(cep_limpo) == 8 and not cep_limpo.endswith("000"):
                        if normalizar(item.get("localidade", "")) == normalizar(nome_cidade):
                            return {
                                "cep": f"{cep_limpo[:5]}-{cep_limpo[5:]}",
                                "logradouro": f"{item.get('logradouro', '')} - {item.get('bairro', '')}".strip(" -"),
                                "lat": round(lat, 6),
                                "lon": round(lon, 6)
                            }
    except Exception:
        pass

    return {
        "cep": "Ponto de Divisa",
        "logradouro": "Trecho Limítrofe",
        "lat": round(lat, 6),
        "lon": round(lon, 6)
    }

def mapear_pedagios_oficiais(coords_rota, dist_km: float, eixos: int):
    if not coords_rota or len(coords_rota) < 2:
        return {"total": 0.0, "quantidade": 0, "pedagios": [], "origem_dados": "Sem dados"}

    step = max(1, len(coords_rota) // 120)
    pontos_rota = coords_rota[::step]
    if coords_rota[-1] not in pontos_rota:
        pontos_rota.append(coords_rota[-1])

    pedagios_interceptados = []
    nomes_adicionados = set()

    for praca in CATALOGO_PRACAS_PEDAGIO:
        p_lat, p_lon = praca["lat"], praca["lon"]
        for pt in pontos_rota:
            if geodesic((p_lat, p_lon), (pt[0], pt[1])).kilometers <= 4.5:
                if praca["nome"] not in nomes_adicionados:
                    nomes_adicionados.add(praca["nome"])
                    valor_manual = round(praca["tarifa_eixo"] * eixos, 2)
                    valor_tag = round(valor_manual * 0.95, 2)

                    pedagios_interceptados.append({
                        "nome": praca["nome"],
                        "valor": valor_manual,
                        "valorTag": valor_tag,
                        "lat": p_lat,
                        "lon": p_lon,
                        "rodovia": praca["rodovia"]
                    })
                break

    if len(pedagios_interceptados) == 0 and dist_km > 70:
        qtd_est = int(dist_km // 85)
        for i in range(1, qtd_est + 1):
            idx = min(len(coords_rota) - 1, i * (len(coords_rota) // (qtd_est + 1)))
            pt = coords_rota[idx]
            v_man = round(10.50 * eixos, 2)
            pedagios_interceptados.append({
                "nome": f"Praça de Pedágio Rodoviária KM {i * 85}",
                "valor": v_man,
                "valorTag": round(v_man * 0.95, 2),
                "lat": pt[0],
                "lon": pt[1],
                "rodovia": "Rodovia Federal/Estadual"
            })

    total_pedagio = sum(p["valor"] for p in pedagios_interceptados)

    return {
        "total": round(total_pedagio, 2),
        "quantidade": len(pedagios_interceptados),
        "pedagios": pedagios_interceptados,
        "origem_dados": "Tarifas Oficiais ANTT / ARTESP"
    }

def obter_rota_veiculo(c1, c2):
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{c1[1]},{c1[0]};{c2[1]},{c2[0]}?overview=full&geometries=geojson"
        r = requests.get(url, headers=HEADERS, timeout=3.5)
        if r.status_code == 200:
            dados = r.json()
            if dados.get("routes"):
                rota = dados["routes"][0]
                dist_km = rota["distance"] / 1000.0
                duracao_min = rota["duration"] / 60.0
                coords = [[p[1], p[0]] for p in rota["geometry"]["coordinates"]]
                dist_real = max(1.0, round(dist_km, 2))
                return {
                    "dist_km": dist_real,
                    "duracao_min": max(1, round(duracao_min)),
                    "coords_rota": coords
                }
    except Exception:
        pass

    dist_geo = geodesic(c1, c2).kilometers
    dist_est = max(1.0, round(dist_geo * 1.25, 2))
    return {
        "dist_km": dist_est,
        "duracao_min": max(1, round((dist_est / 60) * 60)),
        "coords_rota": [[c1[0], c1[1]], [c2[0], c2[1]]]
    }

def calcular_frete_antt_oficial(dist_km: float, categoria: str, eixos: int, composicao: bool, alto_desempenho: bool, retorno_vazio: bool):
    dist_efetiva = max(1.0, float(dist_km))
    cat = COEFICIENTES_ANTT_2026.get(categoria, COEFICIENTES_ANTT_2026["geral"])
    params_eixo = cat.get(eixos, cat[5])
    
    if alto_desempenho:
        chave_tabela = "tab_c" if composicao else "tab_d"
        nome_tab = "Tabela C - Transporte Rodoviário de Carga Lotação de Alto Desempenho" if composicao else "Tabela D - Operações de Alto Desempenho em que Haja a Contratação Apenas do Veículo Automotor de Cargas"
    else:
        chave_tabela = "tab_a" if composicao else "tab_b"
        nome_tab = "Tabela A - Transporte Rodoviário de Carga e Lotação" if composicao else "Tabela B - Operações em que Haja a Contratação Apenas do Veículo Automotor de Cargas"

    coefs = params_eixo[chave_tabela]
    ccd = coefs["ccd"]
    cc = coefs["cc"]

    valor_ida = (dist_efetiva * ccd) + cc
    valor_retorno = (0.92 * dist_efetiva * ccd) if retorno_vazio else 0.0
    valor_total = valor_ida + valor_retorno

    return {
        "valor_total": round(valor_total, 2),
        "valor_ida": round(valor_ida, 2),
        "valor_retorno": round(valor_retorno, 2),
        "distancia_apurada_km": round(dist_efetiva, 2),
        "custo_km": round(ccd, 4),
        "custo_carga_descarga": round(cc, 2),
        "operacao_transporte": nome_tab,
        "possui_retorno_vazio": retorno_vazio
    }

@app.get("/api/verificar_cidade")
def api_verificar_cidade(nome: str = Query(..., min_length=2, max_length=100)):
    res = buscar_municipios(nome)
    if not res:
        raise HTTPException(status_code=404, detail="Município não localizado.")
    return {"total": len(res), "candidatos": res}

@app.get("/api/calcular")
def api_calcular(id_origem: str, id_destino: str, eixos: int = 3):
    c1 = buscar_municipios(id_origem)
    c2 = buscar_municipios(id_destino)
    if not c1 or not c2:
        raise HTTPException(status_code=404, detail="Município não localizado.")

    m1 = c1[0]
    m2 = c2[0]

    poly1, geojson1 = obter_poligono(m1["id"])
    poly2, geojson2 = obter_poligono(m2["id"])

    ponto1, ponto2 = nearest_points(poly1, poly2)
    coord1 = (ponto1.y, ponto1.x)
    coord2 = (ponto2.y, ponto2.x)

    end1 = buscar_cep_e_coordenadas(coord1[0], coord1[1], m1["nome"], m1["uf"])
    end2 = buscar_cep_e_coordenadas(coord2[0], coord2[1], m2["nome"], m2["uf"])

    rota = obter_rota_veiculo(coord1, coord2)
    dados_pedagio = mapear_pedagios_oficiais(rota["coords_rota"], rota["dist_km"], eixos)

    horas = rota["duracao_min"] // 60
    minutos = rota["duracao_min"] % 60
    tempo_fmt = f"{horas}h {minutos}min" if horas > 0 else f"{minutos} min"

    return {
        "distancia_rodoviaria_km": rota["dist_km"],
        "tempo_estimado": tempo_fmt,
        "coords_rota": rota["coords_rota"],
        "pedagios": dados_pedagio,
        "origem": {
            "municipio": f"{m1['nome']}/{m1['uf']}",
            "nome_simples": m1["nome"],
            "uf": m1["uf"],
            "ibge": m1["id"],
            "cep": end1["cep"],
            "logradouro": end1["logradouro"],
            "lat": end1["lat"],
            "lon": end1["lon"],
            "geojson": geojson1
        },
        "destino": {
            "municipio": f"{m2['nome']}/{m2['uf']}",
            "nome_simples": m2["nome"],
            "uf": m2["uf"],
            "ibge": m2["id"],
            "cep": end2["cep"],
            "logradouro": end2["logradouro"],
            "lat": end2["lat"],
            "lon": end2["lon"],
            "geojson": geojson2
        }
    }

@app.get("/api/recalcular_rota_arraste")
def api_recalcular_rota_arraste(lat1: float, lon1: float, lat2: float, lon2: float, id_origem_antigo: str, id_destino_antigo: str, eixos: int = 3):
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    rota = obter_rota_veiculo(coord1, coord2)
    dados_pedagio = mapear_pedagios_oficiais(rota["coords_rota"], rota["dist_km"], eixos)

    m1_novo = identificar_municipio_por_coordenada(lat1, lon1)
    m2_novo = identificar_municipio_por_coordenada(lat2, lon2)

    m1_final = m1_novo if m1_novo else buscar_municipios(id_origem_antigo)[0]
    m2_final = m2_novo if m2_novo else buscar_municipios(id_destino_antigo)[0]

    poly1, geojson1 = obter_poligono(m1_final["id"])
    poly2, geojson2 = obter_poligono(m2_final["id"])

    end1 = buscar_cep_e_coordenadas(lat1, lon1, m1_final["nome"], m1_final["uf"])
    end2 = buscar_cep_e_coordenadas(lat2, lon2, m2_final["nome"], m2_final["uf"])

    horas = rota["duracao_min"] // 60
    minutos = rota["duracao_min"] % 60
    tempo_fmt = f"{horas}h {minutos}min" if horas > 0 else f"{minutos} min"

    return {
        "distancia_rodoviaria_km": rota["dist_km"],
        "tempo_estimado": tempo_fmt,
        "coords_rota": rota["coords_rota"],
        "pedagios": dados_pedagio,
        "origem": {
            "municipio": f"{m1_final['nome']}/{m1_final['uf']}",
            "nome_simples": m1_final["nome"],
            "uf": m1_final["uf"],
            "ibge": m1_final["id"],
            "cep": end1["cep"],
            "logradouro": end1["logradouro"],
            "lat": end1["lat"],
            "lon": end1["lon"],
            "geojson": geojson1,
            "mudou_municipio": (m1_final["id"] != str(id_origem_antigo))
        },
        "destino": {
            "municipio": f"{m2_final['nome']}/{m2_final['uf']}",
            "nome_simples": m2_final["nome"],
            "uf": m2_final["uf"],
            "ibge": m2_final["id"],
            "cep": end2["cep"],
            "logradouro": end2["logradouro"],
            "lat": end2["lat"],
            "lon": end2["lon"],
            "geojson": geojson2,
            "mudou_municipio": (m2_final["id"] != str(id_destino_antigo))
        }
    }

@app.get("/api/calcular_antt")
def api_calcular_antt(dist_km: float, categoria: str, eixos: int, composicao: bool = True, alto_desempenho: bool = False, retorno_vazio: bool = False):
    return calcular_frete_antt_oficial(dist_km, categoria, eixos, composicao, alto_desempenho, retorno_vazio)

# ENDPOINT TRANSMISSÃO mTLS DA JCIOT

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
                    m = re.search(r"\b(\d{14})\b", val_str)
                    if m:
                        cnpj = m.group(1)
                        break
        
        common_name = ""
        for attr in cert.subject:
            if attr.oid == x509_oid.NameOID.COMMON_NAME:
                common_name = attr.value
                if not cnpj:
                    m = re.search(r"\b(\d{14})\b", common_name)
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

@app.post("/api/transmitir")
def transmitir_ciot(
    pfxFile: UploadFile = File(...),
    pfxPassword: str = Form(...),
    xmlPayload: str = Form(...)
):
    try:
        pfx_bytes = pfxFile.file.read()
        
        url_efrete = "https://hpef.ipcadm.com.br/pefws/adicionaroperacaotransporte.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "http://schemas.ipc.adm.br/efrete/pefV2/AdicionarOperacaoTransporte"
        }

        # Execução síncrona com timeout estrito de 20s
        res = pkcs12_post(
            url_efrete,
            data=xmlPayload.encode("utf-8"),
            headers=headers,
            pkcs12_data=pfx_bytes,
            pkcs12_password=pfxPassword,
            timeout=20
        )

        return {
            "status": "OK" if res.status_code == 200 else "ERRO_HTTP",
            "http_code": res.status_code,
            "response": res.text
        }
    except Exception as e:
        import traceback
        return {
            "status": "EXCECAO",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.get("/", response_class=HTMLResponse)
def index():
    caminho = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>templates/index.html não encontrado</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
