# Projeto P4 — Paradigmas de Programação

Projeto semestral da disciplina Paradigmas de Programação, com o objetivo de explorar a resolução de um mesmo problema sob quatro paradigmas distintos: Imperativo, Orientado a Objetos, Funcional e Lógico.

## Progresso do Projeto
* [x] **[P4-ETAPA-01]** Proposta e Especificação do Problema
* [x] **[P4-ETAPA-02]** Contrato semântico e testes `testes/casos.md`
* [x] **[P4-ETAPA-03]** Implementação imperativa `imperativo/`
* [x] **[P4-ETAPA-04]** Implementação Orientada a Objetos (`poo/` e `poo/reflexão.md`)

---

# [P4-ETAPA-01] Proposta e Especificação do Problema

## 1. Descrição do problema
O problema consiste no planejamento e otimização de rotas de transporte rodoviário de cargas entre localidades interconectadas por uma malha de vias terrestres direcionadas. Na operação logística real, frotistas e motoristas autônomos lidam com custos variáveis contínuos de consumo de combustível e manutenção (diretamente atrelados à distância em quilômetros) e custos fixos pontuais de tarifas de pedágio. Cada via possui uma extensão física e um valor tarifário associado. O sistema deve encontrar o melhor trajeto entre dois pontos mantendo o gasto acumulado de pedágio estritamente dentro de um orçamento estipulado.

## 2. Objetivo
Determinar e apresentar o caminho de menor distância total percorrida entre um ponto de partida e um ponto de destino informados, assegurando que o custo total acumulado com tarifas de pedágio não ultrapasse o orçamento estipulado para a viagem, reportando a rota completa, a distância final e o custo despendido.

## 3. Entradas
* **Malha viária (grafo ponderado direcionado):** Conjunto de vias no formato `(origem, destino, distancia, pedagio)`, onde:
  * `origem`: Identificador alfanumérico do nó inicial da via.
  * `destino`: Identificador alfanumérico do nó final da via.
  * `distancia`: Valor numérico estritamente positivo representando a extensão do trecho (km).
  * `pedagio`: Valor numérico não negativo representando a tarifa de pedágio (R$).
* **Ponto de partida:** Identificador do nó onde a viagem se inicia.
* **Ponto de destino:** Identificador do nó de término da viagem.
* **Orçamento máximo:** Valor numérico não negativo estipulando o limite financeiro disponível para pagamento de pedágios.

## 4. Saídas
* **Status do processamento:**
  * `ROTA_ENCONTRADA`: Trajeto viável localizado respeitando o orçamento.
  * `ORCAMENTO_INSUFICIENTE`: Existem rotas físicas conectando origem e destino, mas todas excedem o orçamento estipulado.
  * `ROTA_INEXISTENTE`: Não há conectividade física entre os nós de origem e destino na malha viária.
* **Trajeto:** Sequência ordenada dos identificadores dos nós visitados da origem até o destino (exemplo: `[A, B, D]`).
* **Distância total:** Soma das distâncias em quilômetros das vias que compõem o trajeto.
* **Custo total de pedágio:** Soma das tarifas de pedágio das vias percorridas.

## 5. Regras do problema
1. **Conectividade estrita:** Só é permitida a transição entre nós que possuam ligação direcionada direta na malha viária.
2. **Conformidade orçamentária:** A soma das tarifas de pedágio do trajeto percorrido deve ser menor ou igual ($\le$) ao orçamento estipulado.
3. **Aciclicidade:** Uma rota válida não pode conter nós duplicados; não é permitida a visitação repetida de um mesmo local na mesma viagem.
4. **Critério principal de otimização:** Havendo múltiplos trajetos acíclicos viáveis dentro do orçamento, o sistema deve selecionar aquele com a **menor distância total**.
5. **Critério de desempate:** Se dois ou mais trajetos válidos empatarem na distância total mínima, o desempate prioriza aquele com o **menor custo total de pedágio**.
6. **Orientação das vias:** Vias são unidirecionais por padrão. Estradas de tráfego bidirecional são tratadas como duas vias unidirecionais opostas.

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
2. **Orçamento zero (R$ 0,00):** O sistema deve processar a entrada normalmente, encontrando rotas válidas exclusivamente se todas as vias necessárias possuírem pedágio nulo ($0$).
3. **Empate total em distância e custo:** Caso múltiplos caminhos viáveis empatem tanto na distância quanto no custo, adota-se critério determinístico secundário (ordem lexicográfica dos nós intermediários), garantindo idempotência.

## 8. Restrições
* Condições dinâmicas de tráfego, semáforos, bloqueios de vias e velocidade média dos veículos estão fora do escopo do projeto.
* O sistema não terá interface gráfica (GUI); as operações ocorrerão via entrada e saída de texto em linha de comando ou arquivos.
* O grafo viário permanece imutável durante o processamento de cada rota.
* Vias com distâncias negativas ou pedágios de valor negativo são inválidas e não são suportadas.

## 9. Principais conceitos do domínio
* **Local (Nó / Vértice):** Ponto de partida, conexão intermediária ou destino final de uma rota.
* **Via (Aresta / Conexão):** Trecho direcionado conectando dois locais contendo métricas de distância e tarifa de pedágio.
* **Trajeto (Caminho):** Sequência finita e contínua de locais diretamente conectados sem repetições.
* **Orçamento:** Limite monetário máximo fixado para os custos tarifários da viagem.

## 10. Adequação aos quatro paradigmas
* **Imperativo:** Manipulação sequencial de matrizes ou listas de adjacência por meio de laços de repetição (`for`, `while`), alterando diretamente arrays de nós visitados e acumuladores mutáveis de menor distância e custo.
* **Orientado a Objetos:** Decomposição do domínio em entidades autônomas (`Local`, `Via`, `MalhaViaria`, `PlanejadorDeRotas`), encapsulando os dados e implementando métodos que aplicam as regras de validação de orçamento e cálculo de rota.
* **Funcional:** Tratamento da malha viária e dos trajetos como coleções e tuplas imutáveis. A exploração de caminhos ocorre via recursão estrutural, usando funções puras de alta ordem (`filter` para descartar caminhos caros, `map` para projetar valores e `fold`/`reduce` para selecionar o trajeto ótimo sem efeitos colaterais).
* **Lógico:** O mapa viário é modelado como uma base declarativa de fatos lógicos (`via/4`). A identificação de rotas e a validação das restrições são resolvidas pelo motor de unificação e retrocesso (*backtracking*) do paradigma lógico, acumulando distâncias e custos em predicados recursivos.

## 11. Linguagens inicialmente consideradas
* **Imperativo — Python:** Utilização estrita do subconjunto procedural e imperativo da linguagem, operando diretamente sobre estruturas de dados mutáveis (listas e dicionários de adjacência), controle explícito de fluxo com laços de repetição, mutação de variáveis de estado e decomposição em subprogramas (funções), sem o uso de classes ou abstrações orientadas a objetos.
* **Orientado a Objetos — Python:** Abstração clara de entidades por meio de classes, construtores, métodos de instância e encapsulamento.
* **Funcional — Haskell:** Sistema puramente funcional com imutabilidade estrita, tipagem estática e casamento de padrões (*pattern matching*), ideais para travessia recursiva de listas.
* **Lógico — Prolog (SWI-Prolog):** Paradigma puramente declarativo cuja unificação e busca em profundidade nativas resolvem problemas de caminhos e restrições de forma concisa.