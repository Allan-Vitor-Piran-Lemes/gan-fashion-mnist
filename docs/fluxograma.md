# Fluxograma do processo real

```mermaid
flowchart TD
    A[Fashion-MNIST] --> B[Treino oficial: 60 mil imagens]
    A --> C[Teste oficial: 10 mil reservadas]
    B --> D[Divisão estratificada com semente 42]
    D --> E[Treino: 50 mil]
    D --> F[Validação: 10 mil reservadas]
    E --> G[Normalização para -1 a 1]
    G --> H[Discriminador: imagens reais e geradas]
    I[Ruído aleatório] --> J[Gerador]
    J --> H
    H --> K[Atualizações alternadas das duas redes]
    K --> L[Checkpoint, perdas e imagens por época]
    L --> M[Carregar gerador salvo em modo de avaliação]
    N[Novo ruído definido pela semente] --> M
    M --> O[Interface: geração e visualização]
```

Validação e teste não atualizam as redes. A interface apenas carrega o modelo, sem treinar.
O painel histórico original é apresentado separadamente da execução local.
Este fluxograma complementa o diagrama simplificado exibido na interface.

## Entrega educativa

Os resultados técnicos alimentam a aplicação, a apostila introdutória e o relatório acadêmico. A conclusão inclui revisão dos exemplos, textos e comandos pelos próprios autores. O roteiro é de leitura e exploração autônoma.
