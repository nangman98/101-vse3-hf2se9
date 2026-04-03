#!/usr/bin/env python3
"""Plot initial structures: side view (xz) + top view (xy).

Output:
  mx3-chains.png  — MX₃ TP vs TAP, side + top views (4×2)
  hf2se9.png      — Hf₂Se₉ molecule vs chain
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

CALC_DIR = Path(__file__).resolve().parent.parent.parent / "VSe3-Hf2Se9" / "03-calc"
OUT_DIR = Path(__file__).resolve().parent

ATOM_STYLE = {
    23: {"sym": "V",  "color": "#E04040", "size": 200, "ec": "#A02020"},
    34: {"sym": "Se", "color": "#FFA500", "size": 150, "ec": "#CC8400"},
    52: {"sym": "Te", "color": "#CC7722", "size": 170, "ec": "#995510"},
    72: {"sym": "Hf", "color": "#4CC9F0", "size": 220, "ec": "#3090B0"},
}


def read_xsf(filepath):
    lines = Path(filepath).read_text().strip().split("\n")
    cell, atoms = [], []
    i = 0
    while i < len(lines):
        if "PRIMVEC" in lines[i]:
            for j in range(1, 4):
                cell.append([float(p) for p in lines[i + j].split()[:3]])
            i += 4
        elif "PRIMCOORD" in lines[i]:
            natoms = int(lines[i + 1].split()[0])
            for j in range(2, 2 + natoms):
                parts = lines[i + j].split()
                atoms.append((int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])))
            i += 2 + natoms
        else:
            i += 1
    return np.array(cell), atoms


def get_bonds(atoms_xyz, cutoff=3.0):
    """Find bonds from list of (x, y, z) tuples."""
    bonds = []
    for i in range(len(atoms_xyz)):
        for j in range(i + 1, len(atoms_xyz)):
            d = np.linalg.norm(np.array(atoms_xyz[i]) - np.array(atoms_xyz[j]))
            if 0.1 < d < cutoff:
                bonds.append((i, j))
    return bonds


def clean_ax(ax):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


# ── Side view (xz projection) ─────────────────────────────────────────

def plot_side(ax, xsf_path, title, n_repeat=3, bond_cutoff=3.0):
    cell, atoms = read_xsf(xsf_path)
    c = cell[2, 2]

    all_atoms = []
    for n in range(n_repeat):
        for Z, x, y, z in atoms:
            all_atoms.append((Z, x, y, z + n * c))

    cx = np.mean([a[1] for a in all_atoms])

    # Bonds
    xyz = [(a[1], a[2], a[3]) for a in all_atoms]
    Zs = [a[0] for a in all_atoms]
    for i, j in get_bonds(xyz, bond_cutoff):
        ax.plot([xyz[i][0] - cx, xyz[j][0] - cx], [xyz[i][2], xyz[j][2]],
                color="#AAAAAA", linewidth=1.5, zorder=1)

    # Atoms
    for Z, x, y, z in sorted(all_atoms, key=lambda a: ATOM_STYLE[a[0]]["size"]):
        s = ATOM_STYLE[Z]
        ax.scatter(x - cx, z, s=s["size"], c=s["color"],
                   edgecolors=s["ec"], linewidth=1.2, zorder=3)

    # Cell boundaries
    for n in range(n_repeat + 1):
        ax.axhline(y=n * c, color="#DDDDDD", linewidth=0.8, linestyle="--", zorder=0)

    # c annotation
    ax.annotate("", xy=(3.2, c), xytext=(3.2, 0),
                arrowprops=dict(arrowstyle="<->", color="#666666", lw=1.2))
    ax.text(3.5, c / 2, f"c={c:.2f} Å", fontsize=8, color="#666666",
            rotation=90, va="center", ha="left")

    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.set_xlim(-4.5, 5.0)
    clean_ax(ax)


# ── Top view (xy projection) ──────────────────────────────────────────

def plot_top(ax, xsf_path, title, bond_cutoff=3.0):
    cell, atoms = read_xsf(xsf_path)

    cx = np.mean([a[1] for a in atoms])
    cy = np.mean([a[2] for a in atoms])

    # Bonds (use 3D distance for bond detection)
    xyz = [(a[1], a[2], a[3]) for a in atoms]
    for i, j in get_bonds(xyz, bond_cutoff):
        ax.plot([xyz[i][0] - cx, xyz[j][0] - cx],
                [xyz[i][1] - cy, xyz[j][1] - cy],
                color="#AAAAAA", linewidth=1.5, zorder=1)

    # Draw triangles connecting X₃ groups
    Z_chalc = max(set(a[0] for a in atoms), key=lambda z: sum(1 for a in atoms if a[0] == z))
    chalc_by_z = {}
    for Z, x, y, z in atoms:
        if Z == Z_chalc:
            zk = round(z, 1)
            chalc_by_z.setdefault(zk, []).append((x - cx, y - cy))
    for zk, pts in chalc_by_z.items():
        if len(pts) == 3:
            pts_closed = pts + [pts[0]]
            xs = [p[0] for p in pts_closed]
            ys = [p[1] for p in pts_closed]
            ax.plot(xs, ys, color="#CCCCCC", linewidth=1.0, linestyle="-", zorder=0)

    # Atoms (different alpha for different z to show depth)
    z_vals = sorted(set(round(a[3], 1) for a in atoms))
    z_min, z_max = min(z_vals), max(z_vals)
    z_range = z_max - z_min if z_max > z_min else 1.0

    for Z, x, y, z in sorted(atoms, key=lambda a: a[3]):
        s = ATOM_STYLE[Z]
        # Lighter for lower z, darker for higher z
        alpha = min(1.0, 0.5 + 0.5 * (z - z_min) / z_range)
        ax.scatter(x - cx, y - cy, s=s["size"] * 1.2, c=s["color"],
                   edgecolors=s["ec"], linewidth=1.2, zorder=3, alpha=alpha)

    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    lim = 3.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    clean_ax(ax)


# ── Hf2Se9 ─────────────────────────────────────────────────────────────

def plot_hf2se9_side(ax, xsf_path, title, n_repeat=1, bond_cutoff=3.2):
    cell, atoms = read_xsf(xsf_path)
    c = cell[2, 2]

    all_atoms = []
    for n in range(n_repeat):
        for Z, x, y, z in atoms:
            all_atoms.append((Z, x, y, z + n * c))

    cx = np.mean([a[1] for a in all_atoms])
    cz = np.mean([a[3] for a in all_atoms])

    xyz = [(a[1], a[2], a[3]) for a in all_atoms]
    for i, j in get_bonds(xyz, bond_cutoff):
        ax.plot([xyz[i][0] - cx, xyz[j][0] - cx],
                [xyz[i][2] - cz, xyz[j][2] - cz],
                color="#AAAAAA", linewidth=1.5, zorder=1)

    for Z, x, y, z in sorted(all_atoms, key=lambda a: ATOM_STYLE[a[0]]["size"]):
        s = ATOM_STYLE[Z]
        ax.scatter(x - cx, z - cz, s=s["size"], c=s["color"],
                   edgecolors=s["ec"], linewidth=1.2, zorder=3)

    # Hf-Hf annotation
    hf = [(x - cx, z - cz) for Z, x, y, z in all_atoms if Z == 72]
    if len(hf) >= 2:
        hf_raw = [(x, y, z) for Z, x, y, z in all_atoms if Z == 72]
        d_hf = np.linalg.norm(np.array(hf_raw[0]) - np.array(hf_raw[1]))
        ax.annotate("", xy=(hf[0][0] + 0.15, hf[0][1]),
                    xytext=(hf[1][0] + 0.15, hf[1][1]),
                    arrowprops=dict(arrowstyle="<->", color="#E04040", lw=1.2))
        mid = ((hf[0][0] + hf[1][0]) / 2 + 0.5, (hf[0][1] + hf[1][1]) / 2)
        ax.text(mid[0], mid[1], f"Hf-Hf\n{d_hf:.2f} Å",
                fontsize=8, color="#E04040", ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#E04040", alpha=0.8))

    if n_repeat > 1:
        for n in range(n_repeat + 1):
            ax.axhline(y=n * c - cz, color="#DDDDDD", linewidth=0.8, linestyle="--", zorder=0)

    # Auto-fit with padding
    all_x = [a[1] - cx for a in all_atoms]
    all_z = [a[3] - cz for a in all_atoms]
    pad = 1.5
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_z) - pad, max(all_z) + pad)

    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    clean_ax(ax)


# ── Legend ──────────────────────────────────────────────────────────────

def add_legend(fig, elements):
    handles = []
    for Z in elements:
        s = ATOM_STYLE[Z]
        h = plt.scatter([], [], s=80, c=s["color"], edgecolors=s["ec"],
                        linewidth=1.0, label=s["sym"])
        handles.append(h)
    fig.legend(handles=handles, loc="lower center", ncol=len(elements),
              fontsize=10, frameon=True, fancybox=True, framealpha=0.9,
              edgecolor="#CCCCCC", columnspacing=1.5)


# ── Main ───────────────────────────────────────────────────────────────

def main():
    cases = [
        ("01-vse3-tp-relax",  "VSe₃ TP"),
        ("02-vse3-tap-relax", "VSe₃ TAP"),
        ("03-vte3-tp-relax",  "VTe₃ TP"),
        ("04-vte3-tap-relax", "VTe₃ TAP"),
    ]

    # ── Figure 1: MX3 chains ──────────────────────────────────────
    fig, axes = plt.subplots(2, 4, figsize=(16, 14))
    fig.suptitle("MX₃ Chain — Initial Structures", fontsize=14, fontweight="bold")

    for col, (case, title) in enumerate(cases):
        xsf = CALC_DIR / case / "struct.xsf"
        plot_top(axes[0, col], xsf, f"{title}\n(top view)")
        plot_side(axes[1, col], xsf, f"(side view)", n_repeat=3)

    fig.subplots_adjust(bottom=0.05, top=0.93, hspace=0.20, wspace=0.15)
    add_legend(fig, [23, 34, 52])
    fig.savefig(OUT_DIR / "mx3-chains.png", dpi=150, facecolor="white", bbox_inches="tight")
    print(f"Saved: {OUT_DIR / 'mx3-chains.png'}")

    # ── Figure 2: Hf2Se9 ──────────────────────────────────────────
    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 7))
    fig2.suptitle("Hf₂Se₉ — Initial Structures", fontsize=14, fontweight="bold", y=0.98)

    plot_hf2se9_side(axes2[0], CALC_DIR / "05-hf2se9-mol-relax" / "struct.xsf",
                     "Hf₂Se₉ molecule", n_repeat=1, bond_cutoff=3.2)
    plot_hf2se9_side(axes2[1], CALC_DIR / "06-hf2se9-chain-relax" / "struct.xsf",
                     "Hf₂Se₉ chain", n_repeat=2, bond_cutoff=3.2)

    fig2.subplots_adjust(bottom=0.08, top=0.90, wspace=0.30)
    add_legend(fig2, [72, 34])
    fig2.savefig(OUT_DIR / "hf2se9.png", dpi=150, facecolor="white", bbox_inches="tight")
    print(f"Saved: {OUT_DIR / 'hf2se9.png'}")

    plt.close("all")


if __name__ == "__main__":
    main()
