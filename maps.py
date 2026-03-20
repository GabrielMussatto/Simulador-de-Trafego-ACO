import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

IMG_PATH = "maps.jpeg" # caminho para a imagem do mapa

def build_palmas_graph_px():
    """
    Grafo aproximado (coordenadas em pixels) baseado no print.
    Ajuste fino: mexa só no dict POS (x,y).
    """
    G = nx.DiGraph()

    # ---- Nós (interseções/waypoints) em pixels (x, y) ----
    # (0,0) é canto superior esquerdo
    POS = {
        # Origem/área UFT
        "UFT": (150, 145),
        # Destino/área HGP
        "HGP": (675, 540),
        #Rotatorias
        "R1": (335, 35),
        "R2": (440, 55),
        'R3': (545, 55),
        "H.PLAZA": (675, 50),
        "R5": (145, 230),
        "R6": (545, 230),
        "GIRASSOIS": (675, 230),
        "HIIT": (150, 405),
        "R9": (545, 405),
        "PALMAS.S": (675, 330),
        "R11": (760, 330),
        "R12": (675, 405),
        "R14": (150, 545),
        "R15": (765, 540),
        "R16": (235, 230),
        "R17": (320, 230),
        "R18": (280, 405),
        "R19": (380, 405),
        "CLINICA": (280, 545),
        "R21": (380, 540),
        "CAPIM.D": (440, 230),
        
    }

    for n, (x, y) in POS.items():
        G.add_node(n, x=x, y=y)

    def add(u, v, w=1.0):
        G.add_edge(u, v, weight=w)
        G.add_edge(v, u, weight=w)  # bidirecional (rua dupla) – remova se quiser mão única

    # ---- Arestas (ruas) ----
    add("UFT", "R1")
    add("R1", "R2")
    add("R2", "R3")
    add("R3", "H.PLAZA")
    add("R3", "R6")
    add("H.PLAZA", "GIRASSOIS")
    add("UFT", "R5")
    add("R5", "R16")
    add("R16", "R17")
    add("R17", "CAPIM.D")
    add("CAPIM.D", "R6")
    add("R16", "R18")
    add("R18", "CLINICA")
    add("R17", "R19")
    add("R19", "R21")
    add("R6", "GIRASSOIS")
    add("R6", "R9")
    add("GIRASSOIS", "PALMAS.S")
    add("PALMAS.S", "R11")
    add("PALMAS.S", "R12")
    add("R9", "R12")
    add("R12", "HGP")
    add("R11", "R15")
    add("R5", "HIIT")
    add("R15", "HGP")
    add("HIIT", "R14")
    add("R14", "CLINICA")
    add("CLINICA", "R21")
    add("HIIT", "R18")
    add("R18", "R19")
    add("R21", "HGP")
    
    return G

def draw_overlay(G, img_path=IMG_PATH):
    img = mpimg.imread(img_path)
    plt.figure(figsize=(11, 8))
    plt.imshow(img, alpha=0.5, zorder=1)  # imagem de fundo com transparência
    plt.axis("off")

    # desenha arestas
    for u, v in G.edges():
        x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
        x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
        plt.plot([x1, x2], [y1, y2], linewidth=2, color="black", zorder=2)

    # desenha nós
    for n in G.nodes():
        x, y = G.nodes[n]["x"], G.nodes[n]["y"]
        plt.scatter(x, y, s=60, color="black", zorder=3)

    # rótulos
    for n in ["UFT", "HGP", "H.PLAZA", "GIRASSOIS", "HIIT", "PALMAS.S", "CLINICA", "CAPIM.D"]:
        plt.text(G.nodes[n]["x"] - 30, G.nodes[n]["y"] - 6, n, fontsize=10)

    plt.show()
