"""Carrega um gerador treinado e exporta 16 imagens, sem treinar novamente."""
import argparse
from pathlib import Path

import torch

from dados import RAIZ
from modelos import Gerador
from treinar_gan import DIM_RUIDO, salvar_amostras


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modelo", type=Path,
                        default=RAIZ / "checkpoints/sprint2_local/gerador.pt")
    parser.add_argument("--saida", type=Path, default=RAIZ / "artefatos/geracao_local")
    parser.add_argument("--semente", type=int, default=123)
    args = parser.parse_args()
    if not args.modelo.is_file():
        parser.error(f"Modelo não encontrado: {args.modelo}. Execute o treinamento primeiro.")
    destino = args.saida / "imagens_geradas.png"
    if destino.exists():
        parser.error("A imagem de saída já existe. Escolha outra pasta com --saida.")
    torch.set_num_threads(2)
    torch.manual_seed(args.semente)
    gerador = Gerador(DIM_RUIDO)
    gerador.load_state_dict(torch.load(args.modelo, map_location="cpu", weights_only=True))
    args.saida.mkdir(parents=True, exist_ok=True)
    salvar_amostras(gerador, torch.randn(16, DIM_RUIDO, 1, 1), None, args.saida)
    print(f"Imagem salva em: {destino}")


if __name__ == "__main__":
    main()
