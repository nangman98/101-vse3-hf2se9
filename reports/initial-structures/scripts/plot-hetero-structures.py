"""Render 3 hetero structures individually and as comparison (d=3.5, side view)."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ELEMENT_COLORS = {'V': '#FF6D00', 'Se': '#76FF03', 'Hf': '#4CC9F0'}
ELEMENT_RADII = {'V': 0.35, 'Se': 0.30, 'Hf': 0.40}
SCALE = 80

def parse_xsf(path):
    atoms = []
    Z_MAP = {23: 'V', 34: 'Se', 72: 'Hf'}
    with open(path) as f:
        lines = f.readlines()
    reading = False
    for line in lines:
        s = line.strip()
        if s.startswith('PRIMCOORD'):
            reading = True
            continue
        if reading:
            parts = s.split()
            if len(parts) >= 4:
                try:
                    Z = int(parts[0])
                    if Z in Z_MAP:
                        atoms.append((Z_MAP[Z], float(parts[1]), float(parts[2]), float(parts[3])))
                except ValueError:
                    pass
    return atoms

def parse_xyz(path):
    atoms = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines[2:]:
        parts = line.split()
        if len(parts) >= 4:
            atoms.append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))
    return atoms

def draw_structure(ax, atoms, title):
    atoms_sorted = sorted(atoms, key=lambda a: a[2])
    for elem, x, y, z in atoms_sorted:
        color = ELEMENT_COLORS.get(elem, '#999')
        r = ELEMENT_RADII.get(elem, 0.3) * SCALE
        ax.scatter(x, z, s=r**2, c=color, edgecolors='#333', linewidths=0.5,
                   zorder=3 if elem == 'Hf' else 2)
    # Hf2Se9 region shading
    hf_zs = [a[3] for a in atoms if a[0] == 'Hf']
    if hf_zs:
        chain_se = [a[3] for a in atoms if a[0] == 'Se' and min(hf_zs)-3 < a[3] < max(hf_zs)+3]
        rmin = min(chain_se + hf_zs) - 0.5
        rmax = max(chain_se + hf_zs) + 0.5
        ax.axhspan(rmin, rmax, alpha=0.08, color='#4CC9F0', zorder=0)
        ax.text(16.3, (rmin+rmax)/2, 'Hf$_2$Se$_9$', fontsize=10,
                ha='left', va='center', color='#0088AA', fontweight='bold')
    zs = [a[3] for a in atoms]
    ax.set_xlim(8, 17)
    ax.set_ylim(min(zs)-1.5, max(zs)+1.5)
    ax.set_xlabel('x (Ang)', fontsize=11)
    ax.set_ylabel('z (Ang)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')

base = '/Users/nangman/Library/CloudStorage/GoogleDrive-jnmpsb951@gmail.com/내 드라이브/101-vse3-hf2se9/VSe3-Hf2Se9/03-calc'
outdir = '/Users/nangman/Library/CloudStorage/GoogleDrive-jnmpsb951@gmail.com/내 드라이브/101-vse3-hf2se9/reports/initial-structures'

cases = [
    ('07-hetero-d3.5', '07-hetero (PBE, no vdW)\nd = 3.5 Ang, V-Se$_3$-V ordering',
     parse_xsf(f'{base}/07-hetero/d_3.5/hetero.xsf')),
    ('08-hetero-v2-d3.5', '08-hetero-v2 (vdW-DF2)\nd = 3.5 Ang, Se$_3$-V ordering',
     parse_xyz(f'{base}/08-hetero-v2/d_3.5/hetero.xyz')),
    ('09-hetero-d2-d3.5', '09-hetero-d2 (PBE+D2)\nd = 3.5 Ang, Se$_3$-V ordering',
     parse_xyz(f'{base}/09-hetero-d2/d_3.5/hetero.xyz')),
]

legend_elements = [
    mpatches.Patch(facecolor=ELEMENT_COLORS['V'], edgecolor='#333', label='V'),
    mpatches.Patch(facecolor=ELEMENT_COLORS['Se'], edgecolor='#333', label='Se'),
    mpatches.Patch(facecolor=ELEMENT_COLORS['Hf'], edgecolor='#333', label='Hf'),
]

# --- Individual renders ---
for fname, title, atoms in cases:
    fig, ax = plt.subplots(figsize=(5, 9))
    draw_structure(ax, atoms, title)
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    plt.tight_layout()
    fig.savefig(f'{outdir}/{fname}.png', dpi=150, bbox_inches='tight')
    print(f'Saved {fname}.png')
    plt.close(fig)

# --- Comparison (3 panels) ---
fig, axes = plt.subplots(1, 3, figsize=(16, 9), sharey=True)
for ax, (fname, title, atoms) in zip(axes, cases):
    draw_structure(ax, atoms, title)
    if ax != axes[0]:
        ax.set_ylabel('')
fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=11,
           frameon=True, bbox_to_anchor=(0.5, -0.01))
fig.suptitle('Heterostructure Comparison (d = 3.5 Ang, side view)', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(f'{outdir}/hetero-structures-compare.png', dpi=150, bbox_inches='tight')
print('Saved hetero-structures-compare.png')
plt.close(fig)
