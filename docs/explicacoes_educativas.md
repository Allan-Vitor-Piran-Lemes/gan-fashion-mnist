# Explicações Educativas — Laboratório de IA Generativa com GANs

**Responsável:** Allan Vitor Piran Lemes  
**Esforço registrado:** 3 horas  

---

## 1. Sobre a Base de Dados (Fashion-MNIST)
A inteligência artificial precisa observar milhares de exemplos para identificar padrões. Neste laboratório, utilizamos o conjunto público **Fashion-MNIST**, com 60.000 imagens de treinamento e 10.000 de teste distribuídas em 10 categorias de vestuário (camisetas, calças, pulôveres, vestidos, casacos, sandálias, camisas, tênis, bolsas e botas). Cada imagem possui **28x28 pixels** em tons de cinza: para o computador, trata-se de uma grade numérica que indica a intensidade de brilho de cada ponto.

## 2. O Papel do Gerador
O **Gerador** é a rede neural responsável por produzir novas figuras. Ele recebe como entrada uma lista de números sorteados ao acaso (ruído aleatório) e realiza cálculos para transformá-la em uma imagem de 28x28 pixels. No início do treinamento, ele produz apenas pontos espalhados sem formato definido.

## 3. O Papel do Discriminador
O **Discriminador** é a segunda rede neural e atua como um avaliador. Ele analisa tanto imagens reais da base Fashion-MNIST quanto imagens produzidas pelo Gerador, tentando distinguir quais são originais da base e quais foram geradas artificialmente. O retorno desse avaliador orienta o ajuste matemático do Gerador a cada época.

## 4. Limitações Observadas
- **Baixa resolução (28x28 pixels):** Devido à quantidade reduzida de pixels, as imagens mostram apenas contornos gerais, sem detalhes finos como botões, costuras ou cadarços.
- **Formas borradas ou ambíguas:** A rede não compreende o significado real de uma peça de roupa; ela apenas reproduz padrões estatísticos de brilho. Por isso, surgem figuras manchadas, incompletas ou que misturam formatos de categorias diferentes.
- **Oscilação no treinamento:** Mais tempo de treino altera o formato das imagens, mas não garante melhora constante nem elimina peças defeituosas ou repetitivas.

---

## 5. Situação do Contato com Parceiro Externo (Registro de Pendência)
- **Status:** Não realizado (Registrado como pendência conforme critério da tarefa no Jira e Seção 2.4 do Plano de Projeto).
- **Descrição:** Não houve confirmação de parceiro externo nem apresentação em escola. Os textos educativos foram elaborados pela equipe e integrados diretamente à interface (app.py) e à documentação do repositório para apoiar a demonstração do software.
