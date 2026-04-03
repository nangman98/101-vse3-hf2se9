#!/usr/bin/env python3
"""VSe3 TP/TAP PBE+D2 Band + PDOS — publication quality."""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import sisl

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 40,
    'axes.titlesize': 40,
    'axes.labelsize': 40,
    'xtick.labelsize': 40,
    'ytick.labelsize': 40,
    'legend.fontsize': 28,
    'mathtext.fontset': 'stix',
})

COLORS = {'V': '#7A7A7A', 'Se': '#FF9500'}
PDOS_THRESHOLD = 1e-3

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'VSe3-Hf2Se9', '03-calc')
OUT_DIR = os.path.dirname(__file__)


def parse_pdos(pdos_file):
    tree = ET.parse(pdos_file)
    root = tree.getroot()
    ef = float(root.find('fermi_energy').text.strip())
    ev_text = root.find('energy_values').text.strip()
    energies = np.array([float(x) for x in ev_text.split()])
    species_pdos = {}
    for orb in root.findall('.//orbital'):
        sp = orb.get('species')
        data_text = orb.find('data').text.strip()
        vals = np.array([float(x) for x in data_text.split()])
        if sp not in species_pdos:
            species_pdos[sp] = np.zeros_like(vals)
        species_pdos[sp] += vals
    return energies, ef, species_pdos


def compute_gap(energies, species_pdos, ef):
    total = sum(species_pdos.values())
    above = energies[total > PDOS_THRESHOLD]
    if len(above) == 0:
        return 0.0
    occ = above[above <= ef]
    unocc = above[above > ef]
    if len(occ) == 0 or len(unocc) == 0:
        return 0.0
    return unocc[0] - occ[-1]


def plot_band_pdos(calc_dir, title, out_file, yrange=(-3, 3), pdos_xmax=None):
    # --- Bands ---
    sile = sisl.get_sile(os.path.join(calc_dir, 'siesta.bands'))
    tl, kpath, enk = sile.read_data()
    sisl_ef = sile.read_fermi_level()
    ticks, labels = tl

    # --- PDOS ---
    pdos_file = os.path.join(calc_dir, 'siesta.PDOS')
    energies, pdos_ef, species_pdos = parse_pdos(pdos_file)
    energy_shift = sisl_ef - pdos_ef
    gap = compute_gap(energies, species_pdos, pdos_ef)

    # K-point labels
    labels = [r'$\Gamma$' if l in ('G', 'Gamma', 'gamma') else l for l in labels]

    # --- Figure ---
    fig, (ax_band, ax_pdos) = plt.subplots(
        1, 2, sharey=True, figsize=(14, 10),
        gridspec_kw={'width_ratios': [3, 1], 'wspace': 0.0}
    )

    # == Band panel ==
    for ispin in range(enk.shape[1]):
        for ib in range(enk.shape[2]):
            ax_band.plot(kpath, enk[:, ispin, ib] + energy_shift,
                         color='r', lw=2)

    ax_band.axhline(0, color='darkgrey', ls=':', lw=1)
    ax_band.set_xlim(kpath[0], kpath[-1])
    ax_band.set_ylim(*yrange)
    ax_band.set_ylabel('Energy (eV)', labelpad=10)

    for t in ticks:
        ax_band.axvline(t, color='darkgrey', ls=':', lw=1)
    ax_band.set_xticks(ticks)
    ax_band.set_xticklabels(labels)
    xtl = ax_band.get_xticklabels()
    xtl[0].set_horizontalalignment('left')
    xtl[-1].set_horizontalalignment('right')

    # == PDOS panel ==
    e_shifted = energies - pdos_ef
    mask = (e_shifted >= yrange[0]) & (e_shifted <= yrange[1])

    for sp in ['V', 'Se']:
        if sp in species_pdos:
            ax_pdos.fill_betweenx(
                e_shifted, 0, species_pdos[sp],
                alpha=0.4, color=COLORS[sp], label=sp, lw=0
            )
            ax_pdos.plot(species_pdos[sp], e_shifted,
                         color=COLORS[sp], lw=1.5)

    ax_pdos.axhline(0, color='darkgrey', ls=':', lw=1)
    ax_pdos.set_ylim(*yrange)
    ax_pdos.set_xlabel('PDOS', labelpad=10)
    ax_pdos.legend(loc='upper right', frameon=False, handlelength=1.0)
    ax_pdos.tick_params(axis='y', labelleft=False)
    ax_pdos.set_xlim(left=0)
    if pdos_xmax:
        ax_pdos.set_xlim(0, pdos_xmax)
    else:
        # Auto: max of visible range
        vis_max = 0
        for sp in species_pdos:
            vis_max = max(vis_max, np.max(species_pdos[sp][mask]))
        ax_pdos.set_xlim(0, vis_max * 1.15)

    # Title
    gap_str = f'Gap = {gap*1000:.0f} meV' if gap > 0.001 else 'Metallic'
    ax_band.set_title(f'{title}', pad=15)
    ax_pdos.set_title(gap_str, pad=15, fontsize=32)

    fig.subplots_adjust(left=0.16, right=0.97, bottom=0.12, top=0.88)
    fig.savefig(out_file, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved: {out_file}  ({gap_str})')


if __name__ == '__main__':
    cases = [
        ('01-vse3-tp', r'VSe$_3$ TP — PBE+D2', 'vse3-tp-band-pdos-d2.png'),
        ('02-vse3-tap', r'VSe$_3$ TAP — PBE+D2', 'vse3-tap-band-pdos-d2.png'),
    ]
    for case, title, out_name in cases:
        calc_dir = os.path.join(BASE, case, 'band-pdos-d2')
        out_file = os.path.join(OUT_DIR, out_name)
        plot_band_pdos(calc_dir, title, out_file, yrange=(-3, 3))
