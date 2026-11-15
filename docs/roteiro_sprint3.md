# Roteiro Inicial da Oficina Educativa (20 a 30 minutos)

---

## 1. Apresentação dos Exemplos da Base (5 minutos)
- Exibir na interface os exemplos reais do **Fashion-MNIST** (artefatos/amostras_classes_reais.png).
- Explicar que essas imagens servem como referência para o treinamento e mostrar como a resolução de 28x28 pixels em tons de cinza representa as 10 categorias de vestuário.

## 2. Funcionamento da GAN e Evolução do Treinamento (10 minutos)
- Apresentar de forma acessível o papel conjunto das duas redes: o **Gerador** (que produz imagens a partir de ruído) e o **Discriminador** (que procura distinguir imagens da base das imagens geradas).
- Exibir o painel comparativo (artefatos/sprint3/painel_comparativo_evolucao.png) e comparar os três momentos:
  - **Início (Época 0):** Pixels espalhados sem forma.
  - **Meio (Época 5):** Formação do contraste entre fundo escuro e silhuetas centrais borradas.
  - **Fim (Época 15):** Surgimento de contornos mais definidos de calças, calçados e blusas, ao lado de figuras que continuam ambíguas.
- Mostrar brevemente no código como o modelo treinado previamente é carregado para gerar imagens.

## 3. Experimentação Prática pelos Participantes (10 minutos)
- Convidar os estudantes a acionar o botão de geração na interface (app.py).
- Observar as novas imagens ampliadas na tela e demonstrar o download do conjunto em formato PNG.

## 4. Discussão sobre Limitações e Fechamento (5 minutos)
- Conversar com o grupo sobre imagens confusas, borradas ou repetidas que apareceram durante o teste.
- Discutir os limites da ferramenta (baixa resolução e aprendizado puramente visual) e registrar os comentários e dúvidas dos participantes.
