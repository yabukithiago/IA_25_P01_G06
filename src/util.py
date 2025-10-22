from model import dias_semana, horarios

def gerar_variaveis(dados):
    variaveis = []
    for turma, cursos in dados['cc'].items():
        for curso in cursos:
            num_aulas = 1 if curso in dados['olw'] else 2
            for i in range(1, num_aulas + 1):
                variaveis.append(f"{turma}_{curso}_{i}")
    return variaveis


def gerar_dominio(dados):
    salas = list(set(dados['rr'].values())) if dados['rr'] else ["S1", "S2", "S3"]
    dominio = []
    for d in range(len(dias_semana)):
        for h in range(len(horarios)):
            for s in salas:
                dominio.append((d, h, s))
    return dominio