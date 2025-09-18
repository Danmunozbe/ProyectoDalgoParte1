<div align="center">
<picture>
    <source srcset="https://imgur.com/5RiEY87" media="(prefers-color-scheme: dark)">
    <source srcset="https://imgur.com/5RiEY87" media="(prefers-color-scheme: light)">
    <img src="https://imgur.com/5RiEY87" alt="Escudo UNIANDES" width="350px">
</picture>

<h3>ISIS 1105 Diseño y Análisis de Algoritmos</h3>

<h1>Proyecto Parte 1 - Virtualización de fábrica</h1>

<h5>Daniel Santiago Muñoz<br>
    Juan David Ortiz<br>

<h6>Universidad de los Andes<br>
    2025-II</h6>
</div>

# Algoritmo 1 
$$
dp[i][n] =
\begin{cases}
0 & \text{si } i=0 \lor n=0, \\[6pt]
\text{creativity}(n) & \text{si } i=1, \\[6pt]
\max\limits_{0 \leq x \leq n} \big( dp[i-1][n-x] + dp[1][x] \big) & \text{si } i > 1 \land n>0.
\end{cases}
$$

**Donde:**

- $dp[i][n]$ es la máxima creatividad al llenar hasta la $i$-ésima celda usando un total de $n$ unidades de energía.  
- $\text{creativity}(n)$ es la creatividad generada al colocar $n$ unidades de energía en una sola celda.  

**Principios clave:**
1. El orden en que se llenan las celdas no afecta el resultado.  
2. La creatividad depende únicamente de la cantidad de energía asignada a una celda, y no de cuál celda específica se trate.

A contnuación se presenta un ejemplo:
![Animación](assets/algoritmo1.gif)

## Complejidad
Notese que en el ejemplo anterior, se recorrieron todos los valores de $n$ para hallar la creatividad máxima de $n=13$. Ya que este proceso se debe hacer para cada valor de $n$, entonces esta complejidad seria de $O(n^2)$. Ademas de esto, se realiza por cada celda, por tanto la complejidad final es de:
\[
O(kn^2)
\]
## Optimización
Al realizar la tabla, vemos que muchos valores son 0, o sencillamente se repiten. Para evitar estos valores proponemos guardar una lista de _candidatos_ En los cuales solo se guardan solo los valores únicos de creatividad posibles y además, mayores a los anteriores. En otras palabras hacemos un arreglo monotonicamente creciente.

Para llenar este arreglo, sencillamente emepzamos con un indicador -1, y para cada $0 \le i\le n$ lo agregamos si su creatividad es mayor al indicador. Luego el indicador se actualiza con este valor.

El proceso se ve a continuación.

![Animación](assets/candidatos.gif)

Luego solo realizamos la iteracion en estos valores.

![Animación](assets/algoritmo1O.gif)

Por lo que la complejidad final es de
\[
    O(kNC)
\]
Siendo $C$ la cantidad de candidatos que es aproximadamente $10\log_{10}{N}$
Dejando entonces

\[
    O(kN\log N)
\]
Finalmente Notese que para los calculos, solo dependemos de la fila $1$ y $i-1$, junto al arreglo $C$ que es $<< N$ por lo que en total requririamos de una cantidad de memoria
\[
O(3N)
\]
