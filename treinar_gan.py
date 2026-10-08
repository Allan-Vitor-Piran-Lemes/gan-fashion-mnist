import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

from modelos import Gerador, Discriminador

# 1. Configurações gerais
DISPOSITIVO = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DIM_RUIDO = 100
EPOCAS = 15          # Treino inicial da Sprint 2
BATCH_SIZE = 128
LR = 0.0002
BETA1 = 0.5

os.makedirs("artefatos", exist_ok=True)
os.makedirs("checkpoints", exist_ok=True)

# 2. Carregar dados com normalização [-1, 1]
transformacao = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

dados_treino = datasets.FashionMNIST(
    root="./data", train=True, download=True, transform=transformacao
)
loader_treino = DataLoader(dados_treino, batch_size=BATCH_SIZE, shuffle=True)

# 3. Instanciar redes e otimizadores
gerador = Gerador(dim_ruido=DIM_RUIDO).to(DISPOSITIVO)
discriminador = Discriminador().to(DISPOSITIVO)

criterio = nn.BCELoss()
otim_g = optim.Adam(gerador.parameters(), lr=LR, betas=(BETA1, 0.999))
otim_d = optim.Adam(discriminador.parameters(), lr=LR, betas=(BETA1, 0.999))

# Ruído fixo para acompanhar a evolução da mesma "roupa" ao longo das épocas
ruido_fixo = torch.randn(16, DIM_RUIDO, 1, 1, device=DISPOSITIVO)

def salvar_amostras(epoca):
    with torch.no_grad():
        imgs_falsas = gerador(ruido_fixo).detach().cpu()
    
    # Desnormalizar de [-1, 1] para [0, 1]
    imgs_falsas = (imgs_falsas * 0.5) + 0.5
    
    plt.figure(figsize=(4, 4))
    for i in range(16):
        plt.subplot(4, 4, i + 1)
        plt.imshow(imgs_falsas[i].squeeze(), cmap="gray")
        plt.axis("off")
    
    caminho = f"artefatos/sprint2_epoca_{epoca}.png"
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    print(f"[*] Amostra visual salva em: {caminho}")

# Salvar como a GAN começa antes de treinar (Época 0 = Puro Ruído)
salvar_amostras(0)

# 4. Loop de Treinamento
print(f"Iniciando treinamento na plataforma: {DISPOSITIVO}")
for epoca in range(1, EPOCAS + 1):
    for i, (imgs_reais, _) in enumerate(loader_treino):
        tamanho_lote = imgs_reais.size(0)
        imgs_reais = imgs_reais.to(DISPOSITIVO)
        
        rotulos_reais = torch.ones(tamanho_lote, 1, 1, 1, device=DISPOSITIVO)
        rotulos_falsos = torch.zeros(tamanho_lote, 1, 1, 1, device=DISPOSITIVO)
        
        # --- TREINAR DISCRIMINADOR ---
        otim_d.zero_grad()
        saida_real = discriminador(imgs_reais)
        perda_d_real = criterio(saida_real, rotulos_reais)
        
        ruido = torch.randn(tamanho_lote, DIM_RUIDO, 1, 1, device=DISPOSITIVO)
        imgs_falsas = gerador(ruido)
        saida_falsa = discriminador(imgs_falsas.detach())
        perda_d_falsa = criterio(saida_falsa, rotulos_falsos)
        
        perda_d = perda_d_real + perda_d_falsa
        perda_d.backward()
        otim_d.step()
        
        # --- TREINAR GERADOR ---
        otim_g.zero_grad()
        saida_gerador = discriminador(imgs_falsas)
        perda_g = criterio(saida_gerador, rotulos_reais)  # G quer enganar o D
        perda_g.backward()
        otim_g.step()

    print(f"Época [{epoca}/{EPOCAS}] | Perda D: {perda_d.item():.4f} | Perda G: {perda_g.item():.4f}")
    
    # Salvar amostras em momentos-chave
    if epoca in [1, 5, EPOCAS]:
        salvar_amostras(epoca)

# Salvar o modelo ao final da Sprint 2
torch.save(gerador.state_dict(), "checkpoints/gerador_sprint2.pt")
print("[+] Modelo parcial salvo com sucesso em checkpoints/gerador_sprint2.pt")