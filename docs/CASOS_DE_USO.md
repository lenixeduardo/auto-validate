# Casos de uso reproduzíveis — Auto-Validate

Estes casos usam arquivos concretos, incluídos no repositório, e um motor de pontuação executado. O contexto é **controlado**: cada par `before`/`after` foi criado para testar um tipo de divergência frequente em projetos de software. Não são capturas de um projeto externo ou resultados de um modelo independente em produção.

## Caso 01 — Alterações não solicitadas em interface

**Prompt:** “Crie uma página clara contendo somente as seções hero e features, preservando CTA e seu link. Não adicionar seções extras.”

**Entregue antes:** [`ui/before.html`](../examples/cases/ui/before.html). Contém `background:#101521` (dark mode) e `<section id="testimonials">`, que não foi solicitada.

**Autodiagnóstico:** white mode não atendido; seção adicional infringiu uma restrição expressa. A classificação `must_not / violated` impôs limite 3,0, apesar da média ponderada de 5,0.

**Plano:** mudar apenas as cores globais, remover a seção extra e preservar CTA `/produtos`.

**Entrega corrigida:** [`ui/after.html`](../examples/cases/ui/after.html). Teste [`test_ui_failure_and_fixed_behavior`](../tests/test_demo_cases.py) confirma tema, seções e CTA. **Nota: 3,0 → 10,0.**

**Relatórios:** [avaliação inicial](../examples/results/ui-before.md) · [nova avaliação](../examples/results/ui-after.md).

## Caso 02 — Bug de lógica em código Python

**Prompt:** “Ordenar uma lista de strings monetárias numericamente, do menor ao maior; preservar os textos e duplicatas.”

Entrada:

```python
["11.00", "2.50", "3.00", "2.50"]
```

**Entregue antes:** [`code/before.py`](../examples/cases/code/before.py). `sorted(prices)` ordena strings lexicograficamente, produzindo `11.00` primeiro.

**Autodiagnóstico:** requisito obrigatório de ordenação numérica descumprido. O motor limita a nota a 6,0.

**Plano:** usar `Decimal` como chave de ordenação, mantendo os textos originais e duplicatas.

**Entrega corrigida:** [`code/after.py`](../examples/cases/code/after.py). Teste [`test_code_failure_and_fixed_behavior`](../tests/test_demo_cases.py) executa **as duas funções** e confirma a regressão corrigida. **Nota: 6,0 → 10,0.**

**Relatórios:** [avaliação inicial](../examples/results/code-before.md) · [nova avaliação](../examples/results/code-after.md).

## Caso 03 — Alucinação de capacidades em texto técnico

**Prompt:** “Explicar o Auto-Validate sem prometer ausência total de alucinações ou memória automática sem consentimento.”

**Entregue antes:** [`text/before.md`](../examples/cases/text/before.md). Promete “elimina 100% das alucinações” e “grava automaticamente toda conversa”. Essas afirmações contradizem as limitações reais da skill.

**Autodiagnóstico:** duas exigências descumpridas, incluindo violação de restrição expressa; nota limitada a 3,0.

**Plano:** substituir garantia absoluta por explicação responsável; exigir autorização explícita para memória, sem sugerir que a nota cria persistência.

**Entrega corrigida:** [`text/after.md`](../examples/cases/text/after.md). Teste [`test_text_failure_and_fixed_behavior`](../tests/test_demo_cases.py) verifica a remoção do termo absoluto e a inclusão do consentimento. **Nota: 3,0 → 10,0.**

**Relatórios:** [avaliação inicial](../examples/results/text-before.md) · [nova avaliação](../examples/results/text-after.md).

## Reproduzir tudo

Na raiz do repositório:

```bash
python examples/run_demos.py
python -m unittest discover -s tests -v
```

O script gera Markdown e JSON em `examples/results`. Ele **não persiste memória**, já que nenhum `--save-memory` é passado.

## Memória opt-in: gravação e recuperação isoladas

O comando `python examples/demo_memory.py` salva **uma regra sintética** em um diretório temporário, consulta a regra, valida o retorno e descarta o arquivo na saída. Nenhum dado do usuário é preservado. Em utilização real, a opção `--save-memory` exige autorização, armazenamento durável e recuperação ativa pelo agente.

## O que foi e não foi verificado

| Verificado de verdade | Não verificado por estes exemplos |
|---|---|
| Arquivos antes/depois existem | Capacidade da IA de criar auditorias corretas sem orientação |
| Regras de pontuação e limites executam | Eficácia estatística na redução de alucinações |
| Os três bugs foram corrigidos nos fixtures | Alterações de layout em múltiplos navegadores/dispositivos |
| Testes automatizados aprovam os fixes | Uso automático de memória em conversas futuras |
| Relatórios foram gerados pelo CLI | Segurança de aplicação em produção |

**Nota 10 nos demos = todos os requisitos definidos para esses fixtures foram marcados como atendidos.** Não significa perfeição geral ou ausência de falhas não analisadas.
