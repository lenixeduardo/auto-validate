# Auto-Validate — Relatório de avaliação

**Projeto:** exemplo-ui
**Entrega:** Entrega UI v1, src/pages/Home.tsx
**Escopo:** Inspecionado src/pages/Home.tsx e comparado visualmente com referencia fornecida.

## Nota geral: 5.7/10

**Média ponderada:** 5.7/10

| Critério | Nota | Peso |
|---|---:|---:|
| fidelity | 5/10 | 35% |
| completeness | 6/10 | 25% |
| accuracy | 8/10 | 20% |
| constraints | 3/10 | 15% |
| usability | 7/10 | 5% |

## Requisitos auditados

| ID | Tipo | Status | Requisito | Evidência |
|---|---|---|---|---|
| R1 | must | violated | Preservar a estrutura de componentes da referencia. | Uma seção extra foi adicionada no meio da homepage. |
| R2 | must | met | Usar white mode. | Fundo claro, texto escuro e sem inversao global de tema. |
| R3 | should | partial | Preservar espacamentos originais. | Espacamento do hero alterado em comparacao com a referencia. |

## Desvios e correções

### F1 — R1 (major, observed)

- **Esperado:** Mesmas secoes e ordem visual da referencia.
- **Observado:** Secao extra alterou a estrutura sem solicitacao.
- **Evidência:** src/pages/Home.tsx:42
- **Correção proposta:** Remover apenas a secao extra; preservar componentes aprovados.
- **Como validar:** Comparar a ordem das secoes com a referencia e executar build.
- **Causa possível (hipótese):** Interpretacao indevida de liberdade criativa.

### F2 — R3 (minor, observed)

- **Esperado:** Espacamentos proximos aos da referencia.
- **Observado:** Hero mais alto que a referencia.
- **Evidência:** Comparacao do hero e src/pages/Home.tsx:19
- **Correção proposta:** Restaurar espacos do hero sem refazer outros blocos.
- **Como validar:** Comparar em viewport identica e tirar nova captura.

## Memória

Candidatas à memória (não salvas automaticamente):
- [project] Em ajustes de UI, preserve as secoes e a ordem original salvo pedido explicito de mudanca. (origem: F1)

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** Avaliação de exemplo; as evidências são ilustrativas, não resultados de um repositório real.
