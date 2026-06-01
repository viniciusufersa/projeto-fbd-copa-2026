# ============================================================
# ETAPA 8 - Funções de agregação
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 8 - FUNÇÕES DE AGREGAÇÃO ===')
print()

print('--- Total de jogadores cadastrados ---')

sql = '''
    SELECT COUNT(*) 
    FROM jogadores
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

print(f'Total de jogadores: {resultado[0]}')
print()
print('--- Quantidade de jogadores por seleção ---')

sql = '''
    SELECT selecoes.nome_pais, COUNT(jogadores.id)
    FROM selecoes
    LEFT JOIN jogadores ON selecoes.id = jogadores.id_selecao
    GROUP BY selecoes.id, selecoes.nome_pais
    ORDER BY selecoes.nome_pais
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

for linha in resultados:
    print(f'Seleção: {linha[0]} - Jogadores: {linha[1]}')

print()
print('--- Média de gols por partida ---')

sql = '''
    SELECT AVG(gols_casa + gols_visitante)
    FROM partidas
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

if resultado[0] is None:
    media = 0
else:
    media = round(resultado[0], 2)

print(f'Média de gols por partida: {media}')
print()
print('--- Total de gols do torneio ---')

sql = '''
    SELECT SUM(gols_casa + gols_visitante)
    FROM partidas
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

print(f'Total de gols: {resultado[0]}')
print()
print('--- Maior e menor capacidade dos estádios ---')

sql = '''
    SELECT MAX(capacidade), MIN(capacidade)
    FROM estadios
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

print(f'Maior capacidade: {resultado[0]}')
print(f'Menor capacidade: {resultado[1]}')

print()

print('--- Estádios com mais de uma partida ---')

sql = '''
    SELECT estadios.nome, COUNT(partidas.id)
    FROM estadios
    LEFT JOIN partidas ON estadios.id = partidas.id_estadio
    GROUP BY estadios.id, estadios.nome
    HAVING COUNT(partidas.id) > 1
    ORDER BY COUNT(partidas.id) DESC
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

if len(resultados) == 0:
    print('Nenhum estádio recebeu mais de uma partida.')
else:
    for linha in resultados:
        print(f'Estádio: {linha[0]} - Partidas: {linha[1]}')

cursor.close()
conexao.close()

print()
print('Etapa 8 executada com sucesso!')