# dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
# horarios = ["09h-11h", "11h-13h", "14h-16h", "16h-18h"]

# def variaveis(dados):
#     variaveis = []
#     for turma, cursos, in dados['cc'].items():
#         for curso in cursos:
#             num_aula = 1 if curso in dados['olw'] else 2
#             for i in range(1, num_aula + 1):
#                 variaveis.append(f"{turma}_{curso}_{i}")
#     return variaveis

# def dominio(dados):
#     salas = list(set(dados['rr'].values())) if dados['rr'] else ["S1", "S2", "S3"]
#     dominio = []
#     for d in range(len(dias_semana)):
#         for h in range(len(horarios)):
#             for s in salas:
#                 dominio.append((d, h, s))
#     return dominio