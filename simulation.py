import pygame
import time
from maps import build_palmas_graph_px, IMG_PATH
from veiculo import Veiculo
from relatorio import RelatorioPDF

class SimuladorACO:
    # Configurações de Cores e Estilo
    COR_FUNDO_JANELA = (30, 33, 39) 
    COR_FUNDO_MAPA = (255, 255, 255)
    COR_TEXTO = (0, 0, 0)
    COR_SIDEBAR = (33, 37, 43) 
    COR_BRANCO = (255, 255, 255)
    COR_VERDE_DASH = (152, 195, 121)
    CORES_VEICULOS = [(0, 0, 255), (255, 165, 0), (150, 0, 200), (0, 255, 255), (255, 20, 147)]

    def __init__(self, origem, destino):
        pygame.init()
        self.origem = origem
        self.destino = destino
        self.G = build_palmas_graph_px()
        self.img = pygame.image.load(IMG_PATH)
        self.img.set_alpha(128)
        
        # Dimensões e Posicionamento
        largura_mapa, altura_mapa = self.img.get_rect().size
        self.LARGURA_SIDEBAR, self.ALTURA_FIXA = 550, 900
        self.largura_mapa = largura_mapa
        self.altura_janela = max(altura_mapa, self.ALTURA_FIXA)
        self.offset_y = (self.altura_janela - altura_mapa) // 2
        
        self.tela = pygame.display.set_mode((largura_mapa + self.LARGURA_SIDEBAR, self.altura_janela))
        pygame.display.set_caption(f"ACO Dashboard: {origem} -> {destino}")
        
        # Fontes e Interface
        self.fonte = pygame.font.SysFont("Arial", 12, bold=True)
        self.fonte_hud = pygame.font.SysFont("Consolas", 15)
        self.fonte_titulo = pygame.font.SysFont("Arial", 20, bold=True)
        self.botao_rect = pygame.Rect(largura_mapa + 50, self.altura_janela - 80, 450, 50)
        
        # Lógica ACO
        self.feromonios = {edge: 1.0 for edge in self.G.edges()}
        self.rho = 0.5
        self.iteracao = 1
        
        # Controle de Tempo e Pausa
        self.pausado = False
        self.tempo_pausa_inicio = 0
        self.tempo_inicio_ciclo = time.time()
        
        # Recordes e Histórico
        self.melhor_tempo_geral = float('inf')
        self.menor_passos_geral = float('inf')
        self.melhor_rota_geral = []
        self.historico_tempos = []
        self.dados_para_pdf = []
        self.primeiro_a_chegar_id = None
        self.tempo_venc_individual = 0
        
        # Inicialização de Objetos
        self.veiculos = [Veiculo(id_v, self.G, self.CORES_VEICULOS[id_v], origem, destino) for id_v in range(5)]
        self.locais_importantes = ["UFT", "HGP", "H.PLAZA", "GIRASSOIS", "HIIT", "PALMAS.S", "CLINICA", "CAPIM.D"]
        self.relogio = pygame.time.Clock()

    def desenhar_mapa(self):
        """Renderiza o fundo, o grafo e os feromônios."""
        pygame.draw.rect(self.tela, self.COR_FUNDO_MAPA, (0, self.offset_y, self.largura_mapa, self.img.get_height()))
        self.tela.blit(self.img, (0, self.offset_y))

        # Arestas (Feromônios)
        for u, v in self.G.edges():
            p1 = (self.G.nodes[u]['x'], self.G.nodes[u]['y'] + self.offset_y)
            p2 = (self.G.nodes[v]['x'], self.G.nodes[v]['y'] + self.offset_y)
            pygame.draw.line(self.tela, (70, 70, 70), p1, p2, max(1, int(self.feromonios[(u, v)] * 1.5)))

        # Nós
        for n in self.G.nodes():
            pos = (self.G.nodes[n]['x'], self.G.nodes[n]['y'] + self.offset_y)
            cor = (255,0,0) if n == self.origem else (0,255,0) if n == self.destino else (0,0,0)
            pygame.draw.circle(self.tela, cor, pos, 6)
            if n in self.locais_importantes: 
                self.tela.blit(self.fonte.render(n, True, self.COR_TEXTO), (pos[0] + 10, pos[1] - 15))

    def desenhar_sidebar(self, tempo_decorrido):
        """Renderiza todas as informações de texto no painel lateral."""
        pygame.draw.rect(self.tela, self.COR_SIDEBAR, (self.largura_mapa, 0, self.LARGURA_SIDEBAR, self.altura_janela))
        x_text = self.largura_mapa + 25
        self.tela.blit(self.fonte_titulo.render("RELATORIO DE PERFORMANCE ACO", True, self.COR_BRANCO), (x_text, 30))
        
        if self.pausado:
            self.tela.blit(self.fonte_titulo.render("|| SIMULACAO PAUSADA (ESPACO)", True, (255, 165, 0)), (x_text, 65))
        else:
            pygame.draw.line(self.tela, self.COR_BRANCO, (x_text, 65), (x_text + 500, 65), 2)

        y_off = 100
        media_tempo = f"{sum(self.historico_tempos)/len(self.historico_tempos):.2f}s" if self.historico_tempos else "Calculando..."
        
        infos_globais = [
            f">> ITERACAO ATUAL: {self.iteracao}",
            f">> TEMPO DO CICLO: {tempo_decorrido:.2f}s",
            f">> PRIMEIRO A CHEGAR: Carro {self.primeiro_a_chegar_id if self.primeiro_a_chegar_id is not None else '---'}",
            f">> MEDIA DE TEMPO: {media_tempo}",
        ]
        for info in infos_globais:
            self.tela.blit(self.fonte_hud.render(info, True, self.COR_VERDE_DASH), (x_text, y_off))
            y_off += 35

        y_off += 15
        self.tela.blit(self.fonte_titulo.render("RECORDES DA COLONIA:", True, self.COR_BRANCO), (x_text, y_off))
        y_off += 40
        
        m_tempo = f"{self.melhor_tempo_geral:.2f}s" if self.melhor_tempo_geral != float('inf') else "---"
        m_passos = f"{int(self.menor_passos_geral)}" if self.menor_passos_geral != float('inf') else "---"
        
        recordes = [f"MENOR TEMPO ATE DESTINO: {m_tempo}", f"MENOR ROTA (EM PASSOS): {m_passos}"]
        for rec in recordes:
            self.tela.blit(self.fonte_hud.render(rec, True, self.COR_BRANCO), (x_text, y_off))
            y_off += 30

        y_off += 25
        self.tela.blit(self.fonte_titulo.render("TRACKING INDIVIDUAL:", True, self.COR_BRANCO), (x_text, y_off))
        y_off += 40
        for v in self.veiculos:
            p_rota = [str(e[1]) for e in v.caminho_percorrido[-4:]]
            r_parcial = " -> ".join(p_rota) if p_rota else "Iniciando..."
            txt_v = f"Carro {v.id}: {'CHEGOU!' if v.chegou else f'No nó: {v.no_atual}'} | Passos: {len(v.caminho_percorrido)}"
            pygame.draw.circle(self.tela, v.cor, (x_text + 10, y_off + 8), 8)
            self.tela.blit(self.fonte_hud.render(txt_v, True, self.COR_BRANCO), (x_text + 30, y_off))
            y_off += 25
            self.tela.blit(self.fonte_hud.render(f"      Rota: ...{r_parcial}", True, (170, 170, 170)), (x_text + 30, y_off))
            y_off += 35

        y_off += 15
        self.tela.blit(self.fonte_titulo.render("MELHOR ROTA (MEMORIA):", True, self.COR_BRANCO), (x_text, y_off))
        y_off += 45
        if self.melhor_rota_geral:
            r_form = " -> ".join(self.melhor_rota_geral)
            if len(r_form) > 55:
                self.tela.blit(self.fonte_hud.render(r_form[:55], True, self.COR_VERDE_DASH), (x_text, y_off))
                self.tela.blit(self.fonte_hud.render(r_form[55:], True, self.COR_VERDE_DASH), (x_text, y_off + 22))
            else: 
                self.tela.blit(self.fonte_hud.render(r_form, True, self.COR_VERDE_DASH), (x_text, y_off))

        pygame.draw.rect(self.tela, self.COR_VERDE_DASH, self.botao_rect, border_radius=10)
        texto_btn = self.fonte_titulo.render("GERAR RELATORIO E VOLTAR AO MENU", True, self.COR_BRANCO)
        self.tela.blit(texto_btn, (self.botao_rect.centerx - texto_btn.get_width()//2, self.botao_rect.centery - texto_btn.get_height()//2))

    def atualizar_aco(self):
        """Finaliza o ciclo, atualiza feromônios e reseta veículos."""
        tempo_ciclo_total = time.time() - self.tempo_inicio_ciclo
        self.historico_tempos.append(tempo_ciclo_total)
        
        for edge in self.feromonios: self.feromonios[edge] *= self.rho
        
        v_venc = next(v for v in self.veiculos if v.id == self.primeiro_a_chegar_id)
        passos_venc = len(v_venc.caminho_percorrido)
        rota_venc = " -> ".join([self.origem] + [e[1] for e in v_venc.caminho_percorrido])
        
        self.dados_para_pdf.append({
            'it': self.iteracao, 'vencedor': self.primeiro_a_chegar_id, 'passos': passos_venc,
            'tempo_venc': self.tempo_venc_individual, 'tempo_ciclo': tempo_ciclo_total, 'rota': rota_venc
        })
        
        if passos_venc < self.menor_passos_geral:
            self.menor_passos_geral, self.melhor_rota_geral = passos_venc, rota_venc.split(" -> ")
            
        for v in self.veiculos:
            delta_tau = 1.0 / len(v.caminho_percorrido)
            mult = 2.0 if v.id == self.primeiro_a_chegar_id else 1.0
            for edge in v.caminho_percorrido: self.feromonios[edge] += (delta_tau * mult)

        print("\n" + "="*40)
        print(f"RELATORIO CICLO {self.iteracao} | Vencedor: Carro {self.primeiro_a_chegar_id} | Tempo: {self.tempo_venc_individual:.2f}s")
        print("="*40)
        # Imprime apenas ruas que possuem feromônio acima do nível base ou que foram alteradas
        for edge, tau in self.feromonios.items():
            if tau > 0.5: # Mostra as ruas que ainda têm rastro relevante
                print(f"Rua {edge[0]} -> {edge[1]}: {tau:.4f}")
        print("="*40 + "\n")

        self.iteracao += 1
        self.primeiro_a_chegar_id, self.tempo_inicio_ciclo = None, time.time()
        for v in self.veiculos: v.resetar()

    def rodar(self):
        executando = True
        while executando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: executando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.pausado = not self.pausado
                    if self.pausado: self.tempo_pausa_inicio = time.time()
                    else: self.tempo_inicio_ciclo += (time.time() - self.tempo_pausa_inicio)
                if event.type == pygame.MOUSEBUTTONDOWN and self.botao_rect.collidepoint(event.pos):
                    executando = False 

            self.tela.fill(self.COR_FUNDO_JANELA)
            self.desenhar_mapa()

            todos_chegaram = True
            if not self.pausado:
                tempo_decorrido_agora = time.time() - self.tempo_inicio_ciclo
                for v in self.veiculos:
                    v.mover(self.feromonios)
                    if v.chegou and self.primeiro_a_chegar_id is None:
                        self.primeiro_a_chegar_id = v.id
                        self.tempo_venc_individual = tempo_decorrido_agora
                        if self.tempo_venc_individual < self.melhor_tempo_geral: 
                            self.melhor_tempo_geral = self.tempo_venc_individual
                    if not v.chegou: todos_chegaram = False
            else:
                todos_chegaram = False
                tempo_decorrido_agora = self.tempo_pausa_inicio - self.tempo_inicio_ciclo

            for v in self.veiculos:
                pos_v = (int(v.x), int(v.y) + self.offset_y)
                pygame.draw.circle(self.tela, v.cor, pos_v, v.raio) 
                pygame.draw.circle(self.tela, (0,0,0), pos_v, v.raio, 2)

            self.desenhar_sidebar(tempo_decorrido_agora)

            if todos_chegaram and not self.pausado:
                self.atualizar_aco()

            pygame.display.flip()
            self.relogio.tick(60)

        if self.iteracao > 1:
            RelatorioPDF.gerar(self.origem, self.destino, self.melhor_tempo_geral, self.menor_passos_geral, self.melhor_rota_geral, self.dados_para_pdf)
        pygame.quit()

# Ponto de entrada compatível com o main.py
def rodar_simulacao(origem, destino):
    simulador = SimuladorACO(origem, destino)
    simulador.rodar()