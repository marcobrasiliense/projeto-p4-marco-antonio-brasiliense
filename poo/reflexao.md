# [P4-ETAPA-04] Reflexão — Modelagem Orientada a Objetos

## Como meu modelo mudou ao passar do paradigma imperativo para o orientado a objetos?

Na Etapa 03 (Imperativa), a solução foi projetada em torno de procedimentos que manipulavam diretamente estruturas de dados primitivas e mutáveis (listas e dicionários globais à busca) por referência. Na Etapa 04 (Orientada a Objetos), o sistema deixou de ser uma sequência de mutações sobre dicionários passivos e passou a ser modelado como uma rede de **entidades de domínio autônomas e coesas** (`Via`, `Trajeto`, `MalhaViaria`, `PlanejadorRotas` e `CriterioOtimizacao`) que interagem por meio de envio de mensagens (chamadas de métodos).

---

### 1. Representação do Estado
* **No Paradigma Imperativo:** O estado ficava exposto em estruturas nativas genéricas (`dict` e `list`), como `tabela_adjacencia`, `pilha_fronteira` (contendo listas `[no, trajeto, dist, custo]`) e `estado_busca`. Qualquer função tinha acesso irrestrito para sobrescrever chaves e índices.
* **No Paradigma Orientado a Objetos:** O estado foi distribuído e protegido dentro de objetos com significado semântico:
  * Cada conexão física é uma instância de `Via` com atributos privados (`_origem`, `_destino`, `_distancia`, `_pedagio`).
  * O estado parcial de uma caminhada deixou de ser um vetor de 4 posições e tornou-se a classe `Trajeto`, que conhece seus nós visitados e acumula sua distância e custo de forma íntegra.
  * A topologia do grafo pertence exclusivamente ao estado interno de `MalhaViaria` (`_adjacencias` e `_nos_conhecidos`).

### 2. Responsabilidades
Aplicou-se o Princípio da Responsabilidade Única (*Single Responsibility Principle*), dividindo o sistema em 4 módulos:
* **`Via` (`modelos.py`):** Validar e guardar os dados imutáveis de um trecho rodoviário.
* **`Trajeto` (`modelos.py`):** Gerenciar a sequência de nós percorridos, checar aciclicidade (`ja_visitou`) e conformidade financeira (`respeita_orcamento`), além de gerar novos trajetos estendidos (`estender`).
* **`ResultadoRota` (`modelos.py`):** Encapsular o retorno final e oferecer métodos fábrica semânticos (`rota_encontrada`, `orcamento_insuficiente`, `rota_inexistente`, `entrada_invalida`).
* **`MalhaViaria` (`planejador.py`):** Armazenar as vias e responder consultas sobre a existência de nós e conexões de saída.
* **`CriterioOtimizacao` e subclasses (`criterios.py`):** Decidir qual entre dois trajetos candidatos é o mais vantajoso.
* **`PlanejadorRotas` (`planejador.py`):** Coordenar o algoritmo de busca sem conhecer detalhes de implementação de tela ou de estrutura interna das coleções.
* **`InterfaceConsolePOO` e `ExecutorSuiteTestes` (`main.py`):** Isolar completamente os efeitos colaterais de entrada e saída (`input`/`print`) da lógica de domínio.

### 3. Relacionamento entre Componentes (Composição, Agregação e Herança)
* **Agregação:** `MalhaViaria` agrega múltiplas instâncias de `Via`. As vias podem ser instanciadas de forma independente e adicionadas à malha.
* **Composição e Injeção de Dependência:** `PlanejadorRotas` é composto por uma referência a uma `MalhaViaria` e a uma estratégia `CriterioOtimizacao`.
* **Herança e Polimorfismo (Justificativa de Modelagem):** Seguindo a diretriz de não utilizar herança artificialmente, evitou-se criar heranças desnecessárias entre dados estáticos. Em vez disso, utilizou-se **herança combinada com composição (Padrão *Strategy*)** na hierarquia `CriterioOtimizacao` (classe abstrata `ABC`), da qual herdam `CriterioMenorDistanciaPadrao` e `CriterioMenorPedagioEconomico`. O `PlanejadorRotas` invoca polimorficamente `self._criterio.eh_melhor(trajeto_atual, melhor_trajeto)`, permitindo alterar a regra de negócio sem modificar uma única linha do algoritmo de busca.

### 4. Reutilização
* No modelo imperativo, a lógica de validação de entrada, cópia manual de listas (`for no_hist in trajeto_atual`) e critérios de desempate estavam acoplados ao formato de tuplas e dicionários daquele script.
* No modelo OO, classes como `MalhaViaria`, `Via` e `Trajeto` são componentes reutilizáveis: a mesma classe `PlanejadorRotas` é reutilizada tanto pelo `ExecutorSuiteTestes` (para auditar os 15 casos formais da Etapa 02) quanto pela `InterfaceConsolePOO` (para consultas interativas na malha rodoviária de Goiás/DF).

### 5. Encapsulamento
* Todos os atributos internos das classes foram prefixados como privados por convenção (`_origem`, `_distancia`, `_nos`, `_adjacencias`) e expostos apenas para leitura controlada via `@property`.
* As pré-condições de domínio (como distância estritamente positiva e pedágio não negativo) passaram a ser invariantes de classe protegidas no construtor de `Via`. É impossível existir em memória um objeto `Via` com distância negativa.
* Métodos que retornam coleções internas (como `Trajeto.nos` ou `MalhaViaria.obter_vias_saida`) devolvem cópias ou tuplas imutáveis, impedindo que código externo corrompa acidentalmente o estado interno dos objetos.

### 6. Extensão do Sistema
A arquitetura orientada a objetos tornou o sistema aberto para extensão e fechado para modificação (*Open-Closed Principle*):
* **Novos Critérios de Otimização:** Para criar um critério que minimize o número de paradas (saltos) ou pondere distância e pedágio em uma fórmula única, basta criar uma nova subclasse de `CriterioOtimizacao` e injetá-la no `PlanejadorRotas`.
* **Novos Tipos de Vias:** Caso o domínio passe a considerar pedágios dinâmicos por horário ou tipo de caminhão, basta especializar a classe `Via` sobrescrevendo a propriedade `pedagio`, sem que `MalhaViaria` ou `PlanejadorRotas` precisem ser reescritos.