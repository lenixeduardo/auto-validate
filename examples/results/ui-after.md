# Auto-Validate — Relatório de avaliação

**Projeto:** demo-ui
**Entrega:** examples/cases/ui/after.html
**Escopo:** Arquivo HTML local versionado; testes checam tema, IDs e CTA

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
| R1 | must | met | Usar tema claro (white mode). | after.html: background #ffffff e color #182134 |
| R2 | must_not | met | Não adicionar seções além de hero e features. | after.html: sections hero e features; tests/test_demo_cases.py |
| R3 | must | met | Preservar CTA Explorar produtos apontando para /produtos. | after.html: a.cta href=/produtos |

## Desvios e correções

Nenhum desvio foi registrado dentro do escopo inspecionado.
## Memória

Candidatas à memória (não salvas automaticamente):
- Nenhuma

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** Após alteração real do HTML; resultado verificado por teste automatizado.
