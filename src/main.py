from constraint import Problem, AllDifferentConstraint
from model import *
from parser import *
from util import main as agendar_horario
        
if __name__ == "__main__":
    print("=" * 50)
    print("SISTEMA DE GESTÃO DE HORÁRIOS")
    print("=" * 50)

    # 1. Criar e mostrar quadro horário vazio
    quadro = criar_quadro()
    print("\n HORÁRIO BASE: \n")
    visualizar_quadro(quadro)

    # 2. Carregar dados do ficheiro
    dados = ler_ficheiro(r"..\data\dataset.txt")

    if dados:
       # 3. Mostrar dados carregados
       mostrar_dados(dados)
       print("\n" + "INICIANDO AGENDAMENTO AUTOMÁTICO")
       print("=" * 50)
       agendar_horario(dados)
    else:
        print("Não foi possível carregar os dados. Verifique o ficheiro dataset.txt")