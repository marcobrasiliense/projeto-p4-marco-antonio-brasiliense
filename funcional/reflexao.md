# [P4-ETAPA-06] Implementação Funcional em Haskell

## 1. Identificação dos Conceitos no Código

* **Funções puras:** `buscarCaminhos` e `planejarRota`. Não alteram variáveis nem dependem de estado externo; para os mesmos argumentos de entrada, sempre produzem a mesma saída com total transparência referencial.
* **Funções impuras e I/O:** Apenas a função `main :: IO ()`. É o único ponto do programa que interage com o mundo externo através do console.
* **Dados imutáveis:** Uso de tipos algébricos (`Status`, `Resultado`) e listas nativas do Haskell. Não existem variáveis mutáveis ou reatribuições.
* **Transformações de dados:** O fluxo transforma a lista de arestas brutas em uma lista de trajetos possíveis, depois em uma lista filtrada por orçamento e, por fim, em um registro do trajeto ótimo.
* **Funções de alta ordem e composição:** 
  * `filter` recebendo uma função anônima (lambda) para podar rotas que ultrapassam o teto de gastos.
  * `minimumBy` combinado com `comparing` para aplicar a tupla de desempate (Distância -> Pedágio -> Ordem Lexicográfica).
* **Recursão:** A função `buscarCaminhos` utiliza recursão com list comprehension para navegar pelos nós e evitar ciclos (`v notElem trajetoAtual`), eliminando loops imperativos como `while` ou `for`.

---

## 2. Reflexão Obrigatória

**Explique como o raciocínio da solução mudou ao deixar de pensar principalmente em "Que estado devo modificar?" e passar a pensar em "Que transformação deve ser aplicada aos dados?"**

Nas etapas imperativa e orientada a objetos, a solução dependia diretamente do controle de estado: era necessário manter laços de repetição, atualizar acumuladores de custo e distância a cada iteração e reescrever variáveis temporárias para armazenar a melhor rota encontrada até o momento.

Ao adotar o paradigma funcional com Haskell, o foco mudou para a transformação pura de dados em formato de pipeline:
1. Uma lista inicial de arestas é transformada recursivamente em todas as rotas fisicamente possíveis.
2. Essa lista é transformada via `filter`, eliminando os trajetos que violam a restrição rígida de pedágio.
3. A lista resultante passa por uma redução com `minimumBy`, extraindo diretamente o caminho com menor distância e custo.

Em vez de ditar instruções sequenciais sobre como alterar valores na memória, o código passou a declarar as regras matemáticas de transformação sobre estruturas estritamente imutáveis.
