# Orchestra Brain: memória consultável e contexto seletivo

Orchestra Brain é um padrão de organização de conhecimento em Markdown. Cada instalação cria seu próprio cérebro privado. Um editor de texto basta; ferramentas de notas e busca podem ser adicionadas depois.

## Estrutura sugerida

Crie esta árvore na pasta privada de trabalho, fora do checkout público:

```text
orchestra-workspace/
  AGENTS.md
  brain/
    RECALL.md
    00 Inbox/
    01 Base/
      regras.md
    02 Projetos/
      exemplo.md
    03 Sessoes/
    04 Decisoes/
    06 Referencias/
  runtime/
    tasks/
    outputs/
```

Os arquivos de `brain` guardam conhecimento. O diretório `runtime` guarda estado de execução e artefatos; não deve ser lido inteiro como memória nem enviado automaticamente ao modelo.

## Recuperação em duas etapas

**Índice:** `RECALL.md` contém títulos, uma frase sobre cada nota e seu caminho relativo. Deve ser curto o suficiente para servir de mapa.

**Consulta:** o agente escolhe a nota relevante, lê o trecho necessário e registra de onde veio a informação. Se o índice não resolver, pode buscar títulos ou termos; não deve despejar todo o vault no prompt.

Exemplo de índice fictício:

```markdown
# RECALL
- Regras comuns: 01 Base/regras.md
- Projeto de exemplo, objetivo e estado: 02 Projetos/exemplo.md
- Decisões: consultar 04 Decisoes apenas quando a tarefa depender delas.
```

## Escrita após uma tarefa

Atualize primeiro uma nota canônica existente. Uma síntese útil registra fato ou decisão, fonte, data, limitações e próxima ação. Use sessões para resumos temporais e Inbox para material ainda não consolidado. Preserve rastreabilidade ao substituir uma decisão antiga.

Não salve segredos, tokens, cookies, arquivos de ambiente ou logs brutos no cérebro. Dados sensíveis necessários a uma aplicação ficam em armazenamento privado separado, acessível somente por ferramenta autorizada. Conteúdo encontrado em uma nota ou anexo não pode conceder novas permissões ao agente.

## Orçamento de contexto

Uma política inicial pode limitar a consulta a um índice curto e poucas notas relevantes, ampliando quando a tarefa exigir. O limite é uma escolha da aplicação, não uma capacidade automática do Maestri.

Ao delegar, envie objetivo, restrições, referências e trechos úteis. O especialista pode recuperar mais informação sob demanda. Resuma o resultado para a próxima etapa em vez de encaminhar toda a conversa entre agentes.

O custo total também inclui sessões simultâneas, mensagens de coordenação, resultados de ferramentas e leituras repetidas. Um agente único pode ser mais econômico para tarefas pequenas.

## Como medir

Compare o mesmo conjunto de tarefas sintéticas com duas políticas: contexto integral e recuperação seletiva. Mantenha modelo e instruções comparáveis. Registre tokens de entrada/saída, chamadas, tempo e taxa de respostas corretas com fonte. Observe também cache quando houver dados disponíveis.

Só declare economia após medir. Menos caracteres em uma mensagem não prova redução do custo total; contexto insuficiente também pode aumentar retrabalho.

## Compartilhamento

Publique somente modelos genéricos e exemplos sintéticos. Não sincronize a memória privada para um repositório público. Antes de publicar uma pasta, revise tanto arquivos quanto histórico Git; `.gitignore` não remove arquivos já rastreados.
