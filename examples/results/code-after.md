# Auto-Validate — Relatório de avaliação

**Projeto:** demo-code
**Entrega:** examples/cases/code/after.py
**Escopo:** Execução da função sort_prices corrigida com Decimal

## Nota geral: 10.0/10

**Média ponderada:** 10.0/10

| Critério | Nota | Peso |
|---|---:|---:|
| fidelity | 10/10 | 35% |
| completeness | 10/10 | 25% |
| accuracy | 10/10 | 20% |
| constraints | 10/10 | 15% |
| usability | 10/10 | 5% |

## Requisitos auditados

| ID | Tipo | Status | Requisito | Evidência |
|---|---|---|---|---|
| R1 | must | met | Ordenar preços por valor numérico ascendente. | after.py ordena com key=lambda price: Decimal(price); teste de regressão passou |
| R2 | must | met | Manter strings originais e entradas repetidas. | after.py mantém 2.50 em duas posições |

## Desvios e correções

Nenhum desvio foi registrado dentro do escopo inspecionado.
## Memória

Candidatas à memória (não salvas automaticamente):
- Nenhuma

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** Correção executada localmente e testada; não avalia entrada inválida (fora do escopo).
