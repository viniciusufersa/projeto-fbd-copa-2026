# ============================================================
# ETAPA 3 - Consulta de dados das tabelas
# ============================================================

import mysql.connector

# Essa conexão já acessa o banco copa2026 diretamente,
# porque ele foi criado na Etapa 1 e preenchido na Etapa 2.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 3 - CONSULTA DE DADOS ===')
print()

# ============================================================
# CONSULTA GERAL DAS SELEÇÕES
# ============================================================

# Nessa primeira consulta, o sistema mostra todas as seleções cadastradas.
# O ORDER BY organiza os resultados em ordem alfabética pelo nome do país.
print('--- Seleções cadastradas ---')

cursor.execute('''
    SELECT id, nome_pais, confederacao, tecnico, ranking_fifa
    FROM selecoes
    ORDER BY nome_pais
    ''')

# O fetchall() busca todos os registros retornados pela consulta.
selecoes = cursor.fetchall()

# Se a lista vier vazia, significa que ainda não há seleções cadastradas.
if len(selecoes) == 0:
    print('Nenhuma seleção cadastrada.')
else:
    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]} | {selecao[2]} | Técnico: {selecao[3]} | Ranking: {selecao[4]}')

print()

# ============================================================
# CONSULTA DE SELEÇÕES POR CONFEDERAÇÃO
# ============================================================

# Aqui o usuário informa uma confederação, e o sistema busca somente
# as seleções que pertencem a ela.
print('--- Buscar seleções por confederação ---')

confederacao = input('Confederação: ')

# O WHERE filtra os registros de acordo com a confederação digitada.
# O %s recebe o valor informado pelo usuário de forma parametrizada.
cursor.execute('''
    SELECT id, nome_pais, confederacao
    FROM selecoes
    WHERE confederacao = %s
    ORDER BY nome_pais
    ''', (confederacao,))

resultados = cursor.fetchall()

# Se nenhum registro corresponder ao filtro, o sistema informa que não encontrou resultados.
if len(resultados) == 0:
    print('Nenhuma seleção encontrada para essa confederação.')
else:
    for selecao in resultados:
        print(f'[{selecao[0]}] {selecao[1]} - {selecao[2]}')

print()

# ============================================================
# CONSULTA DE JOGADORES POR POSIÇÃO
# ============================================================

# Nessa parte, o sistema busca jogadores pela posição informada.
# A busca aceita parte do texto, o que deixa a consulta mais flexível.
print('--- Buscar jogadores por posição ---')

posicao = input('Posição: ')

# O LIKE permite fazer uma busca aproximada.
# Os símbolos % antes e depois do texto fazem o MySQL procurar o conteúdo em qualquer parte do campo.
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

# ============================================================
# CONSULTA DE ESTÁDIOS POR CAPACIDADE MÍNIMA
# ============================================================

# Aqui o usuário informa uma capacidade mínima.
# O sistema retorna os estádios com capacidade igual ou superior ao valor informado.
print('--- Buscar estádios por capacidade mínima ---')

# Como capacidade é um número, o programa tenta converter a entrada para inteiro.
# Se o usuário digitar um valor inválido, o sistema usa 0 como padrão para 
# não interromper a execução.
try:
    capacidade = int(input('Capacidade mínima: '))
except ValueError:
    print('Valor inválido. Usando 0 como padrão.')
    capacidade = 0

# O WHERE com >= filtra os estádios que atendem à capacidade mínima.
# O ORDER BY capacidade DESC mostra primeiro os estádios com maior capacidade.
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

# ============================================================
# CONSULTA DE PARTIDAS POR FASE
# ============================================================

# Nessa última consulta, o usuário informa uma fase da competição.
# O sistema busca as partidas correspondentes a essa fase.
print('--- Buscar partidas por fase ---')

fase = input('Fase: ')

# O LIKE permite buscar por parte do nome da fase.
# Assim, se o usuário digitar apenas "grupos", o sistema pode encontrar "Fase de grupos".
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

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 3 concluída com sucesso!')