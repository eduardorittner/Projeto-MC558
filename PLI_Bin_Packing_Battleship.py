from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus

# Parâmetros para solução ótima
n = 4
a = [2, 2, 4, 4]
C = 6
B = 2

# Parâmetros para solução não factível
# n = 3
# a = [3, 3, 5]
# C = 5
# B = 2

# Criação do problema
prob = LpProblem("Empacotamento_em_Caixas", LpMinimize)

# Variáveis de decisão
x = LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(B)], cat=LpBinary)

# Função objetivo
prob += 0, "Funcao_Objetivo"

# Restrições de alocação
for i in range(n):
    prob += lpSum(x[(i, j)] for j in range(B)) == 1, f"Alocacao_Item_{i+1}"

# Restrições de capacidade
for j in range(B):
    prob += lpSum(a[i] * x[(i, j)] for i in range(n)) == C, f"Capacidade_Caixa_{j+1}"

# Resolução do problema
status = prob.solve()

# Resultados
print(f"Status da Solução: {LpStatus[prob.status]}")

if prob.status == 1:
    for j in range(B):
        itens_na_caixa = [i+1 for i in range(n) if x[(i, j)].varValue == 1]
        soma_tamanhos = sum(a[i] for i in range(n) if x[(i, j)].varValue == 1)
        print(f"Caixa {j+1}: Itens {itens_na_caixa}, Soma dos Tamanhos {soma_tamanhos}")
else:
    print("Não foi encontrada uma solução factível.")
