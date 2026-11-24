# Verificação de instalação

Data: 24/11/2026.

## Conclusão e alcance

O gerador foi executado a partir de um clone novo obtido pelo endereço público, sem autenticação Git, memória privada, arquivo de ambiente ou dados de uma instalação existente. Ele montou estruturas novas com os padrões fictícios publicados. Os 17 testes de aceitação passaram em Windows com Python 3.13.

Isso valida a geração local e a consistência dos arquivos. Não equivale a aprovar o fluxo completo de um agente novo em Codex e Claude Code: o teste separado do Codex encontrou uma restrição do ambiente de execução, e Claude Code não estava instalado no ambiente de teste.

## Evidências reproduzíveis

Execute no checkout:

```sh
python -I test_bootstrap.py -v
```

A suíte usa apenas a biblioteca padrão, pastas temporárias e subprocessos Python isolados com ambiente mínimo. Não faz chamadas a modelos ou serviços externos.

| Verificação | Resultado |
| --- | --- |
| Gerador completo por linha de comando | 18 papéis e 34 arquivos criados |
| Perfil mínimo por linha de comando | 3 papéis e 19 arquivos criados |
| Simulação `--dry-run` | Não cria o destino |
| Caminho com espaços e acentos | Estrutura criada e índice legível |
| Reexecução idêntica | Conteúdo e datas de modificação preservados |
| Arquivo modificado pela pessoa | Não sobrescrito |
| Conflito numa instalação parcial | Nenhum arquivo escrito antes de recusar |
| Destino não vazio de outra aplicação | Conteúdo preservado, setup recusado |
| Destino que é um arquivo | Recusado sem alteração |
| Destino dentro do checkout, no checkout ou em seu ancestral | Recusado |
| Troca de perfil sobre instalação existente | Recusada sem alteração |
| Manifesto inválido | Erro controlado, conteúdo preservado |
| JSONs e rotas | Válidos, integrações desativadas e IDs não configurados |
| Entradas Codex/Claude e referências de memória/papéis | Arquivos referenciados presentes |
| Arquivos gerados | Sem caminhos do host ou endereços de contato |
| Links locais dos documentos públicos | Destinos existentes |

## Teste com agente e limitações observadas

Uma sessão separada do Codex recebeu o pedido de ler `AGENTS.md` e montar a estrutura sem acessar informações externas ao diretório de teste. A política efetiva desse ambiente era somente leitura e rejeitou a execução dos comandos de leitura. A montagem não ocorreu nessa sessão; o resultado foi registrado como **bloqueado por ambiente**, não como aprovado.

O guia foi ajustado para explicar a necessidade de execução local e acesso de escrita ao destino privado, que fica fora do checkout. Abrir uma pasta contêiner ou autorizar o destino adicional é parte da preparação do workspace. Isso não garante a liberação de uma execução que a política local ainda recuse.

Claude Code: entrada `CLAUDE.md` e referência ao protocolo verificadas, mas **sem execução real do produto** neste teste.

Maestri, colaboração entre processos, sincronização entre dispositivos, Discord e Instagram: **não testados ponta a ponta aqui**. Dependem de instalações, serviços, contas e permissões próprias. O gerador informa explicitamente que não iniciou terminais nem conectou contas.

## O que não é necessário

A montagem dos arquivos não pede nome, clientes, preferências, histórico de conversas, tokens ou dados do autor. A pessoa precisa de Python e escrita no destino; para usar modelos e serviços depois, configura seus próprios acessos separadamente. O acervo privado real nunca é parte dos padrões deste pacote.
