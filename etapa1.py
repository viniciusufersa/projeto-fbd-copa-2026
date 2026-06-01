# ============================================================
# ETAPA 1 - Criação do banco de dados e das tabelas
# ============================================================

import mysql.connector

# A conexão aqui é feita sem informar um banco de dados,
# porque o banco ainda não existe nesse momento.
# Primeiro precisamos criá-lo, e só depois podemos usá-lo.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    use_pure=True
)

cursor = conexao.cursor()

# O comando IF NOT EXISTS garante que o banco só será criado
# se ele ainda não existir. Assim, não dá erro se rodar o arquivo mais de uma vez.
cursor.execute("CREATE DATABASE IF NOT EXISTS copa2026")
print("Banco de dados copa2026 criado com sucesso!")

# Depois de criar o banco, o USE diz para o MySQL que todas as próximas
# operações devem acontecer dentro do banco copa2026.
cursor.execute("USE copa2026")

# Essa tabela armazena as seleções participantes.
# A chave primária id identifica cada seleção de forma única.
comando_sql = '''
CREATE TABLE IF NOT EXISTS selecoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_pais VARCHAR(100) NOT NULL,
    confederacao VARCHAR(50) NOT NULL,
    tecnico VARCHAR(100),
    ranking_fifa INT
    )'''
cursor.execute(comando_sql)
print("Tabela selecoes criada com sucesso!")

# Essa tabela armazena os jogadores cadastrados no sistema.
# O campo id_selecao será usado depois para relacionar cada jogador
# com a seleção à qual ele pertence.
comando_sql = '''
CREATE TABLE IF NOT EXISTS jogadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    posicao VARCHAR(50) NOT NULL,
    idade INT,
    numero_camisa INT,
    clube_origem VARCHAR(100),
    id_selecao INT
    )'''
cursor.execute(comando_sql)
print("Tabela jogadores criada com sucesso!")

# Essa tabela armazena os estádios onde as partidas podem acontecer.
# A capacidade foi definida como número inteiro,
# pois representa uma quantidade de pessoas.
comando_sql = '''
CREATE TABLE IF NOT EXISTS estadios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    pais_sede VARCHAR(100),
    capacidade INT
    )'''
cursor.execute(comando_sql)
print("Tabela estadios criada com sucesso!")

# Essa tabela guarda as partidas da competição.
# data_jogo e fase são obrigatórios porque toda partida precisa ter quando e em que etapa.
# Os gols podem ficar vazios, já que a partida pode ser cadastrada antes de acontecer.
# Os campos id_selecao_casa, id_selecao_visitante e id_estadio também serão
# transformados em chaves estrangeiras na etapa 6.
comando_sql = '''
CREATE TABLE IF NOT EXISTS partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_jogo DATE NOT NULL,
    fase VARCHAR(50) NOT NULL,
    gols_casa INT,
    gols_visitante INT,
    id_selecao_casa INT,
    id_selecao_visitante INT,
    id_estadio INT
    )'''
cursor.execute(comando_sql)
print("Tabela partidas criada com sucesso!")

print()
print("--- TABELAS DO BANCO copa2026 ---")

# Essa consulta final serve apenas para verificar se as tabelas
# foram realmente criadas no banco de dados.
cursor.execute("SHOW TABLES")

for tabela in cursor:
    print(f"Tabela encontrada: {tabela[0]}")

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print("Etapa 1 executada com sucesso!")