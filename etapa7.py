# ============================================================
# ETAPA 7 - Consultas com JOIN entre tabelas relacionadas
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 7 - CONSULTAS COM JOIN ===')
print()

print('--- Jogadores com suas seleções ---')

sql = '''
    SELECT jogadores.nome, jogadores.posicao, selecoes.nome_pais
    FROM jogadores
    INNER JOIN selecoes ON jogadores.id_selecao = selecoes.id
    ORDER BY selecoes.nome_pais, jogadores.nome
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhum jogador encontrado.')
else:
    for linha in resultados:
        print(f'Jogador: {linha[0]} - Posição: {linha[1]} - Seleção: {linha[2]}')

print()

print('--- Partidas com seleções e estádios ---')

sql = '''
    SELECT partidas.data_jogo, partidas.fase,
        casa.nome_pais, partidas.gols_casa,
        visitante.nome_pais, partidas.gols_visitante,
        estadios.nome
    FROM partidas
    INNER JOIN selecoes AS casa ON partidas.id_selecao_casa = casa.id
    INNER JOIN selecoes AS visitante ON partidas.id_selecao_visitante = visitante.id
    INNER JOIN estadios ON partidas.id_estadio = estadios.id
    ORDER BY partidas.data_jogo
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhuma partida encontrada.')
else:
    for linha in resultados:
        print(f'{linha[0]} - {linha[1]}')
        print(f'{linha[2]} {linha[3]} x {linha[5]} {linha[4]}')
        print(f'Estádio: {linha[6]}')
        print()

print('--- Seleções e seus jogadores ---')

sql = '''
    SELECT selecoes.nome_pais, jogadores.nome, jogadores.posicao
    FROM selecoes
    LEFT JOIN jogadores ON selecoes.id = jogadores.id_selecao
    ORDER BY selecoes.nome_pais, jogadores.nome
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhum resultado encontrado.')
else:
    for linha in resultados:
        if linha[1] is None:
            print(f'Seleção: {linha[0]} - Jogador: Nenhum jogador cadastrado')
        else:
            print(f'Seleção: {linha[0]} - Jogador: {linha[1]} - Posição: {linha[2]}')

print()

print('--- Estádios e partidas ---')

sql = '''
    SELECT estadios.nome, estadios.cidade, partidas.data_jogo, partidas.fase
    FROM estadios
    LEFT JOIN partidas ON estadios.id = partidas.id_estadio
    ORDER BY estadios.nome, partidas.data_jogo
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhum resultado encontrado.')
else:
    for linha in resultados:
        if linha[2] is None:
            print(f'Estádio: {linha[0]} - Cidade: {linha[1]} - Nenhuma partida cadastrada')
        else:
            print(f'Estádio: {linha[0]} - Cidade: {linha[1]} - Data: {linha[2]} - Fase: {linha[3]}')

cursor.close()
conexao.close()

print()
print('Etapa 7 executada com sucesso!')