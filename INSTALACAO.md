# Montagem do núcleo no Maestri

Este guia monta uma equipe local com instruções e memória. Não instala automaticamente Discord, Instagram ou os provedores de IA.

## Caminho assistido por Claude Code ou Codex

Abra o checkout numa sessão local do seu agente e peça: **“Leia AGENTS.md e monte minha orquestra com todos os papéis, em uma pasta privada nova.”** O procedimento cria arquivos com `bootstrap.py`, verifica a memória e os papéis e configura terminais somente quando estiver num ambiente Maestri realmente conectado.

O gerador requer Python 3.10 ou superior e usa somente a biblioteca padrão. Antes de escrever, execute `python bootstrap.py --target ../orchestra-workspace --full --dry-run`; para criar, repita sem `--dry-run`. Depois execute `python bootstrap.py --target ../orchestra-workspace --check`, sem `--full`, para conferir a instalação. O padrão sem `--full` contém três papéis. Não é necessário fornecer dados pessoais ou credenciais para gerar a estrutura.

Reexecutar a mesma configuração preserva os arquivos idênticos. Arquivos alterados ou destino não vazio sem manifesto interrompem o procedimento; escolha outra pasta em vez de sobrescrever trabalho existente.

### Permissões do workspace

O cérebro fica fora do checkout público. Por isso, abrir somente o checkout em uma ferramenta com escrita limitada ao workspace pode impedir a criação do destino irmão. Um ponto de partida simples é:

```text
orchestra-lab/                 ← pasta aberta na ferramenta de IA
  repo/                       ← checkout público
  orchestra-workspace/        ← destino privado criado pelo gerador
```

Peça ao agente: **“Leia repo/AGENTS.md, trabalhe a partir de repo e crie a estrutura completa em ../orchestra-workspace, usando somente os exemplos publicados. Não configure contas.”**

Alternativamente, mantenha o checkout aberto e conceda acesso de escrita apenas ao destino privado pelos controles da ferramenta. No Codex CLI, `--add-dir` adiciona um diretório ao escopo de escrita; o modo da sessão também precisa permitir escrita e execução. Consulte a [referência oficial de comandos](https://learn.chatgpt.com/docs/developer-commands) e a [documentação de sandbox](https://learn.chatgpt.com/docs/sandboxing?surface=cli).

Em Claude Code, use os controles de diretório e permissões disponíveis na versão instalada. Se o ambiente recusar leitura, execução ou escrita, a instalação ainda não aconteceu: registre o bloqueio e ajuste o workspace autorizado. Não contorne a rejeição desativando proteções.

## 1. Pré-requisitos

- Para gerar a estrutura e usar um papel por vez em Codex ou Claude Code, Maestri é opcional. Para montar terminais e conexões no canvas, instale-o pela [página oficial](https://www.themaestri.app/), seguindo as instruções para seu sistema.
- Instale e autentique um agente de código suportado, seguindo a documentação do próprio provedor. A [documentação de terminais do Maestri](https://www.themaestri.app/en/docs/terminals) explica que esses agentes devem estar instalados previamente.
- Tenha acesso autorizado ao modelo escolhido. Assinaturas, limites e APIs são configurados separadamente; este projeto não fornece créditos ou acesso gratuito.
- Git é opcional para baixar o material; também é possível usar o ZIP do GitHub.

## 2. Obtenha os modelos

Na página deste repositório, use **Code → Download ZIP** e extraia em uma pasta nova. Ou copie o endereço HTTPS mostrado em **Code** e execute:

```sh
git clone <URL_HTTPS_COPIADA_DO_REPOSITORIO> orchestra
cd orchestra
```

Substitua o marcador antes de executar. Mantenha este checkout como material público. Crie separadamente uma pasta privada de trabalho, por exemplo `orchestra-workspace`, fora do checkout público e de pastas publicadas.

## 3. Prepare a memória privada

Na pasta privada, monte a árvore descrita em [BRAIN.md](BRAIN.md), usando os exemplos fictícios de [MODELOS.md](MODELOS.md), ou use o gerador acima. Não copie conversas, dados de contas ou vaults existentes para o repositório público.

Crie um `AGENTS.md` na raiz privada com as instruções comuns dos modelos. Se o agente escolhido exigir `CLAUDE.md`, configure também esse arquivo. O Maestri documenta uma opção de sincronização entre ambos em [Workspaces](https://www.themaestri.app/en/docs/workspaces).

## 4. Crie um workspace e três terminais

Se quiser começar diretamente no Codex ou Claude Code, abra a pasta privada gerada e peça **“Leia START_HERE.md e faça o primeiro teste com dados fictícios.”** O arquivo contém prompts para produção de três títulos e revisão sequencial, salvando os resultados em `runtime/outputs/`. Esse uso de papéis numa sessão não cria uma equipe em processos separados. As etapas abaixo são a opção com Maestri.

1. Crie um workspace no Maestri apontando para a pasta privada de trabalho.
2. Crie um terminal com o preset do agente instalado e nomeie-o **Maestro Geral**.
3. Atribua a ele o papel de Maestro usando o modelo de coordenação. Habilite o modo Maestro pelos controles da versão instalada; veja a [documentação oficial](https://www.themaestri.app/en/docs/maestro).
4. Crie um executor, por exemplo **Produção de Carrosséis**, e um revisor, **Revisão e Qualidade**, cada um com seu papel e instruções próprias.
5. Conecte os terminais no canvas para permitir colaboração. O papel de cada um precisa estar nas instruções: apenas desenhar uma conexão não define responsabilidade.

O nome de um preset depende da instalação. Se usar o CLI do Maestri, consulte os presets reais e a ajuda antes de automatizar a criação. Não copie nomes de contas de outra pessoa.

## 5. Verifique a comunicação

Dentro de um terminal aberto pelo próprio Maestri, use:

```sh
maestri list
```

Use exatamente os nomes retornados. Um nome pode incluir o workspace. Para um teste curto, substitua o marcador pelo nome real do executor:

```sh
maestri ask "<NOME_EXATO_DO_EXECUTOR>" "Confirme seu papel e proponha três títulos fictícios sobre organização de arquivos. Não publique nada."
```

Não invente variáveis de sessão nem execute o CLI fora do contexto do aplicativo supondo que ele estará conectado. Em caso de erro, use `maestri debug` e confira a ajuda da versão instalada.

## 6. Faça um teste de memória e delegação

Peça ao Maestro que consulte `brain/RECALL.md`, delegue uma tarefa sintética ao executor e solicite uma revisão. Exija: resultado, autoria, evidência, pendências e próximo passo.

Registre uma decisão fictícia em uma nota canônica e retome o teste em nova sessão. O agente deve encontrar a nota pelo índice, sem carregar o cérebro inteiro. Uma resposta correta isolada não mede economia de tokens; consulte as medições do provedor, quando disponíveis.

## 7. Amplie por função

Adicione os demais papéis da tabela do README conforme a necessidade. Para conteúdo: estratégia → produção → revisão → distribuição. Para desenvolvimento: coordenação técnica → implementador → revisão. Dê a cada tarefa um responsável principal e evite dois agentes editando o mesmo arquivo ao mesmo tempo.

## 8. Integre canais e ferramentas

Para usar o cérebro em vários dispositivos pelo Google Drive e configurar sua leitura no Codex, Claude Code ou Antigravity, siga [TEORIA-MEMORIA.md](TEORIA-MEMORIA.md). Essa etapa é opcional e manual; mantenha runtime e coordenação fora da sincronização de notas. O modelo de governança da equipe está em [INFRAESTRUTURA.md](INFRAESTRUTURA.md).

Siga [INTEGRACOES.md](INTEGRACOES.md). O núcleo local funciona por interação com os terminais; a ponte Discord e os adaptadores de API são uma fase adicional de implementação, não estão incluídos como executáveis neste pacote.

Antes de considerar a instalação ampliada pronta, demonstre: mensagem real chegando ao agente certo, retorno no canal de origem, leitura de memória relevante, revisão, falha visível e nenhuma duplicação após reconexão.

## Verifique a instalação mínima

Na pasta do checkout, execute `python -I test_bootstrap.py -v`. Os testes não conectam contas, não chamam modelos e não usam memória privada. Criam destinos temporários novos e verificam também as entradas `AGENTS.md` e `CLAUDE.md`.

Depois de gerar sua pasta privada, confirme a existência de `brain/RECALL.md`, da nota fictícia, dos papéis e dos JSONs. Para os resultados conhecidos e os fluxos ainda não validados com um agente real, consulte [VERIFICACAO.md](VERIFICACAO.md).

Para verificar a estrutura depois de personalizar notas e papéis, execute no checkout `python bootstrap.py --target <PASTA_PRIVADA> --check`. Essa operação é somente de leitura e usa o perfil registrado no manifesto; não combine `--check` com `--full` ou `--dry-run`. Se faltar um arquivo ou houver configuração inválida, ela informa o erro sem alterar a instalação.
