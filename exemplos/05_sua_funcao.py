"""
05 · Sua vez: troque a função e veja a série dela.

Exemplo escolhido: a "meia onda retificada", o que sai de um retificador de 1 diodo
(a parte negativa da senoide é cortada). Ela aparece em fontes de alimentação.

Coisas para reparar:
  - a0/2 NÃO é zero: a onda tem valor médio positivo (1/π ≈ 0,318). É o "nível DC" que a fonte quer.
  - O harmônico 1 é forte (a senoide original) e depois só aparecem os PARES (2, 4, 6...),
    caindo rápido: a função não tem saltos, só "quinas".

Para testar outra função, é só mudar minha_funcao abaixo. Ideias:
    return np.abs(np.sin(t))                       # onda completa retificada
    return np.where(np.mod(t, 2*np.pi) < 0.5, 1, 0)  # pulso estreito (precisa de MUITOS harmônicos)
    return (np.mod(t, 2*np.pi) - np.pi) ** 2       # parábolas encaixadas

Rode:  py exemplos/05_sua_funcao.py
"""
import numpy as np
import matplotlib.pyplot as plt

from estilo import AZUL, LARANJA, salvar
import fourier


def minha_funcao(t):
    return np.maximum(np.sin(t), 0)    # meia onda retificada: corta o que for negativo


T = 2 * np.pi
N = 10
a0, a, b = fourier.coeficientes(minha_funcao, T, N)
amplitude, fase = fourier.amplitude_fase(a, b)

print(f"a0/2 (valor médio) = {a0 / 2:.4f}")
print(" n      an        bn       An")
for n in range(1, N + 1):
    print(f"{n:2d}  {a[n-1]:+.4f}  {b[n-1]:+.4f}  {amplitude[n-1]:.4f}")

t = np.linspace(0, 3 * T, 1200)
fig, (eixo_t, eixo_f) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.6, 1]})
eixo_t.plot(t, minha_funcao(t), color=AZUL, lw=2.5, alpha=0.4, label="minha_funcao")
for n, estilo in [(1, ":"), (2, "--"), (N, "-")]:
    eixo_t.plot(t, fourier.soma_parcial(t, T, a0, a, b, n), color=LARANJA, ls=estilo, lw=1.5, label=f"N = {n}")
eixo_t.axhline(a0 / 2, color="k", lw=0.8, ls="-.")
eixo_t.text(0.1, a0 / 2 + 0.04, f"valor médio = {a0 / 2:.3f}", fontsize=8)
eixo_t.set_title("Meia onda retificada e suas aproximações", loc="left", fontweight="bold")
eixo_t.legend(fontsize=8, ncol=4, loc="upper right")
eixo_t.set_ylim(-0.4, 1.35)

eixo_f.bar([0], [abs(a0 / 2)], color="k", width=0.6, label="nível DC")
eixo_f.bar(np.arange(1, N + 1), amplitude, color=LARANJA, width=0.6, label="harmônicos")
eixo_f.set_xticks(range(0, N + 1))
eixo_f.set_xlabel("harmônico n")
eixo_f.set_title("Espectro", loc="left", fontweight="bold")
eixo_f.legend(fontsize=8)
fig.tight_layout()
salvar(fig, "05_sua_funcao.png")

if __name__ == "__main__":
    plt.show()
