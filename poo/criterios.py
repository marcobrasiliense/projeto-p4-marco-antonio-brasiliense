# [P4-ETAPA-04] Implementacao Orientada a Objetos
#modulo: criterios.py -> abstracao, heranca, polimorfismo

from abc import ABC, abstractmethod #para criar classes abstratas
from modelos import Trajeto

class CriterioOtimizacao(ABC):
    """Classe base abstrata que define o contrato polimorfico pra avaliacao e desempate entre dois objetos Trajetos validos"""

    @abstractmethod #usado para definir um metodo obrigatorio que todas classes filhas devem implementar, mas que nao possui logica propria na classe mae
    def e_melhor(self, candidato: Trajeto, atual: Trajeto) -> bool:
        """Retorna True se o trajeto candidato for superior ao trajeto atual"""
        pass

class CriterioMenorDistanciaPadrao(CriterioOtimizacao):
    """Implementacao concreta oficial do contrato semantico da Etapa 2?
    1º menor distancia total,
    2º menor custo total de pedagio (1º desempate),
    3º ordem lexicografica dos nós (2º desempate)"""

    def e_melhor(self, candidato: Trajeto, atual: Trajeto) -> bool:
        if atual is None:
            return True

        if candidato.distancia_total != atual.distancia_total:
            return candidato.distancia_total < atual.distancia_total

        if candidato.custo_total != atual.custo_total:
            return candidato.custo_total < atual.custo_total

        return candidato.nos < atual.nos

class CriterioMenorPedagioEconomico(CriterioOtimizacao):
    """Implementacao polimorfica alternativa (extensao do sistema):
    Prioriza a economia financeira (menor pedagio primeiro) e usa a menor distancia apenas como criterio de desempate"""

    def e_melhor(self, candidato: Trajeto, atual: Trajeto) -> bool:
        if atual is None:
            return True

        if candidato.custo_total != atual.custo_total:
            return candidato.custo_total < atual.custo_total

        if candidato.distancia_total != atual.distancia_total:
            return candidato.distancia_total < atual.distancia_total

        return candidato.nos < atual.nos