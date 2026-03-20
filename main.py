from menu import menu_inicial
from simulation import rodar_simulacao

if __name__ == "__main__":
    while True:
        # 1. Abre a tela de menu em um arquivo separado
        origem, destino = menu_inicial()
        
        # 2. Se o usuário confirmou os locais, inicia a simulação
        if not origem and not destino:
            break
        
        rodar_simulacao(origem, destino)