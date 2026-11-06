# [P4-ETAPA-06] Reflexão sobre o Paradigma Funcional

## 1. Identificação dos Requisitos Funcionais Implementados
A arquitetura do código foi estruturada em duas áreas estritas, isolando a lógica matemática do I/O:
* **Funções Puras:** `carregar_malha`, `explorar_caminhos` e `planejar_rota_core`. Elas garantem **transparência referencial** — ao receber os mesmos argumentos, sempre devolvem o mesmo dicionário de saída sem alterar o ambiente.
* **Funções Impuras (Interação externa):** `executar_testes_funcionais`, que é o único ponto onde o programa causa **efeitos colaterais** (imprimir no console) e interage com o mundo exterior.
* **Dados Imutáveis e Transformação:** O algoritmo abandonou `lists` e `dicts` mutáveis no estado do trajeto, utilizando exclusivamente `tuples`. Em vez de alterar um valor, criamos novas instâncias.
* **Funções de Alta Ordem e Composição:** A solução empregou intensamente o `filter()` para eliminar trajetos fora do orçamento, e a função `min()` recebendo uma função anônima `lambda` de primeira classe para reduzir as opções e estabelecer os critérios de desempate (Distância -> Custo -> Lexicográfico).

## 2. Reflexão Obrigatória: A mudança de perspectiva
*Explique como o raciocínio da solução mudou ao deixar de pensar principalmente em: "Que estado devo modificar?" e passar a pensar em: "Que transformação deve ser aplicada aos dados?"*

Nos paradigmas Imperativo e Orientado a Objetos, o motor do projeto era gerido pela pergunta *"Que estado devo modificar?"*. Todo o fluxo se baseava em atualizar as variáveis dentro de um laço `while`: marcar nós como visitados, somar as distâncias nas propriedades dos objetos de trajeto e atualizar uma variável que armazenava temporariamente a "melhor rota" encontrada até o momento. O tempo todo eu estava "mutando" a memória.

Ao migrar para o paradigma Funcional, o raciocínio mudou radicalmente para *"Que transformação deve ser aplicada aos dados?"*. O laço estruturado deixou de existir. A solução virou uma linha de montagem contínua baseada em três transformações sequenciais:
1. Apliquei uma **função recursiva** que transforma os dados do grafo em um agrupamento de todas as rotas fisicamente possíveis.
2. Apliquei a transformação `filter()` para podar as ramificações de dados que quebravam a restrição rígida orçamentária.
3. Apliquei uma transformação de **redução** (`min`) para extrair matematicamente a rota ótima de dentro das que sobreviveram ao filtro.

Deixei de dar ordens de controle de fluxo e passei a modelar o fluxo de dados em formato de *pipeline*, onde os dados originais são imutáveis e cada função produz uma nova versão da realidade para ser repassada à próxima etapa.
