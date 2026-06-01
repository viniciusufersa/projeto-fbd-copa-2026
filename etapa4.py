# ============================================================
# ETAPA 4 - Atualização de registros existentes
# ============================================================

import mysql.connector

# Essa conexão acessa o banco copa2026, onde já existem as tabelas
# e os registros cadastrados nas etapas anteriores.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 4 - ATUALIZAÇÃO DE REGISTROS ===')
print()

# ============================================================
# ATUALIZAÇÃO DE SELEÇÃO
# ============================================================

# Primeiro o sistema mostra as seleções cadastradas.
# Isso vai ajudar o usuário a visualizar os IDs antes de escolher 
# qual registro será alterado.
print('--- Seleções cadastradas ---')

cursor.execute('SELECT id, nome_pais, tecnico, ranking_fifa FROM selecoes ORDER BY id')

for selecao in cursor.fetchall():
    print(f'[{selecao[0]}] {selecao[1]} | Técnico: {selecao[2]} | Ranking: {selecao[3]}')

print()

# O usuário informa o ID da seleção que deseja atualizar.
# Se pressionar ENTER, essa parte é pulada sem alterar nenhum registro.
id_selecao = input('ID da seleção para atualizar (ENTER para pular): ')

if id_selecao.strip() == '':
    print('Nenhuma seleção atualizada.')
else:
    # Como o ID precisa ser numérico, o programa tenta converter o valor para inteiro.
    # Se o usuário digitar algo inválido, o sistema informa o erro e não faz a atualização.
    try:
        id_selecao = int(id_selecao)
    except ValueError:
        print('ID inválido.')
        id_selecao = None

    if id_selecao is not None:
        # Antes de atualizar, o sistema busca a seleção pelo ID informado.
        # Isso evita tentar alterar um registro que não existe.
        cursor.execute(
            'SELECT nome_pais, tecnico, ranking_fifa FROM selecoes WHERE id = %s',
            (id_selecao,)
        )

        selecao = cursor.fetchone()

        if selecao is None:
            print('Seleção não encontrada.')
        else:
            print(f'Seleção: {selecao[0]}')

            # Se o usuário pressionar ENTER, o técnico atual será mantido.
            novo_tecnico = input(f'Novo técnico [{selecao[1]}]: ')

            if novo_tecnico.strip() == '':
                novo_tecnico = selecao[1]

            # O ranking também pode ser mantido com ENTER.
            # Se for digitado um novo valor, ele precisa ser convertido para inteiro.
            novo_ranking = input(f'Novo ranking FIFA [{selecao[2]}]: ')

            if novo_ranking.strip() == '':
                novo_ranking = selecao[2]
            else:
                try:
                    novo_ranking = int(novo_ranking)
                except ValueError:
                    print('Ranking inválido. Mantendo o valor atual.')
                    novo_ranking = selecao[2]

            # O UPDATE altera somente a seleção escolhida.
            # O WHERE id = %s é essencial para evitar alterar todos os registros da tabela.
            cursor.execute('''
                UPDATE selecoes
                SET tecnico = %s, ranking_fifa = %s
                WHERE id = %s
            ''', (novo_tecnico, novo_ranking, id_selecao))

            conexao.commit()

            print('Seleção atualizada com sucesso!')

print()

# ============================================================
# ATUALIZAÇÃO DE JOGADOR
# ============================================================

# Aqui o sistema lista os jogadores cadastrados para que o usuário escolha
# qual jogador deseja atualizar.
print('--- Jogadores cadastrados ---')

cursor.execute('SELECT id, nome, posicao, numero_camisa FROM jogadores ORDER BY id')

for jogador in cursor.fetchall():
    print(f'[{jogador[0]}] {jogador[1]} | {jogador[2]} | Camisa: {jogador[3]}')

print()

# O usuário informa o ID do jogador.
# Se deixar vazio, o programa não altera nenhum jogador.
id_jogador = input('ID do jogador para atualizar (ENTER para pular): ')

if id_jogador.strip() == '':
    print('Nenhum jogador atualizado.')
else:
    try:
        id_jogador = int(id_jogador)
    except ValueError:
        print('ID inválido.')
        id_jogador = None

    if id_jogador is not None:
        # O jogador é buscado pelo ID antes da alteração.
        # Desse jeito, o programa confirma se o registro realmente existe.
        cursor.execute(
            'SELECT nome, posicao, numero_camisa FROM jogadores WHERE id = %s',
            (id_jogador,)
        )

        jogador = cursor.fetchone()

        if jogador is None:
            print('Jogador não encontrado.')
        else:
            print(f'Jogador: {jogador[0]}')

            # A posição pode ser alterada ou mantida.
            # Pressionar ENTER mantém o valor atual.
            nova_posicao = input(f'Nova posição [{jogador[1]}]: ')

            if nova_posicao.strip() == '':
                nova_posicao = jogador[1]

            # O número da camisa é um campo numérico.
            # Se o usuário digitar um valor inválido, o programa mantém o valor anterior.
            nova_camisa = input(f'Novo número de camisa [{jogador[2]}]: ')

            if nova_camisa.strip() == '':
                nova_camisa = jogador[2]
            else:
                try:
                    nova_camisa = int(nova_camisa)
                except ValueError:
                    print('Número inválido. Mantendo o valor atual.')
                    nova_camisa = jogador[2]

            # O UPDATE altera a posição e o número da camisa apenas do jogador escolhido.
            cursor.execute('''
                UPDATE jogadores
                SET posicao = %s, numero_camisa = %s
                WHERE id = %s
            ''', (nova_posicao, nova_camisa, id_jogador))

            conexao.commit()

            print('Jogador atualizado com sucesso!')

print()

# ============================================================
# ATUALIZAÇÃO DE ESTÁDIO
# ============================================================

# Nessa parte, o sistema mostra os estádios cadastrados.
# A atualização será feita a partir do ID escolhido pelo usuário.
print('--- Estádios cadastrados ---')

cursor.execute('SELECT id, nome, cidade, capacidade FROM estadios ORDER BY id')

for estadio in cursor.fetchall():
    print(f'[{estadio[0]}] {estadio[1]} | {estadio[2]} | Capacidade: {estadio[3]}')

print()

id_estadio = input('ID do estádio para atualizar (ENTER para pular): ')

if id_estadio.strip() == '':
    print('Nenhum estádio atualizado.')
else:
    try:
        id_estadio = int(id_estadio)
    except ValueError:
        print('ID inválido.')
        id_estadio = None

    if id_estadio is not None:
        # Antes de alterar a capacidade, o sistema verifica se o estádio existe.
        cursor.execute(
            'SELECT nome, capacidade FROM estadios WHERE id = %s',
            (id_estadio,)
        )

        estadio = cursor.fetchone()

        if estadio is None:
            print('Estádio não encontrado.')
        else:
            print(f'Estádio: {estadio[0]}')

            # A capacidade pode ser mantida com ENTER.
            # Caso seja digitada, precisa ser um número inteiro.
            nova_capacidade = input(f'Nova capacidade [{estadio[1]}]: ')

            if nova_capacidade.strip() == '':
                nova_capacidade = estadio[1]
            else:
                try:
                    nova_capacidade = int(nova_capacidade)
                except ValueError:
                    print('Capacidade inválida. Mantendo o valor atual.')
                    nova_capacidade = estadio[1]
            
            # O UPDATE altera somente a capacidade do estádio escolhido.
            cursor.execute('''
                UPDATE estadios
                SET capacidade = %s
                WHERE id = %s
            ''', (nova_capacidade, id_estadio))

            conexao.commit()

            print('Estádio atualizado com sucesso!')

print()

# ============================================================
# ATUALIZAÇÃO DE PARTIDA
# ============================================================

# Por fim, o sistema lista as partidas cadastradas.
# Aqui é possível atualizar data, fase e placar da partida.
print('--- Partidas cadastradas ---')

cursor.execute('SELECT id, data_jogo, fase, gols_casa, gols_visitante FROM partidas ORDER BY id')

for partida in cursor.fetchall():
    print(f'[{partida[0]}] {partida[1]} | {partida[2]} | Placar: {partida[3]} x {partida[4]}')

print()

id_partida = input('ID da partida para atualizar (ENTER para pular): ')

if id_partida.strip() == '':
    print('Nenhuma partida atualizada.')
else:
    try:
        id_partida = int(id_partida)
    except ValueError:
        print('ID inválido.')
        id_partida = None

    if id_partida is not None:
        # A partida é buscada pelo ID para garantir que o registro existe
        # antes de qualquer alteração.
        cursor.execute(
            'SELECT data_jogo, fase, gols_casa, gols_visitante FROM partidas WHERE id = %s',
            (id_partida,)
        )

        partida = cursor.fetchone()

        if partida is None:
            print('Partida não encontrada.')
        else:
            print(f'Partida: {partida[0]} - {partida[1]}')

            # A data pode ser alterada ou mantida.
            # Se o usuário pressionar ENTER, o valor atual permanece.
            nova_data = input(f'Nova data [{partida[0]}]: ')

            if nova_data.strip() == '':
                nova_data = partida[0]

            # A fase segue a mesma lógica: pode ser atualizada ou mantida.
            nova_fase = input(f'Nova fase [{partida[1]}]: ')

            if nova_fase.strip() == '':
                nova_fase = partida[1]

            # Os gols da seleção mandante são numéricos.
            # Se o usuário digitar um valor inválido, o placar atual será mantido.
            novos_gols_casa = input(f'Gols mandante [{partida[2]}]: ')

            if novos_gols_casa.strip() == '':
                novos_gols_casa = partida[2]
            else:
                try:
                    novos_gols_casa = int(novos_gols_casa)
                except ValueError:
                    print('Valor inválido. Mantendo o valor atual.')
                    novos_gols_casa = partida[2]

            # A mesma validação é feita para os gols da seleção visitante.
            novos_gols_visitante = input(f'Gols visitante [{partida[3]}]: ')

            if novos_gols_visitante.strip() == '':
                novos_gols_visitante = partida[3]
            else:
                try:
                    novos_gols_visitante = int(novos_gols_visitante)
                except ValueError:
                    print('Valor inválido. Mantendo o valor atual.')
                    novos_gols_visitante = partida[3]

            # Esse UPDATE altera data, fase e placar da partida escolhida.
            # Mais uma vez, o WHERE garante que apenas o registro selecionado será atualizado.
            cursor.execute('''
                UPDATE partidas
                SET data_jogo = %s, fase = %s, gols_casa = %s, gols_visitante = %s
                WHERE id = %s
            ''', (nova_data, nova_fase, novos_gols_casa, novos_gols_visitante, id_partida))

            conexao.commit()

            print('Partida atualizada com sucesso!')

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 4 concluída com sucesso!')