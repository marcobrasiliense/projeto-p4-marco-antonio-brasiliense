# Documentação de Decisões de Implementação

## [P4-ETAPA-03] Implementação Imperativa (`imperativo/planejador.py`)

### 1. Quais estados são mantidos
A solução mantém quatro estruturas principais de estado mutável ao longo do ciclo de vida da execução:
* **`tabela_adjacencia` (Dicionário de listas):** Mantém a representação em memória da malha viária indexada pelo nó de origem, onde cada entrada armazena uma lista mutável de dicionários contendo `destino`, `distancia` e `pedagio`.
* **`pilha_fronteira` (Lista operando como pilha LIFO):** Mantém o estado explícito do fluxo de exploração do grafo. Cada quadro (*frame*) empilhado registra `[no_atual, trajeto_atual, dist_atual, custo_atual]`.
* **`estado_busca` (Dicionário acumulador):** Mantém o estado global da busca em curso, registrando flags booleanas de controle (`encontrou_caminho_fisico` e `encontrou_rota_viavel`) e os acumuladores do ótimo atual (`melhor_trajeto`, `melhor_distancia` e `melhor_custo`).
* **`resultado` (Dicionário de saída):** Mantém os campos exigidos pelo contrato semântico (`status`, `trajeto`, `distancia_total` e `custo_total`), iniciados em estado padrão de erro e sobrescritos conforme o desfecho do processamento.

### 2. Quais operações modificam estado
A computação progride por meio de atribuições destrutivas e mutações *in-place* sobre as estruturas de dados:
* **Atribuições de variáveis escalares:** Incrementos explícitos de contadores (`indice = indice + 1`, `total_passou = total_passou + 1`), atualização de flags (`ja_visitado = True`) e cálculos aritméticos (`nova_dist = dist_atual + dist_via`).
* **Mutações de listas:** Inserções na fronteira de busca e nos trajetos via `.append()` e remoção destrutiva do topo da pilha de execução via `pilha_fronteira.pop()`.
* **Mutações de dicionários:** Alteração direta de chaves nos dicionários compartilhados, como `estado_busca["melhor_distancia"] = dist_candidata` e `resultado["status"] = "ROTA_ENCONTRADA"`.

### 3. Onde aparecem efeitos colaterais
Os efeitos colaterais foram deliberadamente projetados na passagem de estruturas mutáveis por referência entre subprogramas e na camada de Entrada/Saída (I/O):
* **Procedimento `construir_lista_adjacencia(malha, tabela_adjacencia)`:** Não retorna valores (`None`); seu efeito é popular diretamente o dicionário `tabela_adjacencia` recebido como argumento.
* **Procedimento `atualizar_estado_otimo(...)`:** Modifica diretamente as chaves `melhor_trajeto`, `melhor_distancia` e `melhor_custo` dentro do dicionário `estado_busca` passado por referência.
* **Procedimento `executar_busca_imperativa(...)`:** Altera o dicionário `estado_busca` à medida que descobre caminhos físicos e rotas que respeitam o orçamento.
* **Procedimento `executar_suite_testes()`:** Produz efeito colateral externo ao escrever o relatório de validação dos 15 casos de teste na saída padrão (`stdout`) por meio da instrução `print()`.

### 4. Quais estruturas de controle foram escolhidas
O controle do fluxo de execução é totalmente explícito e estruturado por meio de:
* **Sequenciamento:** Execução passo a passo ordenada de comandos dentro de cada bloco procedural.
* **Seleção condicional (`if / elif / else`):** Utilizada na validação de fronteira das entradas, na checagem de atendimento ao orçamento (`custo_atual <= orcamento`), na hierarquia de critérios de desempate em `eh_melhor_rota` e na classificação final do status (`ROTA_ENCONTRADA`, `ORCAMENTO_INSUFICIENTE` ou `ROTA_INEXISTENTE`).
* **Repetição indefinida (`while`):** Utilizada em `validar_entrada` (controlada por índice explícito) e no motor de travessia `executar_busca_imperativa` (`while len(pilha_fronteira) > 0`), substituindo a recursão por iteração pura.
* **Repetição definida (`for`) e desvios controlados (`break` e `continue`):** Utilizados para iterar sobre vizinhos, copiar listas elemento a elemento, interromper prematuramente a verificação de ciclo (`break` ao detectar nó repetido) e avançar o laço da pilha ao atingir o nó de destino (`continue`).

### 5. Como os subprogramas foram organizados
O código foi decomposto modularmente em sete subprogramas (entre funções de consulta e procedimentos de mutação de estado):
1. `inicializar_resultado()`: Fábrica procedural da estrutura mutável de retorno.
2. `validar_entrada(...)`: Sub-rotina booleana que inspeciona as pré-condições do contrato semântico.
3. `construir_lista_adjacencia(...)`: Procedimento de transformação da lista bruta de tuplas em estrutura indexada de adjacência.
4. `eh_melhor_rota(...)`: Sub-rotina de comparação que implementa a regra de negócio de otimização e desempate.
5. `atualizar_estado_otimo(...)`: Procedimento auxiliar de gravação de estado ótimo.
6. `executar_busca_imperativa(...)`: Motor iterativo de exploração de caminhos baseado em pilha explícita.
7. `planejar_rota(...)`: Subprograma fachada (*entry point* do contrato) que coordena a chamada sequencial dos demais subprogramas.
8. `executar_suite_testes()`: Procedimento automatizado de verificação dos 15 casos de teste da Etapa 02.

### 6. Por que a solução pode ser considerada predominantemente imperativa
A implementação é genuinamente imperativa porque modela a computação como uma sequência de comandos que modificam o estado da memória passo a passo (modelo de máquina de von Neumann):
* **Ausência de Abstrações OO:** Não há declaração de classes (`class`), encapsulamento de métodos em objetos, herança ou polimorfismo. Dados (dicionários e listas nativas) e procedimentos são estritamente separados.
* **Ausência de Idiomas Funcionais:** Não foram utilizadas funções de alta ordem (`map`, `filter`, `reduce`), expressões `lambda`, compreensões de lista (*list comprehensions*) nem recursão na pilha de chamadas.
* **Controle Explícito do Fluxo e do Estado:** A travessia do grafo, que em paradigmas declarativos seria delegada à recursão ou ao *backtracking* automático, é aqui controlada manualmente por uma pilha mutável explícita (`pilha_fronteira`) manipulada dentro de um laço `while`, com atualização destrutiva de variáveis acumuladoras.