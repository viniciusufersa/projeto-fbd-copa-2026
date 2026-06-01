# ============================================================
# ETAPA 5 - Remoção de registros
# ============================================================

import mysql.connector

# Essa conexão acessa o banco copa2026, onde já existem os registros
# cadastrados nas etapas anteriores.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

# A variável opcao começa em -1 para que o menu apareça logo na primeira vez.
# O loop continua até o usuário escolher 0.
opcao = -1

while opcao != 0:
    print()
    print('=== ETAPA 5 - REMOÇÃO DE REGISTROS ===')
    print('1 - Remover jogador')
    print('2 - Remover partida')
    print('3 - Remover estádio')
    print('4 - Remover seleção')
    print('0 - Sair')
    print()

    # A opção do menu precisa ser numérica.
    # Se o usuário digitar algo inválido, o programa mostra uma mensagem
    # e mantém o menu funcionando.
    try:
        opcao = int(input('Escolha uma opção: '))
    except ValueError:
        print('Opção inválida!')
        opcao = -1

    # ========================================================
    # REMOÇÃO DE JOGADOR
    # ========================================================

    if opcao == 1:
        print()
        print('--- Jogadores cadastrados ---')

        # Antes de remover, o sistema lista os jogadores cadastrados.
        # Isso ajuda o usuário a escolher corretamente o ID do registro.
        cursor.execute('SELECT id, nome, posicao FROM jogadores ORDER BY id')
        jogadores = cursor.fetchall()

        if len(jogadores) == 0:
            print('Nenhum jogador cadastrado.')
        else:
            for jogador in jogadores:
                print(f'[{jogador[0]}] {jogador[1]} - {jogador[2]}')

            print()

            id_jogador = input('ID do jogador para remover: ')

            # O ID precisa ser convertido para inteiro.
            # Se o usuário digitar um valor inválido, a remoção não será feita.
            try:
                id_jogador = int(id_jogador)
            except ValueError:
                print('ID inválido.')
                id_jogador = None

            if id_jogador is not None:
                # Antes do DELETE, o sistema verifica se o jogador existe.
                # Isso evita tentar remover um registro inexistente.
                cursor.execute('SELECT nome, posicao FROM jogadores WHERE id = %s', (id_jogador,))
                jogador = cursor.fetchone()

                if jogador is None:
                    print('Jogador não encontrado.')
                else:
                    print(f'Jogador selecionado: {jogador[0]} - {jogador[1]}')

                    # A confirmação evita que o usuário remova um registro por engano.
                    confirmar = input('Confirmar remoção? (s/n): ')

                    if confirmar.lower() == 's':
                        # O DELETE remove apenas o jogador escolhido.
                        # O WHERE é essencial para impedir que todos os jogadores sejam removidos.
                        sql = '''
                        DELETE FROM jogadores
                        WHERE id = %s
                        '''

                        cursor.execute(sql, (id_jogador,))
                        conexao.commit()

                        print('Jogador removido com sucesso!')
                    else:
                        print('Remoção cancelada.')
    
    # ========================================================
    # REMOÇÃO DE PARTIDA
    # ========================================================

    elif opcao == 2:
        print()
        print('--- Partidas cadastradas ---')

        # O sistema lista as partidas para que o usuário veja os IDs disponíveis
        # antes de escolher qual partida deseja remover.
        cursor.execute('SELECT id, data_jogo, fase, gols_casa, gols_visitante FROM partidas ORDER BY id')
        partidas = cursor.fetchall()

        if len(partidas) == 0:
            print('Nenhuma partida cadastrada.')
        else:
            for partida in partidas:
                print(f'[{partida[0]}] {partida[1]} - {partida[2]} - Placar: {partida[3]} x {partida[4]}')

            print()

            id_partida = input('ID da partida para remover: ')

            try:
                id_partida = int(id_partida)
            except ValueError:
                print('ID inválido.')
                id_partida = None

            if id_partida is not None:
                # A partida é buscada pelo ID para confirmar que ela realmente existe.
                cursor.execute('SELECT data_jogo, fase FROM partidas WHERE id = %s', (id_partida,))
                partida = cursor.fetchone()

                if partida is None:
                    print('Partida não encontrada.')
                else:
                    print(f'Partida selecionada: {partida[0]} - {partida[1]}')

                    confirmar = input('Confirmar remoção? (s/n): ')

                    if confirmar.lower() == 's':
                        # A partida pode ser removida diretamente,
                        # pois ela não é usada como referência em outra tabela do projeto.
                        sql = '''
                        DELETE FROM partidas
                        WHERE id = %s
                        '''

                        cursor.execute(sql, (id_partida,))
                        conexao.commit()

                        print('Partida removida com sucesso!')
                    else:
                        print('Remoção cancelada.')

    # ========================================================
    # REMOÇÃO DE ESTÁDIO
    # ========================================================

    elif opcao == 3:
        print()
        print('--- Estádios cadastrados ---')

        # O sistema mostra os estádios cadastrados para facilitar
        # a escolha do ID que será analisado para remoção.
        cursor.execute('SELECT id, nome, cidade FROM estadios ORDER BY id')
        estadios = cursor.fetchall()

        if len(estadios) == 0:
            print('Nenhum estádio cadastrado.')
        else:
            for estadio in estadios:
                print(f'[{estadio[0]}] {estadio[1]} - {estadio[2]}')

            print()

            id_estadio = input('ID do estádio para remover: ')

            try:
                id_estadio = int(id_estadio)
            except ValueError:
                print('ID inválido.')
                id_estadio = None

            if id_estadio is not None:
                # Primeiro, o sistema verifica se o estádio existe.
                cursor.execute('SELECT nome FROM estadios WHERE id = %s', (id_estadio,))
                estadio = cursor.fetchone()

                if estadio is None:
                    print('Estádio não encontrado.')
                else:
                    # Antes de remover um estádio, é necessário verificar se existem
                    # partidas vinculadas a ele. Isso evita inconsistência no banco.
                    cursor.execute('SELECT COUNT(*) FROM partidas WHERE id_estadio = %s', (id_estadio,))
                    total_partidas = cursor.fetchone()[0]

                    if total_partidas > 0:
                        print(f'Não é possível remover "{estadio[0]}".')
                        print(f'Esse estádio possui {total_partidas} partida(s) vinculada(s).')
                    else:
                        print(f'Estádio selecionado: {estadio[0]}')

                        confirmar = input('Confirmar remoção? (s/n): ')

                        if confirmar.lower() == 's':
                            # O estádio só é removido se não estiver sendo usado
                            # em nenhuma partida cadastrada.
                            sql = '''
                            DELETE FROM estadios
                            WHERE id = %s
                            '''

                            cursor.execute(sql, (id_estadio,))
                            conexao.commit()

                            print('Estádio removido com sucesso!')
                        else:
                            print('Remoção cancelada.')

    # ========================================================
    # REMOÇÃO DE SELEÇÃO
    # ========================================================

    elif opcao == 4:
        print()
        print('--- Seleções cadastradas ---')
        # O sistema lista as seleções para que o usuário escolha qual delas
        # deseja tentar remover.
        cursor.execute('SELECT id, nome_pais, confederacao FROM selecoes ORDER BY id')
        selecoes = cursor.fetchall()

        if len(selecoes) == 0:
            print('Nenhuma seleção cadastrada.')
        else:
            for selecao in selecoes:
                print(f'[{selecao[0]}] {selecao[1]} - {selecao[2]}')

            print()

            id_selecao = input('ID da seleção para remover: ')

            try:
                id_selecao = int(id_selecao)
            except ValueError:
                print('ID inválido.')
                id_selecao = None

            if id_selecao is not None:
                # Primeiro o sistema verifica se a seleção informada existe.
                cursor.execute('SELECT nome_pais FROM selecoes WHERE id = %s', (id_selecao,))
                selecao = cursor.fetchone()

                if selecao is None:
                    print('Seleção não encontrada.')
                else:
                    # Antes de remover uma seleção, o sistema verifica se existem
                    # jogadores ligados a ela.
                    cursor.execute('SELECT COUNT(*) FROM jogadores WHERE id_selecao = %s', (id_selecao,))
                    total_jogadores = cursor.fetchone()[0]

                    # Também é necessário verificar se a seleção aparece em alguma partida,
                    # seja como mandante ou como visitante.
                    cursor.execute('''
                    SELECT COUNT(*) FROM partidas
                    WHERE id_selecao_casa = %s OR id_selecao_visitante = %s
                    ''', (id_selecao, id_selecao))

                    total_partidas = cursor.fetchone()[0]

                    # Se houver jogadores ou partidas vinculadas, a seleção não deve ser removida.
                    # Isso preserva a integridade dos dados do sistema.
                    if total_jogadores > 0 or total_partidas > 0:
                        print(f'Não é possível remover "{selecao[0]}".')
                        print(f'Possui {total_jogadores} jogador(es) e {total_partidas} partida(s) vinculada(s).')
                    else:
                        print(f'Seleção selecionada: {selecao[0]}')

                        confirmar = input('Confirmar remoção? (s/n): ')

                        if confirmar.lower() == 's':
                            # A seleção só é removida se não possuir jogadores
                            # nem partidas relacionadas.
                            sql = '''
                            DELETE FROM selecoes
                            WHERE id = %s
                            '''

                            cursor.execute(sql, (id_selecao,))
                            conexao.commit()

                            print('Seleção removida com sucesso!')
                        else:
                            print('Remoção cancelada.')

    elif opcao == 0:
        print('Saindo da Etapa 5...')

    else:
        if opcao != -1:
            print('Opção inválida!')

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 5 concluída com sucesso!')