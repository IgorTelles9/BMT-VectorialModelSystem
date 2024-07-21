# Métricas de desempenho do sistema de Recuperação da Informação
Não consegui identificar o problema no código, mas todas as métricas ficaram IDÊNTICAS. Eu debuggei por horas e não consegui encontrar a causa. Acredito ser algo estúpido, mas não consegui encontrar a tempo. Os resultados estão diferentes, então acredito que seja algo no gerador de métricas. Mas também não encontrei nada no código dele. De qualquer jeito, seguem os resultados:

## Gráfico de 11 pontos de Precision e Recall
<hr/>

- Com stemmer: 11pontos-stemmer-1.csv e 11pontos-stemmer-2.png.
- Sem stemmer: 11pontos-nostemmer-1.csv e 11pontos-nostemmer-2.png.

## F1
<hr/>

- Com stemmer: 7.60%
- Sem stemmer: 7.60%

## Precision@5
<hr/>

- Com stemmer: 4.44%
- Sem stemmer: 4.44%

## Precision@10
<hr/>

- Com stemmer: 4.14%
- Sem stemmer: 4.14%

## Mean Average Precision (MAP)
<hr/>

- Com stemmer: 4.41% 
- Sem stemmer: 4.41%

## Mean Reciprocal Rank (MRR)
<hr/>

- Com stemmer: 13.25%
- Sem stemmer: 13.25%

## Mean Discounted Cumulative Gain (DCG)
<hr/>

- Com stemmer: 20.54%
- Sem stemmer: 20.54%

## Mean Normalized Discounted Cumulative Gain (NDCG)
<hr/>

- Com stemmer: 12.99%
- Sem stemmer: 12.99%