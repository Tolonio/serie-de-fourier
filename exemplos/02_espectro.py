"""
02 · O espectro: a "receita" de cada onda.

O que este exemplo mostra:
  À esquerda, a onda no tempo. À direita, a amplitude An = √(an² + bn²) de cada harmônico.
  - Onda quadrada: só harmônicos ÍMPARES, caindo como 1/n   (tem saltos → muito agudo)
  - Dente de serra: TODOS os harmônicos, caindo como 1/n     (tem um salto por período)
  - Triangular: só ímpares, caindo como 1/n² (bem mais rápido) (não tem saltos → mais "suave")

Regra prática: quanto mais "quina" ou salto a função tem, mais devagar o espectro cai,
ou seja, mais frequências altas são necessárias para desenhá-la.

Rode:  py exemplos/02_espectro.py
"""
import numpy as np
import matplotlib.pyplot as plt

from estilo import AZUL, LARANJA, salvar
import fourier

T = 2 * np.pi
N = 15
ondas = [
    ("Onda quadrada", fourier.onda_quadrada),
    ("Dente de serra", fourier.dente_de_serra),
    ("Onda triangular", fourier.onda_triangular),
]

t = np.linspace(0, 2 * T, 800)
n = np.arange(1, N + 1)

fig, eixos = plt.subplots(len(ondas), 2, figsize=(10, 7.5), gridspec_kw={"width_ratios": [1.3, 1]})
for (nome, f), (eixo_t, eixo_f) in zip(ondas, eixos):
    a0, a, b = fourier.coeficientes(f, T, N)
    amplitude, _fase = fourier.amplitude_fase(a, b)

    # lado esquerdo: a onda e a aproximação com N harmônicos
    eixo_t.plot(t, f(t), color=AZUL, lw=1.2, alpha=0.6, label="original")
    eixo_t.plot(t, fourier.soma_parcial(t, T, a0, a, b), color=LARANJA, lw=1.6, label=f"Fourier, N = {N}")
    eixo_t.set_title(nome, loc="left", fontweight="bold")
    eixo_t.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi], ["0", "π", "2π", "3π", "4π"])
    eixo_t.legend(fontsize=8, loc="upper right")

    # lado direito: o espectro (uma barra por harmônico)
    eixo_f.bar(n, amplitude, color=LARANJA, width=0.6)
    eixo_f.set_xticks(n[::2])
    eixo_f.set_ylabel("amplitude An")
    eixo_f.set_ylim(0, 1.4)
    for k, A in zip(n[:5], amplitude[:5]):          # escreve o valor dos 5 primeiros
        if A > 0.01:
            eixo_f.text(k, A + 0.04, f"{A:.2f}", ha="center", fontsize=7)

eixos[-1, 0].set_xlabel("tempo t")
eixos[-1, 1].set_xlabel("harmônico n (frequência = n × fundamental)")
fig.suptitle("Tempo × frequência: cada onda tem a sua \"receita\" de harmônicos", fontweight="bold")
fig.tight_layout()
salvar(fig, "02_espectro.png")

if __name__ == "__main__":
    plt.show()
