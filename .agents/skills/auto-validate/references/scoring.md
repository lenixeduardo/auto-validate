# Rubrica e limites

A nota final ponderada é calculada a partir das notas atribuídas pelo agente às dimensões abaixo. Atribua valores de 0 a 10 com uma justificativa e evidências observáveis.

| Dimensão | Peso | Pergunta |
|---|---:|---|
| `fidelity` | 35% | A entrega preservou a intenção e o conteúdo solicitados? |
| `completeness` | 25% | Todos os requisitos explícitos foram atendidos? |
| `accuracy` | 20% | As afirmações são verificáveis, sem invenções detectáveis? |
| `constraints` | 15% | Os itens proibidos e as preservações obrigatórias foram respeitados? |
| `usability` | 5% | A entrega pode ser utilizada na forma solicitada? |

Nota base = soma das notas × pesos. Arredondamento a 1 decimal.

Limites conservadores, aplicados após a média:
- `must_not` com status `violated`: teto **3,0**.
- `must` com status `missed` ou `violated`: teto **6,0**.
- Finding observado `critical`: teto **3,0**.
- Finding observado `major`: teto **7,0**.
- `must` com status `unverifiable`: teto **8,0** (não confunda falta de dados com êxito).

Os tetos são configurados como escolha metodológica desta skill, não como padrão científico ou medição do modelo. Se um requisito está `partial` ou `missed`, um finding correspondente deve explicar a divergência. `unverifiable` não constitui prova de erro nem de êxito.

Faixas de interpretação: 0–3 incompatível; acima de 3 até 6 divergências relevantes; acima de 6 até 8 boa entrega com ajustes; acima de 8 até 10 alta fidelidade. A nota pode ser zero. Nunca eleve artificialmente a nota para agradar o usuário.
