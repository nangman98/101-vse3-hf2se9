import os, re, glob
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 22,
    "axes.labelsize": 30,
    "axes.linewidth": 2.0,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.major.size": 8,
    "ytick.major.size": 8,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    "xtick.labelsize": 24,
    "ytick.labelsize": 24,
    "mathtext.fontset": "stix",
    "legend.frameon": False,
})

ROOT = "/Users/nangman/Library/CloudStorage/GoogleDrive-jnmpsb951@gmail.com/내 드라이브/project/101-vse3-hf2se9/VSe3-Hf2Se9/03-calc"
D_MIN = 2.5

def get_E(path):
    E = None
    with open(path) as f:
        for line in f:
            m = re.search(r'siesta:\s+Total\s*=\s*(-?\d+\.\d+)', line)
            if m:
                E = float(m.group(1))
    return E

def collect(sub):
    pts = []
    for d_dir in sorted(glob.glob(os.path.join(ROOT, sub, "d_*"))):
        if not (os.path.exists(os.path.join(d_dir, "siesta.stdout"))
                and os.path.exists(os.path.join(d_dir, "0_NORMAL_EXIT"))):
            continue
        d = float(os.path.basename(d_dir).replace("d_", ""))
        if d < D_MIN:
            continue
        E = get_E(os.path.join(d_dir, "siesta.stdout"))
        if E is not None:
            pts.append((d, E))
    pts.sort()
    return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

# ─────── Plot A: H-term 3 mode ───────
hterm = {
    "gap":  ("10-hetero-h-term-v3/gap",  "#1f77b4", "o"),
    "bond": ("10-hetero-h-term-v3/bond", "#2ca02c", "D"),
    "tilt": ("10-hetero-h-term-v3/tilt", "#d62728", "^"),
}
data_h = {label: collect(sub) for label, (sub, _, _) in hterm.items()}
E_ref = min(E.min() for _, E in data_h.values() if len(E))
print(f"H-term reference E = {E_ref:.4f} eV")

fig, ax = plt.subplots(figsize=(7, 6))
for label, (sub, c, m) in hterm.items():
    ds, Es = data_h[label]
    if not len(ds):
        continue
    dE = Es - E_ref
    ax.plot(ds, dE, '-' + m, color=c, mfc=c, lw=2.2, ms=9, label=label)
    imin = int(np.argmin(dE))
    ax.plot(ds[imin], dE[imin], m, color=c, mfc='white', mew=2.0, ms=12, zorder=5)
ax.set_xlabel(r'$d$ (Å)')
ax.set_ylabel(r'$\Delta E$ (eV)')
ax.set_ylim(-1, 20)
ax.legend(loc='upper right', fontsize=22)
out = os.path.join(os.path.dirname(__file__), "h-term-three-mode-v3.png")
plt.savefig(out, transparent=True, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"saved: {out}")

# ─────── Plot B: Sandwich (no H) ───────
ds, Es = collect("08-hetero-v3")
dE = Es - Es.min()
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(ds, dE, '-s', color="#444444", mfc="#444444", lw=2.2, ms=9)
imin = int(np.argmin(dE))
ax.plot(ds[imin], dE[imin], 's', color="#444444", mfc='white', mew=2.0, ms=12, zorder=5)
ax.set_xlabel(r'$d$ (Å)')
ax.set_ylabel(r'$\Delta E$ (eV)')
out = os.path.join(os.path.dirname(__file__), "sandwich-no-h-v3.png")
plt.savefig(out, transparent=True, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"saved: {out}")

# ─────── raw 출력 ───────
print()
print("=== raw E (eV), d >= 2.5 ===")
for label in ["gap", "bond", "tilt"]:
    ds, Es = data_h[label]
    print(f"-- H-term {label} --")
    for d, E in zip(ds, Es):
        print(f"  d={d:.2f}  E={E:.4f}  dE_vs_gap_min={E-E_ref:+.4f}")
print("-- Sandwich (no H) --")
for d, E in zip(*collect("08-hetero-v3")):
    print(f"  d={d:.2f}  E={E:.4f}")
