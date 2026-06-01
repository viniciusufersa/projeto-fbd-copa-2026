# ============================================================
# ETAPA 4 - Atualização de registros existentes
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 4 - ATUALIZAÇÃO DE REGISTROS ===')
print()

print('--- Seleções cadastradas ---')

cursor.execute('SELECT id, nome_pais, tecnico, ranking_fifa FROM selecoes ORDER BY id')

for selecao in cursor.fetchall():
    print(f'[{selecao[0]}] {selecao[1]} | Técnico: {selecao[2]} | Ranking: {selecao[3]}')

print()

id_selecao = input('ID da seleção para atualizar (ENTER para pular): ')

if id_selecao.strip() == '':
    print('Nenhuma seleção atualizada.')
else:
    try:
        id_selecao = int(id_selecao)
    except ValueError:
        print('ID inválido.')
        id_selecao = None

    if id_selecao is not None:
        cursor.execute(
            'SELECT nome_pais, tecnico, ranking_fifa FROM selecoes WHERE id = %s',
            (id_selecao,)
        )

        selecao = cursor.fetchone()

        if selecao is None:
            print('Seleção não encontrada.')
        else:
            print(f'Seleção: {selecao[0]}')

            novo_tecnico = input(f'Novo técnico [{selecao[1]}]: ')

            if novo_tecnico.strip() == '':
                novo_tecnico = selecao[1]

            novo_ranking = input(f'Novo ranking FIFA [{selecao[2]}]: ')

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

print()

print('--- Jogadores cadastrados ---')

cursor.execute('SELECT id, nome, posicao, numero_camisa FROM jogadores ORDER BY id')

for jogador in cursor.fetchall():
    print(f'[{jogador[0]}] {jogador[1]} | {jogador[2]} | Camisa: {jogador[3]}')

print()

id_jogador = input('ID do jogador para atualizar (ENTER para pular): ')

if id_jogador.strip() == '':
    print('Nenhum jogador atualizado.')
else:
    try:
        id_jogador = int(id_jogador)
    except ValueError:
        print('ID inválido.')
        id_jogador = None

    if id_jogador is not None:
        cursor.execute(
            'SELECT nome, posicao, numero_camisa FROM jogadores WHERE id = %s',
            (id_jogador,)
        )

        jogador = cursor.fetchone()

        if jogador is None:
            print('Jogador não encontrado.')
        else:
            print(f'Jogador: {jogador[0]}')

            nova_posicao = input(f'Nova posição [{jogador[1]}]: ')

            if nova_posicao.strip() == '':
                nova_posicao = jogador[1]

            nova_camisa = input(f'Novo número de camisa [{jogador[2]}]: ')

            if nova_camisa.strip() == '':
                nova_camisa = jogador[2]
            else:
                try:
                    nova_camisa = int(nova_camisa)
                except ValueError:
                    print('Número inválido. Mantendo o valor atual.')
                    nova_camisa = jogador[2]

            cursor.execute('''
                UPDATE jogadores
                SET posicao = %s, numero_camisa = %s
                WHERE id = %s
            ''', (nova_posicao, nova_camisa, id_jogador))

            conexao.commit()

            print('Jogador atualizado com sucesso!')

print()

print('--- Estádios cadastrados ---')

cursor.execute('SELECT id, nome, cidade, capacidade FROM estadios ORDER BY id')

for estadio in cursor.fetchall():
    print(f'[{estadio[0]}] {estadio[1]} | {estadio[2]} | Capacidade: {estadio[3]}')

print()

id_estadio = input('ID do estádio para atualizar (ENTER para pular): ')

if id_estadio.strip() == '':
    print('Nenhum estádio atualizado.')
else:
    try:
        id_estadio = int(id_estadio)
    except ValueError:
        print('ID inválido.')
        id_estadio = None

    if id_estadio is not None:
        cursor.execute(
            'SELECT nome, capacidade FROM estadios WHERE id = %s',
            (id_estadio,)
        )

        estadio = cursor.fetchone()

        if estadio is None:
            print('Estádio não encontrado.')
        else:
            print(f'Estádio: {estadio[0]}')

            nova_capacidade = input(f'Nova capacidade [{estadio[1]}]: ')

            if nova_capacidade.strip() == '':
                nova_capacidade = estadio[1]
            else:
                try:
                    nova_capacidade = int(nova_capacidade)
                except ValueError:
                    print('Capacidade inválida. Mantendo o valor atual.')
                    nova_capacidade = estadio[1]

            cursor.execute('''
                UPDATE estadios
                SET capacidade = %s
                WHERE id = %s
            ''', (nova_capacidade, id_estadio))

            conexao.commit()

            print('Estádio atualizado com sucesso!')

print()

print('--- Partidas cadastradas ---')

cursor.execute('SELECT id, data_jogo, fase, gols_casa, gols_visitante FROM partidas ORDER BY id')

for partida in cursor.fetchall():
    print(f'[{partida[0]}] {partida[1]} | {partida[2]} | Placar: {partida[3]} x {partida[4]}')

print()

id_partida = input('ID da partida para atualizar (ENTER para pular): ')

if id_partida.strip() == '':
    print('Nenhuma partida atualizada.')
else:
    try:
        id_partida = int(id_partida)
    except ValueError:
        print('ID inválido.')
        id_partida = None

    if id_partida is not None:
        cursor.execute(
            'SELECT data_jogo, fase, gols_casa, gols_visitante FROM partidas WHERE id = %s',
            (id_partida,)
        )

        partida = cursor.fetchone()

        if partida is None:
            print('Partida não encontrada.')
        else:
            print(f'Partida: {partida[0]} - {partida[1]}')

            nova_data = input(f'Nova data [{partida[0]}]: ')

            if nova_data.strip() == '':
                nova_data = partida[0]

            nova_fase = input(f'Nova fase [{partida[1]}]: ')

            if nova_fase.strip() == '':
                nova_fase = partida[1]

            novos_gols_casa = input(f'Gols mandante [{partida[2]}]: ')

            if novos_gols_casa.strip() == '':
                novos_gols_casa = partida[2]
            else:
                try:
                    novos_gols_casa = int(novos_gols_casa)
                except ValueError:
                    print('Valor inválido. Mantendo o valor atual.')
                    novos_gols_casa = partida[2]

            novos_gols_visitante = input(f'Gols visitante [{partida[3]}]: ')

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

print()
print('Etapa 4 concluída com sucesso!')