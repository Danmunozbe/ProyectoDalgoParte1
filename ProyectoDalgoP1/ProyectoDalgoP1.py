import sys
import heapq

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

def algoritmo1_sol(k,N,Pi):
    dp = [[0]*(N+1) for _ in range(k+1)]
    for i in range(1, N+1):
        dp[1][i] = creativity(i, Pi)
    for j in range(2, k+1):
        for i in range(1, N+1):
            for x in range(0, i):
                dp[j][i] = max(dp[j][i], dp[j-1][i-x] + dp[1][x])
    return dp[k][N]


def algoritmo1_opt_sol(k, N, Pi):
    dp1 = [0]*(N+1)
    for i in range(1, N+1):
        dp1[i] = creativity(i, Pi)

    candidates = [0]
    current_max = -1
    for i in range(3, N+1):
        if dp1[i] > current_max:
            candidates.append(i)
            current_max = dp1[i]

    prev = dp1[:]
    for j in range(2, k+1):
        act = [0]*(N+1)
        for s in range(3, N+1):
            best = 0
            for x in candidates:
                if x > s:
                    break
                best = max(best, prev[s-x] + dp1[x])
            act[s] = best
        prev = act  # basta con reasignar

    return prev[N]


def resolver(k, n, Pi):
    # Heurística: usar el algoritmo ingenuo solo si k*n es pequeño
    limite = 2000 * 2000   # ≈ 4 millones de estados
    if k * n <= limite:
        return algoritmo1_sol(k, n, Pi)
    else:
        return algoritmo1_opt_sol(k, n, Pi)


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
