# Segurança e privacidade

O Auto-Validate não transmite prompts a servidores e não invoca APIs externas por si. A skill pode ser lida por agentes com permissões mais amplas: revise as permissões do agente antes de permitir correções ou acesso a arquivos confidenciais.

**Memória:** o modo padrão não grava nada. Com `--save-memory`, é criado o arquivo local JSONL indicado por `--memory-path`; cabe ao usuário controlar acesso, backups, retenção e exclusão. Não grave chaves, credenciais, dados sensíveis, conteúdo pessoal ou código protegido.

**Relatórios:** evidências e prompts estruturados podem conter informações internas. Antes de fazer commit, limpe identificadores, segredos e referências privadas. Prefira ambientes isolados para testes.

Para reportar vulnerabilidades, abra uma issue sem incluir prova de conceito com dados reais ou segredos.
