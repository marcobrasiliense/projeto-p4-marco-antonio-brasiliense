# [P4-ETAPA-04] Implementacao Orientada a Objetos
#modulo main.py -> interface de console e suite de validacao da etapa 2

import sys
import os

#garante que os modulos dessa past sejam encontrados em qualquer ambiente de execucao
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos import Via
from criterios import CriterioMenorDistanciaPadrao, CriterioMenorPedagioEconomico
from planejador import MalhaViaria, PlanejadorRotas, planejar_rota

class ExecutorSuiteTestes:
    """
    Classe responsavel por validar os 15 casos de teste do contrato semântico da Etapa 2 utilizando orientação a objetos
    """

    @staticmethod
    def executar() -> None:
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
            # 10 Casos Normais
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
            # 3 Casos-Limite
            ("TC-LIM-01", malha_g1, "A", "A", 0.0, "ROTA_ENCONTRADA", ["A"], 0.0, 0.0),
            ("TC-LIM-02", malha_ciclo, "X", "W", 10.0, "ROTA_ENCONTRADA", ["X", "Y", "W"], 15.0, 3.0),
            ("TC-LIM-03", malha_empate, "N1", "F", 15.0, "ROTA_ENCONTRADA", ["N1", "N3", "F"], 25.0, 4.0),
            # 2 Casos de Entrada Invalida
            ("TC-INV-01", malha_g1, "A", "D", -5.0, "ENTRADA_INVALIDA", [], 0.0, 0.0),
            ("TC-INV-02", malha_g1, "ORIGEM_DESCONHECIDA", "D", 10.0, "ENTRADA_INVALIDA", [], 0.0, 0.0)
        ]

        total_passou = 0
        total_casos = len(casos_teste)

        print(f"[P4-ETAPA-04] EXECUCAO DA SUITE DE TESTES - ORIENTACAO A OBJETOS")

        for caso in casos_teste:
            id_caso, malha, origem, destino, orcamento, status_esp, trajeto_esp, dist_esp, custo_esp = caso
            obtido = planejar_rota(malha, origem, destino, orcamento)

            passou = (
                    obtido["status"] == status_esp and
                    obtido["trajeto"] == trajeto_esp and
                    obtido["distancia_total"] == dist_esp and
                    obtido["custo_total"] == custo_esp
            )

            if passou:
                total_passou +=1
                print(f"[OK] {id_caso}: Status={obtido['status']} | Trajeto={obtido['trajeto']} | Dist={obtido['distancia_total']} | Custo={obtido['custo_total']}")
            else:
                print(f"[FALHA] {id_caso}:")
                print(f"  Esperado: Status={status_esp}, Trajeto={trajeto_esp}, Dist={dist_esp}, Custo={custo_esp}")
                print(f"  Obtido:   Status={obtido['status']}, Trajeto={obtido['trajeto']}, Dist={obtido['distancia_total']}, Custo={obtido['custo_total']}")
            print(f"Resultado Final: {total_passou}/{total_casos} casos de teste aprovados!")

class InterfaceConsolePOO:
    """Camada de apresentacao interativa desacoplada do dominio
    permite consultar rotas em malha pre carregada, adicionar novas vias e executar testes"""

    def __init__(self):
        self._malha_ativa = MalhaViaria()
        self._criterio_ativo = CriterioMenorDistanciaPadrao()
        self._nome_criterio = "menor Distancia (Padrao do Contrato)"
        self._carregar_malha_regional_inicial()

    def _carregar_malha_regional_inicial(self) -> None:
        """Inicializa o sistema com uma malha rodoviaria regional realista (Goias/DF) somada aos nós classicos (A, B, C, D, E) para facilitar testes interativos"""
        vias_iniciais = [
            # Malha Regional de Goias/DF (Ida e Volta com opcoes de pedagio e desvios)
            ("Goiania", "Anapolis", 55.0, 7.50),
            ("Anapolis", "Goiania", 55.0, 7.50),
            ("Anapolis", "Brasilia", 140.0, 12.00),
            ("Brasilia", "Anapolis", 140.0, 12.00),
            ("Anapolis", "Pirenopolis", 65.0, 0.00),
            ("Pirenopolis", "Anapolis", 65.0, 0.00),
            ("Goiania", "Pirenopolis", 125.0, 0.00),
            ("Pirenopolis", "Goiania", 125.0, 0.00),
            ("Pirenopolis", "Brasilia", 150.0, 0.00),
            ("Brasilia", "Pirenopolis", 150.0, 0.00),
            ("Goiania", "CaldasNovas", 170.0, 6.00),
            ("CaldasNovas", "Goiania", 170.0, 6.00),
            ("Goiania", "Itumbiara", 205.0, 14.00),
            ("Itumbiara", "Goiania", 205.0, 14.00),
            ("CaldasNovas", "Itumbiara", 135.0, 0.00),
            ("Itumbiara", "CaldasNovas", 135.0, 0.00),
            ("CaldasNovas", "Cristalina", 240.0, 5.00),
            ("Cristalina", "Brasilia", 130.0, 8.00),
            # Nos da Malha Padrao G1 do Contrato
            ("A", "B", 10.0, 5.0),
            ("A", "C", 15.0, 0.0),
            ("B", "D", 10.0, 5.0),
            ("C", "D", 12.0, 2.0),
            ("B", "C", 2.0, 1.0),
            ("D", "E", 8.0, 3.0),
            ("C", "E", 25.0, 1.0)
        ]
        self._malha_ativa.carregar_de_tuplas(vias_iniciais)

    def _exibir_cidades_disponiveis(self) -> None:
        nos = self._malha_ativa.listar_nos_ordenados()
        cidades_reais = [n for n in nos if len(n) > 1]
        nos_teste = [n for n in nos if len(n) == 1]
        print("\nLOCAIS CADASTRADOS NA MALHA ATUAL")
        print(f"Cidades Regionais: {', '.join(cidades_reais)}")
        print(f"Vertices G1:      {', '.join(nos_teste)}")

    def _opcao_consultar_rota(self) -> None:
        self._exibir_cidades_disponiveis()
        origem_input = input("Digite o ponto de partida (ex: Goiania ou A): ").strip()
        destino_input = input("Digite o ponto de destino (ex: Brasilia ou D): ").strip()
        orcamento_input = input("Digite o orcamento maximo de pedagio em R$ (ex: 15.0): ").strip()

        try:
            orcamento_val = float(orcamento_input)
        except ValueError:
            print("\n[ERRO] O orçamento deve ser um valor numerico valido!\n")
            return

        origem_resolvida = self._malha_ativa.resolver_nome_no(origem_input)
        destino_resolvido = self._malha_ativa.resolver_nome_no(destino_input)

        planejador = PlanejadorRotas(self._malha_ativa, self._criterio_ativo)
        resultado = planejador.calcular_rota(origem_resolvida, destino_resolvido, orcamento_val)

        print("\nRESULTADO DA CONSULTA: ")
        print(f"Criterio Ativo:  {self._nome_criterio}")
        print(f"Status:          {resultado.status}")
        if resultado.status == "ROTA_ENCONTRADA":
            print(f"Trajeto Otimo:   {' -> '.join(resultado.trajeto)}")
            print(f"Distancia Total: {resultado.distancia_total:.1f} km")
            print(f"Custo Pedagio:   R$ {resultado.custo_total:.2f}")
        elif resultado.status == "ORCAMENTO_INSUFICIENTE":
            print("Motivo: Existem estradas ate o destino, mas todas excedem o seu orcamento.")
        elif resultado.status == "ROTA_INEXISTENTE":
            print("Motivo: Nao ha conexoes direcionadas que liguem a origem ao destino.")
        else:
            print("Motivo: Local nao cadastrado na malha ou orcamento negativo (ENTRADA_INVALIDA).")

    def _opcao_cadastrar_via(self) -> None:
        print("\nCADASTAR NOVA VIA NA MALHA: ")
        origem = input("Nome da cidade de origem: ").strip()
        destino = input("Nome da cidade de destino: ").strip()
        dist_str = input("Distancia em km (estritamente positiva): ").strip()
        ped_str = input("Tarifa de pedagio em R$ (0 ou maior): ").strip()

        try:
            nova_via = Via(origem, destino, float(dist_str), float(ped_str))
            self._malha_ativa.adicionar_via(nova_via)
            print(f"\n[SUCESSO] {nova_via} adicionada a malha!\n")
        except ValueError as erro:
            print(f"\n[ERRO DE VALIDACAO] {erro}\n")

    def _opcao_listar_vias(self) -> None:
        print("VIAS CADASTRADAS NA MALHA")
        for via in self._malha_ativa.listar_todas_vias():
            print(f"  * {via.origem:<12} -> {via.destino:<12} | Dist: {via.distancia:>6.1f} km | Pedagio: R$ {via.pedagio:>5.2f}\n")

    def _opcao_trocar_criterio(self) -> None:
        print("\nSELECIONAR CRITERIO DE OTIMIZACAO (POLIMORFISMO)")
        print("1 - Menor Distancia Primeiro (Padrao do Contrato)")
        print("2 - Menor Custo de Pedagio Primeiro (Modo Economico)")
        escolha = input("Escolha (1 ou 2): ").strip()

        if escolha == "1":
            self._criterio_ativo = CriterioMenorDistanciaPadrao()
            self._nome_criterio = "Menor Distancia (padrao do Contrato)"
            print("Criterio alterado para: Menor Distancia Primeiro\n")
        elif escolha == "2":
            self._criterio_ativo = CriterioMenorPedagioEconomico()
            self._nome_criterio = "Menor Pedagio (Modo Economico)"
            print("Criterio alterado para: Menor Custo de Pedagio Primeiro\n")
        else:
            print("Opcao invalida. Mantendo criterio atual\n")

    def iniciar(self) -> None:
        #executa automaticamente a suite de 15 casos logo ao iniciar para comprovar validacao
        ExecutorSuiteTestes.executar()

        while True:
            print("SISTEMA DE PLANEJAMENTO DE ROTAS - PARADIGMA OO (P4)")
            print(f"Criterio Polimorfico Atual: [{self._nome_criterio}]")
            print("1 - Consultar Rota Interativa (Cidades de Goias/DF ou Malha G1)")
            print("2 - Cadastrar Nova Cidade / Via na Malha")
            print("3 - Listar Todas as Vias Cadastradas")
            print("4 - Alterar Criterio de Otimizacao (Demonstrar Polimorfismo)")
            print("5 - Reexecutar Suite Oficial de 15 Casos de Teste (Etapa 02)")
            print("0 - Sair")

            try:
                opcao = input("Escolha uma opcao: ").strip()
            except EOFError:
                break

            if opcao == "1":
                self._opcao_consultar_rota()
            elif opcao == "2":
                self._opcao_cadastrar_via()
            elif opcao == "3":
                self._opcao_listar_vias()
            elif opcao == "4":
                self._opcao_trocar_criterio()
            elif opcao == "5":
                ExecutorSuiteTestes.executar()
            elif opcao == "0":
                print("Encerrando o sistema!")
                break
            else:
                print("Opcao invalida. DIgite um numero de 0 a 5\n")

if __name__ == "__main__":
    app = InterfaceConsolePOO()
    app.iniciar()