# Auto-Validate — Relatório de avaliação

**Projeto:** demo-code
**Entrega:** examples/cases/code/before.py
**Escopo:** Execução da função sort_prices sobre ["11.00", "2.50", "3.00", "2.50"]

## Nota geral: 6.0/10

**Média ponderada:** 6.0/10

| Critério | Nota | Peso |
|---|---:|---:|
| fidelity | 6/10 | 35% |
| completeness | 6/10 | 25% |
| accuracy | 3/10 | 20% |
| constraints | 10/10 | 15% |
| usability | 5/10 | 5% |

## Requisitos auditados

| ID | Tipo | Status | Requisito | Evidência |
|---|---|---|---|---|
| R1 | must | missed | Ordenar preços por valor numérico ascendente. | before.py usa sorted(prices), saída começa com 11.00 |
| R2 | must | met | Manter strings originais e entradas repetidas. | before.py retorna strings originais e mantém 2.50 duas vezes |

## Desvios e correções

### F1 — R1 (major, observed)

- **Esperado:** 2.50, 2.50, 3.00, 11.00
- **Observado:** 11.00, 2.50, 2.50, 3.00
- **Evidência:** before.py: sorted(prices) faz ordenação lexicográfica
- **Correção proposta:** Converter chave de ordenação para Decimal
- **Como validar:** Executar tests/test_demo_cases.py e validar ordem numérica

## Memória

Candidatas à memória (não salvas automaticamente):
- [project] Ao ordenar valores monetários em strings, use uma chave numérica decimal e preserve os valores originais. (origem: F1)

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** O erro é comprovado executando o código local, não apenas lendo o prompt.
