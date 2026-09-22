### 1.2 Formato das Estruturas
* **Malha Viária:** Lista ou conjunto de vias no formato `(origem, destino, distancia, pedagio)`.
  * `origem`: Identificador alfanumérico do ponto inicial (String/Átomo).
  * `destino`: Identificador alfanumérico do ponto final (String/Átomo).
  * `distancia`: Valor numérico real estritamente positivo representando a extensão em quilômetros.
  * `pedagio`: Valor numérico real não negativo representando o custo da tarifa.
* **ResultadoRota:** Estrutura composta por:
  * `status`: Um valor textual dentre `"ROTA_ENCONTRADA"`, `"ORCAMENTO_INSUFICIENTE"`, `"ROTA_INEXISTENTE"` ou `"ENTRADA_INVALIDA"`.
  * `trajeto`: Lista ordenada de identificadores de nós desde a origem até o destino (exemplo: `["A", "B", "D"]`). Vazio caso o status não seja `"ROTA_ENCONTRADA"`.
  * `distancia_total`: Valor numérico da soma das distâncias das vias percorridas (ou `0.0` se nenhuma rota for retornada).
  * `custo_total`: Valor numérico da soma das tarifas de pedágio das vias percorridas (ou `0.0` se nenhuma rota for retornada).

### 1.3 Regras Semânticas e Invariantes
1. **Conectividade:** Se `trajeto = [v_1, v_2, ..., v_k]`, deve existir uma via direcionada de `v_i` para `v_{i+1}` na malha informada para todo `1 <= i < k`.
2. **Aciclicidade:** Para quaisquer posições distintas `i` e `j` no trajeto, `v_i != v_j`.
3. **Respeito ao Limite:** `custo_total <= orcamento`.
4. **Otimização Primária:** O trajeto selecionado deve possuir a menor `distancia_total` possível entre todos os caminhos válidos que satisfaçam a restrição orçamentária.
5. **Critério de Desempate:** Se múltiplos trajetos válidos possuírem a mesma menor `distancia_total`, o sistema deve escolher aquele com o menor `custo_total`. Se ainda assim persistir o empate, utiliza-se a ordem lexicográfica da representação dos nós.

## 2. Casos de Teste

### Malha Viária Padrão (G1)
A maioria dos testes utiliza a malha viária padrão descrita a seguir:
* `(A, B, 10.0, 5.0)`
* `(A, C, 15.0, 0.0)`
* `(B, D, 10.0, 5.0)`
* `(C, D, 12.0, 2.0)`
* `(B, C, 2.0, 1.0)`
* `(D, E, 8.0, 3.0)`
* `(C, E, 25.0, 1.0)`

### 2.1 Casos Normais (10 casos)

#### TC-NORM-01
* **Descrição:** Trajeto direto simples de nó adjacente com orçamento suficiente.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"B"`
  * Orçamento: `10.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "B"]`
  * `distancia_total`: `10.0`
  * `custo_total`: `5.0`

#### TC-NORM-02
* **Descrição:** Menor caminho irrestrito com múltiplos nós intermediários e orçamento folgado.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `15.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "B", "D"]`
  * `distancia_total`: `20.0`
  * `custo_total`: `10.0`

#### TC-NORM-03
* **Descrição:** Restrição ativa forçando escolha de rota mais longa em quilômetros por causa do pedágio.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `5.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "C", "D"]`
  * `distancia_total`: `27.0`
  * `custo_total`: `2.0`

#### TC-NORM-04
* **Descrição:** Existência de caminhos físicos para o destino, mas nenhum atende ao teto financeiro mínimo.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `1.0`
* **Saída esperada:**
  * `status`: `"ORCAMENTO_INSUFICIENTE"`
  * `trajeto`: `[]`
  * `distancia_total`: `0.0`
  * `custo_total`: `0.0`

#### TC-NORM-05
* **Descrição:** Ausência total de caminhos direcionados entre origem e destino.
* **Entrada:**
  * Malha: G1
  * Origem: `"D"`
  * Destino: `"A"`
  * Orçamento: `50.0`
* **Saída esperada:**
  * `status`: `"ROTA_INEXISTENTE"`
  * `trajeto`: `[]`
  * `distancia_total`: `0.0`
  * `custo_total`: `0.0`

#### TC-NORM-06
* **Descrição:** Caminho com três saltos em sequência alcançando nó periférico com orçamento suficiente.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"E"`
  * Orçamento: `20.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "B", "D", "E"]`
  * `distancia_total`: `28.0`
  * `custo_total`: `13.0`

#### TC-NORM-07
* **Descrição:** Uso de conexão transversal entre ramos (`B -> C`) gerando rota de distância intermediária e custo moderado.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `8.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "B", "C", "D"]`
  * `distancia_total`: `24.0`
  * `custo_total`: `8.0`

#### TC-NORM-08
* **Descrição:** Orçamento limite coincidente exatamente com o pedágio total da melhor rota.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `10.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "B", "D"]`
  * `distancia_total`: `20.0`
  * `custo_total`: `10.0`

#### TC-NORM-09
* **Descrição:** Consulta em rota com pedágio nulo permitida sob orçamento zero.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"C"`
  * Orçamento: `0.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "C"]`
  * `distancia_total`: `15.0`
  * `custo_total`: `0.0`

#### TC-NORM-10
* **Descrição:** Seleção de desvio com múltiplos nós em vez de rota direta cara quando o teto de pedágio é apertado.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"E"`
  * Orçamento: `5.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A", "C", "D", "E"]`
  * `distancia_total`: `35.0`
  * `custo_total`: `5.0`

### 2.2 Casos-Limite (3 casos)

#### TC-LIM-01
* **Descrição:** Origem e destino idênticos (deslocamento zero e pedágio zero).
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"A"`
  * Orçamento: `0.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["A"]`
  * `distancia_total`: `0.0`
  * `custo_total`: `0.0`

#### TC-LIM-02
* **Descrição:** Malha viária com ciclo direcionado sem causar laço infinito ou travamento de recursão.
* **Entrada:**
  * Malha: 
    * `(X, Y, 5.0, 1.0)`
    * `(Y, Z, 5.0, 1.0)`
    * `(Z, X, 5.0, 1.0)`
    * `(Y, W, 10.0, 2.0)`
  * Origem: `"X"`
  * Destino: `"W"`
  * Orçamento: `10.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["X", "Y", "W"]`
  * `distancia_total`: `15.0`
  * `custo_total`: `3.0`

#### TC-LIM-03
* **Descrição:** Empate em distância total solucionado pela escolha do trajeto com menor pedágio.
* **Entrada:**
  * Malha: 
    * `(N1, N2, 20.0, 10.0)`
    * `(N2, F, 5.0, 2.0)`
    * `(N1, N3, 20.0, 4.0)`
    * `(N3, F, 5.0, 0.0)`
  * Origem: `"N1"`
  * Destino: `"F"`
  * Orçamento: `15.0`
* **Saída esperada:**
  * `status`: `"ROTA_ENCONTRADA"`
  * `trajeto`: `["N1", "N3", "F"]`
  * `distancia_total`: `25.0`
  * `custo_total`: `4.0`

### 2.3 Casos de Entrada Inválida (2 casos)

#### TC-INV-01
* **Descrição:** Entrada com valor de orçamento negativo.
* **Entrada:**
  * Malha: G1
  * Origem: `"A"`
  * Destino: `"D"`
  * Orçamento: `-5.0`
* **Saída esperada:**
  * `status`: `"ENTRADA_INVALIDA"`
  * `trajeto`: `[]`
  * `distancia_total`: `0.0`
  * `custo_total`: `0.0`

#### TC-INV-02
* **Descrição:** Consulta informando nó que não existe na malha informada.
* **Entrada:**
  * Malha: G1
  * Origem: `"ORIGEM_DESCONHECIDA"`
  * Destino: `"D"`
  * Orçamento: `10.0`
* **Saída esperada:**
  * `status`: `"ENTRADA_INVALIDA"`
  * `trajeto`: `[]`
  * `distancia_total`: `0.0`
  * `custo_total`: `0.0`