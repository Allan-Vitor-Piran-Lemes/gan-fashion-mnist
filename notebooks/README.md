# GAN condicional — notebooks para a apostila

Execute na ordem, com o kernel Python do ambiente do projeto:

1. `01_dados_e_rotulos.ipynb`: preparação, divisão dos conjuntos e exemplos reais com categorias.
2. `02_treinar_gan_condicional.ipynb`: arquitetura completa, treinamento alternado, retomada, checkpoints e gráficos.
3. `03_evolucao_e_geracao_condicional.ipynb`: comparação entre épocas e geração solicitando uma categoria.

```bash
python3 -m pip install -r requirements-notebooks.txt
python3 -m jupyter lab notebooks
```

Use Shift+Enter para executar cada célula. Para repetir o fluxo, reinicie o kernel e execute as células em ordem. Os notebooks 01 e 02 incluem a mesma preparação; são independentes e não dependem de variáveis de outro kernel. As definições das redes aparecem nos notebooks 02 e 03 para que cada um seja legível e executável sozinho; o teste verifica que permanecem iguais.

## Condicionamento e compatibilidade

O gerador recebe `(ruído, classe)`. O discriminador recebe `(imagem, classe)`. Embeddings aprendidos representam as classes nas duas redes. A condição não é um filtro aplicado depois da geração e não garante, sozinha, fidelidade visual à categoria.

Os scripts Python e a interface existentes continuam sendo a versão incondicional. A arquitetura condicional é uma nova experiência, com largura menor no gerador para reduzir custo de CPU. Não se deve atribuir diferenças visuais apenas ao condicionamento. **Seus pesos não são compatíveis com os checkpoints anteriores nem com a interface atual.** Não copie os novos pesos sobre `checkpoints/sprint2_local/gerador.pt`.

## Teste e treinamento completo

O notebook 02 abre com `TESTE_RAPIDO=True`, 200 imagens balanceadas e duas épocas. Esse modo verifica a execução, não qualidade de aprendizado. Se o nome padrão já existir devido a uma execução anterior, escolha outro nome iniciado por `verificacao_` ou retome.

Para treinar com 50 mil imagens, altere a célula de configuração:

```python
TESTE_RAPIDO = False
NOME_EXECUCAO = 'cgan_apostila_01'
EPOCAS = 15
RETOMAR = False
```

O treinamento completo pode demorar em CPU. Ao continuar, mantenha a configuração e o nome, use `RETOMAR=True` e aumente `EPOCAS` para o total desejado. Interromper uma época perde apenas seus lotes ainda não consolidados; se não houve primeira época concluída, escolha um novo nome para reiniciar. O checkpoint mais recente permite retomar, mas erros entre sua gravação e a exportação das imagens podem deixar um painel ausente; confira as épocas efetivamente disponíveis.

No notebook 03, selecione o mesmo `NOME_EXECUCAO`. Altere `CLASSE` entre 0 e 9 e `SEMENTE_GERACAO` para explorar saídas. Esse notebook não treina.

## Evolução do aprendizado

Os resultados ficam separados por execução:

- `artefatos/cgan/<nome>/`: configuração JSON, perdas e duração por época em CSV, gráfico e painéis PNG.
- `checkpoints/cgan/<nome>/`: estado completo `ultimo.pt`, pesos do gerador por época e tensores das amostras.

O painel usa dez linhas (classes) e três colunas (ruídos). Ruído, rótulos e escala visual permanecem fixos entre épocas; o gerador é visualizado em modo de avaliação. O notebook 03 monta um comparativo de início, momento intermediário e final disponível, usando a primeira amostra de cada classe.

Para a apostila, identifique nome da execução, época, classe, quantidade de imagens e modo de teste/treino. Descreva contornos reconhecíveis, confusões entre categorias, diversidade e artefatos visuais. As perdas não são acurácia. Não misture imagens antigas da GAN incondicional com esta sequência.

Os testes curtos executados no desenvolvimento não substituem uma experiência de treinamento completo da cGAN. A revisão visual de um treino completo e as observações dos autores permanecem necessárias antes de apresentar resultados de aprendizado na apostila.

## Verificação

```bash
python3 -m unittest discover -s tests -p test_condicional.py
```

As verificações unitárias conferem a igualdade das definições das redes nos dois notebooks e se a condição afeta ambas as redes e recebe gradientes. A execução integral dos três notebooks e a equivalência de retomada também são verificadas durante o desenvolvimento.

Referência conceitual: [Mirza e Osindero, Conditional Generative Adversarial Nets (2014)](https://arxiv.org/abs/1411.1784).
