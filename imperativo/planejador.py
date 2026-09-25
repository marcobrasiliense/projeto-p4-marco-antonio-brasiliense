def inicializar_resultado():
    """
        Subprograma que inicializa e retorna a estrutura mutavel de resposta.
        """
    resultado = {
        "status": "ENTRADA_INVALIDA",
        "trajeto": [],
        "distancia_total": 0.0,
        "custo_total": 0.0
    }
    return resultado

def validar_entrada(malha, origem, destino, orcamento):
    """
    Verifica de forma imperativa se os parametros obedecem as pre-condicoes do contrato
    """
    if orcamento < 0.0:
        return False

    if malha is None or len(malha) == 0:
        return False

    nos_conhecidos = []
    indice = 0
    total_arestas = len(malha)

    while indice < total_arestas:
        aresta = malha[indice]
        if len(aresta) != 4:
            return False

        no_orig = aresta[0]
        no_dest = aresta[1]
        distancia = float(aresta[2])
        pedagio = float(aresta[3])

        #distancia deve ser estritamente positiva e pedagio nao negativo
        if distancia <= 0.0 or pedagio < 0.0:
            return False

        if no_orig not in nos_conhecidos:
            nos_conhecidos.append(no_orig)
        if no_dest not in nos_conhecidos:
            nos_conhecidos.append(no_dest)

        indice = indice + 1

    if origem not in nos_conhecidos or destino not in nos_conhecidos:
        return False

    return True

def construir_lista_adjacencia(malha, tabela_adjacencia):
    """
    Procedimento com efeito colateral -> modifica o dicionario tabela_adjacaencia diretamente a partir da lista de arestas da malha
    """
    for aresta in malha:
        no_orig = aresta[0]
        no_dest = aresta[1]
        distancia = float(aresta[2])
        pedagio = float(aresta[3])

        if no_orig not in tabela_adjacencia:
            tabela_adjacencia[no_orig] = []
        if no_dest not in tabela_adjacencia:
            tabela_adjacencia[no_dest] = []

        nova_conexao = {
            "destino": no_dest,
            "distancia": distancia,
            "pedagio": pedagio
        }
        tabela_adjacencia[no_orig].append(nova_conexao)

def e_melhor_rota(nova_dist, novo_custo, novo_trajeto, melhor_dist, melhor_custo, melhor_trajeto):
    """
    Avalia se a rota candidata supera a melhor rota registrada até o momento, respeitando a otimização primaria (menor distancia) e os criterios de desempate
    """
    if melhor_trajeto is None:
        return True

    #1- Critério principal: menor distancia total
    if nova_dist < melhor_dist:
        return True
    elif nova_dist > melhor_dist:
        return False

    #2- Primeiro desempate -> menor custo total de pedagio
    if novo_custo < melhor_custo:
        return True
    elif novo_custo > melhor_custo:
        return False

    #3- Segundo desempate: ordem lexicografica dos nós do trajeto
    if novo_trajeto < melhor_trajeto:
        return True

    return False

def atualizar_estado_otimo(estado_busca, trajeto_candidato, dist_candidata, custo_candidato):
    """
    Procedimento com efeito colateral: muta os acumuladores de melhor rota dentro do dicionario 'estado_busca'
    """
    copia_trajeto = []
    for no in trajeto_candidato:
        copia_trajeto.append(no)

    estado_busca["melhor_trajeto"] = copia_trajeto
    estado_busca["melhor_distancia"] = dist_candidata
    estado_busca["melhor_custo"] = custo_candidato


def executar_busca_imperativa(tabela_adjacencia, origem, destino, orcamento, estado_busca):
    """
    Procedimento central de travessia do garfo
    Utiliza uma pilha mutavel explicita e um laço while para explorar caminhos aciclicos sem recorrencia a recursao, mutando o dicionario 'estado_busca'
    """

    #cada elemento da pilha armazena o estado parcial da caminhada
    #[no_atual, lista_trajeto_percorrido, distancia_acumulada, custo_acumulado]
    pilha_fronteira = []
    pilha_fronteira.append([origem, [origem], 0.0, 0.0])

    while len(pilha_fronteira) > 0:
        #remove o estado do topo da pilha
        quadro_atual = pilha_fronteira.pop()
        no_atual = quadro_atual[0]
        trajeto_atual = quadro_atual[1]
        dist_atual = quadro_atual[2]
        custo_atual = quadro_atual[3]

        #verifica se alcancou o no de destino
        if no_atual == destino:
            estado_busca["encontrou_caminho_fisico"] = True

            if custo_atual <= orcamento:
                estado_busca["encontrou_rota_viavel"] = True

                supera_atual = e_melhor_rota(
                    dist_atual,
                    custo_atual,
                    trajeto_atual,
                    estado_busca["melhor_distancia"],
                    estado_busca["melhor_custo"],
                    estado_busca["melhor_trajeto"]
                )

                if supera_atual:
                    atualizar_estado_otimo(
                        estado_busca,
                        trajeto_atual,
                        dist_atual,
                        custo_atual
                    )
            continue


        #expande os vizinhos do no atual
        vizinhos = tabela_adjacencia.get(no_atual, [])
        for via in vizinhos:
            proximo_no = via["destino"]
            dist_via = via["distancia"]
            pedagio_via = via["pedagio"]

            #Regra da aciclidade -> evita visitar nos ja presentes no trajeto atual
            ja_visitado = False
            for no_hist in trajeto_atual:
                if no_hist == proximo_no:
                    ja_visitado = True
                    break

            if not ja_visitado:
                novo_trajeto = []
                for no_hist in trajeto_atual:
                    novo_trajeto.append(no_hist)
                novo_trajeto.append(proximo_no)

                nova_dist = dist_atual + dist_via
                novo_custo = custo_atual + pedagio_via

                pilha_fronteira.append([proximo_no, novo_trajeto, nova_dist, novo_custo])

def planejar_rota(malha, origem, destino, orcamento):
    """
    Subprograma principal que coordena o fluxo sequencial de validacao, construcao de estruturas mutaveis, busca e formatacao do resultado
    """
    resultado = inicializar_resultado()

    entrada_valida = validar_entrada(malha, origem, destino, float(orcamento))
    if not entrada_valida:
        return resultado

    tabela_adjacencia = {}
    construir_lista_adjacencia(malha, tabela_adjacencia)

    #estrutura mutavel que mantem o estado da exploracao do grafo
    estado_busca = {
        "encontrou_caminho_fisico": False,
        "encontrou_rota_viavel": False,
        "melhor_trajeto": None,
        "melhor_distancia": float("inf"),
        "melhor_custo": float("inf")
    }

    executar_busca_imperativa(
        tabela_adjacencia,
        origem,
        destino,
        float(orcamento),
        estado_busca
    )

    if estado_busca["encontrou_rota_viavel"]:
        resultado["status"] = "ROTA_ENCONTRADA"
        resultado["trajeto"] = estado_busca["melhor_trajeto"]
        resultado["distancia_total"] = estado_busca["melhor_distancia"]
        resultado["custo_total"] = estado_busca["melhor_custo"] = estado_busca["melhor_custo"]
    elif estado_busca["encontrou_caminho_fisico"]:
        resultado["status"] = "ORCAMENTO_INSUFICIENTE"
    else:
        resultado["status"] = "ROTA_INEXISTENTE"

    return resultado


def executar_suite_testes():
    """
    procedimento de validacao que executa os 15 casos de teste definidos na ETAPA 2, produzindo efeitos colaterais de saida padrao no terminal
    """
    malha_g1 = [
        ("A", "B", 10.0, 5.0),
        ("A", "C", 15.0, 0.0),
        ("B", "D", 10.0, 5.0),
        ("C", "D", 12.0, 2.0),
        ("B", "C", 2.0, 1.0),
        ("D", "E", 8.0, 3.0),
        ("C", "E", 25.0, 1.0)
    ]

    malha_ciclo = [
        ("X", "Y", 5.0, 1.0),
        ("Y", "Z", 5.0, 1.0),
        ("Z", "X", 5.0, 1.0),
        ("Y", "W", 10.0, 2.0)
    ]

    malha_empate = [
        ("N1", "N2", 20.0, 10.0),
        ("N2", "F", 5.0, 2.0),
        ("N1", "N3", 20.0, 4.0),
        ("N3", "F", 5.0, 0.0)
    ]

    casos_teste = [
        #10 casos normais
        ("TC-NORM-01", malha_g1, "A", "B", 10.0, "ROTA_ENCONTRADA", ["A", "B"], 10.0, 5.0),
        ("TC-NORM-02", malha_g1, "A", "D", 15.0, "ROTA_ENCONTRADA", ["A", "B", "D"], 20.0, 10.0),
        ("TC-NORM-03", malha_g1, "A", "D", 5.0, "ROTA_ENCONTRADA", ["A", "C", "D"], 27.0, 2.0),
        ("TC-NORM-04", malha_g1, "A", "D", 1.0, "ORCAMENTO_INSUFICIENTE", [], 0.0, 0.0),
        ("TC-NORM-05", malha_g1, "D", "A", 50.0, "ROTA_INEXISTENTE", [], 0.0, 0.0),
        ("TC-NORM-06", malha_g1, "A", "E", 20.0, "ROTA_ENCONTRADA", ["A", "B", "D", "E"], 28.0, 13.0),
        ("TC-NORM-07", malha_g1, "A", "D", 8.0, "ROTA_ENCONTRADA", ["A", "B", "C", "D"], 24.0, 8.0),
        ("TC-NORM-08", malha_g1, "A", "D", 10.0, "ROTA_ENCONTRADA", ["A", "B", "D"], 20.0, 10.0),
        ("TC-NORM-09", malha_g1, "A", "C", 0.0, "ROTA_ENCONTRADA", ["A", "C"], 15.0, 0.0),
        ("TC-NORM-10", malha_g1, "A", "E", 5.0, "ROTA_ENCONTRADA", ["A", "C", "D", "E"], 35.0, 5.0),

        #3 casos limite
        ("TC-LIM-01", malha_g1, "A", "A", 0.0, "ROTA_ENCONTRADA", ["A"], 0.0, 0.0),
        ("TC-LIM-02", malha_ciclo, "X", "W", 10.0, "ROTA_ENCONTRADA", ["X", "Y", "W"], 15.0, 3.0),
        ("TC-LIM-03", malha_empate, "N1", "F", 15.0, "ROTA_ENCONTRADA", ["N1", "N3", "F"], 25.0, 4.0),

        #2 casos de entrada invalida
        ("TC-INV-01", malha_g1, "A", "D", -5.0, "ENTRADA_INVALIDA", [], 0.0, 0.0),
        ("TC-INV-02", malha_g1, "ORIGEM_DESCONHECIDA", "D", 10.0, "ENTRADA_INVALIDA", [], 0.0, 0.0)
    ]

    total_passou = 0
    total_casos = len(casos_teste)

    print("[P4-ETAPA-03] EXECUCAO DA SUITE DE TESTES - PARADIGMA IMPERATIVO")
    for caso in casos_teste:
        id_caso = caso[0]
        malha = caso[1]
        origem = caso[2]
        destino = caso[3]
        orcamento = caso[4]
        status_esp = caso[5]
        trajeto_esp = caso[6]
        dist_esp = caso[7]
        custo_esp = caso[8]

        obtido = planejar_rota(malha, origem, destino, orcamento)

        passou = (
            obtido["status"] == status_esp and
            obtido["trajeto"] == trajeto_esp and
            obtido["distancia_total"] == dist_esp and
            obtido["custo_total"] == custo_esp
        )

        if passou:
            total_passou = total_passou + 1
            print(f"[OK] {id_caso}: Status={obtido['status']} | Trajeto={obtido['trajeto']} | Dist={obtido['distancia_total']} | Custo={obtido['custo_total']}")
        else:
            print(f"[FALHA] {id_caso}:")
            print(f"  Esperado: Status={status_esp}, Trajeto={trajeto_esp}, Dist={dist_esp}, Custo={custo_esp}")
            print(f"  Obtido:   Status={obtido['status']}, Trajeto={obtido['trajeto']}, Dist={obtido['distancia_total']}, Custo={obtido['custo_total']}")

    print(f"Resultado Final: {total_passou}/{total_casos} casos de teste aprovados!")

if __name__ == "__main__":
    executar_suite_testes()