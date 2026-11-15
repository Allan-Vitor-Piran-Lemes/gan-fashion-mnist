import os
import matplotlib.pyplot as plt
from PIL import Image

def gerar_painel():
    os.makedirs("artefatos/sprint3", exist_ok=True)
    
    momentos = [
        ("Início — Época 0\n(Pesos iniciais aleatórios)", "artefatos/sprint2_epoca_0.png"),
        ("Meio — Época 5\n(Execução intermediária)", "artefatos/sprint2_epoca_5.png"),
        ("Fim — Época 15\n(Final da execução analisada)", "artefatos/sprint2_epoca_15.png")
    ]
    
    fig, eixos = plt.subplots(1, 3, figsize=(15, 5.5))
    fig.suptitle("Comparação Visual do Treinamento da GAN (Fashion-MNIST)", fontsize=14, fontweight="bold")
    
    for ax, (titulo, caminho) in zip(eixos, momentos):
        if os.path.exists(caminho):
            img = Image.open(caminho)
            ax.imshow(img)
            ax.set_title(titulo, fontsize=11, pad=10)
        else:
            ax.text(0.5, 0.5, f"Não encontrado:\n{caminho}", ha="center", va="center")
        ax.axis("off")
        
    saida = "artefatos/sprint3/painel_comparativo_evolucao.png"
    plt.tight_layout()
    plt.savefig(saida, dpi=150)
    plt.close()
    print(f"Painel salvo em: {saida}")

if __name__ == "__main__":
    gerar_painel()