# Figures — meetings/next

다음 미팅 노트(`../next.md`)에서 참조하는 figure 모음.

## Active (next.md 참조)

| File | Section | 내용 | 출처 |
|---|---|---|---|
| `gap-d3.5-relaxed.png` | §1 | `gap, d=3.5 Å` heterostructure relaxed 구조 (a-c plane) | `03-calc/11-hetero-h-relax/gap_d3.5` (matviz-capture) |
| `perturbation-ab-structure.png` | §2 | A=`VSe3+분자` / B=`VSe3-only` 셀 구조 (N=8) | `03-calc/12-perturbation-range` |
| `perturbation-range-deltaV.png` | §2 | ΔV<sub>mac</sub>(d) 선형 + log-linear, N=8/10/12/14/20 | `reports/perturbation-range/` |
| `transport-structure.png` | §3 | Transport device cell 구조 | matviz-capture |
| `transport-band-pdos.png` | §3 | Heterostructure band + PDOS (k<sub>z</sub>=50, w=0.02 eV) | `03-calc/13-transport/bands/02_band_pdos`, `reports/transport-workflow/plot_band_pdos.py` |
| `transport-transmission-kz100.png` | §4 | T(E), 전극 k<sub>z</sub>=100 0bias | `03-calc/13-transport-kz100/0bias`, `reports/transport-workflow/plot_transport_kz100.py` |
| `transport-te-dos-hf2se9.png` | §4 | T(E) log + Hf<sub>2</sub>Se<sub>9</sub>+H DOS dual-axis (amide 07 style) | 동, `01-data/figures/TE_DOS/03_TE_DOS_combined.py` |
| `hf2se9-tp-structure.png` | §구조 수정 | TP (mol_relaxed, C₃) | `04-calcs/00-raw/hf2se9-mol/mol_relaxed.xsf` (matviz-capture) |
| `hf2se9-tap-structure.png` | §구조 수정 | TAP (mol_zettl, Cs) | `04-calcs/00-raw/hf2se9-mol/mol_zettl.xsf` (matviz-capture) |

## `_archive/`

미팅노트에서 더 이상 참조하지 않는 이전 버전 / 탐색 잔재. 비교 필요 시 참고.

### kz=4 transport (이전 미팅 버전)
- `transport-transmission-kz4.png`, `transport-pdos-kz4.png`, `transport-tr-pdos-kz4.png`
- `transport-transmission.png`, `transport-pdos.png`, `transport-tr-pdos.png` (위 kz=4와 bit-identical, 무접미사 원본)
- 출처: `03-calc/13-transport/0bias` (전극 kz=4)

### Heterostructure band+PDOS — k-grid scan
- `transport-band-pdos-kz10.png`, `transport-band-pdos-kz50.png`, `transport-band-pdos-kz100.png`, `transport-band-pdos-kz100-grouped.png`
- 전극 k<sub>z</sub> 수렴 확인용 (10/50/100). Active의 `transport-band-pdos.png`(kz=50)이 대표.
- `transport-band-pdos-180atom.png` — 셀 길이 N 비교 잔재

### 이전 미팅 잔재
- `hf2se9-chain-h-relaxed-band-pdos.png`, `hf2se9-chain-polymer-band-pdos.png`
