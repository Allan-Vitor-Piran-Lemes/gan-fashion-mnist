# Sprint 2 — implementação e primeiro treinamento da GAN

Este registro complementa o PDF recebido, que documenta o encerramento da Sprint 1.
O encaminhamento para a Sprint 2 está na seção 4.1.7: estudar uma implementação
introdutória, adaptar o código, executar um primeiro treinamento e iniciar contato
com um parceiro educativo. O PDF não especifica um número mínimo de épocas.

## Conceitos para a apresentação

O **gerador** recebe números aleatórios e os transforma em uma imagem. O
**discriminador** recebe imagens da base e imagens criadas pelo gerador, aprendendo
a distinguir as duas origens. Os dois são atualizados alternadamente: o gerador
recebe um sinal de erro que o ajuda a produzir imagens que o discriminador aceite
como reais. Não há uma descrição textual da roupa nem seleção de categoria.

Uma **época** corresponde a percorrer todas as imagens de treinamento uma vez.
Um **lote** é um grupo de imagens processadas juntas. Nesta execução, cada época
usa 50 mil imagens, em lotes de até 128. As **perdas** orientam a atualização das
redes; não são porcentagens de acerto do gerador.

Usar sempre o mesmo **ruído fixo** permite comparar como a saída para uma mesma
entrada se transforma com o treinamento. O resultado não é garantido: algumas
imagens podem ser ambíguas, borradas ou semelhantes entre si.

## Ponto de partida

O commit `0523e6c`, do Allan, contém a arquitetura, o treinamento inicial e grades
visuais identificadas como épocas 0, 1, 5 e 15. Essas imagens foram preservadas em
`artefatos/sprint2_epoca_*.png`. O checkpoint e o log dessa execução não vieram no
clone; não é possível informar seu tempo ou suas perdas a partir das imagens.

O script original usa todas as 60 mil imagens de treino oficial. A divisão
50 mil/10 mil implementada na Sprint 1 não era utilizada pelo treinamento.
O teste oficial de 10 mil imagens já estava fora do treinamento.

## Adaptação local

- Centralização da divisão estratificada em `dados.py`, com semente 42.
- Manutenção da arquitetura original de `modelos.py`.
- Configuração de épocas e tamanho do lote por argumentos de terminal.
- Salvamento por época das duas redes, dos otimizadores e dos estados aleatórios.
- Exportação separada do gerador para uso sem um novo treinamento.
- Visualização em modo de avaliação, sem alterar as estatísticas de normalização.
- Registro das perdas médias por época, configuração, duração e imagens.
- Separação entre as evidências originais e as novas execuções.

As 10 mil imagens de validação permanecem reservadas, sem métrica quantitativa
implementada nesta etapa. A avaliação é visual e descritiva, conforme o relatório.
Não há uso das imagens de teste ou validação na atualização das redes.

## Execução e evidências locais

A preparação dos dados foi executada com sucesso. A conferência encontrou
5.000 imagens de cada classe no treino e 1.000 na validação, sem sobreposição.

O treinamento local e seus resultados devem ser consultados em:

- `artefatos/sprint2_local/configuracao.json`: parâmetros e ambiente da execução.
- `artefatos/sprint2_local/treinamento.log`: progresso e duração.
- `artefatos/sprint2_local/historico.csv`: épocas concluídas e perdas médias.
- `artefatos/sprint2_local/epoca_*.png`: evolução para o mesmo ruído.
- `artefatos/sprint2_local/perdas.png`: gráfico de acompanhamento.
- `checkpoints/sprint2_local/ultimo.pt`: progresso para retomada (fora do Git).
- `checkpoints/sprint2_local/gerador.pt`: modelo para geração (fora do Git).

O resultado observado e o tempo medido estão registrados ao final deste documento. Não confundir essa nova execução com as 15 épocas
representadas nos artefatos originais do parceiro.

## Verificações realizadas

- Importação das dependências e execução da preparação dos dados.
- Treinamento curto com 256 imagens reais, salvamento e retomada.
- Comparação entre duas épocas contínuas e uma época seguida de retomada:
  pesos das duas redes e perdas idênticos no ambiente CPU testado.
- Confirmação de que a visualização não altera pesos ou estatísticas da rede.
- Conferência da separação e do balanceamento dos conjuntos.
- Carregamento do gerador salvo em outro processo e exportação de novas imagens.
- Recusa de sobrescrita de uma execução existente, de retomada sem checkpoint,
  de configuração incompatível e de número de épocas inválido.

As execuções `verificacao_*` são testes de funcionamento e ficam fora do Git.
Elas não são evidência de qualidade visual de um treinamento completo.

## Pendências da equipe para o encerramento

- Registrar as horas efetivamente dedicadas por integrante; tempo de máquina
  treinando sozinha não é dedicação ativa, conforme o PDF.
- Escrever as reflexões individuais sobre o que foi compreendido e as dificuldades.
- Registrar o contato ou a tentativa de contato com o parceiro educativo, com
  informação verdadeira sobre sua participação.
- Atualizar o Jira e incorporar links, imagens e resultados ao relatório.

A interface educativa, a seleção de categorias e a validação com o público não
foram implementadas nesta adaptação da Sprint 2.

## Resultado da execução de 30/10/2026

Comando executado: `python3 treinar_gan.py --epocas 1 --nome sprint2_local`.
Foi concluída **uma época completa sobre 50.000 imagens**, em CPU, com lote de 128
e duas threads. O tempo do laço de treinamento foi de **296.8 segundos**
(aproximadamente cinco minutos), sem incluir o download e a exportação dos artefatos.
A perda média do discriminador foi **0.7726** e a do gerador foi
**1.5397**. Esses valores são registros de treinamento, não acurácia.

Na época 0, as saídas são texturas acinzentadas sem formas reconhecíveis. Após uma
época, aparecem contornos que lembram roupas e calçados, mas há bastante borramento
e padrões quadriculados. Algumas amostras continuam difíceis de interpretar.
Isso demonstra uma mudança inicial das saídas, sem comprovar qualidade suficiente
para uma apresentação final ao público.

A escala de cinza das novas grades é fixa entre 0 e 1 e o gerador é visualizado em
modo de avaliação. O script original ajustava o contraste de cada imagem
automaticamente e mantinha a rede em modo de treino. Por isso, as grades antigas e
novas não devem ser comparadas como se fossem produzidas pelo mesmo procedimento.

O modelo salvo foi carregado pelo comando `python3 gerar_imagens.py`, que exportou
uma nova grade em `artefatos/geracao_local/imagens_geradas.png`. A retomada foi
verificada separadamente com os testes curtos descritos acima.

Para ampliar esta execução até 15 épocas:

```bash
python3 treinar_gan.py --epocas 15 --nome sprint2_local --retomar
```

Isso executará mais 14 épocas. Pelo tempo desta primeira época, a estimativa inicial
é de cerca de 69 minutos adicionais, sujeita à carga e à temperatura da máquina.
Não foi executado esse prolongamento nesta adaptação. As imagens antigas de 15 épocas
continuam sendo evidências da execução do parceiro, não desta execução local.
