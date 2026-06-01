# ============================================================
# ETAPA 9 - Sistema completo com menu interativo
# ============================================================

import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='copa2026'
    )

def linha():
    print('-' * 50)

def pausar():
    input('Pressione ENTER para continuar...')

def ler_inteiro(mensagem):
    valor = input(mensagem)

    if valor.strip() == '':
        return None

    try:
        return int(valor)
    except ValueError:
        print('Valor inválido. Campo ignorado.')
        return None

def ler_inteiro_obrigatorio(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print('Digite um número válido!')

def ler_texto_obrigatorio(mensagem):
    valor = input(mensagem)

    while valor.strip() == '':
        print('Campo obrigatório!')
        valor = input(mensagem)

    return valor.strip()

def listar_selecoes_resumido(cursor):
    cursor.execute('SELECT id, nome_pais FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]}')

    return selecoes

def listar_estadios_resumido(cursor):
    cursor.execute('SELECT id, nome FROM estadios ORDER BY id')
    estadios = cursor.fetchall()

    for estadio in estadios:
        print(f'[{estadio[0]}] {estadio[1]}')

    return estadios

def cadastrar_selecao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('CADASTRAR SELEÇÃO')
    linha()

    nome_pais = ler_texto_obrigatorio('País: ')
    confederacao = ler_texto_obrigatorio('Confederação: ')

    tecnico = input('Técnico (ENTER para pular): ')
    if tecnico.strip() == '':
        tecnico = None

    ranking_fifa = ler_inteiro('Ranking FIFA (ENTER para pular): ')

    cursor.execute('''
        INSERT INTO selecoes (nome_pais, confederacao, tecnico, ranking_fifa)
        VALUES (%s, %s, %s, %s)
    ''', (nome_pais, confederacao, tecnico, ranking_fifa))

    conexao.commit()

    print('Seleção cadastrada com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def cadastrar_jogador():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('CADASTRAR JOGADOR')
    linha()

    print('Seleções disponíveis:')
    selecoes = listar_selecoes_resumido(cursor)

    if len(selecoes) == 0:
        print('Cadastre uma seleção antes de adicionar jogadores.')
        cursor.close()
        conexao.close()
        pausar()
        return

    print()

    nome = ler_texto_obrigatorio('Nome: ')
    posicao = ler_texto_obrigatorio('Posição: ')
    idade = ler_inteiro('Idade (ENTER para pular): ')
    numero_camisa = ler_inteiro('Número da camisa (ENTER para pular): ')

    clube_origem = input('Clube de origem (ENTER para pular): ')
    if clube_origem.strip() == '':
        clube_origem = None

    id_selecao = ler_inteiro_obrigatorio('ID da seleção: ')

    cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao,))
    selecao = cursor.fetchone()

    if selecao is None:
        print('Seleção não encontrada. Jogador não cadastrado.')
    else:
        cursor.execute('''
            INSERT INTO jogadores (nome, posicao, idade, numero_camisa, clube_origem, id_selecao)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nome, posicao, idade, numero_camisa, clube_origem, id_selecao))

        conexao.commit()

        print('Jogador cadastrado com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def cadastrar_estadio():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('CADASTRAR ESTÁDIO')
    linha()

    nome = ler_texto_obrigatorio('Nome: ')
    cidade = ler_texto_obrigatorio('Cidade: ')

    pais_sede = input('País-sede (ENTER para pular): ')
    if pais_sede.strip() == '':
        pais_sede = None

    capacidade = ler_inteiro('Capacidade (ENTER para pular): ')

    cursor.execute('''
        INSERT INTO estadios (nome, cidade, pais_sede, capacidade)
        VALUES (%s, %s, %s, %s)
    ''', (nome, cidade, pais_sede, capacidade))

    conexao.commit()

    print('Estádio cadastrado com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def cadastrar_partida():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('CADASTRAR PARTIDA')
    linha()

    print('Seleções disponíveis:')
    selecoes = listar_selecoes_resumido(cursor)

    print()
    print('Estádios disponíveis:')
    estadios = listar_estadios_resumido(cursor)

    if len(selecoes) == 0 or len(estadios) == 0:
        print('É necessário ter seleções e estádios cadastrados antes de cadastrar partidas.')
        cursor.close()
        conexao.close()
        pausar()
        return

    print()

    data_jogo = ler_texto_obrigatorio('Data do jogo (AAAA-MM-DD): ')
    fase = ler_texto_obrigatorio('Fase: ')
    gols_casa = ler_inteiro('Gols mandante (ENTER se jogo não ocorreu): ')
    gols_visitante = ler_inteiro('Gols visitante (ENTER se jogo não ocorreu): ')
    id_selecao_casa = ler_inteiro_obrigatorio('ID da seleção mandante: ')
    id_selecao_visitante = ler_inteiro_obrigatorio('ID da seleção visitante: ')
    id_estadio = ler_inteiro_obrigatorio('ID do estádio: ')

    if id_selecao_casa == id_selecao_visitante:
        print('A seleção mandante e a visitante não podem ser iguais.')
        cursor.close()
        conexao.close()
        pausar()
        return

    cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_casa,))
    selecao_casa = cursor.fetchone()

    cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_visitante,))
    selecao_visitante = cursor.fetchone()

    cursor.execute('SELECT id FROM estadios WHERE id = %s', (id_estadio,))
    estadio = cursor.fetchone()

    if selecao_casa is None:
        print('Seleção mandante não encontrada. Partida não cadastrada.')
    elif selecao_visitante is None:
        print('Seleção visitante não encontrada. Partida não cadastrada.')
    elif estadio is None:
        print('Estádio não encontrado. Partida não cadastrada.')
    else:
        cursor.execute('''
            INSERT INTO partidas (data_jogo, fase, gols_casa, gols_visitante,
                                  id_selecao_casa, id_selecao_visitante, id_estadio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data_jogo, fase, gols_casa, gols_visitante,
              id_selecao_casa, id_selecao_visitante, id_estadio))

        conexao.commit()

        print('Partida cadastrada com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def jogadores_por_selecao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('JOGADORES DE UMA SELEÇÃO')
    linha()

    print('Seleções:')
    listar_selecoes_resumido(cursor)

    print()

    id_selecao = ler_inteiro_obrigatorio('ID da seleção: ')

    cursor.execute('''
        SELECT jogadores.nome, jogadores.posicao, selecoes.nome_pais
        FROM jogadores
        INNER JOIN selecoes ON jogadores.id_selecao = selecoes.id
        WHERE selecoes.id = %s
        ORDER BY jogadores.nome
    ''', (id_selecao,))

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Nenhum jogador encontrado para essa seleção.')
    else:
        for jogador in resultado:
            print(f'{jogador[0]} | {jogador[1]} | {jogador[2]}')

    cursor.close()
    conexao.close()

    pausar()

def resultados_partidas():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('RESULTADOS DAS PARTIDAS')
    linha()

    cursor.execute('''
        SELECT partidas.data_jogo, partidas.fase,
               casa.nome_pais, partidas.gols_casa,
               visitante.nome_pais, partidas.gols_visitante,
               estadios.nome
        FROM partidas
        INNER JOIN selecoes AS casa ON partidas.id_selecao_casa = casa.id
        INNER JOIN selecoes AS visitante ON partidas.id_selecao_visitante = visitante.id
        INNER JOIN estadios ON partidas.id_estadio = estadios.id
        ORDER BY partidas.data_jogo
    ''')

    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print('Nenhuma partida cadastrada.')
    else:
        for partida in resultado:
            print()
            print(f'{partida[0]} | {partida[1]}')
            print(f'{partida[2]} {partida[3]} x {partida[5]} {partida[4]}')
            print(f'Estádio: {partida[6]}')

    cursor.close()
    conexao.close()

    pausar()

def partidas_por_fase():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('PARTIDAS POR FASE')
    linha()

    fase = input('Fase: ')

    cursor.execute('''
        SELECT partidas.data_jogo, partidas.fase,
               casa.nome_pais, partidas.gols_casa,
               visitante.nome_pais, partidas.gols_visitante
        FROM partidas
        INNER JOIN selecoes AS casa ON partidas.id_selecao_casa = casa.id
        INNER JOIN selecoes AS visitante ON partidas.id_selecao_visitante = visitante.id
        WHERE partidas.fase LIKE %s
        ORDER BY partidas.data_jogo
    ''', (f'%{fase}%',))

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Nenhuma partida encontrada para essa fase.')
    else:
        for partida in resultado:
            print(f'{partida[0]} | {partida[1]} | {partida[2]} {partida[3]} x {partida[5]} {partida[4]}')

    cursor.close()
    conexao.close()

    pausar()

def contar_jogadores_por_selecao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('JOGADORES POR SELEÇÃO')
    linha()

    cursor.execute('''
        SELECT selecoes.nome_pais, COUNT(jogadores.id) AS total
        FROM selecoes
        LEFT JOIN jogadores ON selecoes.id = jogadores.id_selecao
        GROUP BY selecoes.id, selecoes.nome_pais
        ORDER BY total DESC
    ''')

    resultados = cursor.fetchall()

    for resultado in resultados:
        print(f'{resultado[0]}: {resultado[1]} jogador(es)')

    cursor.close()
    conexao.close()

    pausar()

def media_gols_por_partida():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('MÉDIA DE GOLS POR PARTIDA')
    linha()

    cursor.execute('SELECT AVG(gols_casa + gols_visitante) FROM partidas')

    resultado = cursor.fetchone()[0]

    if resultado is None:
        media = 0
    else:
        media = round(resultado, 2)

    print(f'Média: {media} gols por partida')

    cursor.close()
    conexao.close()

    pausar()

def estadios_por_quantidade_partidas():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('ESTÁDIOS POR QUANTIDADE DE PARTIDAS')
    linha()

    minimo = ler_inteiro_obrigatorio('Mostrar estádios com mais de quantas partidas? ')

    cursor.execute('''
        SELECT estadios.nome, COUNT(partidas.id) AS total
        FROM estadios
        LEFT JOIN partidas ON estadios.id = partidas.id_estadio
        GROUP BY estadios.id, estadios.nome
        HAVING COUNT(partidas.id) > %s
        ORDER BY total DESC
    ''', (minimo,))

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Nenhum estádio encontrado com essa quantidade de partidas.')
    else:
        for estadio in resultado:
            print(f'{estadio[0]}: {estadio[1]} partida(s)')

    cursor.close()
    conexao.close()

    pausar()

def selecao_mais_gols():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('SELEÇÃO COM MAIOR TOTAL DE GOLS')
    linha()

    cursor.execute('''
        SELECT selecoes.nome_pais, SUM(gols_por_selecao.gols) AS total_gols
        FROM (
            SELECT id_selecao_casa AS id_selecao, COALESCE(gols_casa, 0) AS gols
            FROM partidas
            UNION ALL
            SELECT id_selecao_visitante AS id_selecao, COALESCE(gols_visitante, 0) AS gols
            FROM partidas
        ) AS gols_por_selecao
        INNER JOIN selecoes ON gols_por_selecao.id_selecao = selecoes.id
        GROUP BY selecoes.id, selecoes.nome_pais
        ORDER BY total_gols DESC
        LIMIT 1
    ''')

    resultado = cursor.fetchone()

    if resultado is None:
        print('Nenhum dado encontrado.')
    else:
        print(f'{resultado[0]}: {resultado[1]} gol(s) no total')

    cursor.close()
    conexao.close()

    pausar()

def estadios_por_capacidade():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('ESTÁDIOS POR CAPACIDADE MÍNIMA')
    linha()

    capacidade = ler_inteiro_obrigatorio('Capacidade mínima: ')

    cursor.execute('''
        SELECT nome, cidade, pais_sede, capacidade
        FROM estadios
        WHERE capacidade > %s
        ORDER BY capacidade DESC
    ''', (capacidade,))

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Nenhum estádio encontrado.')
    else:
        for estadio in resultado:
            print(f'{estadio[0]} | {estadio[1]}, {estadio[2]} | Capacidade: {estadio[3]}')

    cursor.close()
    conexao.close()

    pausar()

def jogadores_por_posicao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('JOGADORES POR POSIÇÃO')
    linha()

    posicao = input('Posição: ')

    cursor.execute('''
        SELECT jogadores.nome, jogadores.posicao, selecoes.nome_pais
        FROM jogadores
        INNER JOIN selecoes ON jogadores.id_selecao = selecoes.id
        WHERE jogadores.posicao LIKE %s
        ORDER BY jogadores.nome
    ''', (f'%{posicao}%',))

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Nenhum jogador encontrado.')
    else:
        for jogador in resultado:
            print(f'{jogador[0]} | {jogador[1]} | {jogador[2]}')

    cursor.close()
    conexao.close()

    pausar()

def selecoes_sem_partidas():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('SELEÇÕES SEM PARTIDAS')
    linha()

    cursor.execute('''
        SELECT selecoes.nome_pais
        FROM selecoes
        LEFT JOIN partidas
        ON selecoes.id = partidas.id_selecao_casa
        OR selecoes.id = partidas.id_selecao_visitante
        WHERE partidas.id IS NULL
        ORDER BY selecoes.nome_pais
    ''')

    resultado = cursor.fetchall()

    print()

    if len(resultado) == 0:
        print('Todas as seleções já possuem pelo menos uma partida.')
    else:
        for selecao in resultado:
            print(f'{selecao[0]}')

    cursor.close()
    conexao.close()

    pausar()

def atualizar_selecao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('ATUALIZAR SELEÇÃO')
    linha()

    cursor.execute('SELECT id, nome_pais, tecnico, ranking_fifa FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]} | Técnico: {selecao[2]} | Ranking: {selecao[3]}')

    print()

    id_selecao = ler_inteiro_obrigatorio('ID da seleção: ')

    cursor.execute('SELECT nome_pais, tecnico, ranking_fifa FROM selecoes WHERE id = %s', (id_selecao,))
    selecao = cursor.fetchone()

    if selecao is None:
        print('Seleção não encontrada.')
    else:
        print(f'Seleção: {selecao[0]}')

        novo_tecnico = input(f'Técnico [{selecao[1]}] (ENTER para manter): ')

        if novo_tecnico.strip() == '':
            novo_tecnico = selecao[1]

        novo_ranking = input(f'Ranking [{selecao[2]}] (ENTER para manter): ')

        if novo_ranking.strip() == '':
            novo_ranking = selecao[2]
        else:
            try:
                novo_ranking = int(novo_ranking)
            except ValueError:
                print('Ranking inválido. Mantendo o valor atual.')
                novo_ranking = selecao[2]

        cursor.execute('''
            UPDATE selecoes
            SET tecnico = %s, ranking_fifa = %s
            WHERE id = %s
        ''', (novo_tecnico, novo_ranking, id_selecao))

        conexao.commit()

        print('Seleção atualizada com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def atualizar_partida():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('ATUALIZAR PARTIDA')
    linha()

    cursor.execute('SELECT id, data_jogo, fase, gols_casa, gols_visitante FROM partidas ORDER BY id')
    partidas = cursor.fetchall()

    if len(partidas) == 0:
        print('Nenhuma partida cadastrada.')
        cursor.close()
        conexao.close()
        pausar()
        return

    for partida in partidas:
        print(f'[{partida[0]}] {partida[1]} | {partida[2]} | Placar: {partida[3]} x {partida[4]}')

    print()

    id_partida = ler_inteiro_obrigatorio('ID da partida: ')

    cursor.execute(
        'SELECT data_jogo, fase, gols_casa, gols_visitante FROM partidas WHERE id = %s',
        (id_partida,)
    )

    partida = cursor.fetchone()

    if partida is None:
        print('Partida não encontrada.')
    else:
        print(f'Partida: {partida[0]} - {partida[1]}')

        nova_data = input(f'Nova data [{partida[0]}] (ENTER para manter): ')
        if nova_data.strip() == '':
            nova_data = partida[0]

        nova_fase = input(f'Nova fase [{partida[1]}] (ENTER para manter): ')
        if nova_fase.strip() == '':
            nova_fase = partida[1]

        novos_gols_casa = input(f'Gols mandante [{partida[2]}] (ENTER para manter): ')
        if novos_gols_casa.strip() == '':
            novos_gols_casa = partida[2]
        else:
            try:
                novos_gols_casa = int(novos_gols_casa)
            except ValueError:
                print('Valor inválido. Mantendo o valor atual.')
                novos_gols_casa = partida[2]

        novos_gols_visitante = input(f'Gols visitante [{partida[3]}] (ENTER para manter): ')
        if novos_gols_visitante.strip() == '':
            novos_gols_visitante = partida[3]
        else:
            try:
                novos_gols_visitante = int(novos_gols_visitante)
            except ValueError:
                print('Valor inválido. Mantendo o valor atual.')
                novos_gols_visitante = partida[3]

        cursor.execute('''
            UPDATE partidas
            SET data_jogo = %s, fase = %s, gols_casa = %s, gols_visitante = %s
            WHERE id = %s
        ''', (nova_data, nova_fase, novos_gols_casa, novos_gols_visitante, id_partida))

        conexao.commit()

        print('Partida atualizada com sucesso!')

    cursor.close()
    conexao.close()

    pausar()

def remover_jogador():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('REMOVER JOGADOR')
    linha()

    cursor.execute('SELECT id, nome, posicao FROM jogadores ORDER BY id')
    jogadores = cursor.fetchall()

    if len(jogadores) == 0:
        print('Nenhum jogador cadastrado.')
        cursor.close()
        conexao.close()
        pausar()
        return

    for jogador in jogadores:
        print(f'[{jogador[0]}] {jogador[1]} - {jogador[2]}')

    print()

    id_jogador = ler_inteiro_obrigatorio('ID do jogador: ')

    cursor.execute('SELECT nome, posicao FROM jogadores WHERE id = %s', (id_jogador,))
    jogador = cursor.fetchone()

    if jogador is None:
        print('Jogador não encontrado.')
    else:
        print(f'Jogador: {jogador[0]} - {jogador[1]}')

        confirmar = input('Confirmar remoção? (s/n): ')

        if confirmar.lower() == 's':
            cursor.execute('DELETE FROM jogadores WHERE id = %s', (id_jogador,))
            conexao.commit()
            print('Jogador removido com sucesso!')
        else:
            print('Remoção cancelada.')

    cursor.close()
    conexao.close()

    pausar()

def remover_partida():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('REMOVER PARTIDA')
    linha()

    cursor.execute('SELECT id, data_jogo, fase FROM partidas ORDER BY id')
    partidas = cursor.fetchall()

    if len(partidas) == 0:
        print('Nenhuma partida cadastrada.')
        cursor.close()
        conexao.close()
        pausar()
        return

    for partida in partidas:
        print(f'[{partida[0]}] {partida[1]} - {partida[2]}')

    print()

    id_partida = ler_inteiro_obrigatorio('ID da partida: ')

    cursor.execute('SELECT data_jogo, fase FROM partidas WHERE id = %s', (id_partida,))
    partida = cursor.fetchone()

    if partida is None:
        print('Partida não encontrada.')
    else:
        print(f'Partida: {partida[0]} - {partida[1]}')

        confirmar = input('Confirmar remoção? (s/n): ')

        if confirmar.lower() == 's':
            cursor.execute('DELETE FROM partidas WHERE id = %s', (id_partida,))
            conexao.commit()
            print('Partida removida com sucesso!')
        else:
            print('Remoção cancelada.')

    cursor.close()
    conexao.close()

    pausar()

def remover_estadio():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('REMOVER ESTÁDIO')
    linha()

    cursor.execute('SELECT id, nome, cidade FROM estadios ORDER BY id')
    estadios = cursor.fetchall()

    if len(estadios) == 0:
        print('Nenhum estádio cadastrado.')
        cursor.close()
        conexao.close()
        pausar()
        return

    for estadio in estadios:
        print(f'[{estadio[0]}] {estadio[1]} - {estadio[2]}')

    print()

    id_estadio = ler_inteiro_obrigatorio('ID do estádio: ')

    cursor.execute('SELECT nome FROM estadios WHERE id = %s', (id_estadio,))
    estadio = cursor.fetchone()

    if estadio is None:
        print('Estádio não encontrado.')
    else:
        cursor.execute('SELECT COUNT(*) FROM partidas WHERE id_estadio = %s', (id_estadio,))
        total_partidas = cursor.fetchone()[0]

        if total_partidas > 0:
            print(f'Não é possível remover "{estadio[0]}".')
            print(f'Esse estádio possui {total_partidas} partida(s) vinculada(s).')
        else:
            print(f'Estádio: {estadio[0]}')

            confirmar = input('Confirmar remoção? (s/n): ')

            if confirmar.lower() == 's':
                cursor.execute('DELETE FROM estadios WHERE id = %s', (id_estadio,))
                conexao.commit()
                print('Estádio removido com sucesso!')
            else:
                print('Remoção cancelada.')

    cursor.close()
    conexao.close()

    pausar()

def remover_selecao():
    conexao = conectar()
    cursor = conexao.cursor()

    linha()
    print('REMOVER SELEÇÃO')
    linha()

    cursor.execute('SELECT id, nome_pais, confederacao FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    if len(selecoes) == 0:
        print('Nenhuma seleção cadastrada.')
        cursor.close()
        conexao.close()
        pausar()
        return

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]} - {selecao[2]}')

    print()

    id_selecao = ler_inteiro_obrigatorio('ID da seleção: ')

    cursor.execute('SELECT nome_pais FROM selecoes WHERE id = %s', (id_selecao,))
    selecao = cursor.fetchone()

    if selecao is None:
        print('Seleção não encontrada.')
    else:
        cursor.execute('SELECT COUNT(*) FROM jogadores WHERE id_selecao = %s', (id_selecao,))
        total_jogadores = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) FROM partidas
            WHERE id_selecao_casa = %s OR id_selecao_visitante = %s
        ''', (id_selecao, id_selecao))

        total_partidas = cursor.fetchone()[0]

        if total_jogadores > 0 or total_partidas > 0:
            print(f'Não é possível remover "{selecao[0]}".')
            print(f'Possui {total_jogadores} jogador(es) e {total_partidas} partida(s) vinculada(s).')
        else:
            print(f'Seleção: {selecao[0]}')

            confirmar = input('Confirmar remoção? (s/n): ')

            if confirmar.lower() == 's':
                cursor.execute('DELETE FROM selecoes WHERE id = %s', (id_selecao,))
                conexao.commit()
                print('Seleção removida com sucesso!')
            else:
                print('Remoção cancelada.')

    cursor.close()
    conexao.close()

    pausar()

def menu_cadastros():
    opcao = -1

    while opcao != 0:
        print()
        print('================================================')
        print('CADASTROS')
        print('================================================')
        print('1 - Cadastrar seleção')
        print('2 - Cadastrar jogador')
        print('3 - Cadastrar estádio')
        print('4 - Cadastrar partida')
        print('0 - Voltar')
        print()

        try:
            opcao = int(input('Opção: '))
        except ValueError:
            opcao = -1

        if opcao == 1:
            cadastrar_selecao()
        elif opcao == 2:
            cadastrar_jogador()
        elif opcao == 3:
            cadastrar_estadio()
        elif opcao == 4:
            cadastrar_partida()
        elif opcao == 0:
            print('Voltando ao menu principal...')
        else:
            print('Opção inválida!')

def menu_consultas():
    opcao = -1

    while opcao != 0:
        print()
        print('================================================')
        print('CONSULTAS')
        print('================================================')
        print('1  - Jogadores de uma seleção')
        print('2  - Resultados das partidas')
        print('3  - Partidas por fase')
        print('4  - Jogadores por seleção')
        print('5  - Média de gols por partida')
        print('6  - Estádios por quantidade de partidas')
        print('7  - Seleção com maior total de gols')
        print('8  - Estádios por capacidade mínima')
        print('9  - Jogadores por posição')
        print('10 - Seleções sem partidas')
        print('0  - Voltar')
        print()

        try:
            opcao = int(input('Opção: '))
        except ValueError:
            opcao = -1

        if opcao == 1:
            jogadores_por_selecao()
        elif opcao == 2:
            resultados_partidas()
        elif opcao == 3:
            partidas_por_fase()
        elif opcao == 4:
            contar_jogadores_por_selecao()
        elif opcao == 5:
            media_gols_por_partida()
        elif opcao == 6:
            estadios_por_quantidade_partidas()
        elif opcao == 7:
            selecao_mais_gols()
        elif opcao == 8:
            estadios_por_capacidade()
        elif opcao == 9:
            jogadores_por_posicao()
        elif opcao == 10:
            selecoes_sem_partidas()
        elif opcao == 0:
            print('Voltando ao menu principal...')
        else:
            print('Opção inválida!')

def menu_gerenciamento():
    opcao = -1

    while opcao != 0:
        print()
        print('================================================')
        print('GERENCIAMENTO')
        print('================================================')
        print('1 - Atualizar seleção')
        print('2 - Atualizar partida')
        print('3 - Remover jogador')
        print('4 - Remover partida')
        print('5 - Remover estádio')
        print('6 - Remover seleção')
        print('0 - Voltar')
        print()

        try:
            opcao = int(input('Opção: '))
        except ValueError:
            opcao = -1

        if opcao == 1:
            atualizar_selecao()
        elif opcao == 2:
            atualizar_partida()
        elif opcao == 3:
            remover_jogador()
        elif opcao == 4:
            remover_partida()
        elif opcao == 5:
            remover_estadio()
        elif opcao == 6:
            remover_selecao()
        elif opcao == 0:
            print('Voltando ao menu principal...')
        else:
            print('Opção inválida!')

print()
print('================================================')
print('SISTEMA COPA DO MUNDO 2026')
print('================================================')

opcao = -1

while opcao != 0:
    print()
    print('================================================')
    print('MENU PRINCIPAL')
    print('================================================')
    print('1 - Cadastros')
    print('2 - Consultas')
    print('3 - Atualizar / Remover')
    print('0 - Sair')
    print()

    try:
        opcao = int(input('Opção: '))
    except ValueError:
        opcao = -1

    if opcao == 1:
        menu_cadastros()
    elif opcao == 2:
        menu_consultas()
    elif opcao == 3:
        menu_gerenciamento()
    elif opcao == 0:
        print('Até logo!')
    else:
        print('Opção inválida!')