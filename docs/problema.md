# [P4-ETAPA-01] Proposta e Especificação do Problema

## 1. Descrição do problema
O problema consiste no planejamento e otimização de rotas de transporte terrestre entre nós conectados por vias direcionadas. No contexto de frotas de entrega e deslocamento rodoviário, coexistem custos de consumo de combustível e desgaste de frota (proporcionais à distância percorrida) e custos tarifários imediatos (pedágios). A malha viária possui distâncias e valores de pedágio associados a cada via. O sistema deve encontrar o trajeto mais curto entre uma origem e um destino mantendo o custo acumulado de pedágio estritamente dentro de um limite orçamentário.

## 2. Objetivo
Determinar e apresentar o caminho de menor distância total entre um ponto de partida e um ponto de destino informados, assegurando que o custo financeiro acumulado com tarifas de pedágio não exceda o orçamento máximo autorizado, informando o trajeto, a quilometragem total e a tarifa agregada.

## 3. Entradas
* **Malha viária (grafo ponderado direcionado):** Lista de trechos viários no formato `(origem, destino, distancia, pedagio)`, onde:
  * `origem`: Identificador alfanumérico do nó inicial.
  * `destino`: Identificador alfanumérico do nó final.
  * `distancia`: Valor numérico estritamente positivo (km).
  * `pedagio`: Valor numérico não negativo (R$).
* **Ponto de partida:** Identificador do nó onde a viagem se inicia.
* **Ponto de destino:** Identificador do nó de chegada da viagem.
* **Orçamento máximo:** Valor numérico não negativo indicando o teto autorizado para gastos com pedágio.

## 4. Saídas
* **Status do resultado:**
  * `ROTA_ENCONTRADA`: Trajeto viável localizado respeitando o orçamento.
  * `ORCAMENTO_INSUFICIENTE`: Existem rotas físicas conectando origem e destino, mas todas ultrapassam o orçamento estipulado.
  * `ROTA_INEXISTENTE`: Não há conectividade física entre origem e destino na malha viária.
* **Trajeto:** Sequência ordenada dos nós visitados desde a origem até o destino (exemplo: `[A, B, D]`).
* **Distância total:** Soma das distâncias em quilômetros das vias que compõem o trajeto.
* **Custo total de pedágio:** Soma das tarifas de pedágio das vias percorridas.

## 5. Regras do problema
1. **Conectividade estrita:** Só é permitida a transição entre nós que possuam ligação direcionada direta na malha viária.
2. **Conformidade orçamentária:** A soma das tarifas de pedágio do trajeto percorrido deve ser menor ou igual ($\le$) ao orçamento estipulado.
3. **Aciclicidade:** Uma rota válida não pode conter nós duplicados; não é permitida a visitação repetida de um mesmo local na mesma viagem.
4. **Critério principal de otimização:** Havendo múltiplos trajetos acíclicos viáveis dentro do orçamento, o sistema deve escolher aquele que apresentar a **menor distância total**.
5. **Critério de desempate:** Se dois ou mais trajetos válidos empatarem na distância total mínima, o critério de desempate prioriza aquele com **menor custo total de pedágio**.
6. **Orientação das vias:** Vias são unidirecionais por padrão. Estradas de pista dupla com tráfego nos dois sentidos devem ser modeladas como duas vias unidirecionais distintas e opostas.

## 6. Casos de exemplo

Considere a malha viária base composta pelas conexões:
* $A \rightarrow B$ (distância: 10, pedágio: 5)
* $A \rightarrow C$ (distância: 15, pedágio: 0)
* $B \rightarrow D$ (distância: 10, pedágio: 5)
* $C \rightarrow D$ (distância: 12, pedágio: 2)
* $B \rightarrow C$ (distância: 2, pedágio: 1)

* **Caso 1 — Rota ótima sem restrição ativa:**
  * *Entrada:* Origem: `A`, Destino: `D`, Orçamento: `15`
  * *Saída esperada:* `Status: ROTA_ENCONTRADA | Trajeto: [A, B, D] | Distância: 20 | Custo: 10`
* **Caso 2 — Restrição de orçamento exige trajeto de maior quilometragem:**
  * *Entrada:* Origem: `A`, Destino: `D`, Orçamento: `5`
  * *Saída esperada:* `Status: ROTA_ENCONTRADA | Trajeto: [A, C, D] | Distância: 27 | Custo: 2`
* **Caso 3 — Orçamento insuficiente para cobrir qualquer opção existente:**
  * *Entrada:* Origem: `A`, Destino: `D`, Orçamento: `1`
  * *Saída esperada:* `Status: ORCAMENTO_INSUFICIENTE`
* **Caso 4 — Origem e destino coincidentes:**
  * *Entrada:* Origem: `A`, Destino: `A`, Orçamento: `10`
  * *Saída esperada:* `Status: ROTA_ENCONTRADA | Trajeto: [A] | Distância: 0 | Custo: 0`
* **Caso 5 — Destino desconectado:**
  * *Entrada:* Origem: `D`, Destino: `A`, Orçamento: `25`
  * *Saída esperada:* `Status: ROTA_INEXISTENTE`

## 7. Casos-limite
1. **Malhas contendo ciclos direcionados:** Em grafos com caminhos circulares (ex.: $A \rightarrow B \rightarrow C \rightarrow A$), o mecanismo de travessia deve rastrear os nós já visitados para evitar laços ou recursões infinitas.
2. **Orçamento zero (R$ 0,00):** O sistema deve processar a entrada normalmente, encontrando rotas válidas exclusivamente caso todas as vias necessárias possuam pedágio nulo ($0$).
3. **Empate total em distância e custo:** Caso múltiplos caminhos viáveis empatem tanto na distância quanto no custo, adota-se critério determinístico secundário (ordem alfabética dos nós intermediários), garantindo idempotência.

## 8. Restrições
* Condições dinâmicas de tráfego, semáforos, bloqueios de vias e velocidade média dos veículos estão fora do escopo do projeto.
* O sistema não terá interface gráfica (GUI); as operações ocorrerão via entrada e saída de texto em linha de comando ou arquivos.
* O grafo viário permanece imutável durante o processamento de cada rota.
* Vias com distâncias negativas ou pedágios de valor negativo são inválidas e não são suportadas.

## 9. Principais conceitos do domínio
* **Local (Nó / Vértice):** Ponto de partida, conexão intermediária ou destino final de uma rota.
* **Via (Aresta / Conexão):** Trecho direcionado conectando dois locais contendo métricas de distância e tarifa de pedágio.
* **Trajeto (Caminho):** Sequência finita e contínua de locais diretamente conectados sem visitações duplicadas.
* **Orçamento:** Limite monetário máximo fixado para os custos tarifários da viagem.

## 10. Adequação aos quatro paradigmas
* **Imperativo:** Manipulação sequencial de matrizes ou listas de adjacência por meio de laços de repetição (`for`, `while`), alterando diretamente arrays de nós visitados e acumuladores mutáveis de menor distância e custo.
* **Orientado a Objetos:** Decomposição do domínio em entidades autônomas (`Local`, `Via`, `MalhaViaria`, `PlanejadorDeRotas`), encapsulando os dados e implementando métodos que aplicam as regras de validação de orçamento e cálculo de rota.
* **Funcional:** Tratamento da malha viária e dos trajetos como listas e tuplas imutáveis. A exploração de caminhos ocorre via recursão estrutural, usando funções puras de alta ordem (`filter` para descartar caminhos caros, `map` para projetar valores e `fold`/`reduce` para selecionar o caminho ótimo sem efeitos colaterais).
* **Lógico:** O mapa viário é expresso como uma base declarativa de fatos lógicos (`via/4`). A identificação de rotas e a validação das restrições são resolvidas nativamente pelo motor de unificação e retrocesso (*backtracking*) do paradigma lógico, acumulando custos em predicados recursivos.

## 11. Linguagens inicialmente consideradas
* **Imperativo — C:** Controle direto de estruturas de memória, vetores de adjacência e iterações explícitas sem mecanismos de orientação a objetos.
* **Orientado a Objetos — Python:** Abstração clara de entidades por meio de classes, construtores, encapsulamento e composição.
* **Funcional — Haskell:** Sistema puramente funcional com imutabilidade estrita, tipagem estática e casamento de padrões (*pattern matching*), ideais para travessia recursiva de listas de caminhos.
* **Lógico — Prolog (SWI-Prolog):** Paradigma puramente declarativo cuja unificação e busca em profundidade nativas resolvem problemas de grafos e restrições de forma concisa.