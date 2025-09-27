import sys
import heapq

# ==== Límites (ajústalos si quieres ser más conservador/atrevido) ====
BUDGET_EXACT = 80_000_000    # tiempo aprox: usa exacta si k * n^2 <= 8e7
MAX_DP_CELLS = 2_000_000     # memoria aprox: usa exacta si k * (n+1) <= 2e6
BUDGET_OPT   = 100_000_000   # tiempo aprox: usa opt si k * n * |C| <= 1e8

# ---- Aquí van tus algoritmos y función creativity ----
def creativity(x, P):
    """
    Calcula la creatividad de asignar x unidades de energía a una celda,
    según las reglas con dígitos (3,6,9) y los pesos P.
    """
    score = 0
    pos = 0
    while x > 0:
        d = x % 10
        if d in (3, 6, 9):
            mult = d // 3  # 3->1, 6->2, 9->3
            score += mult * P[pos]
        pos += 1
        x //= 10
    return score

def compute_dp1(N, P):
    """dp1[x] = creatividad de asignar x a UNA celda, para x = 0..N."""
    dp1 = [0]*(N+1)
    for x in range(1, N+1):
        dp1[x] = creativity(x, P)
    return dp1

def build_candidates(dp1):
    """
    Candidatos = puntos donde dp1[i] marca nuevo máximo al crecer i.
    Incluye 0 (no asignar). Arranca en 3 porque <3 no aporta (no hay 3/6/9).
    """
    N = len(dp1) - 1
    candidates = [0]
    current_max = -1
    for i in range(3, N+1):
        if dp1[i] > current_max:
            candidates.append(i)
            current_max = dp1[i]
    return candidates

def algoritmo1_sol(k, N, Pi):
    dp = [[0]*(N+1) for _ in range(k+1)]
    for i in range(1, N+1):
        dp[1][i] = creativity(i, Pi)
    for j in range(2, k+1):
        for i in range(1, N+1):
            for x in range(0, i):
                dp[j][i] = max(dp[j][i], dp[j-1][i-x] + dp[1][x])
    return dp[k][N]

def algoritmo1_opt_sol_with_dp1(k, N, dp1, candidates):
    prev = dp1[:]  # base: 1 celda
    for _ in range(2, k+1):
        act = [0]*(N+1)
        for s in range(3, N+1):
            best = 0
            for x in candidates:
                if x > s:
                    break
                val = prev[s-x] + dp1[x]
                if val > best:
                    best = val
            act[s] = best
        prev = act
    return prev[N]

def algoritmo1_greedy(k, N, P):
    """
    Greedy súper rápido:
    - Elige un tamaño de asignación x* que maximiza dp1[x]/x
    - Rellena tantas celdas como sea posible con x*
    - El resto al final (si cabe otra celda)
    Nota: puede ser subóptimo, pero es muy veloz.
    """
    if N == 0 or k == 0:
        return 0

    dp1 = [0]*(N+1)
    for x in range(1, N+1):
        dp1[x] = creativity(x, P)

    best_x = 1
    best_ratio = dp1[1] / 1 if dp1[1] > 0 else 0.0
    for x in range(2, N+1):
        if dp1[x] == 0:
            continue
        ratio = dp1[x] / x
        if ratio > best_ratio:
            best_ratio = ratio
            best_x = x

    if best_ratio == 0.0:
        return 0

    max_copias_por_N = N // best_x
    copias = min(max_copias_por_N, k)

    total = copias * dp1[best_x]
    usado = copias * best_x
    celdas_usadas = copias

    resto = N - usado
    if resto > 0 and celdas_usadas < k:
        total += dp1[resto]
        celdas_usadas += 1
        usado += resto
        resto = 0

    if resto > 0 and copias > 0:
        x_old = best_x
        x_new = best_x + resto
        if x_new <= N:
            mejora = dp1[x_new] - dp1[x_old]
            if mejora > 0:
                total += mejora
                resto = 0
    return total

def resolver(k, n, Pi):
    """
    Selección automática sin 'modos':
    - Exacta si (tiempo y memoria) caben.
    - Si no, intenta OPT si el estimado k*n*|C| cabe.
    - Si tampoco, usa greedy.
    """
    # 1) Exacta: tiempo y memoria
    if k * (n**2) <= BUDGET_EXACT and k * (n + 1) <= MAX_DP_CELLS:
        return algoritmo1_sol(k, n, Pi)

    # 2) Prepara dp1 y candidates (separados) para estimar y/o usar OPT
    dp1 = compute_dp1(n, Pi)
    candidates = build_candidates(dp1)
    if k * n * max(1, len(candidates)) <= BUDGET_OPT:
        return algoritmo1_opt_sol_with_dp1(k, n, dp1, candidates)

    # 3) Si nada cabe, greedy ultra-rápido
    return algoritmo1_greedy(k, n, Pi)

# ---------------- MAIN -----------------
def main():
    linea = sys.stdin.readline()
    ncasos = int(linea.strip())

    for _ in range(ncasos):
        linea = sys.stdin.readline().strip()
        if not linea:
            continue
        datos = [int(num) for num in linea.split()]
        k = datos[0]
        n = datos[1]
        Pi = datos[2:]
        respuesta = resolver(k, n, Pi)
        print(respuesta)

if __name__ == "__main__":
    main()
