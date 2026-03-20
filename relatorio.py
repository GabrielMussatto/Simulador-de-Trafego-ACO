from fpdf import FPDF

class RelatorioPDF:
    @staticmethod
    def gerar(origem, destino, melhor_tempo, menor_passos, melhor_rota, historico):
        pdf = FPDF('L', 'mm', 'A4') 
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Relatorio de Simulacao ACO - Palmas", ln=True, align='C')
        pdf.ln(5)
        
        tempo_inicial = historico[0]['tempo_venc']
        taxa_otimizacao = ((tempo_inicial - melhor_tempo) / tempo_inicial) * 100 if tempo_inicial > 0 else 0
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="RESUMO DA SIMULACAO", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, txt=f"Trajeto Selecionado: {origem} -> {destino}", ln=True)
        pdf.cell(0, 8, txt=f"Melhor Tempo Individual (Vencedor): {melhor_tempo:.2f}s", ln=True)
        pdf.cell(0, 8, txt=f"Menor Rota Encontrada: {menor_passos} passos", ln=True)
        
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 8, txt=f"Melhoria de Performance: {taxa_otimizacao:.2f}% (Baseado no tempo da 1a Iteracao)", ln=True)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 8, txt=f"Melhor Caminho Historico: {' -> '.join(melhor_rota)}")
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 11)
        w = [15, 25, 20, 35, 35, 145] 
        pdf.cell(w[0], 10, "Iter.", 1, 0, 'C')
        pdf.cell(w[1], 10, "Vencedor", 1, 0, 'C')
        pdf.cell(w[2], 10, "Passos", 1, 0, 'C')
        pdf.cell(w[3], 10, "T. Vencedor", 1, 0, 'C')
        pdf.cell(w[4], 10, "T. Ciclo", 1, 0, 'C')
        pdf.cell(w[5], 10, "Rota Percorrida pelo Vencedor", 1, 1, 'C')
        
        pdf.set_font("Arial", '', 9)
        for h in historico:
            pdf.cell(w[0], 8, str(h['it']), 1, 0, 'C')
            pdf.cell(w[1], 8, f"Carro {h['vencedor']}", 1, 0, 'C')
            pdf.cell(w[2], 8, str(h['passos']), 1, 0, 'C')
            pdf.cell(w[3], 8, f"{h['tempo_venc']:.2f}s", 1, 0, 'C')
            pdf.cell(w[4], 8, f"{h['tempo_ciclo']:.2f}s", 1, 0, 'C')
            pdf.cell(w[5], 8, h['rota'], 1, 1, 'L')
            
        pdf.output("relatorio_final_aco.pdf")
        print(f"\n[INFO] Relatorio gerado com {taxa_otimizacao:.2f}% de otimizacao.")