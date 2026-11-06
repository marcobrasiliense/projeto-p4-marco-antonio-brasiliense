# Etapa 06 - Paradigma Funcional
# Implementacao com dados imutaveis (tuplas), recursao e funcoes de alta ordem


def carregar_malha(arestas):
    """Gera o grafo como dicionario de tuplas imutaveis."""
    malha = {}
    for u, v, dist, ped in arestas:
        if u not in malha:
            malha[u] = ()
        malha[u] = malha[u] + ((v, float(dist), float(ped)),)
    return malha


def buscar_caminhos(malha, atual, destino, visitados, dist_acc, custo_acc):
    """Busca recursiva de todos os caminhos possiveis sem gerar ciclos."""
    caminho_atual = visitados + (atual,)

    # Se chegou ao destino, retorna o trajeto acumulado
    if atual == destino:
        return ((caminho_atual, dist_acc, custo_acc),)

    vizinhos = malha.get(atual, ())

    # Filtra apenas quem ainda nao foi visitado no trajeto
    vizinhos_livres = tuple(filter(lambda x: x[0] not in caminho_atual, vizinhos))
    if not vizinhos_livres:
        return ()

    # Explora recursivamente cada ramificacao valida
    todos = ()
    for v, dist, ped in vizinhos_livres:
        todos = todos + buscar_caminhos(
            malha, v, destino, caminho_atual, dist_acc + dist, custo_acc + ped
        )
    return todos


def planejar_rota(malha_tuplas, origem, destino, orcamento):
    """Pipeline principal: explora caminhos, filtra por pedagio e seleciona o otimo."""
    try:
        orcamento_num = float(orcamento)
        if orcamento_num < 0:
            return {
                "status": "ENTRADA_INVALIDA",
                "trajeto": [],
                "distancia_total": 0.0,
                "custo_total": 0.0,
            }
    except (ValueError, TypeError):
        return {
            "status": "ENTRADA_INVALIDA",
            "trajeto": [],
            "distancia_total": 0.0,
            "custo_total": 0.0,
        }

    if not malha_tuplas:
        return {
            "status": "ENTRADA_INVALIDA",
            "trajeto": [],
            "distancia_total": 0.0,
            "custo_total": 0.0,
        }

    malha = carregar_malha(malha_tuplas)

    # Identifica todos os vertices cadastrados
    nos = set()
    for u, vizinhos in malha.items():
        nos.add(u)
        for v, _, _ in vizinhos:
            nos.add(v)

    if origem not in nos or destino not in nos:
        return {
            "status": "ENTRADA_INVALIDA",
            "trajeto": [],
            "distancia_total": 0.0,
            "custo_total": 0.0,
        }

    # 1. Busca todos os trajetos fisicos
    caminhos = buscar_caminhos(malha, origem, destino, (), 0.0, 0.0)
    if not caminhos:
        return {
            "status": "ROTA_INEXISTENTE",
            "trajeto": [],
            "distancia_total": 0.0,
            "custo_total": 0.0,
        }

    # 2. Filtra os trajetos que cabem no orcamento
    validos = tuple(filter(lambda c: c[2] <= orcamento_num, caminhos))
    if not validos:
        return {
            "status": "ORCAMENTO_INSUFICIENTE",
            "trajeto": [],
            "distancia_total": 0.0,
            "custo_total": 0.0,
        }

    # 3. Desempate: menor distancia, menor pedagio e ordem alfabetica
    melhor = min(validos, key=lambda c: (c[1], c[2], c[0]))

    return {
        "status": "ROTA_ENCONTRADA",
        "trajeto": list(melhor[0]),
        "distancia_total": melhor[1],
        "custo_total": melhor[2],
    }


# Teste manual simples
if __name__ == "__main__":
    grafo_exemplo = (
        ("A", "B", 10.0, 5.0),
        ("A", "C", 15.0, 0.0),
        ("B", "D", 10.0, 5.0),
        ("C", "D", 12.0, 2.0),
        ("D", "E", 8.0, 3.0),
    )

    resultado = planejar_rota(grafo_exemplo, "A", "D", 15.0)
    print("Status:", resultado["status"])
    print("Trajeto:", resultado["trajeto"])
    print("Distancia:", resultado["distancia_total"])
    print("Custo Pedagio:", resultado["custo_total"])
