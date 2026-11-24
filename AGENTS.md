# Brain Orchestra — entrada de instalação para agentes

Este repositório contém uma estrutura genérica e um gerador local. Não contém memória, contas ou credenciais de uma pessoa.

## Quando o usuário pedir para montar ou instalar

1. Leia `README.md`, `INSTALACAO.md` e `bootstrap.py`. Explique brevemente o que será criado.
2. Localize Python 3.10 ou superior no ambiente. Não instale dependências globalmente; o gerador usa somente a biblioteca padrão.
3. Escolha uma pasta privada nova, irmã deste checkout, chamada `orchestra-workspace`. Não escreva o cérebro dentro do checkout público. Se ela já tiver conteúdo, inspecione o manifesto do gerador; nunca substitua arquivos modificados ou uma instalação alheia.
4. Execute primeiro `python bootstrap.py --target <PASTA_PRIVADA> --full --dry-run` e depois a mesma chamada sem `--dry-run`. Use o comando Python disponível na plataforma. Passe o caminho como argumento literal com o quoting correto.
5. Verifique os arquivos gerados: `AGENTS.md`, `CLAUDE.md`, `brain/RECALL.md`, `roles/`, `config/routes.example.json`, `config/integrations.example.json` e `setup-manifest.json`.
6. Se esta sessão realmente estiver dentro do Maestri, use `maestri list`, `maestri preset list` e a ajuda da versão instalada para descobrir terminais, presets, papéis e conexões. Reutilize agentes existentes. Configure os papéis de `roles/`, o Maestro e as conexões usando as capacidades reais disponíveis. Não invente flags, IDs, contas ou variáveis de sessão. Para falha de comunicação, use `maestri debug`.
7. Se a sessão não estiver no Maestri, conclua a geração local e mostre como abrir a pasta privada no aplicativo. Não declare terminais criados ou agentes ativos apenas porque seus arquivos existem.
8. Teste com um pedido fictício: três títulos sobre organização de arquivos, seguido de revisão. Teste recuperação seletiva lendo o índice e a nota de exemplo; não carregue o cérebro inteiro.
9. Explique quais etapas estão prontas e quais dependem do ambiente. Discord e Instagram são integrações opcionais a implementar/configurar conforme `INTEGRACOES.md`; este pacote não contém seus serviços executáveis. Não crie contas, exponha tokens ou publique conteúdo como parte do setup.

## Limites

- Este procedimento se aplica ao pedido explícito de instalação. Uma revisão do repositório não autoriza executar o gerador ou criar agentes.
- Não importe perfil pessoal, conversas, clientes, credenciais ou memória preexistente.
- Não publique a pasta privada, não faça push e não altere configurações de contas durante o setup.
- Para mudanças no próprio projeto, preserve links, execute os testes pertinentes e mantenha exemplos sintéticos.
