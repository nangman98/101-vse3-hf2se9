"""Perturbation-range analysis: planar + macroscopic averaged ΔV(z).

Reads ElectrostaticPotential.grid.nc for each (A_mol, B_nomol) pair,
computes ΔV(z), macroscopic averages with VSe3 period (6.27 Å),
fits exponential decay, and emits figure + CSV + JSON summary.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sisl

ROOT = Path(__file__).resolve().parent
CALC = ROOT.parent.parent / "VSe3-Hf2Se9" / "03-calc" / "12-perturbation-range"
FIG_DIR = ROOT
MEET_FIG_DIR = ROOT.parent.parent / "meetings" / "next" / "figures"
NS = [8, 10, 12, 14, 20]
PERIOD_VSE3 = 3.135  # Å, Se-to-Se primitive period (from struct.fdf)


def planar_avg(gridfile: Path) -> tuple[np.ndarray, np.ndarray, float]:
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


def hf_z(struct_fdf: Path) -> float:
    """Mean z of Hf atoms (species 3) in struct.fdf."""
    text = struct_fdf.read_text()
    zs = []
    for line in text.splitlines():
        m = re.match(r"\s*([-\d.Ee+]+)\s+([-\d.Ee+]+)\s+([-\d.Ee+]+)\s+3\s+#", line)
        if m:
            zs.append(float(m.group(3)))
    return float(np.mean(zs))


def analyze_one(N: int):
    Ad = CALC / f"N{N:02d}_A_mol"
    Bd = CALC / f"N{N:02d}_B_nomol"
    zA, VA, cz = planar_avg(Ad / "ElectrostaticPotential.grid.nc")
    zB, VB, czB = planar_avg(Bd / "ElectrostaticPotential.grid.nc")
    assert np.allclose(zA, zB), "z grid mismatch"
    assert abs(cz - czB) < 1e-6, "cell c mismatch"
    dz = zA[1] - zA[0]

    dV = VA - VB  # eV
    VA_m = macroscopic_avg(VA, dz, PERIOD_VSE3)
    VB_m = macroscopic_avg(VB, dz, PERIOD_VSE3)
    dV_m = VA_m - VB_m

    z_mol = hf_z(Ad / "struct.fdf")
    d = zA - z_mol  # distance from molecule center along z (signed)

    # Gauge correction: A and B have different total electrons → ΔV has a
    # constant offset unrelated to the local perturbation. Subtract the value
    # at the cell midpoint (farthest from molecule, d ≈ cz/2).
    mid_idx = int(np.argmax(np.abs(d) % cz))  # point farthest from mol along z
    # Use the region near d ≈ ±cz/2 (last ~period-width window, averaged) as reference
    far_mask = np.abs(d) > (cz / 2 - PERIOD_VSE3)
    offset = float(np.mean(dV_m[far_mask]))
    dV_m = dV_m - offset
    dV = dV - offset

    return dict(
        N=N,
        cz=cz,
        z=zA,
        d=d,
        VA=VA,
        VB=VB,
        dV=dV,
        dVm=dV_m,
        z_mol=z_mol,
        offset=offset,
    )


def fit_exp_tail(d, dVm, d_min=8.0):
    """Fit ln|ΔV_mac| = -d/λ + c on |d| >= d_min region (one-sided, positive d)."""
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

    # Save CSV per N
    for r in results:
        arr = np.column_stack([r["z"], r["d"], r["VA"], r["VB"], r["dV"], r["dVm"]])
        np.savetxt(
            FIG_DIR / f"profile_N{r['N']:02d}.csv",
            arr,
            header="z_Ang d_from_mol_Ang V_A_eV V_B_eV dV_eV dV_mac_eV",
            fmt="%.6e",
        )

    # --- Figure: 2-panel ---
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0), gridspec_kw={"width_ratios": [1, 2]})

    colors = {8: "#1b5e9a", 10: "#a04000", 12: "#2e7d32", 14: "#6a1b9a", 20: "#d32f2f"}
    x_lim = 80.0  # 측정된 d_max = 68.5 Å + 여유

    # Panel 1: linear ΔV_mac vs d
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

    # Panel 2: log |ΔV_mac| vs d  (one-sided, positive side)
    for r in results:
        d = r["d"]
        y = np.abs(r["dVm"]) * 1000.0  # meV
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
    out = FIG_DIR / "perturbation-range-deltaV.png"
    plt.savefig(out, dpi=220, bbox_inches="tight")
    MEET_FIG_DIR.mkdir(exist_ok=True, parents=True)
    plt.savefig(MEET_FIG_DIR / "perturbation-range-deltaV.png", dpi=220, bbox_inches="tight")
    plt.close()

    # --- Numerical summary ---
    summary = []
    for r in results:
        d = r["d"]
        dVm = r["dVm"] * 1000.0  # meV
        pos = d >= 0
        half_len = d[pos].max()
        # peak in region near molecule (|d| < 6 Å)
        near = np.abs(d) < 6.0
        peak_meV = float(np.max(np.abs(dVm[near])))
        # cross threshold 10 meV on positive side
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
