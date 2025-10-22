from constraint import Problem, AllDifferentConstraint

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = ["09h-11h", "11h-13h", "14h-16h", "16h-18h"]

BLOCOS_POR_DIA = len(horarios)
DIAS_SEMANA = len(dias_semana)

problem = Problem()

def criar_quadro():
    quadro = []
    for i in range(BLOCOS_POR_DIA):
        linha = []
        for j in range(DIAS_SEMANA):
            timeslot_index = j * BLOCOS_POR_DIA + i + 1
            linha.append(f"timeslot_{timeslot_index}")
        quadro.append(linha)
    return quadro   

def visualizar_quadro(quadro):
    cabecalho = f"{'':<12} | "
    for dia in dias_semana:
        cabecalho += f"{dia:<15} | "
    print(cabecalho)
    print("-" * 110)

    # Imprimir cada linha com horário e timeslots
    for i in range(BLOCOS_POR_DIA):
        linha_str = f"{horarios[i]:<12} | "
        for j in range(DIAS_SEMANA):
            timeslot = quadro[i][j]
            linha_str += f"{timeslot:<15} | "
        print(linha_str)
        print("-" * 110)