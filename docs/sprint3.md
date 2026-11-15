# Sprint 3 — implementação e reconciliação das evidências

Verificação em 15/11/2026. O arquivo de contexto da equipe informa seis itens
concluídos e prazo planejado de 13/11/2026. Não houve consulta direta ao Jira nem
alteração de prazo ou estado. Este registro distingue esse relato do conteúdo local.

Ao iniciar, o branch era main, com commit mais recente `451cde6`. Não havia aplicação
Streamlit, fluxograma, roteiro ou registro da Sprint 3. O relatório anterior está em `docs/Sprint2.tex`. Os artefatos e checkpoints anteriores também foram preservados.

| Item / responsável informado | Evidência e situação verificada |
|---|---|
| SCRUM-11 / Guilherme | `checkpoints/sprint2_local/ultimo.pt` e `gerador.pt` existem. O histórico disponível termina na época 1. O modelo pode ser usado para geração, mas a continuidade do treinamento na Sprint 3 não está comprovada. |
| SCRUM-12 / Allan | A aba de evolução de `app.py` apresenta épocas 0, 5 e 15 da execução original, preservadas no commit `0523e6c`. O procedimento é o do script original: ruído fixo, modo de treino e contraste automático. As imagens locais, com outro procedimento, estão separadas. |
| SCRUM-13 / Guilherme | `app.py` foi criado nesta intervenção: exemplos reais, comparação e geração de 16 imagens com o modelo local. Não havia interface neste checkout. |
| SCRUM-14 / Allan | Textos educativos integrados às quatro abas: base, redes, época, semente e limitações. Critério atual: explicações educativas revisadas pelos autores; a revisão autoral final ainda precisa ser registrada. |
| SCRUM-26 / Guilherme | `docs/fluxograma.md` e diagrama simplificado na interface, criados nesta intervenção. |
| SCRUM-15 / Allan | `docs/roteiro_sprint3.md`: roteiro de 25 minutos; este arquivo registra evidências e pendências. Ambos foram criados nesta intervenção. |

Os responsáveis acima vêm do registro da equipe, não constituem comprovação de
quem implementou cada artefato. As estimativas são 5, 4, 5, 3 e 3 horas, respectivamente
para SCRUM-11, 12, 13, 14 e 15; SCRUM-26 não tem estimativa informada. As 20 horas
previstas não são horas realizadas. Horas e reflexões individuais não foram fornecidas.

## Modelo disponível e limites

O histórico local registra 50.000 imagens, lote 128, semente 42, Adam com taxa 0,0002,
uma época em 296,7776 segundos, perda D 0,7726 e perda G 1,5397. Esses valores vêm da
Sprint 2 e não são acurácia. Não foi iniciado outro treino longo nesta revisão.
As imagens ainda são borradas. A execução antiga tem imagens de 15 épocas, mas não
há checkpoint correspondente comprovado neste checkout.

Para SCRUM-11, falta localizar a versão posterior citada pela equipe ou realizar e
registrar a continuação do treino. Não declaramos as seis entregas tecnicamente
confirmadas só porque o arquivo de contexto informa esse estado no Jira.

## Executar

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py --server.address 127.0.0.1
```

Abrir http://localhost:8501. Não é necessário baixar os dados nem treinar para usar
os exemplos existentes e o modelo local. Em outro computador, transferir também
`checkpoints/sprint2_local/gerador.pt`, pois não é versionado no Git.

A aplicação não seleciona classe, não oferece download e não publica na internet.
A comparação original e a geração local pertencem a execuções diferentes, explicitadas
na interface. A ausência do modelo ou dos painéis é apresentada com uma mensagem.

## Pendências do projeto

Confirmar a versão treinada da Sprint 3, registrar horas e aprendizados individuais,
revisar a apostila e consolidar o relatório oficial em LaTeX.
Não há informações suficientes para criar tarefas ou afirmar entregas da Sprint 4.

## Verificação executada

Ambiente: Streamlit 1.67.0, usando as dependências de aprendizado já instaladas.
Teste funcional automatizado em `tests/test_interface.py` com AppTest: abertura da
aplicação, alternância da comparação, geração real com checkpoint, formato 16 × 28 × 28,
valores finitos entre 0 e 1, repetição da semente e mudança da semente. Também foi
verificada a mensagem para modelo ausente, sem remover o checkpoint existente.

```bash
python3 -m unittest discover -s tests
```

O teste de geração requer o checkpoint local. O servidor Streamlit foi iniciado em
127.0.0.1:8501 e respondeu `ok` em `/_stcore/health`; foi encerrado após a verificação.
Não houve inspeção visual em navegador.

## Ajuste de escopo — 15/11/2026

Por solicitação da equipe, as entregas educativas passam a ser a apostila introdutória, a aplicação local e a documentação, verificadas pelos autores.

SCRUM-14 exige explicações sobre dados, redes e limitações, com revisão dos autores. SCRUM-15 exige roteiro de exploração autônoma, documentação e organização dos aprendizados. Chaves, responsáveis, estimativas e status informados foram preservados; o Jira não foi acessado neste ajuste.

Foram produzidos `docs/apostila_educativa.tex` e `docs/Sprint3.tex`. O primeiro é o material introdutório; o segundo é a versão corrente de trabalho do relatório oficial, derivada do estilo de `Sprint2.tex`, também disponível no repositório. A existência dos arquivos não comprova revisão final dos autores. Este `.md` é apoio à continuidade entre chats.

### Verificação do ajuste

Os dois testes funcionais da interface passaram após a alteração textual. Foram conferidos os caminhos das figuras, os links locais e o balanceamento dos ambientes LaTeX. Não há `pdflatex`, `xelatex`, `lualatex`, `tectonic` ou `latexmk` neste ambiente: os novos fontes não foram compilados e não há PDF novo verificado. Compilar e revisar a apresentação dos documentos faz parte da revisão autoral pendente.
