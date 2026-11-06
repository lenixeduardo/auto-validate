---
name: auto-validate
description: Avalia entregas de agentes de IA contra a solicitação original (nota 0–10), identifica desvios com evidências, planeja correções mínimas, revalida e propõe regras para memória persistente opcional. Use quando o usuário solicitar nota, auditoria, comparação prompt vs resposta, autocorreção ou prevenção de erros recorrentes. Não acione para toda resposta simples nem afirme ter executado validação sem fazê-la.
license: MIT
metadata:
  version: "1.1.0"
---

# Auto-Validate

## Objetivo

Comparar o pedido **original** e suas restrições com uma entrega concreta; tornar os desvios observáveis; corrigir apenas o necessário; reavaliar; e, quando autorizado, registrar regras reutilizáveis. A nota é uma **heurística explicável**, não uma prova de correção ou de ausência de alucinação.

## Quando ativar

- Pedido explícito: "dê uma nota de 0 a 10", "valide", "corrija o desvio", "compare com o prompt", "auto-validate".
- Revisão de uma entrega crítica na qual os requisitos originais possam ser recuperados.
- Revisão após uma correção anterior para comprovar se o problema foi resolvido.

Não presuma acesso a prompts ocultos, arquivos não lidos, histórico indisponível ou memória não conectada. Se faltarem evidências, marque `unverifiable`; não invente um resultado. Não aplique automaticamente alterações em repositórios externos ou salve memória sem autorização adequada.

## Ciclo obrigatório

1. **Recuperar a fonte de verdade.** Use o pedido original, restrições, referências e arquivos efetivamente acessíveis. Registre o escopo auditado. Não substitua uma exigência explícita por uma preferência inferida.
2. **Extrair requisitos atômicos.** Identifique `must`, `must_not` e `should`, separando itens verificáveis. Defina IDs `R1`, `R2` etc. Respeite prioridades e conflitos: solicite decisão quando essencial, senão marque a limitação.
3. **Inspecionar a entrega real.** Para cada requisito, marque `met`, `partial`, `missed`, `violated` ou `unverifiable`; inclua evidência verificável (trecho, arquivo/linha, captura, teste ou escopo inspecionado). A ausência não deve ser alegada sem indicar o escopo verificado.
4. **Pontuar segundo rubrica.** Avalie fidelidade (35%), completude (25%), precisão/lastro (20%), restrições (15%) e utilidade (5%), cada uma de 0 a 10. Leia `references/scoring.md`; não force nota alta. Uma falha grave pode limitar a nota final.
5. **Reconhecer os erros.** Para cada desvio, registre o que foi pedido, o que foi observado, a evidência, a gravidade, a correção mínima e o teste de confirmação. Use "causa possível" para hipóteses; não afirme conhecer processos internos do modelo.
6. **Apresentar um plano de correção.** Priorize erros críticos, preserve o que já está correto, não invente novos requisitos. Corrija somente se houver autorização e meios de execução; caso contrário entregue o plano.
7. **Revalidar.** Após cada correção, repita a avaliação sobre o resultado atualizado e compare com a avaliação anterior. Limite a **duas** rodadas de autocorreção por padrão; se persistirem falhas, reporte impedimentos em vez de iniciar um loop infinito.
8. **Aprendizado opcional.** Proponha regras preventivas atômicas, contextuais e verificáveis. Só grave em um armazenamento persistente **real** com autorização explícita, explicando seu escopo, retenção e possibilidade de remoção. Não guarde senhas, tokens, dados pessoais sensíveis ou trechos confidenciais sem autorização específica. A memória é uma ajuda de recuperação, não garantia de que um agente a usará futuramente.
9. **Validar a própria validação.** Confira se cada conclusão se ancora em evidência, se a nota condiz com os desvios e se os itens não verificáveis não foram tratados como atendidos.

## Artefato e automação local

Monte um JSON no formato `assets/audit.template.json`, usando `references/schema.md` como contrato. Os valores das cinco dimensões são julgamentos do agente baseados nas evidências, **não** calculados por similaridade de palavras.

Execute, da raiz desta skill (ou use caminhos absolutos):

```bash
python scripts/auto_validate.py check --input caminho/avaliacao.json --output caminho/relatorio.md
```

O script valida estrutura, aplica pesos e limites, emite relatório e retorna código não zero para uma avaliação incoerente. Para gravar aprendizados com autorização prévia:

```bash
python scripts/auto_validate.py check --input caminho/avaliacao.json --output caminho/relatorio.md \
  --save-memory --memory-path caminho/auto-validate-rules.jsonl
python scripts/auto_validate.py memory search --path caminho/auto-validate-rules.jsonl --query "preservar layout" --project "meu-projeto"
```

Outros comandos: `memory list`, `memory remove`. O armazenamento JSONL precisa estar em disco persistente ou repositório controlado; armazenamento temporário não garante persistência entre sessões. Revise sempre as regras recuperadas antes de aplicá-las. Consulte `references/memory.md`.

## Resposta mínima ao usuário

Informe: **nota geral**, **nota por dimensão**, **desvios observados e evidências**, **o que será corrigido**, **verificação planejada ou executada**, **itens inconclusivos** e **estado da memória** (`não gravada`, `gravada em <local>` ou `indisponível`). Se nada foi executado, não diga que foi corrigido. Se a skill não foi acionada, não declare que foi aplicada.

Use linguagem no idioma do usuário. Evite classificações cosméticas: uma entrega atraente mas infiel ao pedido deve receber nota baixa.
