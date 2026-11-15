# Laboratório Educativo de IA Generativa com GANs

Projeto de graduação da disciplina optativa **Oficina de Projetos em Ciência de Dados e IA**, da Universidade Tecnológica Federal do Paraná (UTFPR), campus Pato Branco.

**Equipe:** Allan Vitor Piran Lemes e Guilherme Rodrigues dos Santos.

**Professor:** Dr. Luiz Fernando Puttow Southier.

O projeto desenvolve um material educativo introdutório sobre IA generativa usando uma GAN treinada com Fashion-MNIST e uma aplicação local de demonstração. As entregas são a GAN, a aplicação, a documentação acadêmica e uma apostila com explicações acessíveis ao ensino médio e a leitores iniciantes, exemplos visuais, orientações de uso e aprendizados documentados da equipe.

O escopo foi ajustado em 15/11/2026: contempla a produção dos materiais e sua verificação pelos próprios autores. O sucesso é definido pelo funcionamento dos artefatos, coerência dos exemplos e revisão técnica e textual pelos autores.

Este README é o guia geral de execução e organização do repositório. O estado descrito foi conferido em **15/11/2026**.

## Documentação: o que serve para cada finalidade

| Material | Finalidade |
|---|---|
| `README.md` | Visão geral, instalação, comandos e orientação para usar o projeto. |
| Relatórios `docs/*.tex` | **Documentos oficiais para entrega na disciplina.** Cada sprint tem sua atualização em LaTeX, até a versão final consolidar todo o desenvolvimento. |
| `docs/sprint2.md` e `docs/sprint3.md` | Memória técnica e contexto para **orquestrar o desenvolvimento entre chats do GPT**. Não são os relatórios oficiais de entrega. |
| `docs/roteiro_sprint3.md` e `docs/fluxograma.md` | Materiais de apoio ao protótipo e à demonstração educativa. Podem subsidiar os relatórios oficiais. |
| `artefatos/` | Evidências produzidas pelo código: imagens, logs, configurações e histórico de treinamento. |

A versão corrente de trabalho para entrega acadêmica é [docs/Sprint3.tex](docs/Sprint3.tex). A versão anterior [docs/Sprint2.tex](docs/Sprint2.tex) registra a etapa anterior. A apostila está em [docs/apostila_educativa.tex](docs/apostila_educativa.tex). Os `.md` das sprints continuam sendo apoio à orquestração entre chats, sem substituir os relatórios oficiais.

Os registros de apoio devem ajudar a manter a continuidade entre conversas. Resultados, horas e contribuições só devem ser levados ao relatório oficial quando confirmados pela equipe e pelas evidências.

## O que temos até agora

| Etapa | Implementação e evidências disponíveis |
|---|---|
| Sprint 1 — dados | Download, normalização, divisão estratificada e painel das dez classes; registro da preparação. |
| Sprint 2 — GAN | Gerador e discriminador, treinamento, salvamento e retomada, geração por terminal e registros visuais. |
| Sprint 3 — protótipo educativo | Interface Streamlit, comparação de épocas, explicações, fluxograma, roteiro de 25 minutos e testes funcionais. |

**Situação do treinamento:** existem grades antigas identificadas como épocas 0, 1, 5 e 15. Já o checkpoint da execução local `sprint2_local` e seu histórico confirmam apenas **uma época completa**. São execuções diferentes.

O documento de contexto da equipe informa seis itens da Sprint 3 concluídos no Jira. A revisão local não consultou diretamente o quadro nem comprovou a continuidade do treinamento prevista em SCRUM-11. Os componentes da interface e os materiais educativos que estavam ausentes foram implementados; essa diferença está detalhada em [docs/sprint3.md](docs/sprint3.md).

## Como a GAN funciona

O **gerador** recebe 100 números aleatórios e produz uma imagem de 28 × 28 pixels. O **discriminador** recebe imagens reais e geradas e aprende a distinguir suas origens. Durante o treinamento, as duas redes são atualizadas alternadamente.

A arquitetura usa camadas convolucionais em PyTorch. O treinamento utiliza Adam e perda binária. O gerador é salvo para que a aplicação possa criar novas imagens sem executar o treinamento novamente.

Uma **época** é uma passagem por todo o conjunto de treino. O **ruído fixo** permite acompanhar como as saídas para as mesmas entradas mudam entre épocas. As perdas registradas orientam o treinamento; **não representam acurácia** nem substituem a observação das imagens.

### Dados

Fashion-MNIST contém imagens em tons de cinza de dez categorias: camiseta/top, calça, pulôver, vestido, casaco, sandália, camisa, tênis, bolsa e bota.

| Conjunto local | Quantidade | Uso atual |
|---|---:|---|
| Treino | 50.000 | Atualização das redes. |
| Validação | 10.000 | Reservado do treino oficial; sem métrica de validação implementada. |
| Teste oficial | 10.000 | Separado e fora do treinamento. |

A divisão das 60 mil imagens oficiais de treino é estratificada, com semente 42: 5.000 imagens de cada classe no treino local e 1.000 na validação. Os pixels são normalizados para o intervalo de -1 a 1.

## Estrutura do projeto

| Caminho | Conteúdo |
|---|---|
| [dados.py](dados.py) | Carregamento e divisão compartilhada dos dados. |
| [preparacao_dados.py](preparacao_dados.py) | Conferência dos conjuntos e exportação de exemplos reais. |
| [modelos.py](modelos.py) | Arquitetura do gerador e do discriminador. |
| [treinar_gan.py](treinar_gan.py) | Treinamento, checkpoints, retomada e registro de resultados. |
| [gerar_imagens.py](gerar_imagens.py) | Geração de uma grade de 16 imagens pelo terminal. |
| [app.py](app.py) | Interface educativa local em Streamlit. |
| [tests/test_interface.py](tests/test_interface.py) | Testes funcionais da interface e da geração. |
| [requirements.txt](requirements.txt) | Dependências Python. |
| `artefatos/` | Evidências originais e resultados organizados por execução. |
| `checkpoints/` | Pesos do gerador e estado para retomar o treino; fora do Git. |
| `data/` | Base baixada localmente; fora do Git. |
| `docs/` | Relatórios oficiais em LaTeX e arquivos de apoio em Markdown. |

## Repositório e fluxo de colaboração

O repositório de trabalho e publicação da equipe nesta etapa é o [fork de Guilherme](https://github.com/GuilhermeRds1921/gan-fashion-mnist).

```bash
git clone https://github.com/GuilhermeRds1921/gan-fashion-mnist.git
cd gan-fashion-mnist
```

Nesta cópia local, `origin` aponta para o fork de Guilherme e é o destino padrão de push. O repositório de Allan está configurado como `upstream` para consulta e atualização, com push direto desativado. Essas configurações locais não são transferidas automaticamente por um clone.

Publique primeiro no fork:

```bash
git add <arquivos>
git commit -m "Descreva a alteração"
git push origin main
```

Após a revisão da equipe, as alterações podem ser propostas ao repositório de Allan por pull request. Os checkpoints e a base de dados continuam fora do Git.

## Instalação

Use Python 3.10 ou superior. As principais bibliotecas são PyTorch, Torchvision, NumPy, Matplotlib, Scikit-learn e Streamlit.

Na pasta do projeto, em Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows, usando o Prompt de Comando:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Os comandos seguintes pressupõem que o ambiente com as dependências esteja ativo. A instalação e o primeiro download da base precisam de internet.

As execuções locais registradas utilizaram Python 3.11.11, PyTorch 2.5.1+cu121, Torchvision 0.20.1+cu121, NumPy 2.2.2, Matplotlib 3.10.0 e Scikit-learn 1.6.1. A interface foi testada com Streamlit 1.67.0. O arquivo de requisitos define intervalos de versões, não um ambiente congelado.

## Abrir a interface

```bash
python -m streamlit run app.py --server.address 127.0.0.1
```

Abra **http://localhost:8501**. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

A aplicação tem quatro abas:

1. **Conheça os dados:** exemplos reais e apresentação da base.
2. **Observe a evolução:** comparação das épocas 0, 5 e 15 originais ou das imagens locais disponíveis, sem misturar as execuções.
3. **Gere imagens:** geração de 16 imagens a partir de uma semente numérica. Repetir a semente repete as imagens no mesmo ambiente e modelo.
4. **Entenda o processo:** explicações das redes, diagrama simplificado, limitações e perguntas para discussão.

A geração usa `checkpoints/sprint2_local/gerador.pt`. Esse arquivo existe na máquina usada no desenvolvimento, mas **não acompanha um clone do Git**. Em outro computador, transfira-o separadamente ou execute o treinamento. Os painéis existentes podem ser consultados sem esse modelo; a aplicação avisa quando ele está ausente.

A interface não treina a GAN, não permite escolher a categoria e não oferece download de PNG. A exportação de imagens está disponível pelo script de terminal. Não há publicação na internet.

## Preparar os dados

```bash
python preparacao_dados.py
```

Esse comando baixa a base, confere quantidades e distribuição das classes e exporta o painel em `artefatos/preparacao_local/amostras_classes_reais.png`. O treinamento também chama o carregamento compartilhado; não é obrigatório executar a preparação antes dele.

## Treinar e retomar

### Teste curto

```bash
python treinar_gan.py --teste-rapido --epocas 1 --nome verificacao_manual
```

Usa 256 imagens para conferir o funcionamento. Não serve como evidência de qualidade visual de um modelo treinado. As pastas `artefatos/verificacao_*/` ficam fora do Git.

### Nova execução

```bash
python treinar_gan.py --epocas 1 --nome meu_treino
```

Usa as 50 mil imagens de treino. Escolha um nome ainda não utilizado para preservar os resultados existentes. O padrão sem argumentos é 15 épocas, lote 128, duas threads e nome `sprint2_local`.

### Continuar a execução local existente

```bash
python treinar_gan.py --epocas 15 --nome sprint2_local --retomar
```

Esse comando exige `checkpoints/sprint2_local/ultimo.pt`. `--epocas` indica o **total desejado**: a partir da época 1, serão executadas mais 14.

O checkpoint é salvo ao final de cada época, com as duas redes, os otimizadores, o histórico e os estados aleatórios. Se interromper com `Ctrl+C`, a retomada refaz os lotes da época incompleta. Antes de terminar a primeira época ainda não existe checkpoint; nesse caso, reinicie com outro nome.

Use `--batch-size` e `--threads` para ajustar a execução. Ao retomar, mantenha o tamanho do lote e o modo de teste originais. Consulte todas as opções com:

```bash
python treinar_gan.py --help
```

O treino escolhe CUDA quando disponível, ou CPU caso contrário. A execução registrada foi em CPU: uma época levou cerca de cinco minutos. Mais 14 épocas levariam aproximadamente 69 minutos naquele ritmo, sujeitos à carga da máquina. Ter uma versão de PyTorch com CUDA instalada não garante que a GPU esteja disponível.

## Gerar e exportar imagens pelo terminal

```bash
python gerar_imagens.py --modelo checkpoints/sprint2_local/gerador.pt --semente 456 --saida artefatos/geracao_456
```

O resultado é `artefatos/geracao_456/imagens_geradas.png`, uma grade de 16 imagens. Escolha outra pasta se o arquivo já existir: o script evita sobrescrevê-lo. A geração ocorre em CPU e não altera o modelo.

Para usar um modelo de outra execução, ajuste `--modelo`. A interface utiliza o caminho fixo `checkpoints/sprint2_local/gerador.pt`.

## Resultados e evidências

| Local | Evidência |
|---|---|
| `artefatos/registro_sprint1.txt` e `amostras_classes_reais.png` | Preparação original e exemplos reais. |
| `artefatos/sprint2_epoca_*.png` | Grades originais das épocas 0, 1, 5 e 15. |
| `artefatos/preparacao_local/` | Painel e registro da preparação local. |
| `artefatos/sprint2_local/` | Imagens locais, configuração, log, histórico CSV e gráfico das perdas. |
| `artefatos/geracao_local/` | Grade exportada com o gerador local salvo. |
| `checkpoints/sprint2_local/gerador.pt` | Pesos para gerar imagens. |
| `checkpoints/sprint2_local/ultimo.pt` | Estado completo para retomar a execução local. |

O histórico local registra uma época sobre 50 mil imagens, em **296,8 segundos**, com perda média do discriminador **0,7726** e do gerador **1,5397**. Esses números pertencem à execução da Sprint 2. O resultado apresenta contornos de roupas e calçados, ainda com borramento e padrões quadriculados.

As grades originais usam visualização em modo de treino e ajuste automático de contraste. As locais usam modo de avaliação e escala fixa. Por isso, elas são apresentadas separadamente. As imagens antigas não comprovam que o checkpoint local chegou à época 15.

## Verificação

```bash
python -m unittest discover -s tests
```

Os testes verificam a abertura da interface, a alternância da comparação, a geração com o checkpoint, o formato e os valores das imagens, a repetição e mudança da semente e a mensagem de modelo ausente. O teste de geração exige o checkpoint local.

Também foram verificados, durante a adaptação da Sprint 2, a separação dos conjuntos, o salvamento e a retomada equivalentes ao treino contínuo em CPU e a preservação das estatísticas da rede durante a visualização. Na Sprint 3, o servidor respondeu à checagem de funcionamento. Não houve inspeção visual automatizada em navegador.

## Materiais educativos e próximos passos

A [apostila educativa](docs/apostila_educativa.tex) reúne conceitos, imagens e exercícios comentados. O [roteiro de 25 minutos](docs/roteiro_sprint3.md) organiza a leitura e exploração autônoma dos dados, das redes, da evolução e da geração; também pode apoiar a apresentação acadêmica ao professor. O [fluxograma](docs/fluxograma.md) representa o processo completo, incluindo os conjuntos reservados e o uso do gerador salvo.

Permanecem pendentes de confirmação ou execução:

- Localizar a versão posterior do modelo informada pela equipe ou continuar e registrar o treinamento.
- Revisar pelos autores a apostila e a versão de trabalho `docs/Sprint3.tex`, consolidando o desenvolvimento no relatório final nas etapas seguintes.
- Registrar horas efetivamente trabalhadas e reflexões individuais. Tempo de máquina treinando sozinho não equivale a dedicação ativa.

As imagens têm baixa resolução e podem ser repetitivas ou difíceis de reconhecer. Não há geração por categoria ou métricas quantitativas de qualidade. A verificação prevista é descritiva e feita pelos autores: funcionamento, evolução visual e coerência entre código, exemplos e explicações.

## Referências e origem do código

- [Fashion-MNIST — repositório original da Zalando](https://github.com/zalandoresearch/fashion-mnist).
- [PyTorch — tutorial de DCGAN](https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html).
- [PyTorch — salvar e carregar modelos e checkpoints](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html).

A implementação inicial foi entregue por Allan Vitor Piran Lemes nos commits `806317a` e `0523e6c`; a adaptação da Sprint 2 está registrada em `451cde6`. As referências acima apoiam o desenvolvimento. A origem de exemplos eventualmente utilizados na implementação inicial deve ser confirmada com o autor antes da atribuição no relatório oficial.

## Preparar os documentos oficiais

Os fontes são completos e podem ser compilados no Overleaf ou com uma instalação LaTeX. Para incluir as figuras, mantenha `docs/` e `artefatos/` na estrutura do projeto. A apostila sinaliza figuras ausentes sem impedir a compilação.

Na raiz do projeto, com `pdflatex` instalado, execute duas vezes cada comando para atualizar sumário e referências:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=docs docs/Sprint3.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=docs docs/apostila_educativa.tex
```

Nesta revisão, o ambiente não dispunha de compilador LaTeX. Os fontes tiveram sua estrutura e referências locais conferidas; a compilação e a inspeção visual dos PDFs permanecem para o ambiente dos autores.
