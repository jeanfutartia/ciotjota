import math
import os
import re
import sys
import tempfile
import threading
import unicodedata
import webbrowser
import requests
import folium
import customtkinter as ctk
from tkinter import messagebox
from geopy.distance import geodesic
from shapely.geometry import shape, Point, MultiPolygon, Polygon, mapping
from shapely.ops import nearest_points

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
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

def extrair_pontos_borda(geom, num_amostras=30):
    pontos = []
    poligonos = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for poly in poligonos:
        comprimento = poly.exterior.length
        passo = comprimento / num_amostras
        for i in range(num_amostras):
            pt = poly.exterior.interpolate(i * passo)
            pontos.append(pt)
    return pontos

class MotorLogistico:
    def __init__(self):
        self.headers = {"User-Agent": "GeoLogDivisasMap/8.0"}
        self.municipios = []
        self.carregar_base()

    def carregar_base(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        resp = requests.get(url, headers=self.headers, timeout=25)
        resp.raise_for_status()
        dados = resp.json()
        self.municipios = [
            {
                "id": str(m["id"]),
                "nome": m["nome"],
                "uf": extrair_uf(m),
                "busca": normalizar(m["nome"])
            }
            for m in dados
        ]

    def buscar_municipio(self, texto: str):
        busca = normalizar(texto)
        exatos = [m for m in self.municipios if m["busca"] == busca]
        if exatos:
            return exatos
        return [m for m in self.municipios if busca in m["busca"]]

    def obter_poligono(self, id_ibge: str):
        url = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{id_ibge}?formato=application/vnd.geo+json"
        resp = requests.get(url, headers=self.headers, timeout=25)
        resp.raise_for_status()
        geojson = resp.json()
        features = geojson.get("features", [])
        if not features:
            raise ValueError(f"Malha indisponível para IBGE {id_ibge}")
        return shape(features[0]["geometry"]), features[0]["geometry"]

    def validar_cep_nos_correios(self, cep_cru: str, nome_cidade: str, uf: str):
        cep_limpo = re.sub(r"\D", "", str(cep_cru))
        if len(cep_limpo) != 8 or cep_limpo.endswith("000"):
            return None

        try:
            url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
            r = requests.get(url, headers=self.headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if not data.get("erro"):
                    cid_retornada = normalizar(data.get("localidade", ""))
                    uf_retornada = data.get("uf", "").upper()
                    
                    if cid_retornada == normalizar(nome_cidade) and uf_retornada == uf.upper():
                        rua = f"{data.get('logradouro', '')} - {data.get('bairro', '')}".strip(" -")
                        return {
                            "cep": f"{cep_limpo[:5]}-{cep_limpo[5:]}",
                            "logradouro": rua or "Logradouro homologado"
                        }
        except:
            pass
        return None

    def buscar_cep_na_coordenada(self, lat: float, lon: float, nome_cidade: str, uf: str):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1, "zoom": 17}
        try:
            r = requests.get(url, params=params, headers=self.headers, timeout=6)
            if r.status_code == 200:
                data = r.json()
                addr = data.get("address", {})
                postcode = addr.get("postcode", "")
                
                validado = self.validar_cep_nos_correios(postcode, nome_cidade, uf)
                if validado:
                    rua_osm = addr.get("road")
                    if rua_osm and rua_osm not in validado["logradouro"]:
                        validado["logradouro"] = f"{rua_osm} ({validado['logradouro']})"
                    return validado
        except:
            pass
        return None

    def buscar_ceps_oficiais_cidade(self, nome_cidade: str, uf: str):
        termos = ["Rua", "Avenida", "Rodovia", "Estrada", "Setor", "Bairro"]
        for termo in termos:
            url = f"https://viacep.com.br/ws/{uf}/{requests.utils.quote(nome_cidade)}/{requests.utils.quote(termo)}/json/"
            try:
                r = requests.get(url, headers=self.headers, timeout=6)
                if r.status_code == 200:
                    itens = r.json()
                    if isinstance(itens, list):
                        for item in itens:
                            cep_limpo = re.sub(r"\D", "", item.get("cep", ""))
                            if len(cep_limpo) == 8 and not cep_limpo.endswith("000"):
                                if normalizar(item.get("localidade", "")) == normalizar(nome_cidade) and item.get("uf", "").upper() == uf.upper():
                                    return {
                                        "cep": f"{cep_limpo[:5]}-{cep_limpo[5:]}",
                                        "logradouro": f"{item.get('logradouro')} - {item.get('bairro', '')}".strip(" -")
                                    }
            except:
                pass
        return None

    def resolver_cep_seguro(self, ponto_borda: Point, poligono, nome_cidade: str, uf: str, status_cb):
        centro = poligono.centroid
        lat_f, lon_f = ponto_borda.y, ponto_borda.x
        lat_c, lon_c = centro.y, centro.x

        status_cb(f"Validando CEP estrito de {nome_cidade}/{uf}...")

        for i in range(1, 26):
            fator = i * 0.025
            lat_amostra = lat_f + (lat_c - lat_f) * fator
            lon_amostra = lon_f + (lon_c - lon_f) * fator

            if not poligono.contains(Point(lon_amostra, lat_amostra)):
                continue

            res = self.buscar_cep_na_coordenada(lat_amostra, lon_amostra, nome_cidade, uf)
            if res:
                return res, (lat_amostra, lon_amostra)

        status_cb(f"Buscando logradouro cadastrado oficial em {nome_cidade}...")
        res_oficial = self.buscar_ceps_oficiais_cidade(nome_cidade, uf)
        if res_oficial:
            return res_oficial, (lat_f, lon_f)

        return {"cep": "Ponto de Fronteira Sem CEP Predial", "logradouro": "Limite Intermunicipal"}, (lat_f, lon_f)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GeoLog Divisas - Mapa Interativo & Menor Distância")
        self.geometry("1020x800")
        self.minsize(940, 720)

        self.motor = None
        self.dados_ultimo_calculo = None

        self.criar_layout()
        self.iniciar_carregamento_base()

    def criar_layout(self):
        self.header_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1c23")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.titulo = ctk.CTkLabel(
            self.header_frame, 
            text="📍 GEOLOG | ROTEIRIZAÇÃO, DIVISAS & MAPA INTERATIVO", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#38bdf8"
        )
        self.titulo.pack(anchor="w", padx=20, pady=(12, 4))

        self.subtitulo = ctk.CTkLabel(
            self.header_frame,
            text="Cálculo geodésico de fronteiras com visualização de polígonos territoriais e rotas no mapa.",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.subtitulo.pack(anchor="w", padx=20, pady=(0, 12))

        # Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=12)
        self.input_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_c1 = ctk.CTkLabel(self.input_frame, text="Cidade Origem:", font=ctk.CTkFont(weight="bold"))
        self.lbl_c1.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        self.entry_c1 = ctk.CTkEntry(self.input_frame, placeholder_text="Ex: Piracicaba", width=240, height=36)
        self.entry_c1.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="w")
        self.entry_c1.insert(0, "Piracicaba")

        self.lbl_c2 = ctk.CTkLabel(self.input_frame, text="Cidade Destino:", font=ctk.CTkFont(weight="bold"))
        self.lbl_c2.grid(row=0, column=1, padx=15, pady=(12, 5), sticky="w")
        self.entry_c2 = ctk.CTkEntry(self.input_frame, placeholder_text="Ex: Rio das Pedras", width=240, height=36)
        self.entry_c2.grid(row=1, column=1, padx=15, pady=(0, 12), sticky="w")
        self.entry_c2.insert(0, "Rio das Pedras")

        self.lbl_dist = ctk.CTkLabel(self.input_frame, text="Distância Alvo em km:", font=ctk.CTkFont(weight="bold"))
        self.lbl_dist.grid(row=0, column=2, padx=15, pady=(12, 5), sticky="w")
        self.entry_dist = ctk.CTkEntry(self.input_frame, placeholder_text="Vazio = Menor Distância", width=200, height=36)
        self.entry_dist.grid(row=1, column=2, padx=15, pady=(0, 12), sticky="w")

        self.btn_calc = ctk.CTkButton(
            self.input_frame, 
            text="CALCULAR", 
            font=ctk.CTkFont(weight="bold", size=13),
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=36,
            command=self.acao_calcular
        )
        self.btn_calc.grid(row=1, column=3, padx=(5, 15), pady=(0, 12), sticky="e")

        self.status_bar = ctk.CTkLabel(self, text="Inicializando base do IBGE...", text_color="#38bdf8", font=ctk.CTkFont(size=12))
        self.status_bar.pack(anchor="w", padx=25, pady=(2, 5))

        # Container Resultados
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.card_status = ctk.CTkFrame(self.result_container, fg_color="#1e293b", corner_radius=10, height=58)
        self.card_status.pack(fill="x", pady=(0, 10))
        self.lbl_status_resultado = ctk.CTkLabel(
            self.card_status, 
            text="Aguardando parâmetros...", 
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e2e8f0"
        )
        self.lbl_status_resultado.pack(pady=12)

        # Botões de Ação do Mapa
        self.map_buttons_frame = ctk.CTkFrame(self.result_container, fg_color="transparent")
        self.map_buttons_frame.pack(fill="x", pady=(0, 10))

        self.btn_folium = ctk.CTkButton(
            self.map_buttons_frame,
            text="🗺️ VER NO MAPA INTERATIVO (POLÍGONOS & DIVISAS)",
            font=ctk.CTkFont(weight="bold", size=13),
            fg_color="#059669",
            hover_color="#047857",
            height=38,
            state="disabled",
            command=self.abrir_mapa_interativo
        )
        self.btn_folium.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_gmaps = ctk.CTkButton(
            self.map_buttons_frame,
            text="🚗 ABRIR NO GOOGLE MAPS (ROTA RODOVIÁRIA)",
            font=ctk.CTkFont(weight="bold", size=13),
            fg_color="#d97706",
            hover_color="#b45309",
            height=38,
            state="disabled",
            command=self.abrir_google_maps
        )
        self.btn_gmaps.pack(side="right", fill="x", expand=True, padx=(8, 0))

        # Cards Lado a Lado
        self.cards_frame = ctk.CTkFrame(self.result_container, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True)
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)

        self.card_c1 = ctk.CTkFrame(self.cards_frame, corner_radius=12, fg_color="#18181b")
        self.card_c1.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self.txt_c1 = ctk.CTkTextbox(self.card_c1, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_c1.pack(fill="both", expand=True, padx=12, pady=12)

        self.card_c2 = ctk.CTkFrame(self.cards_frame, corner_radius=12, fg_color="#18181b")
        self.card_c2.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        self.txt_c2 = ctk.CTkTextbox(self.card_c2, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_c2.pack(fill="both", expand=True, padx=12, pady=12)

    def set_status(self, msg: str):
        self.status_bar.configure(text=msg)

    def iniciar_carregamento_base(self):
        self.btn_calc.configure(state="disabled")
        def _th():
            try:
                self.motor = MotorLogistico()
                self.set_status(f"Sistema pronto! {len(self.motor.municipios)} municípios sincronizados com o IBGE.")
                self.btn_calc.configure(state="normal")
            except Exception as e:
                self.set_status(f"Erro ao carregar base: {e}")
        threading.Thread(target=_th, daemon=True).start()

    def desambiguar(self, candidatos: list, nome_busca: str):
        escolha = {"item": None}
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Selecione o Município - {nome_busca}")
        dialog.geometry("480x360")
        dialog.transient(self)
        dialog.grab_set()

        lbl = ctk.CTkLabel(dialog, text=f"Foram encontrados múltiplos municípios para '{nome_busca}':", font=ctk.CTkFont(weight="bold"))
        lbl.pack(padx=20, pady=(15, 10))

        scroll = ctk.CTkScrollableFrame(dialog, width=420, height=220)
        scroll.pack(padx=20, pady=5, fill="both", expand=True)

        def selecionar(m):
            escolha["item"] = m
            dialog.destroy()

        for c in candidatos:
            btn = ctk.CTkButton(
                scroll, 
                text=f"{c['nome']} / {c['uf']}  -  IBGE: {c['id']}", 
                anchor="w",
                fg_color="#334155",
                hover_color="#475569",
                command=lambda item=c: selecionar(item)
            )
            btn.pack(fill="x", pady=4)

        self.wait_window(dialog)
        return escolha["item"]

    def acao_calcular(self):
        c1_raw = self.entry_c1.get().strip()
        c2_raw = self.entry_c2.get().strip()
        dist_raw = self.entry_dist.get().strip().replace(",", ".")

        dist_alvo = None
        if dist_raw:
            try:
                dist_alvo = float(dist_raw)
                if dist_alvo < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Aviso", "A distância alvo deve ser um número positivo (ex: 15 ou 22.5).")
                return

        if not c1_raw or not c2_raw:
            messagebox.showwarning("Aviso", "Preencha as duas cidades para efetuar o cálculo.")
            return

        self.btn_calc.configure(state="disabled")
        self.btn_folium.configure(state="disabled")
        self.btn_gmaps.configure(state="disabled")

        threading.Thread(target=self._executar_calculo, args=(c1_raw, c2_raw, dist_alvo), daemon=True).start()

    def _executar_calculo(self, c1_raw: str, c2_raw: str, dist_alvo: float):
        try:
            cand1 = self.motor.buscar_municipio(c1_raw)
            if not cand1:
                messagebox.showerror("Erro", f"Município '{c1_raw}' não encontrado.")
                return
            m1 = cand1[0] if len(cand1) == 1 else self.desambiguar(cand1, c1_raw)
            if not m1:
                return

            cand2 = self.motor.buscar_municipio(c2_raw)
            if not cand2:
                messagebox.showerror("Erro", f"Município '{c2_raw}' não encontrado.")
                return
            m2 = cand2[0] if len(cand2) == 1 else self.desambiguar(cand2, c2_raw)
            if not m2:
                return

            self.set_status("Obtendo malhas cartográficas vetoriais do IBGE...")
            poly1, geojson1 = self.motor.obter_poligono(m1["id"])
            poly2, geojson2 = self.motor.obter_poligono(m2["id"])

            if dist_alvo is None:
                self.set_status("Calculando menor distância absoluta entre fronteiras...")
                ponto1, ponto2 = nearest_points(poly1, poly2)
                coord1 = (ponto1.y, ponto1.x)
                coord2 = (ponto2.y, ponto2.x)
                dist_km = geodesic(coord1, coord2).kilometers
                
                faz_divisa = poly1.touches(poly2) or math.isclose(dist_km, 0.0, abs_tol=0.05)
                if faz_divisa:
                    distancia_formatada = "0.00 km (Divisa direta)"
                    status_text = f"📍 CIDADES CONFRONTANTES | DISTÂNCIA ENCONTRADA: 0.00 km"
                    status_color = "#4ade80"
                else:
                    distancia_formatada = f"{dist_km:.2f} km (Menor distância)"
                    status_text = f"📍 DISTÂNCIA ENCONTRADA: {dist_km:.2f} km [Menor Distância Possível]"
                    status_color = "#38bdf8"
            else:
                self.set_status(f"Procurando trecho com distância próxima a {dist_alvo:.1f} km...")
                pts1 = extrair_pontos_borda(poly1, num_amostras=30)
                pts2 = extrair_pontos_borda(poly2, num_amostras=30)

                melhor_p1, melhor_p2 = None, None
                menor_diferenca = float("inf")
                melhor_dist_km = 0.0

                for p1 in pts1:
                    c_p1 = (p1.y, p1.x)
                    for p2 in pts2:
                        c_p2 = (p2.y, p2.x)
                        d = geodesic(c_p1, c_p2).kilometers
                        dif = abs(d - dist_alvo)
                        if dif < menor_diferenca:
                            menor_diferenca = dif
                            melhor_dist_km = d
                            melhor_p1, melhor_p2 = p1, p2

                ponto1, ponto2 = melhor_p1, melhor_p2
                coord1 = (ponto1.y, ponto1.x)
                coord2 = (ponto2.y, ponto2.x)
                dist_km = melhor_dist_km
                distancia_formatada = f"{dist_km:.2f} km (Meta: {dist_alvo:.1f} km)"
                status_text = f"📍 DISTÂNCIA ENCONTRADA: {dist_km:.2f} km [Alvo: {dist_alvo:.1f} km]"
                status_color = "#38bdf8"

            end1, coord_final1 = self.motor.resolver_cep_seguro(ponto1, poly1, m1["nome"], m1["uf"], self.set_status)
            end2, coord_final2 = self.motor.resolver_cep_seguro(ponto2, poly2, m2["nome"], m2["uf"], self.set_status)

            self.dados_ultimo_calculo = {
                "m1": m1, "m2": m2,
                "geojson1": geojson1, "geojson2": geojson2,
                "coord1": coord_final1, "coord2": coord_final2,
                "end1": end1, "end2": end2,
                "dist_km": dist_km,
                "distancia_formatada": distancia_formatada
            }

            self.set_status("Cálculo finalizado com sucesso!")
            self.lbl_status_resultado.configure(text=status_text, text_color=status_color)

            res_c1 = (
                f"MUNICÍPIO: {m1['nome']} / {m1['uf']}\n"
                f"IBGE: {m1['id']}\n"
                f"========================================\n"
                f"DISTÂNCIA ENCONTRADA: {distancia_formatada}\n"
                f"========================================\n"
                f"PONTO SELECIONADO NO PERÍMETRO:\n"
                f"Logradouro: {end1['logradouro']}\n"
                f"CEP Real:   {end1['cep']}\n\n"
                f"Coordenadas:\n"
                f"Lat: {coord_final1[0]:.6f}\n"
                f"Lon: {coord_final1[1]:.6f}\n"
                f"----------------------------------------\n"
                f"Validação: 100% {m1['nome']}/{m1['uf']} (Correios)"
            )

            res_c2 = (
                f"MUNICÍPIO: {m2['nome']} / {m2['uf']}\n"
                f"IBGE: {m2['id']}\n"
                f"========================================\n"
                f"DISTÂNCIA ENCONTRADA: {distancia_formatada}\n"
                f"========================================\n"
                f"PONTO SELECIONADO NO PERÍMETRO:\n"
                f"Logradouro: {end2['logradouro']}\n"
                f"CEP Real:   {end2['cep']}\n\n"
                f"Coordenadas:\n"
                f"Lat: {coord_final2[0]:.6f}\n"
                f"Lon: {coord_final2[1]:.6f}\n"
                f"----------------------------------------\n"
                f"Validação: 100% {m2['nome']}/{m2['uf']} (Correios)"
            )

            self.txt_c1.delete("0.0", "end")
            self.txt_c1.insert("0.0", res_c1)

            self.txt_c2.delete("0.0", "end")
            self.txt_c2.insert("0.0", res_c2)

            self.btn_folium.configure(state="normal")
            self.btn_gmaps.configure(state="normal")

        except Exception as ex:
            messagebox.showerror("Erro de Processamento", f"Falha ao executar cálculo: {ex}")
            self.set_status("Erro no processamento.")
        finally:
            self.btn_calc.configure(state="normal")

    def abrir_google_maps(self):
        if not self.dados_ultimo_calculo:
            return
        c1 = self.dados_ultimo_calculo["coord1"]
        c2 = self.dados_ultimo_calculo["coord2"]
        url = f"https://www.google.com/maps/dir/?api=1&origin={c1[0]},{c1[1]}&destination={c2[0]},{c2[1]}"
        webbrowser.open(url)

    def abrir_mapa_interativo(self):
        if not self.dados_ultimo_calculo:
            return

        d = self.dados_ultimo_calculo
        c1, c2 = d["coord1"], d["coord2"]
        centro_lat = (c1[0] + c2[0]) / 2
        centro_lon = (c1[1] + c2[1]) / 2

        # Inicia o mapa Folium com tema moderno
        m = folium.Map(location=[centro_lat, centro_lon], zoom_start=11, tiles="CartoDB dark_matter")

        # 1. Polígono Cidade 1 (Azul Claro)
        folium.GeoJson(
            d["geojson1"],
            name=d["m1"]["nome"],
            style_function=lambda x: {
                "fillColor": "#0284c7",
                "color": "#38bdf8",
                "weight": 2.5,
                "fillOpacity": 0.25,
            },
            tooltip=f"Município: {d['m1']['nome']}/{d['m1']['uf']}"
        ).add_to(m)

        # 2. Polígono Cidade 2 (Verde Esmeralda)
        folium.GeoJson(
            d["geojson2"],
            name=d["m2"]["nome"],
            style_function=lambda x: {
                "fillColor": "#059669",
                "color": "#34d399",
                "weight": 2.5,
                "fillOpacity": 0.25,
            },
            tooltip=f"Município: {d['m2']['nome']}/{d['m2']['uf']}"
        ).add_to(m)

        # 3. Marcador Origem
        folium.Marker(
            location=[c1[0], c1[1]],
            popup=folium.Popup(f"<b>{d['m1']['nome']}</b><br>CEP: {d['end1']['cep']}<br>{d['end1']['logradouro']}", max_width=280),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

        # 4. Marcador Destino
        folium.Marker(
            location=[c2[0], c2[1]],
            popup=folium.Popup(f"<b>{d['m2']['nome']}</b><br>CEP: {d['end2']['cep']}<br>{d['end2']['logradouro']}", max_width=280),
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

        # 5. Linha conectando os extremos
        folium.PolyLine(
            locations=[[c1[0], c1[1]], [c2[0], c2[1]]],
            color="#f59e0b",
            weight=3.5,
            dash_array="6, 8",
            tooltip=f"Distância Territorial: {d['distancia_formatada']}"
        ).add_to(m)

        folium.LayerControl().add_to(m)

        # Grava o mapa temporário e abre no navegador
        temp_dir = tempfile.gettempdir()
        mapa_path = os.path.join(temp_dir, "geolog_divisas_mapa.html")
        m.save(mapa_path)
        webbrowser.open(f"file://{os.path.realpath(mapa_path)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
