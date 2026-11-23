"""
01 · Montando uma onda quadrada só com senos.

O que este exemplo mostra:
  Com 1 harmônico temos só uma senoide. Somando mais harmônicos (frequências 3, 5, 7...)
  a curva vai "endireitando" até parecer a onda quadrada.

Rode:  py exemplos/01_onda_quadrada.py
"""
import numpy as np
import matplotlib.pyplot as plt

from estilo import AZUL, LARANJA, salvar
import fourier

T = 2 * np.pi                       # período da onda
N_MAX = 49                          # maior quantidade de harmônicos que vamos usar

# Calcula os coeficientes uma vez só (até N_MAX). As somas parciais reaproveitam.
a0, a, b = fourier.coeficientes(fourier.onda_quadrada, T, N_MAX)

# 1000 pontos para desenhar dois períodos: de -π a 3π
t = np.linspace(-np.pi, 3 * np.pi, 1000)
original = fourier.onda_quadrada(t)

fig, eixos = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)
for eixo, N in zip(eixos.flat, [1, 3, 9, 49]):
    aproximacao = fourier.soma_parcial(t, T, a0, a, b, N)
    eixo.plot(t, original, color=AZUL, lw=1.2, alpha=0.5, label="onda quadrada")
    eixo.plot(t, aproximacao, color=LARANJA, lw=2, label=f"soma até n = {N}")
    eixo.set_title(f"N = {N} harmônicos")
    eixo.set_ylim(-1.5, 1.5)
    eixo.legend(loc="lower left", fontsize=8)

# marca os eixos x em múltiplos de π, que é mais natural aqui
for eixo in eixos[1]:
    eixo.set_xticks(np.arange(-1, 4) * np.pi, ["-π", "0", "π", "2π", "3π"])
    eixo.set_xlabel("t")

fig.suptitle("Quanto mais harmônicos, mais a soma de senos parece a onda quadrada", fontweight="bold")
salvar(fig, "01_onda_quadrada.png")

if __name__ == "__main__":
    plt.show()
