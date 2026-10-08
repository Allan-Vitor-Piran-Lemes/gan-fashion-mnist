import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# 1. Configuração de Sementes para Reprodutibilidade
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

CLASSES = [
    'Camiseta/Top', 'Calça', 'Pulôver', 'Vestido', 'Casaco',
    'Sandália', 'Camisa', 'Tênis', 'Bolsa', 'Bota'
]

print("=" * 60)
print("SPRINT 1 - PREPARAÇÃO E PIPELINE DE DADOS (FASHION-MNIST)")
print("=" * 60)

# 2. Pipeline de Transformação e Normalização [-1.0, 1.0]
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 3. Aquisição Automatizada dos Dados
print("\n[1/5] Realizando download e ingestão do Fashion-MNIST...")
dados_brutos_treino = datasets.FashionMNIST(
    root='./data', train=True, download=True, transform=transform
)
dados_teste_oficial = datasets.FashionMNIST(
    root='./data', train=False, download=True, transform=transform
)

# 4. Separação Estratificada (50.000 Treino / 10.000 Validação)
print("[2/5] Realizando separação estratificada dos dados de treino...")
targets = dados_brutos_treino.targets.numpy()
indices = np.arange(len(targets))

idx_treino, idx_val = train_test_split(
    indices,
    test_size=10000,
    train_size=50000,
    random_state=SEED,
    stratify=targets
)

dados_treino = Subset(dados_brutos_treino, idx_treino)
dados_val = Subset(dados_brutos_treino, idx_val)

print(f" -> Conjunto de Treino: {len(dados_treino)} imagens")
print(f" -> Conjunto de Validação: {len(dados_val)} imagens")
print(f" -> Conjunto de Teste Oficial (Reservado): {len(dados_teste_oficial)} imagens")

# 5. Verificação da Distribuição de Classes
print("\n[3/5] Verificando integridade e balanceamento das classes:")
rotulos_treino = targets[idx_treino]
rotulos_val = targets[idx_val]

print(f"{'Classe':<15} | {'Treino':<10} | {'Validação':<10}")
print("-" * 42)
for i, nome_classe in enumerate(CLASSES):
    qtd_t = np.sum(rotulos_treino == i)
    qtd_v = np.sum(rotulos_val == i)
    print(f"{nome_classe:<15} | {qtd_t:<10} | {qtd_v:<10}")

# 6. Criação dos DataLoaders e Checagem de Dimensões
print("\n[4/5] Instanciando DataLoaders e validando tensores...")
train_loader = DataLoader(dados_treino, batch_size=128, shuffle=True)
val_loader = DataLoader(dados_val, batch_size=128, shuffle=False)

lote_imagens, lote_rotulos = next(iter(train_loader))
print(f" -> Formato do lote de imagens: {lote_imagens.shape} (Batch, Canal, Altura, Largura)")
print(f" -> Formato do lote de rótulos: {lote_rotulos.shape}")
print(f" -> Valor mínimo do pixel: {lote_imagens.min().item():.2f}")
print(f" -> Valor máximo do pixel: {lote_imagens.max().item():.2f}")

# 7. Geração de Amostras Visuais para Entrega
print("\n[5/5] Gerando grade visual de amostras reais...")
os.makedirs('artefatos', exist_ok=True)

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

caminho_imagem = os.path.join('artefatos', 'amostras_classes_reais.png')
plt.savefig(caminho_imagem, dpi=300)
plt.close()

print(f" -> Evidência visual salva em: '{caminho_imagem}'")
print("\nProcessamento da Sprint 1 finalizado com sucesso!")