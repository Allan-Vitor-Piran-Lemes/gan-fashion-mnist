# Laboratório educativo de IA generativa — Fashion-MNIST

Projeto da disciplina Oficina de Projetos em Ciência de Dados e IA (UTFPR).
A GAN aprende a gerar imagens de roupas em tons de cinza, com 28 × 28 pixels.
O objetivo é apoiar uma demonstração introdutória para estudantes do ensino médio.
O registro da adaptação, dos resultados e das pendências está em
[docs/sprint2.md](docs/sprint2.md).

## Ambiente

Python 3.10 ou superior. No ambiente local utilizado nesta adaptação, as dependências
já estavam instaladas: Python 3.11.11, PyTorch 2.5.1+cu121, Torchvision 0.20.1+cu121,
NumPy 2.2.2, Matplotlib 3.10.0 e Scikit-learn 1.6.1.

Para uma instalação nova, na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows, ative com `.venv\Scripts\activate`.
O treinamento usa CUDA quando disponível e CPU caso contrário. A presença de uma
versão de PyTorch com CUDA não garante que o driver e a GPU estejam disponíveis.

## Executar

Use o terminal na pasta do projeto. O primeiro comando baixa os dados (é necessária
internet nessa primeira execução) e mostra a divisão e o balanceamento das classes:

```bash
python preparacao_dados.py
```

A imagem dessa execução fica em `artefatos/preparacao_local/`.
Os registros originais do parceiro na raiz de `artefatos/` são preservados.

Antes de um treino maior, confira o fluxo com apenas 256 imagens:

```bash
python treinar_gan.py --teste-rapido --epocas 1 --nome verificacao_manual
```

Esse modo é um teste de funcionamento; suas imagens não demonstram um modelo treinado
adequadamente. Para o primeiro treino completo sobre as 50 mil imagens:

```bash
python treinar_gan.py --epocas 1 --nome sprint2_local
```

Para continuar a mesma execução até completar 15 épocas:

```bash
python treinar_gan.py --epocas 15 --nome sprint2_local --retomar
```

`--epocas` indica o total desejado: ao retomar da época 1 com `--epocas 15`, são
executadas mais 14 épocas. Se `sprint2_local` já existir, use `--retomar` ou outro
`--nome`. Não é necessário refazer uma época já concluída.

É possível interromper com Ctrl+C. A retomada parte da última época concluída;
os lotes da época interrompida serão refeitos. Antes do fim da primeira época ainda
não existe checkpoint. Cada época usa 50 mil imagens, inclusive em CPU.
Se interromper antes do primeiro checkpoint, inicie novamente com outro `--nome`.

Os parâmetros `--batch-size` (padrão 128) e `--threads` (padrão 2) permitem ajustar
a execução à máquina. Para retomar, mantenha o batch-size e o modo de teste originais.

## Resultados

Cada execução cria duas pastas:

| Pasta | Conteúdo |
|---|---|
| `artefatos/<nome>/` | Imagens da época 0 e de cada época concluída, perdas médias em CSV, gráfico, configuração e log |
| `checkpoints/<nome>/` | `ultimo.pt` para retomar e `gerador.pt` para gerar imagens |

As perdas são médias ponderadas pelo número de imagens de cada lote. Não representam
acurácia nem devem ser usadas isoladamente para avaliar qualidade visual.
A avaliação desta etapa é descritiva: formas reconhecíveis, diversidade e falhas visíveis.

Para gerar uma nova grade de 16 imagens com o modelo salvo:

```bash
python gerar_imagens.py --modelo checkpoints/sprint2_local/gerador.pt
```

Para outra grade, escolha nova semente e pasta:

```bash
python gerar_imagens.py --modelo checkpoints/sprint2_local/gerador.pt --semente 456 --saida artefatos/geracao_456
```

Os arquivos `.pt` ficam fora do Git. Para compartilhar o modelo treinado, é necessário
transferir `gerador.pt` entre os integrantes separadamente. As imagens PNG não substituem
os pesos do modelo.

## Como funciona

- `dados.py`: normaliza os pixels para [-1, 1] e divide o treino oficial em 50 mil
  imagens para treino e 10 mil para validação, com estratificação e semente 42.
  As 10 mil imagens de teste oficial ficam separadas. Validação e teste não entram
  no treinamento; não há métrica de validação implementada nesta sprint.
- `preparacao_dados.py`: verifica essa divisão e exporta exemplos reais.
- `modelos.py`: o gerador transforma ruído de dimensão 100 em imagens; o discriminador
  aprende a distinguir imagens reais das geradas. A arquitetura original foi mantida.
- `treinar_gan.py`: alterna o aprendizado das redes com Adam e perda binária. Salva
  ambas as redes, otimizadores e estados aleatórios para retomar por época.
- `gerar_imagens.py`: carrega apenas o gerador e produz novas imagens em CPU.

A semente ajuda a repetir a execução no mesmo ambiente; resultados podem variar entre
versões, dispositivos e plataformas. O ruído fixo das imagens por época permite acompanhar
a transformação das mesmas entradas. A visualização usa `eval()` e `no_grad()`.

A GAN atual não recebe rótulos de classe: não é possível solicitar especificamente
uma calça ou um tênis. A interface e o roteiro educativo são etapas posteriores.

## Referências

- [Fashion-MNIST — repositório original da Zalando](https://github.com/zalandoresearch/fashion-mnist).
- [PyTorch — tutorial de DCGAN](https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html).
- [PyTorch — salvar e carregar modelos e checkpoints](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html).

O código de partida foi entregue por Allan Vitor Piran Lemes nos commits `806317a`
e `0523e6c`. As fontes acima servem de referência para esta adaptação; a origem de
exemplos eventualmente usados na implementação inicial deve ser confirmada com o autor.
