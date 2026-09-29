# [P4-ETAPA-04] Implementacao Orientada a Objetos
#modulo planejador.py -> agregacao da malha viaria e motor de busca OO

from modelos import Via, Trajeto, ResultadoRota
from criterios import CriterioOtimizacao, CriterioMenorDistanciaPadrao

class MalhaViaria:
    """Agregador responsavel por gerenciar os locais (nós) e as vias (arestas). Encapsula a tabela de adjacencia impedindo modificacoes externas diretas"""

    def __init__(self):
        self._adjacencias = {}
        self._nos_conhecidos = set()

    def adicionar_via(self, via: Via) -> None:
        """Registra um objeto Via na malha e atualiza o conjunto de nós"""
        if not isinstance(via, Via):
            raise TypeError("O elemento adicionado deve ser uma instancia da classe Via")

        self._nos_conhecidos.add(via.origem)
        self._nos_conhecidos.add(via.destino)

        if via.origem not in self._adjacencias:
            self._adjacencias[via.origem] = []
        if via.destino not in self._adjacencias:
            self._adjacencias[via.destino] = []

        self._adjacencias[via.origem].append(via)

    def carregar_de_tuplas(self, arestas_brutas: list) -> None:
        """Constroi as vias a partir de uma colecao de tuplas (origem, destino, distancia, ped)"""
        if arestas_brutas is None or len(arestas_brutas) == 0:
            raise ValueError("A lista de arestas não pode ser vazia")

        for item in arestas_brutas:
            if len(item) != 4:
                raise ValueError("Cada tupla deve conter exatamente 4 elementos")
            nova_via = Via(item[0], item[1], item[2], item[3])
            self.adicionar_via(nova_via)

    def possui_no(self, identificador_no: str) -> bool:
        return identificador_no in self._nos_conhecidos

    def resolver_nome_no(self, nome_digitado: str) -> str:
        """Busca o nome exato do nó ignorando diferenças de maiusculas/minusculas para facilitar a digitação do usuario no menu interativo"""
        if not isinstance(nome_digitado, str):
            return ""
        alvo = nome_digitado.strip().lower()
        for no in self._nos_conhecidos:
            if no.lower() == alvo:
                return no
        return nome_digitado.strip()

    def obter_vias_saida(self, no: str) -> tuple:
        """Retorna uma tupla imutavel com as vias que partem do no informado"""
        return tuple(self._adjacencias.get(no, []))

    def listar_nos_ordenados(self) -> list:
        return sorted(list(self._nos_conhecidos))

    def listar_todas_vias(self) -> list:
        todas = []
        for origem in sorted(self._adjacencias.keys()):
            for via in self._adjacencias[origem]:
                todas.append(via)
        return todas

    @property
    def esta_vazia(self) -> bool:
        return len(self._nos_conhecidos) == 0

class PlanejadorRotas:
    """Servico de dominio que coordena a busca de rotas otimas sobre uma MalhaViaria, delegando a comparaçao de otimalidade de maneira polifmornica a um CriterioOtimizacoa"""
    def __init__(self, malha: MalhaViaria, criterio: CriterioOtimizacao = None):
        self._malha = malha
        self._criterio = criterio if criterio is not None else CriterioMenorDistanciaPadrao()

    def definir_criterio(self, novo_criterio: CriterioOtimizacao) -> None:
        """Permite trocar de forma polimorfica a estrategia de otimizacao em tempo de execucao"""
        self._criterio = novo_criterio

    def calcular_rota(self, origem: str, destino: str, orcamento: float) -> ResultadoRota:
        """Executa a busca orientada a objetos manipulando instancias de trajeto e via"""
        try:
            orcamento_num = float(orcamento)
        except (ValueError, TypeError):
            return ResultadoRota.entrada_invalida()

        if orcamento_num < 0.0 or self._malha is None or self._malha.esta_vazia:
            return ResultadoRota.entrada_invalida()

        if not self._malha.possui_no(origem) or not self._malha.possui_no(destino):
            return ResultadoRota.entrada_invalida()

        fronteira = [Trajeto([origem], 0.0, 0.0)]
        encontrou_caminho_fisico = False
        melhor_trajeto = None

        while len(fronteira) > 0:
            trajeto_atual = fronteira.pop()

            if trajeto_atual.no_atual == destino:
                encontrou_caminho_fisico = True

                if trajeto_atual.respeita_orcamento(orcamento_num):
                    if self._criterio.e_melhor(trajeto_atual, melhor_trajeto):
                        melhor_trajeto = trajeto_atual
                continue

            for via in self._malha.obter_vias_saida(trajeto_atual.no_atual):
                if not trajeto_atual.ja_visitou(via.destino):
                    novo_trajeto = trajeto_atual.estender(via)
                    fronteira.append(novo_trajeto)

        if melhor_trajeto is not None:
            return ResultadoRota.rota_encontrada(melhor_trajeto)
        elif encontrou_caminho_fisico:
            return ResultadoRota.orcamento_insuficiente()
        else:
            return ResultadoRota.rota_inexistente()


def planejar_rota(malha_tuplas: list, origem: str, destino: str, orcamento: float) -> dict:
    """Fachada de compatibilidade direta com a assinatura do Contrato semantico da Etapa 2. Instancia os objetos internamente e retorna com o dicionario padronizado"""
    try:
        malha_obj = MalhaViaria()
        malha_obj.carregar_de_tuplas(malha_tuplas)
        planejador = PlanejadorRotas(malha_obj, CriterioMenorDistanciaPadrao())
        resultado_obj = planejador.calcular_rota(origem, destino, orcamento)
        return resultado_obj.para_dicionario()
    except (ValueError, TypeError):
        return ResultadoRota.entrada_invalida().para_dicionario()