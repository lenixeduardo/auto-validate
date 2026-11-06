# Auto-Validate — Relatório de avaliação

**Projeto:** demo-text
**Entrega:** examples/cases/text/before.md
**Escopo:** Inspeção do Markdown local para afirmações absolutas e política de persistência

## Nota geral: 3.0/10

**Média ponderada:** 3.4/10

| Critério | Nota | Peso |
|---|---:|---:|
| fidelity | 3/10 | 35% |
| completeness | 6/10 | 25% |
| accuracy | 2/10 | 20% |
| constraints | 1/10 | 15% |
| usability | 6/10 | 5% |

**Limites aplicados:** Restrição expressa violada (must_not).; Desvio crítico observado.

## Requisitos auditados

| ID | Tipo | Status | Requisito | Evidência |
|---|---|---|---|---|
| R1 | must_not | violated | Não afirmar que elimina 100% das alucinações. | before.md: elimina 100% das alucinações |
| R2 | must | missed | Informar que memória persistente exige consentimento explícito. | before.md: grava automaticamente toda conversa |
| R3 | must | met | Explicar que compara o pedido e propõe correções. | before.md: compara o pedido com o resultado e propõe correções |

## Desvios e correções

### F1 — R1 (critical, observed)

- **Esperado:** Evitar promessa absoluta
- **Observado:** Promete eliminação de 100% das alucinações
- **Evidência:** before.md: expressão literal 100%
- **Correção proposta:** Trocar garantia por benefício condicional verificável
- **Como validar:** Buscar afirmações absolutas no texto final

### F2 — R2 (major, observed)

- **Esperado:** Memória persistente requer autorização
- **Observado:** Afirma armazenamento automático de toda conversa
- **Evidência:** before.md: grava automaticamente
- **Correção proposta:** Especificar opt-in e armazenamento real
- **Como validar:** Testar presença de consentimento explícito

## Memória

Candidatas à memória (não salvas automaticamente):
- [project] Evite garantias absolutas de precisão e descreva limitações verificáveis. (origem: F1)

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** Este caso demonstra revisão editorial de afirmações verificáveis; não é uma medição de taxa de alucinação.
