# ============================================================
# ETAPA 3 - Consulta de dados das tabelas
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 3 - CONSULTA DE DADOS ===')
print()

print('--- Seleções cadastradas ---')

cursor.execute('''
    SELECT id, nome_pais, confederacao, tecnico, ranking_fifa
    FROM selecoes
    ORDER BY nome_pais
    ''')

selecoes = cursor.fetchall()

if len(selecoes) == 0:
    print('Nenhuma seleção cadastrada.')
else:
    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]} | {selecao[2]} | Técnico: {selecao[3]} | Ranking: {selecao[4]}')

print()

print('--- Buscar seleções por confederação ---')

confederacao = input('Confederação: ')

cursor.execute('''
    SELECT id, nome_pais, confederacao
    FROM selecoes
    WHERE confederacao = %s
    ORDER BY nome_pais
    ''', (confederacao,))

resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhuma seleção encontrada para essa confederação.')
else:
    for selecao in resultados:
        print(f'[{selecao[0]}] {selecao[1]} - {selecao[2]}')

print()

print('--- Buscar jogadores por posição ---')

posicao = input('Posição: ')

cursor.execute('''
    SELECT id, nome, posicao, numero_camisa, clube_origem
    FROM jogadores
    WHERE posicao LIKE %s
    ORDER BY nome
    ''', (f'%{posicao}%',))

jogadores = cursor.fetchall()

if len(jogadores) == 0:
    print('Nenhum jogador encontrado para essa posição.')
else:
    for jogador in jogadores:
        print(f'[{jogador[0]}] {jogador[1]} | {jogador[2]} | Camisa: {jogador[3]} | Clube: {jogador[4]}')

print()

print('--- Buscar estádios por capacidade mínima ---')

try:
    capacidade = int(input('Capacidade mínima: '))
except ValueError:
    print('Valor inválido. Usando 0 como padrão.')
    capacidade = 0

cursor.execute('''
    SELECT id, nome, cidade, pais_sede, capacidade
    FROM estadios
    WHERE capacidade >= %s
    ORDER BY capacidade DESC
    ''', (capacidade,))

estadios = cursor.fetchall()

if len(estadios) == 0:
    print('Nenhum estádio encontrado com essa capacidade.')
else:
    for estadio in estadios:
        print(f'[{estadio[0]}] {estadio[1]} | {estadio[2]}, {estadio[3]} | Capacidade: {estadio[4]}')

print()

print('--- Buscar partidas por fase ---')

fase = input('Fase: ')

cursor.execute('''
    SELECT id, data_jogo, fase, gols_casa, gols_visitante
    FROM partidas
    WHERE fase LIKE %s
    ORDER BY data_jogo
    ''', (f'%{fase}%',))

partidas = cursor.fetchall()

if len(partidas) == 0:
    print('Nenhuma partida encontrada para essa fase.')
else:
    for partida in partidas:
        print(f'[{partida[0]}] {partida[1]} | {partida[2]} | Placar: {partida[3]} x {partida[4]}')

cursor.close()
conexao.close()

print()
print('Etapa 3 concluída com sucesso!')