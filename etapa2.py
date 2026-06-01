# ============================================================
# ETAPA 2 - Inserção de registros nas tabelas
# ============================================================

import mysql.connector

# Aqui já informamos o banco copa2026, que foi criado na etapa 1.
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='copa2026',
    use_pure=True
)

cursor = conexao.cursor()

print('=== ETAPA 2 - INSERÇÃO DE REGISTROS ===')
print()

# ============================================================
# CADASTRO DE SELEÇÕES
# ============================================================

# Nessa parte serão cadastradas 5 seleções.
# O laço while permite repetir o cadastro até completar a quantidade definida.
print('--- Cadastro de seleções ---')
print('Serão cadastradas 5 seleções.')
print()

contador = 1

while contador <= 5:
    print(f'Seleção {contador} de 5')

    # O nome do país é obrigatório, pois identifica a seleção no sistema.
    # Enquanto o usuário deixar o campo vazio, o programa pede o valor novamente.
    nome_pais = input('Nome do país: ')
    while nome_pais.strip() == '':
        print('O nome do país é obrigatório!')
        nome_pais = input('Nome do país: ')

    # A confederação também é obrigatória, porque ajuda a classificar a seleção
    # de acordo com a região ou entidade continental a que pertence.
    # Enquanto o usuário deixar o campo vazio, o programa pede o valor novamente.
    confederacao = input('Confederação: ')
    while confederacao.strip() == '':
        print('A confederação é obrigatória!')
        confederacao = input('Confederação: ')

    # O técnico pode ficar vazio, pois nem todo dado opcional precisa ser informado.
    # Quando o usuário deixa em branco, o valor salvo no banco será None.
    tecnico = input('Técnico: ')
    if tecnico.strip() == '':
        tecnico = None

    # O ranking FIFA é um dado numérico.
    # Por isso, quando o usuário digita algum valor, o programa tenta converter para inteiro.
    ranking_fifa = input('Ranking FIFA: ')

    while ranking_fifa != '':
        try:
            ranking_fifa = int(ranking_fifa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            ranking_fifa = input('Ranking FIFA: ')

    if ranking_fifa == '':
        ranking_fifa = None

    # Depois de receber e tratar os dados, o INSERT grava a seleção na tabela selecoes.
    # Os %s são usados para enviar os valores de forma parametrizada.
    sql = '''
    INSERT INTO selecoes (nome_pais, confederacao, tecnico, ranking_fifa)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome_pais, confederacao, tecnico, ranking_fifa))
    conexao.commit()

    print('Seleção cadastrada com sucesso!')
    print()

    contador = contador + 1

# ============================================================
# CADASTRO DE JOGADORES
# ============================================================

# Nessa parte serão cadastrados 5 jogadores.
# Antes de pedir os dados de cada jogador, o sistema mostra as seleções disponíveis
# para que o usuário escolha um ID válido.
print('--- Cadastro de jogadores ---')
print('Serão cadastrados 5 jogadores.')
print()

contador = 1

while contador <= 5:
    print(f'Jogador {contador} de 5')

    print('Seleções cadastradas:')
    cursor.execute('SELECT id, nome_pais FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]}')

    print()

    # O nome do jogador é obrigatório, pois é o principal dado de identificação.
    # Se o usuário deixar o campo vazio, o programa pede o valor novamente.
    nome = input('Nome do jogador: ')
    while nome.strip() == '':
        print('O nome do jogador é obrigatório!')
        nome = input('Nome do jogador: ')

    # A posição também é obrigatória, pois caracteriza a função do jogador no time.
    # Aqui também se deixar o campo vazio, o programa pede o valor novamente.
    posicao = input('Posição: ')
    while posicao.strip() == '':
        print('A posição é obrigatória!')
        posicao = input('Posição: ')

    # A idade é opcional, mas se for informada precisa ser um número inteiro.
    idade = input('Idade: ')

    while idade != '':
        try:
            idade = int(idade)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            idade = input('Idade: ')

    if idade == '':
        idade = None

    # O número da camisa também é opcional, mas precisa ser inteiro quando preenchido.
    numero_camisa = input('Número da camisa: ')

    while numero_camisa != '':
        try:
            numero_camisa = int(numero_camisa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            numero_camisa = input('Número da camisa: ')

    if numero_camisa == '':
        numero_camisa = None

    # O clube de origem é um campo opcional.
    clube_origem = input('Clube de origem: ')
    if clube_origem.strip() == '':
        clube_origem = None

    # Essa validação evita cadastrar um jogador ligado a uma seleção inexistente.
    # O programa só continua quando o ID informado realmente existe na tabela selecoes.
    id_selecao_valido = False

    while id_selecao_valido == False:
        id_selecao = input('ID da seleção do jogador: ')

        while id_selecao.strip() == '':
            print('O ID da seleção é obrigatório!')
            id_selecao = input('ID da seleção do jogador: ')

        try:
            id_selecao = int(id_selecao)

            cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao,))
            selecao_encontrada = cursor.fetchone()

            if selecao_encontrada is None:
                print('Seleção não encontrada. Digite um ID existente.')
            else:
                id_selecao_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção.')

    # Após validar os dados, o jogador é inserido na tabela jogadores,
    # agora já associado à seleção escolhida pelo usuário.
    sql = '''
    INSERT INTO jogadores (nome, posicao, idade, numero_camisa, clube_origem, id_selecao)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome, posicao, idade, numero_camisa, clube_origem, id_selecao))
    conexao.commit()

    print('Jogador cadastrado com sucesso!')
    print()

    contador = contador + 1

# ============================================================
# CADASTRO DE ESTÁDIOS
# ============================================================

# Nessa parte serão cadastrados 5 estádios.
# Os campos nome e cidade são obrigatórios porque identificam o local.
print('--- Cadastro de estádios ---')
print('Serão cadastrados 5 estádios.')
print()

contador = 1

while contador <= 5:
    print(f'Estádio {contador} de 5')

    nome = input('Nome do estádio: ')
    while nome.strip() == '':
        print('O nome do estádio é obrigatório!')
        nome = input('Nome do estádio: ')

    cidade = input('Cidade: ')
    while cidade.strip() == '':
        print('A cidade é obrigatória!')
        cidade = input('Cidade: ')

    # O país-sede é opcional, pois o cadastro pode ser feito mesmo sem essa informação.
    pais_sede = input('País-sede: ')
    if pais_sede.strip() == '':
        pais_sede = None

    # A capacidade é opcional, pois o cadastro pode ser feito mesmo sem essa informação.
    capacidade = input('Capacidade: ')

    while capacidade != '':
        try:
            capacidade = int(capacidade)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            capacidade = input('Capacidade: ')

    if capacidade == '':
        capacidade = None

    # Depois de ler os dados, o estádio é gravado na tabela estadios.
    sql = '''
    INSERT INTO estadios (nome, cidade, pais_sede, capacidade)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(sql, (nome, cidade, pais_sede, capacidade))
    conexao.commit()

    print('Estádio cadastrado com sucesso!')
    print()

    contador = contador + 1

# ============================================================
# CADASTRO DE PARTIDAS
# ============================================================

# Nessa parte serão cadastradas 5 partidas.
# O sistema mostra as seleções e os estádios já cadastrados pra facilitar
# a escolha dos IDs corretos.
print('--- Cadastro de partidas ---')
print('Serão cadastradas 5 partidas.')
print()

contador = 1

while contador <= 5:
    print(f'Partida {contador} de 5')

    print('Seleções cadastradas:')
    cursor.execute('SELECT id, nome_pais FROM selecoes ORDER BY id')
    selecoes = cursor.fetchall()

    for selecao in selecoes:
        print(f'[{selecao[0]}] {selecao[1]}')

    print()

    print('Estádios cadastrados:')
    cursor.execute('SELECT id, nome FROM estadios ORDER BY id')
    estadios = cursor.fetchall()

    for estadio in estadios:
        print(f'[{estadio[0]}] {estadio[1]}')

    print()

    # A data é obrigatória porque toda partida precisa estar associada a um dia.
    data_jogo = input('Data do jogo (AAAA-MM-DD): ')
    while data_jogo.strip() == '':
        print('A data do jogo é obrigatória!')
        data_jogo = input('Data do jogo (AAAA-MM-DD): ')

    # A fase também é obrigatória para indicar em que momento da competição
    # a partida acontece.
    fase = input('Fase da competição: ')
    while fase.strip() == '':
        print('A fase é obrigatória!')
        fase = input('Fase da competição: ')

    # Os gols podem ficar vazios, já que uma partida pode ser cadastrada antes de acontecer.
    # Quando forem informados, precisam ser números inteiros.
    gols_casa = input('Gols da seleção mandante: ')

    while gols_casa != '':
        try:
            gols_casa = int(gols_casa)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            gols_casa = input('Gols da seleção mandante: ')

    if gols_casa == '':
        gols_casa = None

    gols_visitante = input('Gols da seleção visitante: ')

    while gols_visitante != '':
        try:
            gols_visitante = int(gols_visitante)
            break
        except ValueError:
            print('Digite um número válido ou pressione ENTER para pular.')
            gols_visitante = input('Gols da seleção visitante: ')

    if gols_visitante == '':
        gols_visitante = None

    # Essa validação confirma se a seleção mandante existe antes de cadastrar a partida.
    id_casa_valido = False

    while id_casa_valido == False:
        id_selecao_casa = input('ID da seleção mandante: ')

        while id_selecao_casa.strip() == '':
            print('O ID da seleção mandante é obrigatório!')
            id_selecao_casa = input('ID da seleção mandante: ')

        try:
            id_selecao_casa = int(id_selecao_casa)

            cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_casa,))
            selecao_casa = cursor.fetchone()

            if selecao_casa is None:
                print('Seleção mandante não encontrada. Digite um ID existente.')
            else:
                id_casa_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção mandante.')

    # A seleção visitante também precisa existir e não pode ser igual à mandante,
    # pois uma partida deve envolver duas seleções diferentes.
    id_visitante_valido = False

    while id_visitante_valido == False:
        id_selecao_visitante = input('ID da seleção visitante: ')

        while id_selecao_visitante.strip() == '':
            print('O ID da seleção visitante é obrigatório!')
            id_selecao_visitante = input('ID da seleção visitante: ')

        try:
            id_selecao_visitante = int(id_selecao_visitante)

            if id_selecao_visitante == id_selecao_casa:
                print('A seleção visitante não pode ser igual à mandante.')
            else:
                cursor.execute('SELECT id FROM selecoes WHERE id = %s', (id_selecao_visitante,))
                selecao_visitante = cursor.fetchone()

                if selecao_visitante is None:
                    print('Seleção visitante não encontrada. Digite um ID existente.')
                else:
                    id_visitante_valido = True

        except ValueError:
            print('Digite um número válido para o ID da seleção visitante.')

    # O estádio informado também é verificado para evitar que a partida seja ligada
    # a um estádio inexistente.
    id_estadio_valido = False

    while id_estadio_valido == False:
        id_estadio = input('ID do estádio: ')

        while id_estadio.strip() == '':
            print('O ID do estádio é obrigatório!')
            id_estadio = input('ID do estádio: ')

        try:
            id_estadio = int(id_estadio)

            # Essa consulta confirma se existe um estádio com o ID informado.
            cursor.execute('SELECT id FROM estadios WHERE id = %s', (id_estadio,))
            estadio_encontrado = cursor.fetchone()

            if estadio_encontrado is None:
                print('Estádio não encontrado. Digite um ID existente.')
            else:
                id_estadio_valido = True

        except ValueError:
            print('Digite um número válido para o ID do estádio.')

    # Com todos os dados validados, a partida é inserida na tabela partidas.
    # Os IDs informados serão usados depois para criar os relacionamentos da etapa 6.
    sql = '''
    INSERT INTO partidas (data_jogo, fase, gols_casa, gols_visitante, id_selecao_casa, id_selecao_visitante, id_estadio)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(sql, (data_jogo, fase, gols_casa, gols_visitante, id_selecao_casa, id_selecao_visitante, id_estadio))
    conexao.commit()

    print('Partida cadastrada com sucesso!')
    print()

    contador = contador + 1

# Sempre fechamos o cursor e a conexão ao final.
# Isso encerra a comunicação com o banco e libera os recursos.
cursor.close()
conexao.close()

print()
print('Etapa 2 executada com sucesso!')