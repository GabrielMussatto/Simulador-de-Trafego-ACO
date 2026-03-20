import random

class Veiculo:
    def __init__(self, id, grafo, cor, origem, destino):
        self.id = id
        self.grafo = grafo
        self.cor = cor
        self.origem = origem
        self.destino = destino
        self.resetar()
        self.raio = 14 - (id * 2)

    def resetar(self):
        self.no_atual = self.origem
        self.no_anterior = None
        self.no_proximo = None
        self.progresso = 0.0
        self.chegou = False
        self.caminho_percorrido = [] 
        self.x, self.y = self.grafo.nodes[self.origem]['x'], self.grafo.nodes[self.origem]['y']

    def mover(self, feromonios):
        if self.chegou: return
        if self.no_proximo is None:
            vizinhos = list(self.grafo.neighbors(self.no_atual))
            if len(vizinhos) > 1 and self.no_anterior in vizinhos:
                vizinhos.remove(self.no_anterior)
            if vizinhos:
                pesos = [feromonios.get((self.no_atual, v), 1.0) for v in vizinhos]
                self.no_proximo = random.choices(vizinhos, weights=pesos, k=1)[0]
                self.caminho_percorrido.append((self.no_atual, self.no_proximo))
            else:
                if self.no_atual != self.destino: self.resetar()
                return 

        x1, y1 = self.grafo.nodes[self.no_atual]['x'], self.grafo.nodes[self.no_atual]['y']
        x2, y2 = self.grafo.nodes[self.no_proximo]['x'], self.grafo.nodes[self.no_proximo]['y']
        self.progresso += 0.015 
        self.x = x1 + (x2 - x1) * self.progresso
        self.y = y1 + (y2 - y1) * self.progresso
        if self.progresso >= 1.0:
            self.no_anterior = self.no_atual
            self.no_atual = self.no_proximo
            self.no_proximo = None
            self.progresso = 0.0
            if self.no_atual == self.destino: self.chegou = True