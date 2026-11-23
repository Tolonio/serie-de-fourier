"""
03 · O fenômeno de Gibbs: o "chifre" que nunca some.

O que este exemplo mostra:
  Perto de um salto, a soma de Fourier passa do ponto (overshoot). Aumentar N deixa
  o chifre mais ESTREITO, mas a altura dele fica sempre em ~9% do tamanho do salto.
  Para a onda quadrada (salto de -1 a +1, tamanho 2) o pico tende a ≈ 1,179.

Isso acontece porque estamos aproximando uma função descontínua com funções suaves:
a convergência é boa "na média", mas não ponto a ponto perto do salto.
Na prática, é a origem dos "halos" em imagens JPEG muito comprimidas e do "ringing" em áudio.

Rode:  py exemplos/03_gibbs.py
"""
import numpy as np
import matplotlib.pyplot as plt

from estilo import AZUL, salvar
import fourier

T = 2 * np.pi
valores_N = [9, 29, 99, 299]
a0, a, b = fourier.coeficientes(fourier.onda_quadrada, T, max(valores_N))

# zoom perto do salto em t = 0 (de -1 para +1)
t = np.linspace(-0.6, 0.6, 4000)
cores = plt.cm.plasma(np.linspace(0.1, 0.8, len(valores_N)))

fig, eixo = plt.subplots(figsize=(9, 4.8))
eixo.plot(t, fourier.onda_quadrada(t), color=AZUL, lw=2, alpha=0.4, label="onda quadrada")
for N, cor in zip(valores_N, cores):
    s = fourier.soma_parcial(t, T, a0, a, b, N)
    pico = s.max()
    eixo.plot(t, s, color=cor, lw=1.4, label=f"N = {N:>3}  ·  pico = {pico:.4f}")
    print(f"N = {N:>3}: pico = {pico:.4f} (passou {100 * (pico - 1) / 2:.2f}% do salto)")

eixo.axhline(1.17898, color="k", ls="--", lw=0.8)
eixo.text(-0.58, 1.19, "limite ≈ 1,179  (≈ 9% do salto)", fontsize=9)
eixo.set_ylim(-1.3, 1.35)
eixo.set_xlabel("t (perto do salto em t = 0)")
eixo.legend(loc="lower right", fontsize=8)
eixo.set_title("Fenômeno de Gibbs: o pico fica mais estreito, mas não mais baixo", fontweight="bold")
salvar(fig, "03_gibbs.png")

if __name__ == "__main__":
    plt.show()
