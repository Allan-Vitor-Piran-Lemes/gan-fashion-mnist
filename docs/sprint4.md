# Registro da Quarta Sprint (13/11 a 04/12/2026)

## 1. Planejado vs. Concluído
- **Planejado:** Concluir a interface educativa, registrar instruções de instalação e execução sem aguardar treinamento, conduzir e registrar a demonstração da versão final do software, consolidar ajustes e documentar a Sprint 4 distinguindo resultados obtidos e pendências.
- **Concluído:**
  - Instruções de instalação e execução disponíveis no repositório (`README.md`) com artefatos e modelos organizados para uso imediato.
  - Interface educativa finalizada em Streamlit (`app.py`) com visualização da base, comparação de épocas, geração de imagens e download em PNG.
  - Demonstração e verificação funcional da versão final registradas em `docs/relato_demonstracao_sprint4.md`.
  - Documentação da Sprint 4 consolidada neste arquivo (`docs/sprint4.md`), distinguindo claramente os resultados técnicos entregues e a pendência da atividade externa.

---

## 2. Ajustes e Melhorias Realizados na Versão Final
1. **Organização visual por etapas:** A interface (`app.py`) foi estruturada para apresentar de forma clara os dados reais, a evolução do treinamento, os textos educativos e a área de geração.
2. **Geração sem necessidade de treino ao vivo:** Os arquivos de imagem e checkpoints das épocas foram vinculados para que a demonstração funcione imediatamente ao abrir o projeto.
3. **Verificação automatizada:** Foram mantidos e validados os testes em `tests/test_interface.py` e `tests/test_condicional.py`.
4. **Identificação de imagens sintéticas:** Inclusão de avisos na interface e na documentação indicando que as figuras produzidas são geradas artificialmente por IA.

---

## 3. Distinção entre Resultados Obtidos e Pendências

### 3.1. Resultados Obtidos (Critérios Técnicos e Documentais Atendidos)
- **GAN treinada e documentada:** Pipeline de dados (`preparacao_dados.py`, `dados.py`), arquitetura (`modelos.py`), treinamento (`treinar_gan.py`) e geração (`gerar_imagens.py`) concluídos.
- **Comparação visual dos três momentos:** Painel com Época 0 (início), Época 5 (meio) e Época 15 (fim) gerado (`artefatos/sprint3/painel_comparativo_evolucao.png`) e analisado descritivamente sem presumir melhora automática (`docs/comparacao_visual_sprint3.md`).
- **Interface educativa funcional (`app.py`):** Aplicação abrindo localmente, exibindo exemplos da base, mostrando a evolução do treino, gerando novas imagens e permitindo baixá-las em formato PNG.
- **Material didático e registros das 4 Sprints:** Explicações educativas (`docs/explicacoes_educativas.md`), roteiro de demonstração (`docs/roteiro_sprint3.md`) e registros completos das Sprints 1, 2, 3 e 4 entregues no repositório.

### 3.2. Pendências Explicitadas
- **Contato com parceiro externo e aplicação em escola:** Não realizados. A equipe não levou o projeto a uma escola de ensino médio nem contou com validação de professor externo. Conforme previsto nas Seções 2.4 e 5.4 do Plano de Projeto e nos critérios do Jira, essa etapa é registrada formalmente como pendência justificada.

---

## 4. Participação dos Integrantes e Horas Dedicadas na Sprint 4

| Integrante | Atividades Realizadas na Sprint 4 | Tempo Dedicado |
| :--- | :--- | :---: |
| **Allan Vitor Piran Lemes** | Execução dos testes de validação e registro da versão final do software (`docs/relato_demonstracao_sprint4.md` — 6h); consolidação dos ajustes, distinção entre resultados obtidos e pendências e documentação da Sprint 4 (`docs/sprint4.md` — 4h). | 10 horas |
| **Guilherme Rodrigues dos Santos** | Escrita das instruções de instalação e execução no repositório e organização dos arquivos para demonstração sem aguardar treinamento (4h); conclusão da interface (`app.py`), testes automatizados e suporte técnico (6h). | 10 horas |
| **Total da Equipe** | — | **20 horas** |

---

## 5. Aprendizados e Dificuldades
- **Aprendizados:** Integração completa entre um modelo generativo em PyTorch e uma interface interativa em Streamlit; importância de manter artefatos pré-gerados para demonstrações rápidas; documentação transparente de escopo realizado versus atividades externas pendentes.
- **Dificuldades:** Limitação de tempo para viabilizar agendas externas paralelamente ao desenvolvimento e refinamento técnico do software.

---

## 6. Evidências da Sprint 4
- Registro da demonstração e verificação do software: `docs/relato_demonstracao_sprint4.md`
- Documentação da Sprint 4: `docs/sprint4.md`
- Interface principal: `app.py`
- Instruções de instalação e uso: `README.md`