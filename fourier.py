"""
fourier.py: o "motor" da série de Fourier, explicado linha a linha.

IDEIA CENTRAL
-------------
Qualquer função periódica razoável f(t), com período T, pode ser escrita como
uma soma de senos e cossenos:

    f(t) ≈ a0/2 + Σ [ an·cos(n·ω0·t) + bn·sin(n·ω0·t) ]     (n = 1, 2, 3, ..., N)

onde ω0 = 2π/T é a "frequência fundamental" e:

    a0 = (2/T) ∫ f(t) dt                    → 2× o valor médio da função
    an = (2/T) ∫ f(t)·cos(n·ω0·t) dt        → "quanto de cosseno de frequência n" existe em f
    bn = (2/T) ∫ f(t)·sin(n·ω0·t) dt        → "quanto de seno de frequência n" existe em f

(as integrais são sobre um período inteiro, de 0 até T)

Por que a integral "mede" quanto de cada seno existe?
Porque senos e cossenos de frequências diferentes são ORTOGONAIS: a integral
do produto de dois deles, num período, dá zero. Multiplicar f(t) por sin(n·ω0·t)
e integrar "filtra" só a parte de f que tem aquela frequência, e o resto cancela.
É o mesmo que projetar um vetor num eixo: an e bn são as "coordenadas" de f.
"""

import numpy as np


def coeficientes(f, T, N, amostras=20_000):
    """
    Calcula numericamente a0, an e bn (n = 1..N) de uma função f com período T.

    f        : função Python que recebe um array numpy de tempos e devolve os valores
    T        : período da função (ex.: 2π)
    N        : quantos harmônicos calcular
    amostras : em quantos pontos dividir o período para aproximar a integral

    Retorna (a0, a, b), em que a[n-1] = an e b[n-1] = bn.
    """
    # 1) Dividimos um período [0, T) em muitas fatias iguais e pegamos o MEIO de cada uma
    #    ("regra do ponto médio"). Assim nenhum ponto cai bem em cima de um salto da função.
    dt = T / amostras                         # largura de cada "fatia" da integral
    t = (np.arange(amostras) + 0.5) * dt      # centro de cada fatia
    w0 = 2 * np.pi / T         # frequência fundamental (rad/s)
    y = f(t)                   # valores da função nesses pontos

    # 2) Integral ≈ soma dos valores × largura da fatia (soma de Riemann).
    #    Para funções periódicas amostradas no período inteiro, isso é muito preciso.
    a0 = (2 / T) * np.sum(y) * dt

    # 3) Para cada harmônico n, "projetamos" f sobre cos(nω0t) e sin(nω0t).
    n = np.arange(1, N + 1)[:, None]   # coluna [1, 2, ..., N] → permite calcular todos de uma vez
    cos_n = np.cos(n * w0 * t)         # matriz N × amostras: cada linha é um cosseno
    sin_n = np.sin(n * w0 * t)
    a = (2 / T) * np.sum(y * cos_n, axis=1) * dt
    b = (2 / T) * np.sum(y * sin_n, axis=1) * dt
    return a0, a, b


def soma_parcial(t, T, a0, a, b, N=None):
    """
    Reconstrói f(t) somando só os N primeiros harmônicos:

        S_N(t) = a0/2 + Σ_{n=1..N} [ an·cos(nω0t) + bn·sin(nω0t) ]

    Quanto maior N, mais "detalhe" (frequências altas) entra, e mais a soma parece f.
    """
    N = len(a) if N is None else N
    w0 = 2 * np.pi / T
    s = np.full_like(t, a0 / 2, dtype=float)   # começa pelo valor médio (o "nível DC")
    for k in range(1, N + 1):                  # vai somando harmônico por harmônico
        s += a[k - 1] * np.cos(k * w0 * t) + b[k - 1] * np.sin(k * w0 * t)
    return s


def amplitude_fase(a, b):
    """
    Cada par (an, bn) pode ser escrito como UMA senoide deslocada:

        an·cos(x) + bn·sin(x) = An·cos(x - φn)

    com An = √(an² + bn²)  (amplitude: o "tamanho" desse harmônico)
    e   φn = atan2(bn, an) (fase: o "atraso" dele).

    O gráfico de An por n é o ESPECTRO: mostra quais frequências compõem o sinal.
    """
    return np.hypot(a, b), np.arctan2(b, a)


# ---------------------------------------------------------------------------
# Funções clássicas para brincar (todas com período 2π)
# ---------------------------------------------------------------------------

def onda_quadrada(t):
    """+1 na primeira metade do período, -1 na segunda."""
    return np.where(np.mod(t, 2 * np.pi) < np.pi, 1.0, -1.0)


def dente_de_serra(t):
    """Sobe em linha reta de -1 a +1 e cai de uma vez."""
    return np.mod(t, 2 * np.pi) / np.pi - 1


def onda_triangular(t):
    """Sobe e desce em linha reta, sem saltos."""
    x = np.mod(t, 2 * np.pi) / np.pi   # vai de 0 a 2
    return np.where(x < 1, 2 * x - 1, 3 - 2 * x)


if __name__ == "__main__":
    # Teste rápido: os coeficientes teóricos da onda quadrada são
    # bn = 4/(nπ) para n ímpar e 0 para n par; an = 0 para todo n.
    a0, a, b = coeficientes(onda_quadrada, 2 * np.pi, 7)
    print("n   an (~0)      bn calculado   bn teórico")
    for n in range(1, 8):
        teorico = 4 / (n * np.pi) if n % 2 else 0.0
        print(f"{n}   {a[n-1]:+.5f}    {b[n-1]:+.5f}       {teorico:+.5f}")
