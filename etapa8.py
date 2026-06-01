# ============================================================
# ETAPA 8 - Funções de agregação
# ============================================================

import mysql.connector

# Essa conexão acessa o banco copa2026, que já possui registros cadastrados.
# Nesta etapa, o objetivo é fazer consultas resumidas usando funções de agregação.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 8 - FUNÇÕES DE AGREGAÇÃO ===')
print()

# ============================================================
# TOTAL DE JOGADORES CADASTRADOS
# ============================================================

# Nessa primeira consulta, o COUNT conta quantos jogadores existem na tabela.
# Ele é útil quando queremos saber a quantidade total de registros cadastrados.
print('--- Total de jogadores cadastrados ---')

sql = '''
    SELECT COUNT(*) 
    FROM jogadores
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

# Como essa consulta retorna apenas um valor, usamos fetchone().
# O resultado fica na posição [0] porque vem como uma tupla.
print(f'Total de jogadores: {resultado[0]}')

print()

# ============================================================
# QUANTIDADE DE JOGADORES POR SELEÇÃO
# ============================================================

# Aqui o sistema conta quantos jogadores estão ligados a cada seleção.
# O LEFT JOIN foi usado para mostrar também seleções que não possuem jogadores cadastrados.
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

# O GROUP BY agrupa os jogadores por seleção.
# Assim, o COUNT calcula a quantidade de jogadores dentro de cada grupo.
for linha in resultados:
    print(f'Seleção: {linha[0]} - Jogadores: {linha[1]}')

print()

# ============================================================
# MÉDIA DE GOLS POR PARTIDA
# ============================================================

# Nessa consulta, o sistema calcula a média de gols por partida.
# Primeiro somamos os gols da seleção mandante com os gols da visitante.
# Depois, o AVG calcula a média dessas somas.
print('--- Média de gols por partida ---')

sql = '''
    SELECT AVG(gols_casa + gols_visitante)
    FROM partidas
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

# Se não existir nenhuma partida com gols cadastrados, o resultado pode ser None.
# Nesse caso, a média é considerada 0 apenas para a exibição não ficar vazia.
if resultado[0] is None:
    media = 0
else:
    # O round deixa a média mais organizada, evitando muitas casas decimais.
    media = round(resultado[0], 2)

print(f'Média de gols por partida: {media}')

print()

# ============================================================
# TOTAL DE GOLS DO TORNEIO
# ============================================================

# Aqui o SUM soma todos os gols registrados nas partidas.
# A soma considera os gols da seleção mandante e da seleção visitante.
print('--- Total de gols do torneio ---')

sql = '''
    SELECT SUM(gols_casa + gols_visitante)
    FROM partidas
    '''

cursor.execute(sql)
resultado = cursor.fetchone()

print(f'Total de gols: {resultado[0]}')

print()

# ============================================================
# MAIOR E MENOR CAPACIDADE DOS ESTÁDIOS
# ============================================================

# Nessa consulta, o MAX busca a maior capacidade cadastrada.
# O MIN busca a menor capacidade cadastrada entre os estádios.
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

# ============================================================
# ESTÁDIOS COM MAIS DE UMA PARTIDA
# ============================================================

# Essa consulta conta quantas partidas existem em cada estádio.
# O GROUP BY agrupa as partidas por estádio, e o HAVING filtra apenas
# os estádios que possuem mais de uma partida cadastrada.
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

# Se nenhum estádio tiver mais de uma partida, o sistema informa isso.
# Caso contrário, mostra o nome do estádio e a quantidade de partidas.
if len(resultados) == 0:
    print('Nenhum estádio recebeu mais de uma partida.')
else:
    for linha in resultados:
        print(f'Estádio: {linha[0]} - Partidas: {linha[1]}')

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 8 executada com sucesso!')