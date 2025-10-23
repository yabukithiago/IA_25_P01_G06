from constraint import Problem, AllDifferentConstraint
from model import *

def criar_quadro_horario_com_aulas():
    """Cria quadro horário vazio com estrutura para aulas"""
    quadro = []
    for i in range(BLOCOS_POR_DIA):
        linha = []
        for j in range(DIAS_SEMANA):
            timeslot_index = j * BLOCOS_POR_DIA + i + 1
            linha.append({
                'timeslot': f"timeslot_{timeslot_index}",
                'aulas': [],
                'dia': dias_semana[j],
                'horario': horarios[i],
                'numero': timeslot_index
            })
        quadro.append(linha)
    return quadro


def atribuir_aulas_ao_horario(dados):
    """Atribui aulas respeitando restrições"""
    problem = Problem()
    variables = []
    dominio_timeslots = list(range(1, TOTAL_TIMESLOTS + 1))

    # Criar variáveis
    for turma, cursos in dados['cc'].items():
        for curso in cursos:
            for aula_index in [1, 2]:
                var_name = f"{turma}_{curso}_aula{aula_index}"
                problem.addVariable(var_name, dominio_timeslots)
                variables.append(var_name)

    print(f"📊 Total de aulas para agendar: {len(variables)}")

    #RESTRIÇOES(HARD_CONSTRAINS)
    #Aulas Diferentes por Turma
    for turma in dados['cc'].keys():
        turma_vars = [var for var in variables if var.startswith(f"{turma}_")]
        problem.addConstraint(AllDifferentConstraint(), turma_vars)

    #Professor Não Pode Dar 2 Aulas Simultâneas
    for professor, cursos_prof in dados['dsd'].items():
        professor_vars = []
        for var_name in variables:
            curso = var_name.split('_')[1]
            if curso in cursos_prof:
                professor_vars.append(var_name)
        if professor_vars:
            problem.addConstraint(AllDifferentConstraint(), professor_vars)

    #Restrições de Disponibilidade do Professor
    for professor, slots_indisponiveis in dados['tr'].items():
        cursos_prof = dados['dsd'][professor]
        for var_name in variables:
            curso = var_name.split('_')[1]
            if curso in cursos_prof:
                def professor_disponivel(timeslot, indisponiveis=slots_indisponiveis):
                    return timeslot not in indisponiveis

                problem.addConstraint(professor_disponivel, [var_name]) # TO DO - Não está a funcionar

    #Máximo 3 Aulas por Dia por Turma
    for turma in dados['cc'].keys():
        turma_vars = [var for var in variables if var.startswith(f"{turma}_")]

        for dia in range(DIAS_SEMANA):
            slots_do_dia = list(range(dia * BLOCOS_POR_DIA + 1, (dia + 1) * BLOCOS_POR_DIA + 1))

            # Constraint individual para cada dia
            def max_aulas_dia(*assignments, slots_dia=slots_do_dia):
                count = 0
                for slot in assignments:
                    if slot in slots_dia:
                        count += 1
                return count <= 3

            problem.addConstraint(max_aulas_dia, turma_vars)


    #TENTATIVA ANTERIOR
    # for turma in dados['cc'].keys():
    #     turma_vars = [var for var in variables if var.startswith(f"{turma}_")]
    #     for dia in range(DIAS_SEMANA):
    #         slots_do_dia = list(range(dia * BLOCOS_POR_DIA + 1, (dia + 1) * BLOCOS_POR_DIA + 1))
    #
    #         def max_3_aulas_por_dia(*assignments):
    #             aulas_no_dia = 0
    #             for timeslot in assignments:
    #                 if timeslot in slots_do_dia:
    #                     aulas_no_dia += 1
    #             return aulas_no_dia <= 3
    #
    #         problem.addConstraint(max_3_aulas_por_dia, turma_vars)


    #Aulas Online no Mesmo Dia
    for curso_online in dados['oc'].keys():
        aulas_online = [var for var in variables if f"_{curso_online}_" in var]
        if len(aulas_online) >= 2:
            def aulas_online_mesmo_dia(timeslot1, timeslot2):
                dia1 = (timeslot1 - 1) // BLOCOS_POR_DIA
                dia2 = (timeslot2 - 1) // BLOCOS_POR_DIA
                return dia1 == dia2

            problem.addConstraint(aulas_online_mesmo_dia, aulas_online)

            # TENTATIVA ANTERIOR
    # for curso_online in dados['oc'].keys():
    #     aulas_online = [var for var in variables if f"_{curso_online}_" in var]
    #     if len(aulas_online) >= 2:
    #         def aulas_online_mesmo_dia(timeslot1, timeslot2):
    #             dia1 = (timeslot1 - 1) // BLOCKS_PER_DAY
    #             dia2 = (timeslot2 - 1) // BLOCKS_PER_DAY
    #             return dia1 == dia2
    #
    #         problem.addConstraint(aulas_online_mesmo_dia, aulas_online)

    print("🔍 A resolver o problema de agendamento...")
    solution = problem.getSolution()

    if not solution:
        print("❌ Não foi possível encontrar uma solução!")
        return None

    print("✅ Solução encontrada!")
    return solution

def preencher_quadro_com_solucao(quadro, solution, dados):
    """Preenche o quadro com a solução - VERSÃO CORRIGIDA"""
    for var_name, timeslot in solution.items():
        partes = var_name.split('_')
        turma = partes[0]
        curso = partes[1]

        timeslot_index = timeslot - 1


        #print(f"DEBUG: {var_name} = timeslot {timeslot}")
        # VERSÃO 1:
        linha = timeslot_index // DIAS_SEMANA  # 0-3
        coluna = timeslot_index % DIAS_SEMANA  # 0-4

        # VERSÃO 2 (alternativa):
        # linha = timeslot_index % BLOCOS_POR_DIA     # 0-3
        # coluna = timeslot_index // BLOCOS_POR_DIA   # 0-4

        sala = dados['rr'].get(curso, f"Room{turma[-1]}")
        aula_info = {'turma': turma, 'curso': curso, 'sala': sala}
        quadro[linha][coluna]['aulas'].append(aula_info)

    return quadro


def visualizar_horario_por_turma(quadro_geral, dados):
    """Mostra horário separado para cada turma"""
    for turma in dados['cc'].keys():
        print(f"\n" + "=" * 80)
        print(f"HORÁRIO DA TURMA {turma}")
        print("=" * 80)

        cabecalho = f"{'Horário':<12} |"
        for dia in dias_semana:
            cabecalho += f" {dia:<20} |"
        print(cabecalho)
        print("-" * 140)

        for i in range(BLOCOS_POR_DIA):
            linha_str = f"{horarios[i]:<12} |"

            for j in range(DIAS_SEMANA):
                celula = quadro_geral[i][j]
                conteudo = "---"

                for aula in celula['aulas']:
                    if aula['turma'] == turma:
                        conteudo = f"{aula['curso']} {aula['sala']}"
                        break

                linha_str += f" {conteudo:<20} |"

            print(linha_str)
            print("-" * 140)


def verificar_restricoes(quadro, dados):
    """
    Verifica manualmente se todas as restrições estão a ser cumpridas
    """
    print("\n" + "🔍 VERIFICAÇÃO DE RESTRIÇÕES")
    print("=" * 50)

    problemas = []

    # Verificar conflitos de professor
    for i in range(BLOCOS_POR_DIA):
        for j in range(DIAS_SEMANA):
            celula = quadro[i][j]
            professores_na_celula = {}

            for aula in celula['aulas']:
                # Encontrar professor desta aula
                professor = None
                for prof, cursos in dados['dsd'].items():
                    if aula['curso'] in cursos:
                        professor = prof
                        break

                if professor:
                    if professor in professores_na_celula:
                        problemas.append(
                            f"❌ Professor {professor} com aula dupla: {professores_na_celula[professor]} e {aula['curso']} no {celula['dia']} {celula['horario']}")
                    professores_na_celula[professor] = aula['curso']

    # Verificar restrições de horário do professor
    for professor, slots_proibidos in dados['tr'].items():
        for timeslot_proibido in slots_proibidos:
            # Converter timeslot para coordenadas
            coluna = (timeslot_proibido - 1) // BLOCOS_POR_DIA
            linha = (timeslot_proibido - 1) % BLOCOS_POR_DIA

            celula = quadro[linha][coluna]
            for aula in celula['aulas']:
                if aula['curso'] in dados['dsd'].get(professor, []):
                    problemas.append(
                        f"❌ Professor {professor} a dar {aula['curso']} em slot proibido {timeslot_proibido} ({celula['dia']} {celula['horario']})")

    # Verificar máximo 3 aulas por dia por turma
    for turma in dados['cc'].keys():
        for dia_idx in range(DIAS_SEMANA):
            aulas_no_dia = 0
            for i in range(BLOCOS_POR_DIA):
                celula = quadro[i][dia_idx]
                for aula in celula['aulas']:
                    if aula['turma'] == turma:
                        aulas_no_dia += 1

            if aulas_no_dia > 3:
                problemas.append(f"❌ Turma {turma} com {aulas_no_dia} aulas na {dias_semana[dia_idx]} (máximo: 3)")

    # Mostrar resultados
    if problemas:
        print("⛔ PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(problema)
    else:
        print("✅ TODAS AS RESTRIÇÕES CUMPRIDAS!")

    return len(problemas) == 0

       
def main(dados):
    """Função principal do agendamento"""
    print("INICIANDO AGENDAMENTO")

    # 1. Criar quadro vazio
    quadro = criar_quadro_horario_com_aulas()

    # 2. Atribuir aulas
    solution = atribuir_aulas_ao_horario(dados)
    if not solution:
        print("Não foi possível criar o horário.")
        return

    # 3. Preencher quadro
    quadro_preenchido = preencher_quadro_com_solucao(quadro, solution, dados)

    # 4. VERIFICAR RESTRIÇÕES
    todas_cumpridas = verificar_restricoes(quadro_preenchido, dados)
    print(f"\nVerificação final das restrições: {'Todas cumpridas' if todas_cumpridas else 'Problemas encontrados'}")
    
    # 4. Mostrar horários
    print("\n" + "HORÁRIOS FINAIS")
    print("=" * 50)
    visualizar_horario_por_turma(quadro_preenchido, dados)

    print("\nAgendamento concluído com sucesso!")
    