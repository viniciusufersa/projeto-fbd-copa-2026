# ============================================================
# ETAPA 7 - Consultas com JOIN entre tabelas relacionadas
# ============================================================

import mysql.connector

# Essa conexão acessa o banco copa2026, que já possui as tabelas,
# os registros cadastrados e os relacionamentos criados na Etapa 6.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 7 - CONSULTAS COM JOIN ===')
print()

# Nessa consulta, o sistema mostra cada jogador junto com a seleção à qual ele pertence.
# O INNER JOIN é usado porque queremos apenas jogadores que estejam relacionados
# a uma seleção cadastrada.
print('--- Jogadores com suas seleções ---')

sql = '''
    SELECT jogadores.nome, jogadores.posicao, selecoes.nome_pais
    FROM jogadores
    INNER JOIN selecoes ON jogadores.id_selecao = selecoes.id
    ORDER BY selecoes.nome_pais, jogadores.nome
    '''

cursor.execute(sql)
resultados = cursor.fetchall()

# Se não houver resultados, o sistema informa que nenhum jogador foi encontrado.
# Caso contrário, percorre os registros e exibe jogador, posição e seleção.
if len(resultados) == 0:
    print('Nenhum jogador encontrado.')
else:
    for linha in resultados:
        print(f'Jogador: {linha[0]} - Posição: {linha[1]} - Seleção: {linha[2]}')

print()

# ============================================================
# CONSULTA DE PARTIDAS COM SELEÇÕES E ESTÁDIOS
# ============================================================

# Aqui o sistema mostra as partidas junto com os nomes das seleções e o estádio.
# Como a tabela partidas possui duas seleções, a tabela selecoes é usada duas vezes:
# uma como casa, para representar a seleção mandante, e outra como visitante.
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

# ============================================================
# CONSULTA DE SELEÇÕES E SEUS JOGADORES
# ============================================================

# Nessa parte, o LEFT JOIN mostra todas as seleções, mesmo que alguma delas
# ainda não tenha jogador cadastrado.
# Isso é diferente do INNER JOIN, que mostraria apenas os registros com correspondência.
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
        # Quando o jogador vem como None, significa que aquela seleção
        # não possui jogador relacionado na tabela jogadores.
        if linha[1] is None:
            print(f'Seleção: {linha[0]} - Jogador: Nenhum jogador cadastrado')
        else:
            print(f'Seleção: {linha[0]} - Jogador: {linha[1]} - Posição: {linha[2]}')

print()

# ============================================================
# CONSULTA DE ESTÁDIOS E PARTIDAS
# ============================================================

# Essa consulta mostra todos os estádios e as partidas vinculadas a eles.
# O LEFT JOIN foi usado para que estádios sem partidas também apareçam no resultado.
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
        # Se a data da partida vier como None, significa que aquele estádio
        # ainda não está vinculado a nenhuma partida cadastrada.
        if linha[2] is None:
            print(f'Estádio: {linha[0]} - Cidade: {linha[1]} - Nenhuma partida cadastrada')
        else:
            print(f'Estádio: {linha[0]} - Cidade: {linha[1]} - Data: {linha[2]} - Fase: {linha[3]}')

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 7 executada com sucesso!')