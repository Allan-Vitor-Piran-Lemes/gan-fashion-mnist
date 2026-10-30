import torch
from torch.utils.data import DataLoader
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from dados import CLASSES, RAIZ, SEED, carregar_dados


def main():
    # 1. Configuração de Sementes para Reprodutibilidade
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    print("=" * 60)
    print("SPRINT 1 - PREPARAÇÃO E PIPELINE DE DADOS (FASHION-MNIST)")
    print("=" * 60)

    # A mesma divisão é utilizada pelo treinamento da GAN.
    print("\n[1/5] Realizando download e ingestão do Fashion-MNIST...")
    dados_treino, dados_val, dados_teste_oficial = carregar_dados()
    print("[2/5] Separação estratificada: 50.000 treino / 10.000 validação.")
    targets = dados_treino.dataset.targets.numpy()
    idx_treino, idx_val = dados_treino.indices, dados_val.indices

    print(f" -> Conjunto de Treino: {len(dados_treino)} imagens")
    print(f" -> Conjunto de Validação: {len(dados_val)} imagens")
    print(f" -> Conjunto de Teste Oficial (Reservado): {len(dados_teste_oficial)} imagens")

    # 3. Verificação da Distribuição de Classes
    print("\n[3/5] Verificando integridade e balanceamento das classes:")
    rotulos_treino = targets[idx_treino]
    rotulos_val = targets[idx_val]

    print(f"{'Classe':<15} | {'Treino':<10} | {'Validação':<10}")
    print("-" * 42)
    for i, nome_classe in enumerate(CLASSES):
        qtd_t = np.sum(rotulos_treino == i)
        qtd_v = np.sum(rotulos_val == i)
        print(f"{nome_classe:<15} | {qtd_t:<10} | {qtd_v:<10}")

    # 4. Criação do DataLoader e Checagem de Dimensões
    print("\n[4/5] Instanciando DataLoaders e validando tensores...")
    train_loader = DataLoader(dados_treino, batch_size=128, shuffle=True)

    lote_imagens, lote_rotulos = next(iter(train_loader))
    print(f" -> Formato do lote de imagens: {lote_imagens.shape} (Batch, Canal, Altura, Largura)")
    print(f" -> Formato do lote de rótulos: {lote_rotulos.shape}")
    print(f" -> Valor mínimo do pixel: {lote_imagens.min().item():.2f}")
    print(f" -> Valor máximo do pixel: {lote_imagens.max().item():.2f}")

    # 5. Geração de Amostras Visuais para Entrega
    print("\n[5/5] Gerando grade visual de amostras reais...")
    pasta_artefatos = RAIZ / 'artefatos' / 'preparacao_local'
    pasta_artefatos.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 5))
    for i in range(10):
        idx = (lote_rotulos == i).nonzero(as_tuple=True)[0]
        if len(idx) > 0:
            img_np = lote_imagens[idx[0]].squeeze().numpy()
            img_desnormalizada = (img_np * 0.5) + 0.5

            plt.subplot(2, 5, i + 1)
            plt.imshow(img_desnormalizada, cmap='gray')
            plt.title(f"{i}: {CLASSES[i]}", fontsize=9)
            plt.axis('off')

    plt.suptitle("Fashion-MNIST - Amostras das 10 Classes Reais", fontsize=12)
    plt.tight_layout()

    caminho_imagem = pasta_artefatos / 'amostras_classes_reais.png'
    plt.savefig(caminho_imagem, dpi=300)
    plt.close()

    print(f" -> Evidência visual salva em: '{caminho_imagem}'")
    print("\nProcessamento da Sprint 1 finalizado com sucesso!")


if __name__ == "__main__":
    main()
