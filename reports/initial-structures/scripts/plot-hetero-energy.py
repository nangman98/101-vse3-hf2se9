import matplotlib.pyplot as plt
import numpy as np

sep = [2.5, 3.0, 3.5, 4.0]

# Total energies (eV)
het07   = np.array([-114568.0482, -114566.3168, -114565.1530, -114564.3151])  # vdW-DF2, V-Se3-V
het08   = np.array([-114571.1258, -114569.0155, -114566.5231, -114564.9176])  # vdW-DF2, Se3-V-Se3
het09   = np.array([-114025.6708, -114022.2510, -114019.2032, -114017.3596])  # PBE+D2,  Se3-V-Se3

# Relative energy w.r.t. d=4.0
het07_rel = het07 - het07[-1]
het08_rel = het08 - het08[-1]
het09_rel = het09 - het09[-1]

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

datasets = [
    (het07_rel, 'vdW-DF2\nV-Se$_3$-V (asymmetric)', '#E91E63', 'o',
     'vdW-DF2 relaxed struct\nasymmetric interface'),
    (het08_rel, 'vdW-DF2\nSe$_3$-V-Se$_3$ (symmetric)', '#9C27B0', 's',
     'vdW-DF2 relaxed struct\nsymmetric interface'),
    (het09_rel, 'PBE+D2\nSe$_3$-V-Se$_3$ (symmetric)', '#4CAF50', '^',
     'PBE+D2 relaxed struct\nsymmetric interface'),
]

for ax, (data, title, color, marker, note) in zip(axes, datasets):
    ax.plot(sep, data, f'{marker}-', color=color, linewidth=2, markersize=8)
    ax.set_xlabel('Separation (Ang)', fontsize=12)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(sep)
    for s, e in zip(sep, data):
        ax.annotate(f'{e:.2f}', (s, e), textcoords='offset points',
                    xytext=(0, 10), ha='center', fontsize=9)
    ax.text(0.05, 0.05, note, transform=ax.transAxes, fontsize=8,
            verticalalignment='bottom', bbox=dict(boxstyle='round', alpha=0.1))

axes[0].set_ylabel('Relative Energy (eV, ref: d=4.0)', fontsize=12)

fig.suptitle('Heterostructure Energy vs Separation', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('hetero-energy-vs-sep.png', dpi=150, bbox_inches='tight')
print('Saved hetero-energy-vs-sep.png')
