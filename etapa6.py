# ============================================================
# ETAPA 6 - Relacionamentos entre tabelas
# ============================================================

import mysql.connector

# Essa etapa deve ser executada apenas uma vez.
# Como ela cria chaves estrangeiras com nomes definidos, o MySQL pode gerar erro
# se o mesmo relacionamento for criado novamente.

# Essa conexão acessa o banco copa2026, que já possui as tabelas criadas
# e os registros inseridos nas etapas anteriores.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 6 - RELACIONAMENTOS ENTRE TABELAS ===')
print()

# ============================================================
# RELACIONAMENTO ENTRE JOGADORES E SELEÇÕES
# ============================================================

# Essa parte cria uma chave estrangeira entre a tabela jogadores e a tabela selecoes.
# Com isso, cada jogador passa a ficar ligado a uma seleção existente no banco.
# O campo jogadores.id_selecao passa a referenciar o campo selecoes.id.
comando_sql = '''
    ALTER TABLE jogadores
    ADD CONSTRAINT fk_jogadores_selecoes
    FOREIGN KEY (id_selecao) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento jogadores -> seleções criado com sucesso!')

# ============================================================
# RELACIONAMENTO ENTRE PARTIDAS E SELEÇÃO MANDANTE
# ============================================================

# Essa chave estrangeira liga a seleção mandante da partida à tabela selecoes.
# Assim, o campo id_selecao_casa só pode receber o ID de uma seleção cadastrada.
comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_selecao_casa
    FOREIGN KEY (id_selecao_casa) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> seleção mandante criado com sucesso!')

# ============================================================
# RELACIONAMENTO ENTRE PARTIDAS E SELEÇÃO VISITANTE
# ============================================================

# Essa parte cria o relacionamento da seleção visitante com a tabela selecoes.
# Como uma partida tem duas seleções, foi necessário criar uma chave estrangeira
# para a seleção mandante e outra para a seleção visitante.
comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_selecao_visitante
    FOREIGN KEY (id_selecao_visitante) REFERENCES selecoes(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> seleção visitante criado com sucesso!')

# ============================================================
# RELACIONAMENTO ENTRE PARTIDAS E ESTÁDIOS
# ============================================================

# Essa chave estrangeira liga cada partida a um estádio existente.
# Dessa forma, o sistema evita cadastrar uma partida apontando para um estádio
# que não existe na tabela estadios.
comando_sql = '''
    ALTER TABLE partidas
    ADD CONSTRAINT fk_partidas_estadios
    FOREIGN KEY (id_estadio) REFERENCES estadios(id)
    '''

cursor.execute(comando_sql)

print('Relacionamento partidas -> estádios criado com sucesso!')

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 6 executada com sucesso!')