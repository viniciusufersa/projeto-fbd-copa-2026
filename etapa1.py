# ============================================================
# ETAPA 1 - Criação do banco de dados e das tabelas
# ============================================================

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

cursor = conexao.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS copa2026")
print("Banco de dados copa2026 criado com sucesso!")

cursor.execute("USE copa2026")

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

cursor.execute("SHOW TABLES")

for tabela in cursor:
    print(f"Tabela encontrada: {tabela[0]}")

cursor.close()
conexao.close()

print()
print("Etapa 1 executada com sucesso!")