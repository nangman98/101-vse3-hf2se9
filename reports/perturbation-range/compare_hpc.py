"""Overlay ΔV̄_mac(d) from Nurion and Perlmutter runs for N = 8, 10, 12.

If the curves match within ~1 meV, the two HPC systems agree and we can mix
Nurion N=8/10/12 with Perlmutter N=14 in the final figure.
"""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sisl

ROOT = Path(__file__).resolve().parent
CALC = ROOT.parent.parent / "VSe3-Hf2Se9" / "03-calc" / "12-perturbation-range"
PERIOD = 3.135
NS = [8, 10, 12]

import re
def hf_z(struct: Path) -> float:
    zs = []
    for line in struct.read_text().splitlines():
        m = re.match(r"\s*([-\d.Ee+]+)\s+([-\d.Ee+]+)\s+([-\d.Ee+]+)\s+3\s+#", line)
        if m:
            zs.append(float(m.group(3)))
    return float(np.mean(zs))


def planar_avg(gridfile: Path):
    g = sisl.get_sile(str(gridfile)).read_grid()
    V = np.asarray(g.grid)
    cz = g.lattice.cell[2, 2]
    z = np.linspace(0, cz, V.shape[2], endpoint=False)
    return z, V.mean(axis=(0, 1)), cz


def macro(V, dz, period):
    w = max(1, int(round(period / dz)))
    k = np.ones(w) / w
    return np.convolve(V, k, mode="same")


def profile(Ad: Path, Bd: Path):
    zA, VA, cz = planar_avg(Ad / "ElectrostaticPotential.grid.nc")
    zB, VB, _ = planar_avg(Bd / "ElectrostaticPotential.grid.nc")
    dz = zA[1] - zA[0]
    dVm = macro(VA - VB, dz, PERIOD)
    z_mol = hf_z(Ad / "struct.fdf")
    d = zA - z_mol
    far = np.abs(d) > (cz / 2 - PERIOD)
    dVm -= float(np.mean(dVm[far]))
    return d, dVm


plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "savefig.transparent": True,
})

fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
max_absdiff = {}

for ax, N in zip(axes, NS):
    An = CALC / "_nurion" / f"N{N:02d}_A_mol"
    Bn = CALC / "_nurion" / f"N{N:02d}_B_nomol"
    Ap = CALC / f"N{N:02d}_A_mol"
    Bp = CALC / f"N{N:02d}_B_nomol"

    dN, yN = profile(An, Bn)
    dP, yP = profile(Ap, Bp)

    ax.plot(dN, yN * 1000, label="Nurion", color="#1b5e9a", lw=1.4)
    ax.plot(dP, yP * 1000, label="Perlmutter", color="#a04000", lw=1.4, ls="--")
    ax.set_title(f"N = {N}")
    ax.set_xlabel(r"$d$ (Å)")
    ax.axvline(0, c="red", lw=0.5, ls=":", alpha=0.5)
    ax.axhline(0, c="k", lw=0.3)
    ax.set_ylim(-60, 60)

    # max absolute difference after alignment (same grid expected)
    if len(dN) == len(dP) and np.allclose(dN, dP):
        diff = (yN - yP) * 1000
        max_absdiff[N] = float(np.max(np.abs(diff)))
    else:
        max_absdiff[N] = None

axes[0].set_ylabel(r"$\Delta \bar{V}_\mathrm{mac}$ (meV)")
axes[0].legend(frameon=False, loc="lower right")

plt.tight_layout()
out = ROOT / "compare-hpc-deltaV.png"
plt.savefig(out, dpi=220, bbox_inches="tight")
print(f"saved: {out}")
print("max |ΔV_nurion − ΔV_perlmutter| (meV):")
for N, v in max_absdiff.items():
    print(f"  N={N}: {v:.3f}" if v is not None else f"  N={N}: grid mismatch")
