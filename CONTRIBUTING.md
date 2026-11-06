# Contribuindo

PRs são bem-vindos para novas rubricas, validações, melhorias no CLI, novos cenários reprodutíveis e correções de segurança.

Antes de enviar um PR, rode:

```bash
python -m unittest discover -s tests -v
python examples/run_demos.py
```

Mantenha três princípios: evidência concreta por requisito, correções mínimas sem modificar requisitos não solicitados e memória persistente somente mediante autorização explícita. Não alegue testes que não executou nem crie números fictícios de melhoria.

Ao adicionar um cenário, inclua arquivos `before`/`after`, suas auditorias JSON, os relatórios gerados e testes verificáveis.
