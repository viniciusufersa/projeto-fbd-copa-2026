# ============================================================
# ETAPA 2 - Inserção de registros nas tabelas
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 2 - INSERÇÃO DE REGISTROS ===')
print()

print('--- Cadastro de seleções ---')
print('Serão cadastradas 5 seleções.')
print()

contador = 1

while contador <= 5:
    print(f'Seleção {contador} de 5')

    nome_pais = input('Nome do país: ')
    while nome_pais.strip() == '':
        print('O nome do país é obrigatório!')
        nome_pais = input('Nome do país: ')

    confederacao = input('Confederação: ')
    while confederacao.strip() == '':
        print('A confederação é obrigatória!')
        confederacao = input('Confederação: ')

    tecnico = input('Técnico: ')
    if tecnico.strip() == '':
        tecnico = None

    ranking_fifa = input('Ranking FIFA: ')

    while ranking_fifa != '':
        try:
            ranking_fifa = int(ranking_fifa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            ranking_fifa = input('Ranking FIFA: ')

    if ranking_fifa == '':
        ranking_fifa = None

    sql = '''
    INSERT INTO selecoes (nome_pais, confederacao, tecnico, ranking_fifa)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome_pais, confederacao, tecnico, ranking_fifa))
    conexao.commit()

    print('Seleção cadastrada com sucesso!')
    print()

    contador = contador + 1

print('--- Cadastro de jogadores ---')
print('Serão cadastrados 5 jogadores.')
print()

contador = 1

while contador <= 5:
    print(f'Jogador {contador} de 5')

    print('Seleções cadastradas:')
    cursor.execute('SELECT id, nome_pais FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]}')

    print()

    nome = input('Nome do jogador: ')
    while nome.strip() == '':
        print('O nome do jogador é obrigatório!')
        nome = input('Nome do jogador: ')

    posicao = input('Posição: ')
    while posicao.strip() == '':
        print('A posição é obrigatória!')
        posicao = input('Posição: ')

    idade = input('Idade: ')

    while idade != '':
        try:
            idade = int(idade)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            idade = input('Idade: ')

    if idade == '':
        idade = None

    numero_camisa = input('Número da camisa: ')

    while numero_camisa != '':
        try:
            numero_camisa = int(numero_camisa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            numero_camisa = input('Número da camisa: ')

    if numero_camisa == '':
        numero_camisa = None

    clube_origem = input('Clube de origem: ')
    if clube_origem.strip() == '':
        clube_origem = None

    id_selecao_valido = False

    while id_selecao_valido == False:
        id_selecao = input('ID da seleção do jogador: ')

        while id_selecao.strip() == '':
            print('O ID da seleção é obrigatório!')
            id_selecao = input('ID da seleção do jogador: ')

        try:
            id_selecao = int(id_selecao)

            cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao,))
            selecao_encontrada = cursor.fetchone()

            if selecao_encontrada is None:
                print('Seleção não encontrada. Digite um ID existente.')
            else:
                id_selecao_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção.')

    sql = '''
    INSERT INTO jogadores (nome, posicao, idade, numero_camisa, clube_origem, id_selecao)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome, posicao, idade, numero_camisa, clube_origem, id_selecao))
    conexao.commit()

    print('Jogador cadastrado com sucesso!')
    print()

    contador = contador + 1

print('--- Cadastro de estádios ---')
print('Serão cadastrados 5 estádios.')
print()

contador = 1

while contador <= 5:
    print(f'Estádio {contador} de 5')

    nome = input('Nome do estádio: ')
    while nome.strip() == '':
        print('O nome do estádio é obrigatório!')
        nome = input('Nome do estádio: ')

    cidade = input('Cidade: ')
    while cidade.strip() == '':
        print('A cidade é obrigatória!')
        cidade = input('Cidade: ')

    pais_sede = input('País-sede: ')
    if pais_sede.strip() == '':
        pais_sede = None

    capacidade = input('Capacidade: ')

    while capacidade != '':
        try:
            capacidade = int(capacidade)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            capacidade = input('Capacidade: ')

    if capacidade == '':
        capacidade = None

    sql = '''
    INSERT INTO estadios (nome, cidade, pais_sede, capacidade)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome, cidade, pais_sede, capacidade))
    conexao.commit()

    print('Estádio cadastrado com sucesso!')
    print()

    contador = contador + 1

print('--- Cadastro de partidas ---')
print('Serão cadastradas 5 partidas.')
print()

contador = 1

while contador <= 5:
    print(f'Partida {contador} de 5')

    print('Seleções cadastradas:')
    cursor.execute('SELECT id, nome_pais FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]}')

    print()

    print('Estádios cadastrados:')
    cursor.execute('SELECT id, nome FROM estadios ORDER BY id')
    estadios = cursor.fetchall()

    for estadio in estadios:
        print(f'[{estadio[0]}] {estadio[1]}')

    print()

    data_jogo = input('Data do jogo (AAAA-MM-DD): ')
    while data_jogo.strip() == '':
        print('A data do jogo é obrigatória!')
        data_jogo = input('Data do jogo (AAAA-MM-DD): ')

    fase = input('Fase da competição: ')
    while fase.strip() == '':
        print('A fase é obrigatória!')
        fase = input('Fase da competição: ')

    gols_casa = input('Gols da seleção mandante: ')

    while gols_casa != '':
        try:
            gols_casa = int(gols_casa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            gols_casa = input('Gols da seleção mandante: ')

    if gols_casa == '':
        gols_casa = None

    gols_visitante = input('Gols da seleção visitante: ')

    while gols_visitante != '':
        try:
            gols_visitante = int(gols_visitante)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            gols_visitante = input('Gols da seleção visitante: ')

    if gols_visitante == '':
        gols_visitante = None

    id_casa_valido = False

    while id_casa_valido == False:
        id_selecao_casa = input('ID da seleção mandante: ')

        while id_selecao_casa.strip() == '':
            print('O ID da seleção mandante é obrigatório!')
            id_selecao_casa = input('ID da seleção mandante: ')

        try:
            id_selecao_casa = int(id_selecao_casa)

            cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_casa,))
            selecao_casa = cursor.fetchone()

            if selecao_casa is None:
                print('Seleção mandante não encontrada. Digite um ID existente.')
            else:
                id_casa_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção mandante.')

    id_visitante_valido = False

    while id_visitante_valido == False:
        id_selecao_visitante = input('ID da seleção visitante: ')

        while id_selecao_visitante.strip() == '':
            print('O ID da seleção visitante é obrigatório!')
            id_selecao_visitante = input('ID da seleção visitante: ')

        try:
            id_selecao_visitante = int(id_selecao_visitante)

            if id_selecao_visitante == id_selecao_casa:
                print('A seleção visitante não pode ser igual à mandante.')
            else:
                cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_visitante,))
                selecao_visitante = cursor.fetchone()

                if selecao_visitante is None:
                    print('Seleção visitante não encontrada. Digite um ID existente.')
                else:
                    id_visitante_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção visitante.')

    id_estadio_valido = False

    while id_estadio_valido == False:
        id_estadio = input('ID do estádio: ')

        while id_estadio.strip() == '':
            print('O ID do estádio é obrigatório!')
            id_estadio = input('ID do estádio: ')

        try:
            id_estadio = int(id_estadio)

            cursor.execute('SELECT id FROM estadios WHERE id = %s', (id_estadio,))
            estadio_encontrado = cursor.fetchone()

            if estadio_encontrado is None:
                print('Estádio não encontrado. Digite um ID existente.')
            else:
                id_estadio_valido = True

        except ValueError:
            print('Digite um número válido para o ID do estádio.')

    sql = '''
    INSERT INTO partidas (data_jogo, fase, gols_casa, gols_visitante, id_selecao_casa, id_selecao_visitante, id_estadio)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(sql, (data_jogo, fase, gols_casa, gols_visitante, id_selecao_casa, id_selecao_visitante, id_estadio))
    conexao.commit()

    print('Partida cadastrada com sucesso!')
    print()

    contador = contador + 1

cursor.close()
conexao.close()

print()
print('Etapa 2 executada com sucesso!')