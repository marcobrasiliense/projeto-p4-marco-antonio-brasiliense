# [P4-ETAPA-04] Implementacao Orientada a Objetos
#modulo: modelos.py -> Entidades de dominio encapsuladas

class StatusRota:
    """Constantes de dominio para o status do processamento"""
    ROTA_ENCONTRADA = "ROTA_ENCONTRADA"
    ORCAMENTO_INSUFICIENTE = "ORCAMENTO_INSUFICIENTE"
    ROTA_INEXISTENTE = "ROTA_INEXISTENTE"
    ENTRADA_INVALIDA = "ENTRADA_INVALIDA"

class Via:
    """Representa uma conexao direcionada e ponderada entre dois locais. Garante por encapsulamento que distancia seja positiva e pedagio nao negativo"""

    def __init__(self, origem: str, destino: str, distancia: float, pedagio: float):
        if not isinstance(origem, str) or not origem.strip():
            raise ValueError("A origem da via deve ser um identificador valido.")
        if not isinstance(destino, str) or not destino.strip():
            raise ValueError("O destino da via deve ser um identificador valido.")

        dist_float = float(distancia)
        ped_float = float(pedagio)

        if dist_float <= 0.0:
            raise ValueError("A distância da via deve ser estritamente positiva.")
        if ped_float < 0.0:
            raise ValueError("O valor do pedágio não pode ser negativo.")

        self._origem = origem.strip()
        self._destino = destino.strip()
        self._distancia = dist_float
        self._pedagio = ped_float

    @property #transforma um metodo de classe em um atributo. permite acessar diretamente sem o uso de parenteses
    def origem(self) -> str:
        return self._origem

    @property
    def destino(self) -> str:
        return self._destino

    @property
    def distancia(self) -> float:
        return self._distancia

    @property
    def pedagio(self) -> float:
        return self._pedagio

    def __repr__(self) -> str:
        return f"Via({self._origem} -> {self._destino}, dist={self._distancia}km, ped=R${self._pedagio:.2f})"

class Trajeto:
    """Objeto de valor que representa uma caminhada aciclica em construcao no grafo. Substitui as listas soltas do paradigma imperativo por operações encapsuladas"""
    def __init__(self, nos: list, distancia_total: float = 0.0, custo_total: float = 0.0):
        self._nos = list(nos)
        self._distancia_total = float(distancia_total)
        self._custo_total = float(custo_total)

    @property
    def no_atual(self) -> str:
        return self._nos[-1]

    @property
    def nos(self) -> list:
        return list(self._nos)

    @property
    def distancia_total(self) -> float:
        return self._distancia_total

    @property
    def custo_total(self) -> float:
        return self._custo_total

    def ja_visitou(self, no: str) -> bool:
        """Verifica se um local ja faz parte do trajeto para garantir aciclidade"""
        return no in self._nos

    def respeita_orcamento(self, orcamento_maximo: float) -> bool:
        """Verifica se o custo acumulado esta dentro do limite financeiro"""
        return self._custo_total <= orcamento_maximo

    def estender(self, via: Via) -> "Trajeto":
        """Retorna uma nova instancia de trajeto acrescentando a via informada, preservando a integridade do objeto original"""
        if via.origem != self.no_atual:
            raise ValueError("A via nao parte do nó atual do trajeto")
        if self.ja_visitou(via.destino):
            raise ValueError("Violação da aciclidade: Nó destino já visitado")

        novos_nos = self._nos + [via.destino]
        nova_distancia = self._distancia_total + via.distancia
        novo_custo = self._custo_total + via.pedagio
        return Trajeto(novos_nos, nova_distancia, novo_custo)

class ResultadoRota:
    """Encapsula a resposta final do planejador conforme o contrato semantico"""
    def __init__(self, status: str, trajeto: list = None, distancia_total: float = 0.0, custo_total: float = 0.0):
        self._status = status
        self._trajeto = list(trajeto) if trajeto is not None else []
        self._distancia_total = float(distancia_total)
        self._custo_total = float(custo_total)


    @property
    def status(self) -> str:
        return self._status

    @property
    def trajeto(self) -> list:
        return list(self._trajeto)

    @property
    def distancia_total(self) -> float:
        return self._distancia_total

    @property
    def custo_total(self) -> float:
        return self._custo_total

    def para_dicionario(self) -> dict:
        """Converte o objeto para o formato de dicionario do contrato semantico"""
        return {
            "status": self._status,
            "trajeto": self.trajeto,
            "distancia_total": self._distancia_total,
            "custo_total": self._custo_total
        }

    @classmethod #define um metodo que pertence a classe e nao a um objeto especifico
    def rota_encontrada(cls, trajeto_otimo: Trajeto) -> "ResultadoRota":
        return cls(
            StatusRota.ROTA_ENCONTRADA,
            trajeto_otimo.nos,
            trajeto_otimo.distancia_total,
            trajeto_otimo.custo_total
        )

    @classmethod
    def orcamento_insuficiente(cls) -> "ResultadoRota":
        return cls(StatusRota.ORCAMENTO_INSUFICIENTE, [], 0.0, 0.0)

    @classmethod
    def rota_inexistente(cls) -> "ResultadoRota":
        return cls(StatusRota.ROTA_INEXISTENTE, [], 0.0, 0.0)

    @classmethod
    def entrada_invalida(cls) -> "ResultadoRota":
        return cls(StatusRota.ENTRADA_INVALIDA, [], 0.0, 0.0)



