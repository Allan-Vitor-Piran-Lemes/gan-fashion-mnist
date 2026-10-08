import torch
import torch.nn as nn

class Gerador(nn.Module):
    def __init__(self, dim_ruido=100):
        super(Gerador, self).__init__()
        self.modelo = nn.Sequential(
            # Entrada: ruído de tamanho (dim_ruido, 1, 1)
            nn.ConvTranspose2d(dim_ruido, 256, kernel_size=7, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            
            # Saída da camada acima: (256, 7, 7) -> dobra para (128, 14, 14)
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            
            # Dobra de (128, 14, 14) -> para (1, 28, 28)
            nn.ConvTranspose2d(128, 1, kernel_size=4, stride=2, padding=1, bias=False),
            nn.Tanh()  # Garante saída no intervalo [-1, 1]
        )

    def forward(self, x):
        return self.modelo(x)


class Discriminador(nn.Module):
    def __init__(self):
        super(Discriminador, self).__init__()
        self.modelo = nn.Sequential(
            # Entrada: imagem 1 canal (28, 28) -> reduz para (64, 14, 14)
            nn.Conv2d(1, 64, kernel_size=4, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            
            # Reduz de (64, 14, 14) -> para (128, 7, 7)
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            
            # Reduz de (128, 7, 7) -> para (1, 1, 1)
            nn.Conv2d(128, 1, kernel_size=7, stride=1, padding=0, bias=False),
            nn.Sigmoid()  # Saída de probabilidade: real (1) ou falsa (0)
        )

    def forward(self, x):
        return self.modelo(x)