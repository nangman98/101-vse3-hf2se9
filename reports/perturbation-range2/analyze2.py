"""Perturbation-range analysis (v3 base, N=14 우선).

Reads ElectrostaticPotential.grid.nc for each (A_mol, B_nomol) pair,
computes ΔV(z), macroscopic averages with VSe3 period (3.18 Å, v3 base),
fits exponential decay, and emits figure + CSV + JSON summary.

N=20, N=24는 SCF 끝나면 NS 리스트에 추가.
"""
from __future__ import annotations
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sisl

ROOT = Path(__file__).resolve().parent
CALC = ROOT.parent.parent / "VSe3-Hf2Se9" / "03-calc" / "11-perturbation-range"
FIG_DIR = ROOT
MEET_FIG_DIR = ROOT.parent.parent / "meetings" / "next" / "figures"
NS = [14]  # N20, N24는 결과 나오면 추가
PERIOD_VSE3 = 3.18  # Å, v3 base V-V mean (chain 3.143~3.232 평균)


def planar_avg(gridfile: Path):
    g = sisl.get_sile(str(gridfile)).read_grid()
    V = np.asarray(g.grid)
    cz = g.lattice.cell[2, 2]
    Nz = V.shape[2]
    z = np.linspace(0, cz, Nz, endpoint=False)
    return z, V.mean(axis=(0, 1)), cz


def macroscopic_avg(V: np.ndarray, dz: float, period: float) -> np.ndarray:
    w = max(1, int(round(period / dz)))
    kernel = np.ones(w) / w
    return np.convolve(V, kernel, mode="same")


def hf_z_from_xv(xv_path: Path) -> float:
    """Mean z (Å) of Hf atoms from siesta.XV (species 1 = Hf in v3)."""
    text = xv_path.read_text()
    lines = text.splitlines()
    # XV format: line1 = na, lines 2..1+ncell are cell vectors actually
    # Standard: lines 0-2 = cell vectors (a,b,c) in Bohr, line 3 = natoms,
    #   lines 4.. = "isp Z x y z vx vy vz" with x,y,z in Bohr
    BOHR = 0.529177
    natoms = int(lines[3].split()[0])
    zs = []
    for i in range(4, 4 + natoms):
        parts = lines[i].split()
        isp = int(parts[0])
        z_bohr = float(parts[4])  # 5th column = z
        if isp == 1:  # Hf
            zs.append(z_bohr * BOHR)
    if not zs:
        # fallback: parse struct.fdf
        return 0.0
    return float(np.mean(zs))


def hf_z_from_struct(struct_fdf: Path) -> float:
    """Mean z (Å) of Hf atoms from struct.fdf, looking up species 1 = Hf."""
    text = struct_fdf.read_text()
    in_block = False
    zs = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("%block AtomicCoordinatesAndAtomicSpecies"):
            in_block = True
            continue
        if s.startswith("%endblock AtomicCoordinatesAndAtomicSpecies"):
            in_block = False
            continue
        if in_block and s and not s.startswith("#"):
            parts = s.split()
            if len(parts) >= 4:
                # x y z species
                try:
                    isp = int(parts[3])
                    if isp == 1:  # Hf
                        zs.append(float(parts[2]))
                except ValueError:
                    pass
    return float(np.mean(zs)) if zs else 0.0


def analyze_one(N: int):
    Ad = CALC / f"N{N:02d}_A_mol"
    Bd = CALC / f"N{N:02d}_B_nomol"
    zA, VA, cz = planar_avg(Ad / "ElectrostaticPotential.grid.nc")
    zB, VB, czB = planar_avg(Bd / "ElectrostaticPotential.grid.nc")
    assert np.allclose(zA, zB), "z grid mismatch"
    assert abs(cz - czB) < 1e-6, "cell c mismatch"
    dz = zA[1] - zA[0]

    dV = VA - VB
    VA_m = macroscopic_avg(VA, dz, PERIOD_VSE3)
    VB_m = macroscopic_avg(VB, dz, PERIOD_VSE3)
    dV_m = VA_m - VB_m

    z_mol = hf_z_from_struct(Ad / "struct.fdf")
    d = zA - z_mol

    # Gauge correction near cell edges
    far_mask = np.abs(d) > (cz / 2 - PERIOD_VSE3)
    offset = float(np.mean(dV_m[far_mask]))
    dV_m = dV_m - offset
    dV = dV - offset

    return dict(N=N, cz=cz, z=zA, d=d, VA=VA, VB=VB, dV=dV, dVm=dV_m,
                z_mol=z_mol, offset=offset)


def fit_exp_tail(d, dVm, d_min=8.0):
    mask = (d >= d_min) & (np.abs(dVm) > 1e-6)
    if mask.sum() < 5:
        return None, None
    x = d[mask]
    y = np.log(np.abs(dVm[mask]))
    slope, intercept = np.polyfit(x, y, 1)
    lam = -1.0 / slope if slope < 0 else None
    A = np.exp(intercept)
    return lam, A


def main():
    results = [analyze_one(N) for N in NS]

    for r in results:
        arr = np.column_stack([r["z"], r["d"], r["VA"], r["VB"], r["dV"], r["dVm"]])
        np.savetxt(FIG_DIR / f"profile_N{r['N']:02d}.csv", arr,
                   header="z_Ang d_from_mol_Ang V_A_eV V_B_eV dV_eV dV_mac_eV",
                   fmt="%.6e")

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "savefig.transparent": True,
    })
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0),
                                   gridspec_kw={"width_ratios": [1, 2]})

    colors = {14: "#6a1b9a", 20: "#d32f2f", 24: "#1b5e9a"}
    x_lim = 80.0

    for r in results:
        ax1.plot(r["d"], r["dVm"] * 1000.0,
                 color=colors[r["N"]], lw=1.6, label=f"N={r['N']}")
    ax1.axhline(10, ls=":", c="gray", lw=0.8)
    ax1.axhline(-10, ls=":", c="gray", lw=0.8)
    ax1.axhline(0, c="k", lw=0.5)
    ax1.axvline(0, ls="--", c="red", lw=0.8, label="molecule center")
    ax1.set_xlabel(r"$d = z - z_\mathrm{mol}$ (Å)")
    ax1.set_ylabel(r"$\Delta \bar{V}_\mathrm{mac}$ (meV)")
    ax1.set_xlim(-x_lim, x_lim)
    ax1.legend(frameon=False, loc="lower right")

    for r in results:
        d = r["d"]
        y = np.abs(r["dVm"]) * 1000.0
        pos = d >= 0
        ax2.semilogy(d[pos], y[pos], color=colors[r["N"]], lw=1.6, label=f"N={r['N']}")
        lam, A = fit_exp_tail(r["d"], r["dVm"])
        if lam is not None:
            dd = np.linspace(8, r["d"].max(), 50)
            ax2.semilogy(dd, A * 1000.0 * np.exp(-dd / lam),
                         color=colors[r["N"]], lw=0.8, ls="--", alpha=0.6)

    ax2.axhline(10, ls=":", c="gray", lw=0.8, label="10 meV")
    ax2.axhline(1, ls=":", c="lightgray", lw=0.8, label="1 meV")
    ax2.set_xlabel(r"$d$ (Å)")
    ax2.set_ylabel(r"$|\Delta \bar{V}_\mathrm{mac}|$ (meV)")
    ax2.set_ylim(1e-3, 1e4)
    ax2.set_xlim(0, x_lim)
    ax2.legend(frameon=False, loc="upper right")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "perturbation-range2-deltaV.png", dpi=220, bbox_inches="tight")
    MEET_FIG_DIR.mkdir(exist_ok=True, parents=True)
    (MEET_FIG_DIR / "perturbation-v3").mkdir(exist_ok=True, parents=True)
    plt.savefig(MEET_FIG_DIR / "perturbation-v3" / "perturbation-range2-deltaV.png", dpi=220, bbox_inches="tight")
    plt.close()

    summary = []
    for r in results:
        d = r["d"]
        dVm = r["dVm"] * 1000.0
        pos = d >= 0
        half_len = d[pos].max()
        near = np.abs(d) < 6.0
        peak_meV = float(np.max(np.abs(dVm[near])))
        idx10 = np.where((d[pos] > 3.0) & (np.abs(dVm[pos]) < 10.0))[0]
        d10 = float(d[pos][idx10[0]]) if len(idx10) else None
        idx1 = np.where((d[pos] > 3.0) & (np.abs(dVm[pos]) < 1.0))[0]
        d1 = float(d[pos][idx1[0]]) if len(idx1) else None
        tail_meV = float(np.abs(dVm[pos])[-1])
        lam, _ = fit_exp_tail(r["d"], r["dVm"])
        summary.append(dict(
            N=r["N"],
            cell_c_Ang=round(r["cz"], 3),
            half_length_Ang=round(half_len, 2),
            gauge_offset_eV=round(r["offset"], 4),
            peak_dVm_meV=round(peak_meV, 2),
            d_10meV_Ang=None if d10 is None else round(d10, 2),
            d_1meV_Ang=None if d1 is None else round(d1, 2),
            tail_dVm_meV_at_cell_edge=round(tail_meV, 3),
            screening_length_lambda_Ang=None if lam is None else round(lam, 2),
        ))
    (FIG_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
