# Registro da Versão Final do Software e Demonstração — Sprint 4

**Responsável:** Allan Vitor Piran Lemes (com apoio técnico de Guilherme Rodrigues dos Santos)  
**Esforço registrado:** 6 horas  

---

## 1. Execução e Verificação da Versão Final do Software
A versão final da aplicação interativa (pp.py) integrada à GAN treinada foi executada e verificada localmente pela equipe, cumprindo os critérios funcionais estabelecidos na Seção 2.4 do Plano de Projeto:

1. **Inicialização sem espera de treinamento:** A interface abre diretamente no navegador via Streamlit, carregando os pesos salvos e os artefatos visuais sem exigir que o usuário aguarde o treinamento da rede.
2. **Exploração da base de dados:** Exibição das amostras reais do Fashion-MNIST (rtefatos/amostras_classes_reais.png) com explicação sobre a resolução de 28x28 pixels em tons de cinza e as 10 categorias de vestuário.
3. **Comparação visual do treinamento:** Exibição dos três momentos do treinamento (rtefatos/sprint3/painel_comparativo_evolucao.png — Épocas 0, 5 e 15), permitindo observar a passagem do ruído inicial para silhuetas parciais e finais.
4. **Geração e Download em PNG:** O botão de geração produz novas imagens sintéticas na tela (identificadas como geradas por IA) e disponibiliza o download funcional em arquivo .png.

---

## 2. Situação da Atividade Externa (Registro de Pendência com Justificativa)
- **Status da atividade em escola/comunidade:** **Não realizada (Pendência registrada).**
- **Justificativa (conforme Seções 2.4 e 5.4 do Plano de Projeto):** A equipe não realizou visita ou oficina presencial em escola de ensino médio devido à ausência de confirmação de parceiro externo e à limitação de tempo dentro do calendário do semestre, priorizando-se a conclusão integral da interface educativa, do treinamento da GAN e da documentação técnica. Conforme estipulado no Plano de Projeto, a não realização externa é explicitada de forma transparente como pendência, sem ser apresentada como validação externa concluída.

---

## 3. Observações e Testes Realizados na Demonstração Interna da Equipe
Durante a execução guiada da versão final do software pelos dois integrantes seguindo o roteiro de demonstração:
- **Geração de amostras:** Verificou-se que o modelo gera silhuetas reconhecíveis de calças, calçados e blusas em parte das amostras, enquanto outras permanecem borradas ou com formatos retangulares ambíguos — comportamento esperado para a resolução de 28x28 pixels e documentado nas explicações da interface.
- **Estabilidade e usabilidade:** Os controles da interface em Streamlit responderam sem erros, os testes automatizados (	ests/test_interface.py e 	ests/test_condicional.py) passaram integralmente e o download das imagens em PNG funcionou conforme previsto.
