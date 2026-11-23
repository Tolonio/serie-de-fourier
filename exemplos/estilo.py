"""Visual comum a todos os gráficos (cores, fontes) e pasta onde as imagens são salvas."""
import sys
from pathlib import Path

import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))          # permite "import fourier" de dentro de exemplos/
IMAGENS = RAIZ / "imagens"
IMAGENS.mkdir(exist_ok=True)

AZUL, LARANJA, CINZA, VERDE = "#2563eb", "#ea580c", "#9ca3af", "#16a34a"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 110,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "font.size": 10,
})


def salvar(fig, nome):
    """Salva a figura em imagens/<nome> e avisa no terminal."""
    caminho = IMAGENS / nome
    fig.savefig(caminho)
    print("salvo:", caminho.relative_to(RAIZ))
