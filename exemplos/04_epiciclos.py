"""
04 · Epiciclos: vendo a série de Fourier girar.

O que este exemplo mostra:
  Cada harmônico é um CÍRCULO girando:
    - raio      = amplitude An (o "tamanho" daquele harmônico)
    - velocidade = n vezes a fundamental (o harmônico 3 dá 3 voltas enquanto o 1 dá uma)
    - ângulo inicial = a fase
  Os círculos são encaixados um na ponta do outro. A altura da ponta do último círculo,
  somada ao longo do tempo, desenha a onda (à direita).

Matemática por trás:
    an·cos(x) + bn·sin(x) = An·sin(x + ψn),   com An = √(an²+bn²) e ψn = atan2(an, bn)
  Então cada termo é a altura (parte imaginária) de um ponto girando num círculo de raio An.

Rode:  py exemplos/04_epiciclos.py   (gera imagens/04_epiciclos.gif, leva alguns segundos)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D

from estilo import LARANJA, CINZA, IMAGENS, RAIZ
import fourier

T = 2 * np.pi
N = 9                                   # harmônicos usados (na quadrada, só os ímpares contam)
QUADROS = 120                           # quadros por volta completa
FUNCAO = fourier.onda_quadrada          # troque por fourier.dente_de_serra, por exemplo

a0, a, b = fourier.coeficientes(FUNCAO, T, N)
A = np.hypot(a, b)                      # raios dos círculos
psi = np.arctan2(a, b)                  # fase de cada círculo
usados = [k for k in range(N) if A[k] > 1e-6]   # ignora círculos de raio zero (harmônicos pares)

fig, (eixo_c, eixo_w) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [1, 1.6]})
fig.subplots_adjust(wspace=0.02)
limite = 1.9
for eixo in (eixo_c, eixo_w):
    eixo.set_ylim(-limite, limite)
    eixo.grid(False)
eixo_c.set_xlim(-limite, limite)
eixo_c.set_aspect("equal")
eixo_c.axis("off")
eixo_w.set_xlim(0, 2 * T)
eixo_w.set_yticks([])
eixo_w.set_xticks([])
eixo_w.spines["left"].set_visible(False)
eixo_w.spines["bottom"].set_visible(False)
eixo_w.axhline(0, color=CINZA, lw=0.6)

circulos = [eixo_c.add_patch(plt.Circle((0, 0), A[k], fill=False, color=CINZA, lw=0.8)) for k in usados]
bracos, = eixo_c.plot([], [], color="k", lw=1.2, marker="o", ms=2.5)
ponta, = eixo_c.plot([], [], "o", color=LARANJA, ms=5)
onda, = eixo_w.plot([], [], color=LARANJA, lw=2)
historico = []                          # alturas já desenhadas (mais recente primeiro)
eixo_c.set_title(f"{len(usados)} círculos girando", fontsize=10)
eixo_w.set_title("altura da ponta ao longo do tempo", fontsize=10)

# o gráfico da direita "anda": o ponto novo entra em x = 0 e vai sendo empurrado
passo_x = T / QUADROS


def desenhar(quadro):
    t = 2 * np.pi * quadro / QUADROS
    x, y = 0.0, a0 / 2                  # começa no nível médio
    xs, ys = [x], [y]
    for circulo, k in zip(circulos, usados):
        n = k + 1
        circulo.center = (x, y)          # cada círculo nasce na ponta do anterior
        angulo = n * t + psi[k]          # o harmônico n gira n vezes mais rápido
        x += A[k] * np.cos(angulo)
        y += A[k] * np.sin(angulo)
        xs.append(x)
        ys.append(y)
    bracos.set_data(xs, ys)
    ponta.set_data([x], [y])

    historico.insert(0, y)
    del historico[2 * QUADROS:]
    onda.set_data(np.arange(len(historico)) * passo_x, historico)
    return [*circulos, bracos, ponta, onda]


# linha pontilhada ligando a ponta dos círculos ao começo da onda.
# Ela atravessa de um gráfico para o outro, então é desenhada em coordenadas da FIGURA.
ponte = Line2D([], [], color=LARANJA, lw=0.8, ls=":", transform=fig.transFigure)
fig.add_artist(ponte)


def quadro_completo(quadro):
    artistas = desenhar(quadro)
    x, y = ponta.get_data()
    p1 = fig.transFigure.inverted().transform(eixo_c.transData.transform((x[0], y[0])))
    p2 = fig.transFigure.inverted().transform(eixo_w.transData.transform((0, y[0])))
    ponte.set_data([p1[0], p2[0]], [p1[1], p2[1]])
    return artistas + [ponte]


# "Aquece" a animação: roda 2 voltas sem gravar, para a onda já começar desenhada.
# Como o movimento é periódico, gravar UMA volta depois disso gera um GIF que repete sem emenda.
for q in range(2 * QUADROS):
    desenhar(q)
anim = FuncAnimation(fig, quadro_completo, frames=QUADROS, interval=33, blit=False)

if __name__ == "__main__":
    caminho = IMAGENS / "04_epiciclos.gif"
    anim.save(caminho, writer=PillowWriter(fps=30), dpi=80)
    print("salvo:", caminho.relative_to(RAIZ))
