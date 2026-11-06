# Contrato da avaliação (`schema_version = "1.0"`)

O arquivo de entrada é JSON com os seguintes campos:

- `schema_version`: string `"1.0"`.
- `project`: identificador não vazio (use nome genérico se necessário).
- `request`: pedido original ou resumo fiel com referência ao documento/fonte.
- `deliverable`: identificação não vazia da entrega auditada (commit, caminho, mensagem etc.).
- `scope`: o que foi de fato lido, executado ou inspecionado.
- `criteria`: objeto com números de 0 a 10 para `fidelity`, `completeness`, `accuracy`, `constraints`, `usability`.
- `requirements`: array não vazio de objetos com `id`, `text`, `type` (`must`, `must_not`, `should`), `status` (`met`, `partial`, `missed`, `violated`, `unverifiable`) e `evidence`. Especifique `location` quando aplicável.
- `findings`: array de objetos com `id`, `requirement_id`, `severity` (`critical`, `major`, `minor`), `classification` (`observed`, `hypothesis`), `expected`, `observed`, `evidence`, `fix`, `verify`. `possible_cause` é opcional. Finding `hypothesis` não prova violação.
- `memory_candidates`: array opcional com `rule`, `scope` (`project`, `global`), `source_finding_id` e `reason`. Só regras vinculadas a um finding observado podem ser salvas. Armazenamento é opt-in.
- `notes`: texto opcional.

Exemplo em `assets/audit.template.json`. O script verifica consistência do preenchimento, e não a veracidade semântica das evidências. Um ser humano ou um teste externo continua necessário para checagem independente.
