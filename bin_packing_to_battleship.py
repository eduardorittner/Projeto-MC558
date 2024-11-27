import unittest

def bin_packing_para_batalha_naval(n, C, B, lista_ais):
    # Verifica se a soma dos tamanhos dos itens é igual a C * B
    if sum(lista_ais) != C * B:
        raise ValueError("A soma dos tamanhos dos itens não é igual a C * B.")
    
    # Calcula o número total de linhas e colunas
    total_linhas = sum(lista_ais) + (n - 1)  # Adiciona linhas separadoras entre itens
    total_colunas = B + (B - 1)  # Adiciona colunas separadoras entre bins
    
    # Inicializa a grade com água ('~')
    grade = [['~' for _ in range(total_colunas)] for _ in range(total_linhas)]
    
    # Inicializa os contadores de linhas
    contagem_linhas = []
    
    # Inicializa os contadores de colunas
    contagem_colunas = []
    
    # Frota (lista de comprimentos de navios)
    frota = lista_ais.copy()
    
    # Define os contadores de colunas
    for b in range(B):
        # As colunas dos bins estão nas posições b * 2 (devido aos separadores)
        coluna_bin = b * 2
        contagem_colunas.append(C)
        if b < B - 1:
            # Adiciona separador de colunas
            contagem_colunas.append(0)
    # Ajusta para o último bin (sem separador após o último bin)
    if len(contagem_colunas) < total_colunas:
        contagem_colunas.append(0)
    
    linha_atual = 0
    for idx, ai in enumerate(lista_ais):
        # Para cada item ai
        comprimento_item = ai
        # Linhas para este item
        linhas_item = list(range(linha_atual, linha_atual + comprimento_item))
        # Define contadores de linhas para as linhas do item
        for r in linhas_item:
            contagem_linhas.append(1)
        linha_atual += comprimento_item
        if idx < n - 1:
            # Adiciona uma linha separadora
            contagem_linhas.append(0)
            linha_atual += 1
    
        # Para cada bin
        for b in range(B):
            coluna_bin = b * 2
            # Define '?' na grade para as faixas do item nos bins
            for r in linhas_item:
                grade[r][coluna_bin] = '?'
    
    # Preenche as colunas separadoras com '~' e define contagem de colunas como 0
    for c in range(total_colunas):
        if c % 2 == 1:
            # Coluna separadora
            for r in range(total_linhas):
                grade[r][c] = '~'
    
    # Prepara a saída como uma string
    linhas_saida = []
    for r in range(total_linhas):
        linha_str = ' '.join(grade[r])
        linhas_saida.append(f"{linha_str} {contagem_linhas[r]}")
    linhas_saida.append(f"Contagem de colunas: {contagem_colunas}")
    linhas_saida.append(f"Frota (comprimentos dos navios): {frota}")
    
    # Retorna a saída como uma única string
    return '\n'.join(linhas_saida)

# Testes unitários
class TesteBinPackingParaBatalhaNaval(unittest.TestCase):
    def teste_caso_1(self):
        n, C, B = 3, 5, 2
        lista_ais = [3, 2, 5]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 1:")
        print(saida_esperada)

    def teste_caso_2(self):
        n, C, B = 4, 10, 2
        lista_ais = [7, 3, 6, 4]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 2:")
        print(saida_esperada)

    def teste_caso_3(self):
        n, C, B = 5, 8, 2
        lista_ais = [2, 6, 3, 5, 0]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 3:")
        print(saida_esperada)

    def teste_caso_4(self):
        # Caso corrigido
        n, C, B = 7, 9, 3
        lista_ais = [3, 3, 3, 6, 6, 3, 3]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 4:")
        print(saida_esperada)

    def teste_caso_5(self):
        n, C, B = 2, 15, 2
        lista_ais = [15, 15]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 5:")
        print(saida_esperada)

    def teste_caso_6(self):
        n, C, B = 3, 4, 3
        lista_ais = [4, 4, 4]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 6:")
        print(saida_esperada)

    def teste_caso_7(self):
        n, C, B = 4, 5, 4
        lista_ais = [5, 5, 5, 5]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 7:")
        print(saida_esperada)

    def teste_caso_8(self):
        n, C, B = 5, 6, 3
        lista_ais = [2, 4, 6, 6, 0]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 8:")
        print(saida_esperada)

    def teste_caso_9(self):
        # Caso corrigido
        n, C, B = 7, 10, 3
        lista_ais = [5, 5, 10, 5, 5, 0, 0]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 9:")
        print(saida_esperada)

    def teste_caso_10(self):
        n, C, B = 3, 9, 1
        lista_ais = [3, 3, 3]
        saida_esperada = bin_packing_para_batalha_naval(n, C, B, lista_ais)
        print("\nSaída do Caso de Teste 10:")
        print(saida_esperada)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)

'''
Explicação do Código

    Função bin_packing_para_batalha_naval:
        Converte uma instância do problema de Bin Packing para uma instância do jogo Batalha Naval.
        Verifica a validade dos dados de entrada, como a soma dos tamanhos dos itens ser igual a C * B.
        Gera uma grade onde:
            '?' indica células onde navios podem ser posicionados.
            '~' indica células de água.
        Adiciona separadores (~) entre bins e itens.
'''
