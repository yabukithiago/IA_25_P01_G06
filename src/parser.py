def ler_ficheiro(nome="dataset.txt"):
    dados = {
        'cc': {},   # Cursos por turma
        'olw': [],  # Cursos com uma aula por semana
        'dsd': {},  # Cursos por professor
        'tr': {},   # Restrições de horário dos professores
        'rr': {},   # Cursos e respetivas salas
        'oc': {}    # Cursos e respetivos índices de aula
    }
    try:
        with open(nome, 'r', encoding='utf-8') as ficheiro:
            linhas = ficheiro.readlines()

        seccao_atual = None

        for linha in linhas:
            linha = linha.strip()

            # Ignorar linhas vazias
            if not linha:
                continue

            # Detetar secções
            if linha.startswith('#cc'):
                seccao_atual = 'cc'
                continue
            elif linha.startswith('#olw'):
                seccao_atual = 'olw'
                continue
            elif linha.startswith('#dsd'):
                seccao_atual = 'dsd'
                continue
            elif linha.startswith('#tr'):
                seccao_atual = 'tr'
                continue
            elif linha.startswith('#rr'):
                seccao_atual = 'rr'
                continue
            elif linha.startswith('#oc'):
                seccao_atual = 'oc'
                continue
            elif linha.startswith('#head'):
                seccao_atual = None
                continue

            # Processar dados baseado na secção atual
            if seccao_atual == 'cc':
                partes = linha.split()
                if partes:
                    turma = partes[0]
                    cursos = partes[1:]
                    dados['cc'][turma] = cursos

            elif seccao_atual == 'olw':
                # No exemplo está vazio, mas processamos caso existam dados
                if linha and not linha.startswith('#'):
                    cursos = linha.split()
                    dados['olw'].extend(cursos)

            elif seccao_atual == 'dsd':
                partes = linha.split()
                if partes:
                    professor = partes[0]
                    cursos = partes[1:]
                    dados['dsd'][professor] = cursos

            elif seccao_atual == 'tr':
                partes = linha.split()
                if partes:
                    professor = partes[0]
                    slots = list(map(int, partes[1:]))
                    dados['tr'][professor] = slots

            elif seccao_atual == 'rr':
                partes = linha.split()
                if len(partes) >= 2:
                    curso = partes[0]
                    sala = partes[1]
                    dados['rr'][curso] = sala

            elif seccao_atual == 'oc':
                partes = linha.split()
                if len(partes) >= 2:
                    curso = partes[0]
                    indice_aula = int(partes[1])
                    dados['oc'][curso] = indice_aula
        return dados
    
    except FileNotFoundError:
        print(f"Erro: Ficheiro '{nome}' não encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao ler ficheiro: {e}")
        return None
    
def mostrar_dados(dados):
    if not dados:
        print("Nenhum dado para mostrar!")
        return

    # # Mostrar cursos por turma (cc)
    # print("\nCURSOS POR TURMA (#cc):")
    # print("-" * 40)
    # for turma, cursos in dados['cc'].items():
    #     print(f"{turma}: {', '.join(cursos)}")
    # print("=" * 50)

    # # Mostrar cursos com uma aula por semana (olw)
    # print(f"\nCURSOS COM UMA AULA POR SEMANA (#olw):")
    # print("-" * 40)
    # if dados['olw']:
    #     print(', '.join(dados['olw']))
    # else:
    #     print("Nenhum curso com uma aula por semana")
    # print("=" * 50)

    # # Mostrar cursos por professor (dsd)
    # print("\nCURSOS POR PROFESSOR (#dsd):")
    # print("-" * 40)
    # for professor, cursos in dados['dsd'].items():
    #     print(f"{professor}: {', '.join(cursos)}")
    # print("=" * 50)

    # # Mostrar restrições de horário (tr)
    # print("\nRESTRIÇÕES DE HORÁRIO DOS PROFESSORES (#tr):")
    # print("-" * 40)
    # for professor, slots in dados['tr'].items():
    #     slots_str = ', '.join(map(str, slots))
    #     print(f"{professor}: slots {slots_str}")
    # print("=" * 50)

    # # Mostrar restrições de sala (rr)
    # print("\nRESTRIÇÕES DE SALA (#rr):")
    # print("-" * 40)
    # for curso, sala in dados['rr'].items():
    #     print(f"{curso}: {sala}")

    # print("=" * 50)
    # # Mostrar aulas online (oc)
    # print("\nAULAS ONLINE (#oc):")
    # print("-" * 40)
    # for curso, indice in dados['oc'].items():
    #     print(f"{curso}: aula {indice} é online")
