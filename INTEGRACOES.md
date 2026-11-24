# Discord e APIs por função

Este documento define como implementar integrações. Não há ponte, serviço de fila ou adaptador pronto neste pacote.

## Discord como interface

Um canal pode falar com o Maestro ou diretamente com um especialista. Rotas diretas continuam obedecendo aos mesmos limites e contratos de tarefa.

Fluxo proposto: evento Discord → identificação do autor autorizado → deduplicação → rota do canal → fila → agente real → resultado estruturado → resposta no canal de origem.

### Passos de implementação

1. Crie uma aplicação e um bot próprios no portal do Discord. Mantenha o token em armazenamento privado de credenciais, fora do Git e do cérebro.
2. Instale o bot em um servidor de teste com permissões mínimas. Configure os intents necessários; texto comum pode exigir Message Content, conforme as regras do Discord.
3. Configure uma tabela privada `channel_id → agent_id`, e uma lista de autores autorizados. Nomes visíveis não substituem IDs.
4. Implemente um serviço para receber eventos pelo Gateway e enviar respostas pelas APIs apropriadas, seguindo a [documentação oficial](https://docs.discord.com/developers/events/gateway).
5. Integre esse serviço ao ambiente real do Maestri. Use um terminal conectado no aplicativo ou uma integração suportada, como o [Maestri Wire](https://www.themaestri.app/en/docs/wire), verificando as capacidades anunciadas pela versão. Wire está em beta; não suponha que exista um endpoint específico de delegação sem conferir o contrato.
6. Persista uma fila local com identificador do pedido e controle de concorrência por agente. Ignore mensagens do próprio bot e deduplique pelo evento de origem.
7. Exija confirmação de recebimento do executor e resultado estruturado. Tela de terminal não é um contrato de entrega.
8. Responda ao canal original com autoria e resultado. Em caso de falha, informe pendência; não simule uma resposta do agente indisponível.

Comece com texto. Depois acrescente voz, transcrição e anexos com limites explícitos de tamanho, formato e retenção. O download e a extração de texto são etapas de preparação, não prova de que o agente compreendeu o arquivo.

Teste reconexão, reinício, evento repetido, agente offline e resposta demorada. Antes de repetir uma ação externa cujo resultado é incerto, reconcilie o estado com o serviço remoto para evitar duplicação.

## Distribuição e Publicação e Instagram

Distribuição e Publicação é responsável pela distribuição; Produção de Carrosséis produz carrosséis e os outros especialistas produzem seus formatos. A integração da Distribuição e Publicação deve expor operações delimitadas, como validar mídia, preparar publicação, consultar processamento e publicar uma versão aprovada.

### Montagem do adaptador

1. Consulte os requisitos atuais da [plataforma Instagram](https://developers.facebook.com/docs/instagram-platform/) e escolha o fluxo de autenticação suportado para a aplicação.
2. Configure uma aplicação Meta e uma conta profissional elegível. Obtenha as permissões necessárias pelo fluxo oficial e passe pelas revisões aplicáveis ao uso pretendido.
3. Armazene credenciais no backend privado. O agente recebe uma ferramenta com operações permitidas; não precisa receber o token no prompt.
4. Implemente o fluxo de publicação indicado pela [documentação de conteúdo](https://developers.facebook.com/docs/instagram-platform/content-publishing/): preparação do contêiner, tratamento de mídia/processamento e publicação. Requisitos diferem por formato e fluxo de login.
5. Vincule a aprovação a destino, legenda, arquivos e versão. Se o conteúdo mudar, obtenha nova aprovação.
6. Registre o identificador devolvido pela API e permita consultar o resultado. Antes de tentar novamente após um timeout, verifique se a publicação ocorreu.

A conexão com o Instagram usa APIs da plataforma Meta; não é uma conexão com o chatbot Meta AI. Este projeto não garante aprovação de aplicação nem substitui as regras do serviço.

## Outras funções

| Função | Adaptador possível | Escopo inicial |
| --- | --- | --- |
| Secretaria | Calendário/e-mail | Consulta e rascunhos; envio conforme autorização |
| Produção visual | Editor e armazenamento | Criar artefatos versionados para revisão |
| Desenvolvimento | Git e ambiente de testes | Branch de trabalho, revisão e evidências |
| Estudos | Fontes e arquivos | Consulta com referência e materiais de estudo |
| Operações | Quadro de tarefas | Estado, dependências e próximo passo |

Não conecte todas as contas a todos os agentes. Separe ferramentas, contextos e permissões por função. Ter um papel configurado não implica acesso a um serviço.

## Contrato mínimo de ferramenta

Toda operação define entrada, resultado, erros, autenticação, tempo limite e comportamento ao repetir um pedido. Para ações externas, mantenha a aprovação e o estado da execução fora do texto livre produzido pelo modelo. Consulte [MODELOS.md](MODELOS.md) para um contrato fictício de tarefa.
