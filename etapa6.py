# ============================================================
# ETAPA 6 - Relacionamentos entre tabelas
# ============================================================

import mysql.connector

# Esta etapa deve ser executada apenas uma vez,
# pois as chaves estrangeiras não podem ser criadas novamente com o mesmo nome.

# Conectando ao banco de dados criado na Etapa 1
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026'
)

cursor = conexao.cursor()

print('=== ETAPA 6 - RELACIONAMENTOS ENTRE TABELAS ===')
print()

comando_sql = '''
    ALTER TABLE jogadores
    ADD CONSTRAINT fk_jogadores_selecoes
    FOREIGN KEY (id_selecao) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento jogadores -> seleções criado com sucesso!')

comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_selecao_casa
    FOREIGN KEY (id_selecao_casa) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> seleção mandante criado com sucesso!')

comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_selecao_visitante
    FOREIGN KEY (id_selecao_visitante) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> seleção visitante criado com sucesso!')

comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_estadios
    FOREIGN KEY (id_estadio) REFERENCES estadios(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> estádios criado com sucesso!')

cursor.close()
conexao.close()

print()
print('Etapa 6 executada com sucesso!')