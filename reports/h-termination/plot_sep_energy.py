#!/usr/bin/env python3
"""Separation energy comparison: H-terminated vs bare heterostructure"""
import matplotlib.pyplot as plt
import numpy as np

# 10-hetero-h-term bond (vdW-DF2, 44 atoms)
d_bond = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
E_bond = [-114635.601367, -114657.580874, -114662.359735,
          -114663.189723, -114662.981889, -114662.505032]

# 08-hetero-v2 (vdW-DF2, 38 atoms, no H)
d_bare = [2.5, 3.0, 3.5, 4.0]
E_bare = [-114571.125790, -114569.015497, -114566.523081, -114564.917614]

E_sep_bond = np.array(E_bond) - E_bond[-1]
E_sep_bare = np.array(E_bare) - E_bare[-1]

fig, ax = plt.subplots(figsize=(5, 3.8))

ax.plot(d_bond, E_sep_bond, 'o-', color='#1565C0', lw=1.8, ms=5, label='w/ H')
ax.plot(d_bare, E_sep_bare, 's--', color='#C62828', lw=1.8, ms=5, label='w/o H')

# minimum marker only (no text)
i_min = np.argmin(E_sep_bond)
ax.plot(d_bond[i_min], E_sep_bond[i_min], 'o', color='#1565C0', ms=10,
        mfc='none', mew=2, zorder=5)

# experiment band
ax.axvspan(3.3, 3.7, alpha=0.06, color='#4CAF50', zorder=0)
ax.text(3.5, -7.3, 'expt.', fontsize=8, color='#388E3C', ha='center')

ax.set_xlabel('Interface separation ($\\AA$)', fontsize=11)
ax.set_ylabel('$E_{\\mathrm{sep}}$ (eV)', fontsize=11)
ax.legend(fontsize=9, framealpha=0.8, edgecolor='#ccc')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_xlim(2.3, 4.7)
ax.set_ylim(-8, 6)

plt.tight_layout()
plt.savefig('sep_energy_h_term.png', dpi=200, transparent=True, bbox_inches='tight')
print('Saved: sep_energy_h_term.png')
