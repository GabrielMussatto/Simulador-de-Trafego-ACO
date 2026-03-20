# 🐜 Simulador de Tráfego ACO - Palmas

Este projeto é um simulador de tráfego urbano que utiliza o algoritmo de **Otimização por Colônia de Formigas (ACO)** para encontrar rotas otimizadas em um recorte do mapa de **Palmas, Tocantins**. O sistema simula múltiplos agentes (veículos) que aprendem o melhor caminho através do depósito e evaporação de feromônios sintéticos.

## 🏗️ Arquitetura do Projeto

O código foi refatorado utilizando **Orientação a Objetos (POO)**, dividindo as responsabilidades em classes para facilitar a manutenção:

* **`main.py`**: Ponto de entrada que gerencia a alternância entre o menu e a simulação.
* **`simulation.py`**: Contém a classe `SimuladorACO`, responsável pelo loop principal do Pygame, lógica de feromônios e interface do dashboard.
* **`veiculo.py`**: Contém a classe `Veiculo`, que define o comportamento de movimentação, decisão de rota e estado individual de cada agente.
* **`relatorio.py`**: Contém a classe `RelatorioPDF`, que processa os dados da simulação e exporta os resultados técnicos em PDF.
* **`maps.py`**: Define a topologia da cidade (nós e arestas) com base em coordenadas de pixels da imagem real.
* **`menu.py`**: Interface gráfica para seleção dos pontos de origem e destino.

---

## 🧠 Funcionamento do Algoritmo (ACO)

A simulação busca a convergência para a rota mais rápida através de ciclos repetitivos:

1.  **Exploração**: Os veículos escolhem caminhos baseados em pesos (feromônios). Ruas com mais feromônio têm maior probabilidade de escolha.
2.  **Premiação**: O veículo que chega primeiro ao destino reforça a sua rota com mais feromônio, "ensinando" a colônia.
3.  **Evaporação**: A cada ciclo, os feromônios evaporam em uma taxa de 50% ($\rho = 0.5$), o que permite que a colônia "esqueça" rotas ruins e se adapte a novas descobertas.
4.  **Otimização**: Com o tempo, a trilha de feromônio mais forte indicará o caminho mais eficiente entre os dois pontos selecionados.

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado e as bibliotecas listadas no `requirements.txt`:
```bash
pip install pygame networkx matplotlib fpdf
```

### Execução
Inicie o sistema pelo arquivo principal:
```bash
python main.py
```

## 📊 Recursos do Dashboard

* **Tracking em Tempo Real**: Monitoramento individual de cada carro, exibindo posição, quantidade de passos e a rota parcial percorrida.
* **Recordes da Colônia**: Exibição em tempo real do menor tempo histórico atingido e da rota com menos passos encontrada até o momento.
* **Relatório Técnico**: Ao clicar no botão de encerramento, o sistema processa o histórico de iterações e gera o arquivo `relatorio_final_aco.pdf` com estatísticas de evolução.

## Colaboradores
* Gabriel Mussatto Silva
* Kethelen Victoria de Souza Parra
* Erick Meneses de Sousa
* Hugo Valuar Bailona
* Leticia Espindola
* Pedro Vieira
