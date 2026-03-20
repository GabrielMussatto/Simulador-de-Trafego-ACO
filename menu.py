import pygame

def menu_inicial():
    pygame.init()
    tela = pygame.display.set_mode((805, 592))
    pygame.display.set_caption("Configuração da Simulação - Palmas")
    
    fonte_titulo = pygame.font.SysFont("Arial", 26, bold=True)
    fonte_item = pygame.font.SysFont("Arial", 20)
    fonte_aviso = pygame.font.SysFont("Arial", 16, bold=True)
    
    locais = ["UFT", "HGP", "H.PLAZA", "GIRASSOIS", "HIIT", "PALMAS.S", "CLINICA", "CAPIM.D"]
    origem_idx = 0
    destino_idx = 1
    
    configurando = True
    while configurando:
        tela.fill((245, 245, 245))
        
        # Títulos
        tela.blit(fonte_titulo.render("Selecione os Pontos", True, (0,0,0)), (290, 40))
        
        # Instruções de Colunas
        tela.blit(fonte_item.render("ORIGEM", True, (200, 0, 0)), (150, 110))
        tela.blit(fonte_item.render("DESTINO", True, (0, 150, 0)), (500, 110))

        # Orientações de Controle 
        cor_instrucao = (100, 100, 100)
        tela.blit(fonte_aviso.render("Alterar: Setas (Cima/Baixo)", True, cor_instrucao), (140, 140))
        tela.blit(fonte_aviso.render("Alterar: Teclas W / S", True, cor_instrucao), (490, 140))

        # Renderizar lista de Origem
        for i, local in enumerate(locais):
            cor = (255, 255, 255) if i == origem_idx else (50, 50, 50)
            fundo = (200, 0, 0) if i == origem_idx else None
            txt = fonte_item.render(f" {local} ", True, cor, fundo)
            tela.blit(txt, (150, 180 + i * 35))

        # Renderizar lista de Destino
        for i, local in enumerate(locais):
            cor = (255, 255, 255) if i == destino_idx else (50, 50, 50)
            fundo = (0, 150, 0) if i == destino_idx else None
            txt = fonte_item.render(f" {local} ", True, cor, fundo)
            tela.blit(txt, (500, 180 + i * 35))

        # --- VALIDAÇÃO VISUAL ---
        if origem_idx == destino_idx:
            # Se forem iguais, mostra aviso em vermelho e oculta o comando de confirmação
            aviso = fonte_aviso.render("ERRO: ORIGEM E DESTINO NÃO PODEM SER IGUAIS!", True, (255, 0, 0))
            tela.blit(aviso, (210, 470))
        else:
            # Se forem diferentes, mostra o comando para iniciar
            tela.blit(fonte_titulo.render("Pressione ENTER para Confirmar", True, (0,0,0)), (210, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: origem_idx = (origem_idx - 1) % len(locais)
                if event.key == pygame.K_DOWN: origem_idx = (origem_idx + 1) % len(locais)
                if event.key == pygame.K_w: destino_idx = (destino_idx - 1) % len(locais)
                if event.key == pygame.K_s: destino_idx = (destino_idx + 1) % len(locais)
                
                # --- VALIDAÇÃO NO ENTER ---
                if event.key == pygame.K_RETURN:
                    if origem_idx != destino_idx:
                        configurando = False
                    else:
                        print("Seleção inválida: origem e destino são iguais.")

        pygame.display.flip()
    
    return locais[origem_idx], locais[destino_idx]
