"""Treinamento introdutório da GAN com registros e retomada por época."""
import argparse
import csv
import json
import time
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, Subset

from dados import RAIZ, SEED, carregar_dados
from modelos import Gerador, Discriminador

DIM_RUIDO = 100


def argumentos():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epocas", type=int, default=15,
                        help="Total de épocas desejado, inclusive ao retomar (padrão: 15).")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--threads", type=int, default=2, help="Threads da CPU.")
    parser.add_argument("--nome", default="sprint2_local",
                        help="Nome da pasta de resultados e checkpoints.")
    parser.add_argument("--retomar", action="store_true",
                        help="Continua a partir da última época concluída da execução nomeada.")
    parser.add_argument("--teste-rapido", action="store_true",
                        help="Usa apenas 256 imagens de treino para verificar o código.")
    args = parser.parse_args()
    if min(args.epocas, args.batch_size, args.threads) < 1:
        parser.error("Épocas, batch-size e threads devem ser positivos.")
    if not args.nome or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in args.nome):
        parser.error("Use apenas letras, números, _ e - no nome da execução.")
    return args


def salvar_amostras(gerador, ruido, epoca, pasta):
    """Visualiza sem alterar as estatísticas de BatchNorm do gerador."""
    estava_treinando = gerador.training
    gerador.eval()
    with torch.no_grad():
        imagens = (gerador(ruido).cpu() + 1) / 2
    gerador.train(estava_treinando)
    fig, axes = plt.subplots(4, 4, figsize=(5, 5))
    for eixo, imagem in zip(axes.flat, imagens):
        eixo.imshow(imagem.squeeze(), cmap="gray", vmin=0, vmax=1)
        eixo.axis("off")
    titulo = f"época {epoca}" if epoca is not None else "novas amostras"
    nome_arquivo = f"epoca_{epoca:03d}.png" if epoca is not None else "imagens_geradas.png"
    fig.suptitle(f"GAN Fashion-MNIST — {titulo}")
    fig.tight_layout()
    fig.savefig(pasta / nome_arquivo, dpi=120)
    plt.close(fig)


def salvar_historico(historico, pasta):
    with (pasta / "historico.csv").open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["epoca", "perda_d", "perda_g", "segundos"])
        writer.writeheader()
        writer.writerows(historico)
    fig, eixo = plt.subplots(figsize=(7, 4))
    for campo, nome in [("perda_d", "Discriminador"), ("perda_g", "Gerador")]:
        eixo.plot([h["epoca"] for h in historico], [h[campo] for h in historico],
                  marker="o", label=nome)
    eixo.set(xlabel="Época", ylabel="Perda média", title="Acompanhamento do treino (não é acurácia)")
    eixo.legend()
    fig.tight_layout()
    fig.savefig(pasta / "perdas.png", dpi=120)
    plt.close(fig)


def salvar_checkpoint(estado, caminho):
    # Evita substituir um checkpoint válido por um arquivo parcialmente escrito.
    temporario = caminho.with_suffix(".tmp")
    torch.save(estado, temporario)
    temporario.replace(caminho)


def main():
    args = argumentos()
    torch.set_num_threads(args.threads)
    torch.manual_seed(SEED)
    dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pasta = RAIZ / "artefatos" / args.nome
    pasta_modelo = RAIZ / "checkpoints" / args.nome
    checkpoint = pasta_modelo / "ultimo.pt"
    if args.retomar and not checkpoint.exists():
        raise SystemExit(f"Checkpoint não encontrado: {checkpoint}")
    if not args.retomar and (pasta.exists() or pasta_modelo.exists()):
        raise SystemExit("Execução já existe. Use --retomar ou escolha outro --nome.")

    print(f"Dispositivo: {dispositivo} | threads CPU: {args.threads}", flush=True)
    treino, validacao, teste = carregar_dados()
    if args.teste_rapido:
        treino = Subset(treino, range(256))
    print(f"Treino: {len(treino)} | Validação reservada: {len(validacao)} | Teste reservado: {len(teste)}", flush=True)
    if args.teste_rapido:
        print("TESTE RÁPIDO: verifica a execução, não avalia a qualidade da GAN.", flush=True)
    # Gerador próprio para manter a ordem dos lotes ao retomar.
    rng_loader = torch.Generator().manual_seed(SEED)
    loader = DataLoader(treino, batch_size=args.batch_size, shuffle=True,
                        generator=rng_loader)
    gerador = Gerador(DIM_RUIDO).to(dispositivo)
    discriminador = Discriminador().to(dispositivo)
    criterio = nn.BCELoss()
    otim_g = optim.Adam(gerador.parameters(), lr=0.0002, betas=(0.5, 0.999))
    otim_d = optim.Adam(discriminador.parameters(), lr=0.0002, betas=(0.5, 0.999))
    ruido_fixo = torch.randn(16, DIM_RUIDO, 1, 1, device=dispositivo)
    historico = []
    inicio = 1
    configuracao = {
        "semente": SEED, "dim_ruido": DIM_RUIDO, "batch_size": args.batch_size,
        "taxa_aprendizado": 0.0002, "betas": [0.5, 0.999],
        "imagens_treino": len(treino), "imagens_validacao_reservadas": len(validacao),
        "imagens_teste_reservadas": len(teste), "teste_rapido": args.teste_rapido,
    }
    if args.retomar:
        estado = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if estado["configuracao"] != configuracao:
            raise SystemExit("A configuração difere do checkpoint. Repita o batch-size e o modo de teste originais.")
        gerador.load_state_dict(estado["gerador"])
        discriminador.load_state_dict(estado["discriminador"])
        otim_g.load_state_dict(estado["otimizador_g"])
        otim_d.load_state_dict(estado["otimizador_d"])
        ruido_fixo = estado["ruido_fixo"].to(dispositivo)
        historico = estado["historico"]
        inicio = estado["epoca"] + 1
        torch.set_rng_state(estado["rng_torch"])
        rng_loader.set_state(estado["rng_loader"])
        if dispositivo.type == "cuda" and estado["rng_cuda"] is not None:
            torch.cuda.set_rng_state_all(estado["rng_cuda"])
        if inicio > args.epocas:
            print(f"Já foram concluídas {inicio - 1} épocas. Aumente --epocas para continuar.")
            return
        print(f"Retomando na época {inicio}.", flush=True)

    pasta.mkdir(parents=True, exist_ok=True)
    pasta_modelo.mkdir(parents=True, exist_ok=True)
    metadata = dict(configuracao, dispositivo=str(dispositivo), threads=args.threads,
                    pytorch=str(torch.__version__), epocas_solicitadas=args.epocas,
                    ultima_execucao=datetime.now().astimezone().isoformat())
    (pasta / "configuracao.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if inicio == 1:
        salvar_amostras(gerador, ruido_fixo, 0, pasta)
    # Se houve interrupção após gravar o checkpoint, reconstitui os registros.
    if historico:
        salvar_historico(historico, pasta)

    with (pasta / "treinamento.log").open("a", encoding="utf-8") as log:
        def registrar(mensagem):
            print(mensagem, flush=True)
            log.write(mensagem + "\n")
            log.flush()

        registrar(f"Execução: {metadata['ultima_execucao']} | {dispositivo} | treino={len(treino)} | teste_rapido={args.teste_rapido}")
        try:
            for epoca in range(inicio, args.epocas + 1):
                t0 = time.perf_counter()
                soma_d = soma_g = 0.0
                quantidade = 0
                for lote, (imagens, _) in enumerate(loader, start=1):
                    imagens = imagens.to(dispositivo)
                    tamanho = imagens.size(0)
                    reais = torch.ones(tamanho, 1, 1, 1, device=dispositivo)
                    falsas = torch.zeros_like(reais)

                    # D aprende a distinguir imagens reais e geradas.
                    otim_d.zero_grad(set_to_none=True)
                    ruido = torch.randn(tamanho, DIM_RUIDO, 1, 1, device=dispositivo)
                    geradas = gerador(ruido)
                    perda_d = criterio(discriminador(imagens), reais) + criterio(discriminador(geradas.detach()), falsas)
                    perda_d.backward()
                    otim_d.step()

                    # G aprende a produzir imagens que D considere reais.
                    discriminador.requires_grad_(False)
                    otim_g.zero_grad(set_to_none=True)
                    perda_g = criterio(discriminador(geradas), reais)
                    perda_g.backward()
                    otim_g.step()
                    discriminador.requires_grad_(True)
                    if not torch.isfinite(perda_d) or not torch.isfinite(perda_g):
                        raise RuntimeError("Perda não finita. A última época concluída permanece salva.")
                    soma_d += perda_d.item() * tamanho
                    soma_g += perda_g.item() * tamanho
                    quantidade += tamanho
                    if lote % 50 == 0:
                        registrar(f"Época {epoca}/{args.epocas} | lote {lote}/{len(loader)} | {time.perf_counter() - t0:.1f}s")

                segundos = time.perf_counter() - t0
                historico.append(dict(epoca=epoca, perda_d=soma_d / quantidade,
                                      perda_g=soma_g / quantidade, segundos=segundos))
                salvar_checkpoint({
                    "epoca": epoca, "configuracao": configuracao,
                    "gerador": gerador.state_dict(), "discriminador": discriminador.state_dict(),
                    "otimizador_g": otim_g.state_dict(), "otimizador_d": otim_d.state_dict(),
                    "ruido_fixo": ruido_fixo.cpu(), "historico": historico,
                    "rng_torch": torch.get_rng_state(), "rng_loader": rng_loader.get_state(),
                    "rng_cuda": torch.cuda.get_rng_state_all() if dispositivo.type == "cuda" else None,
                }, checkpoint)
                salvar_checkpoint(gerador.state_dict(), pasta_modelo / "gerador.pt")
                salvar_amostras(gerador, ruido_fixo, epoca, pasta)
                salvar_historico(historico, pasta)
                registrar(f"Época {epoca}/{args.epocas} concluída | D={soma_d / quantidade:.4f} | G={soma_g / quantidade:.4f} | {segundos:.1f}s")
        except KeyboardInterrupt:
            registrar("Interrompido. Use --retomar para continuar da última época concluída; os lotes da época incompleta serão refeitos.")
            return
    print(f"Resultados: {pasta}\nGerador: {pasta_modelo / 'gerador.pt'}", flush=True)


if __name__ == "__main__":
    main()
