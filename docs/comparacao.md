# [P4-ETAPA-05] Comparação entre Imperativo e POO

## 1. Análise Comparativa de Aspectos
Conforme exigido pelos critérios do projeto, a transição do paradigma imperativo para a Orientação a Objetos (POO) alterou fundamentalmente a estrutura do software:
*   **Representação do Estado e Mutabilidade:** No imperativo, o estado da busca era mutável e ficava exposto em dicionários e vetores soltos. Na POO, o estado foi encapsulado de forma segura na classe `Trajeto`, que valida sua própria integridade.
*   **Fluxo de Controle e Decomposição:** O imperativo baseava-se em laços monolíticos. A POO descentralizou o controle, separando a `MalhaViaria` (dados), os `Criterios` (regras) e o `PlanejadorRotas` (motor).
*   **Facilidade de Extensão e Reutilização:** A POO permitiu adicionar novas cidades e regras de pedágio dinamicamente em tempo de execução através de herança e polimorfismo, sem tocar na lógica core da busca.

---

## 2. Perguntas e Respostas

**1. Qual problema ficou mais fácil de expressar de forma imperativa?**
A parte matemática e lógica fundamental. Fazer o cálculo bruto da rota foi mais direto porque envolveu apenas o uso de estruturas nativas básicas do Python (loops, condicionais, tuplas e dicionários). Ter esse controle direto foi mais fácil do que criar classes, instanciar objetos e escrever muito mais código para executar cálculos matemáticos simples.

**2. Qual problema ficou mais fácil de expressar utilizando orientação a objetos?**
A parte de interação com o usuário. No imperativo, como tudo estava no mesmo escopo, ficaria confuso e arriscado separar a lógica de inputs. Na orientação a objetos, foi mais fácil porque empacotei algumas cidades de Goiás nas classes `MalhaViaria` e `Via`. Foi bem mais simples criar o menu interativo diferenciando as responsabilidades, sem correr o risco de a entrada do usuário quebrar o motor de busca do projeto.

**3. Onde a orientação a objetos realmente trouxe vantagem?**
Na separação estrita de escopos e responsabilidades. Atribuindo uma função específica para cada classe, o código não se misturou, reduzindo significativamente a chance de erros invisíveis (diferente do imperativo, onde tudo fica em um único bloco de código). O uso da herança e do polimorfismo foi a maior vantagem: criando uma classe base de otimização, pude trocar os critérios do motor (menor distância vs. mais econômico) com base na execução, sem alterar uma linha do algoritmo principal.

**4. Em quais situações a utilização de objetos acrescentou complexidade desnecessária?**
No transporte de dados simples e operações diretas. No paradigma imperativo, resolvi a manipulação de dados em poucas linhas usando as funções e estruturas eficientes do próprio Python. Ao migrar para a POO, precisei escrever muito mais linhas de código de forma desnecessária — como métodos construtores (`__init__`) e propriedades — apenas para armazenar valores estáticos como a distância e o nome de uma cidade.

**5. Que partes do problema praticamente não mudaram entre as duas implementações?**
A validação do contrato semântico e a essência matemática da busca. Os 15 casos de teste puderam ser praticamente reciclados, pois as entradas e os resultados esperados são imutáveis em relação às regras de negócio. O laço de busca principal manteve a mesma lógica algorítmica, embora adaptado para consumir os novos objetos.

**6. Que partes precisaram ser completamente remodeladas?**
A parte de otimização e o controle do estado. A otimização ganhou um escopo próprio em um arquivo separado de critérios, utilizando o Padrão *Strategy* (Polimorfismo) para aplicar regras flexíveis de validação. Além disso, o histórico de nós percorridos — que no imperativo era apenas uma lista solta — foi remodelado em uma entidade ativa (`Trajeto`), que agora é responsável por realizar a própria validação e impedir ciclos no programa.