"""Carregamento e divisão dos dados usados nas duas sprints."""
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset
from torchvision import datasets, transforms

RAIZ = Path(__file__).resolve().parent
SEED = 42
CLASSES = [
    'Camiseta/Top', 'Calça', 'Pulôver', 'Vestido', 'Casaco',
    'Sandália', 'Camisa', 'Tênis', 'Bolsa', 'Bota',
]


def carregar_dados():
    """Reserva 10 mil imagens para validação e mantém o teste oficial separado."""
    transformacao = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])
    treino_oficial = datasets.FashionMNIST(
        root=str(RAIZ / 'data'), train=True, download=True,
        transform=transformacao,
    )
    teste = datasets.FashionMNIST(
        root=str(RAIZ / 'data'), train=False, download=True,
        transform=transformacao,
    )
    idx_treino, idx_val = train_test_split(
        np.arange(len(treino_oficial)), train_size=50000, test_size=10000,
        random_state=SEED, stratify=treino_oficial.targets.numpy(),
    )
    return Subset(treino_oficial, idx_treino), Subset(treino_oficial, idx_val), teste
