# ============================================================
# ETAPA 5 - Remoção de registros
# ============================================================

import mysql.connector

# Conectando ao banco de dados criado na Etapa 1
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

opcao = -1

while opcao != 0:
    print()
    print('=== ETAPA 5 - REMOÇÃO DE REGISTROS ===')
    print('1 - Remover jogador')
    print('2 - Remover partida')
    print('3 - Remover estádio')
    print('4 - Remover seleção')
    print('0 - Sair')
    print()

    try:
        opcao = int(input('Escolha uma opção: '))
    except ValueError:
        print('Opção inválida!')
        opcao = -1

    if opcao == 1:
        print()
        print('--- Jogadores cadastrados ---')

        cursor.execute('SELECT id, nome, posicao FROM jogadores ORDER BY id')
        jogadores = cursor.fetchall()

        if len(jogadores) == 0:
            print('Nenhum jogador cadastrado.')
        else:
            for jogador in jogadores:
                print(f'[{jogador[0]}] {jogador[1]} - {jogador[2]}')

            print()

            id_jogador = input('ID do jogador para remover: ')

            try:
                id_jogador = int(id_jogador)
            except ValueError:
                print('ID inválido.')
                id_jogador = None

            if id_jogador is not None:
                cursor.execute('SELECT nome, posicao FROM jogadores WHERE id = %s', (id_jogador,))
                jogador = cursor.fetchone()

                if jogador is None:
                    print('Jogador não encontrado.')
                else:
                    print(f'Jogador selecionado: {jogador[0]} - {jogador[1]}')

                    confirmar = input('Confirmar remoção? (s/n): ')

                    if confirmar.lower() == 's':
                        sql = '''
                        DELETE FROM jogadores
                        WHERE id = %s
                        '''

                        cursor.execute(sql, (id_jogador,))
                        conexao.commit()

                        print('Jogador removido com sucesso!')
                    else:
                        print('Remoção cancelada.')

    elif opcao == 2:
        print()
        print('--- Partidas cadastradas ---')

        cursor.execute('SELECT id, data_jogo, fase, gols_casa, gols_visitante FROM partidas ORDER BY id')
        partidas = cursor.fetchall()

        if len(partidas) == 0:
            print('Nenhuma partida cadastrada.')
        else:
            for partida in partidas:
                print(f'[{partida[0]}] {partida[1]} - {partida[2]} - Placar: {partida[3]} x {partida[4]}')

            print()

            id_partida = input('ID da partida para remover: ')

            try:
                id_partida = int(id_partida)
            except ValueError:
                print('ID inválido.')
                id_partida = None

            if id_partida is not None:
                cursor.execute('SELECT data_jogo, fase FROM partidas WHERE id = %s', (id_partida,))
                partida = cursor.fetchone()

                if partida is None:
                    print('Partida não encontrada.')
                else:
                    print(f'Partida selecionada: {partida[0]} - {partida[1]}')

                    confirmar = input('Confirmar remoção? (s/n): ')

                    if confirmar.lower() == 's':
                        sql = '''
                        DELETE FROM partidas
                        WHERE id = %s
                        '''

                        cursor.execute(sql, (id_partida,))
                        conexao.commit()

                        print('Partida removida com sucesso!')
                    else:
                        print('Remoção cancelada.')

    elif opcao == 3:
        print()
        print('--- Estádios cadastrados ---')

        cursor.execute('SELECT id, nome, cidade FROM estadios ORDER BY id')
        estadios = cursor.fetchall()

        if len(estadios) == 0:
            print('Nenhum estádio cadastrado.')
        else:
            for estadio in estadios:
                print(f'[{estadio[0]}] {estadio[1]} - {estadio[2]}')

            print()

            id_estadio = input('ID do estádio para remover: ')

            try:
                id_estadio = int(id_estadio)
            except ValueError:
                print('ID inválido.')
                id_estadio = None

            if id_estadio is not None:
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
                        print(f'Estádio selecionado: {estadio[0]}')

                        confirmar = input('Confirmar remoção? (s/n): ')

                        if confirmar.lower() == 's':
                            sql = '''
                            DELETE FROM estadios
                            WHERE id = %s
                            '''

                            cursor.execute(sql, (id_estadio,))
                            conexao.commit()

                            print('Estádio removido com sucesso!')
                        else:
                            print('Remoção cancelada.')

    elif opcao == 4:
        print()
        print('--- Seleções cadastradas ---')

        cursor.execute('SELECT id, nome_pais, confederacao FROM selecoes ORDER BY id')
        selecoes = cursor.fetchall()

        if len(selecoes) == 0:
            print('Nenhuma seleção cadastrada.')
        else:
            for selecao in selecoes:
                print(f'[{selecao[0]}] {selecao[1]} - {selecao[2]}')

            print()

            id_selecao = input('ID da seleção para remover: ')

            try:
                id_selecao = int(id_selecao)
            except ValueError:
                print('ID inválido.')
                id_selecao = None

            if id_selecao is not None:
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
                        print(f'Seleção selecionada: {selecao[0]}')

                        confirmar = input('Confirmar remoção? (s/n): ')

                        if confirmar.lower() == 's':
                            sql = '''
                            DELETE FROM selecoes
                            WHERE id = %s
                            '''

                            cursor.execute(sql, (id_selecao,))
                            conexao.commit()

                            print('Seleção removida com sucesso!')
                        else:
                            print('Remoção cancelada.')

    elif opcao == 0:
        print('Saindo da Etapa 5...')

    else:
        if opcao != -1:
            print('Opção inválida!')

cursor.close()
conexao.close()

print()
print('Etapa 5 concluída com sucesso!')