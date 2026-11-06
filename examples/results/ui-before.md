# Auto-Validate — Relatório de avaliação

**Projeto:** demo-ui
**Entrega:** examples/cases/ui/before.html
**Escopo:** Arquivo HTML local versionado; inspecionar CSS e IDs das seções, com assertions em tests/test_demo_cases.py

## Nota geral: 3.0/10

**Média ponderada:** 5.0/10

| Critério | Nota | Peso |
|---|---:|---:|
| fidelity | 4/10 | 35% |
| completeness | 6/10 | 25% |
| accuracy | 7/10 | 20% |
| constraints | 2/10 | 15% |
| usability | 7/10 | 5% |

**Limites aplicados:** Restrição expressa violada (must_not).

## Requisitos auditados

| ID | Tipo | Status | Requisito | Evidência |
|---|---|---|---|---|
| R1 | must | missed | Usar tema claro (white mode). | examples/cases/ui/before.html: body background #101521, color #ffffff |
| R2 | must_not | violated | Não adicionar seções além de hero e features. | examples/cases/ui/before.html: section id=testimonials |
| R3 | must | met | Preservar CTA Explorar produtos apontando para /produtos. | examples/cases/ui/before.html: a.cta href=/produtos |

## Desvios e correções

### F1 — R1 (major, observed)

- **Esperado:** Body com fundo branco e texto escuro
- **Observado:** Fundo quase preto e texto branco
- **Evidência:** before.html: style body
- **Correção proposta:** Mudar apenas as cores globais para white mode
- **Como validar:** Conferir CSS de body e executar teste de regressão

### F2 — R2 (major, observed)

- **Esperado:** Exatamente hero e features
- **Observado:** Seção testimonials foi adicionada
- **Evidência:** before.html: section id=testimonials
- **Correção proposta:** Remover seção não autorizada
- **Como validar:** Verificar IDs de section via HTMLParser

## Memória

Candidatas à memória (não salvas automaticamente):
- [project] Em UI baseada em referência, não acrescente seções além das solicitadas. (origem: F2)

## Limitações

A nota usa critérios fornecidos pelo agente. Este script verifica consistência e calcula notas, mas não verifica semanticamente a verdade das evidências.

**Observações:** Demonstração reproduzível: fixture local, não uma inspeção de interface externa.
