# Perturbation Range 측정 (v3 base)

> **Log**
> - `2026-05-08` — v3 분자 좌표 정정 base로 재진행. N = 14/20/24/30 디렉토리 생성 + N = 14/20/24 SCF (Perlmutter).
> - `2026-05-09` — N = 14 완료, 분석. N = 20/24 RUNNING.
>
> **Tags**: `#perturbation` `#transport-cell-design` `#VSe3` `#Hf2Se9` `#1D-chain` `#hartree-potential` `#v3`

## 목적

기존 [`reports/perturbation-range/perturbation-range.md`](../perturbation-range/perturbation-range.md) (v1, 04-19) 와 동일 — Transport 셀 scattering region 최소 길이 결정. v3 분자 좌표(2026-05-06 정정)가 들어간 새 base relaxed 구조로 재측정.

## v1 대비 차이

| 항목 | v1 (04-19) | v3 (05-08) |
|---|---|---|
| Base 구조 | `11-hetero-h-relax/gap-d3.5/relaxed.xsf` (44 atoms, Lz = 30.52 Å) | `10-hetero-h-term-v3-relax/gap_d3.5/relaxed.xsf` (44 atoms, Lz = 32.50 Å) |
| Hf-Hf | 3.43 Å | 3.23 Å (분자 정정) |
| d (terminal Se-Se 수직) | 3.40 Å | 3.73 Å |
| VSe3 V-V period | 3.135 Å | 3.18 Å |
| N 변종 | 8 / 10 / 12 / 14 / 20 | 14 / 20 / 24 (+ 30 디렉토리만) |

## 원리·SCF 설정

[`perturbation-range/perturbation-range.md`](../perturbation-range/perturbation-range.md) 의 "원리", "두 시스템 설정", "SCF 계산 설정" 그대로. input.fdf 동일 (`MD.Steps 0`, VDW LMKLL, MeshCutoff 500 Ry, kgrid 1×1×1, `SaveElectrostaticPotential T`, `SaveTotalPotential T`, SCF tolerance 1e-8). 단 macroscopic average window는 새 base의 V-V 평균 `a = 3.18 Å`.

`build_perturb_structs.py` (`03-calc/11-perturbation-range/`)로 새 base에서 K = N − 3 unit cell씩 양쪽으로 확장해 N = 14/20/24/30 A_mol/B_nomol 8 디렉토리 생성. 분자 atom indexing은 새 base 기준 0-indexed `range(18, 29)`, top V atom = 43. C_VSE3 = 3.18 Å.

## Results — N = 14 (2026-05-09 우선, N = 20 / 24 진행 중)

### 1. 측정한 양

$$
\Delta\bar{V}_\mathrm{mac}(d) \;=\; \big[\bar{V}^{A}(z) - \bar{V}^{B}(z)\big]_\mathrm{mac} \;-\; c_0,
\qquad d = z - z_\mathrm{mol}
$$

`c_0`는 셀 양 끝 (가장 분자에서 먼 ~`a` 폭) 평균 — A/B 총 전자수 차이로 인한 gauge 어긋남 제거. macro window = `a = 3.18 Å`. `z_mol` = Hf 두 원자 z 평균.

### 2. 핵심 수치

| N | cell c (Å) | half_length (Å) | gauge `c_0` (eV) | peak \|ΔV\| (meV) | `d_10meV` (Å) | `d_1meV` (Å) | tail at edge (meV) | λ fit (Å) |
|---|---|---|---|---|---|---|---|---|
| 14 | 102.46 | 52.76 | −0.067 | 221.46 | 5.79 | 33.9 | 27.98 | 11.28 |

(N = 20, 24 SCF RUNNING — 결과 후 row 추가.)

### 3. 피겨

![ΔV(d) profile](perturbation-range2-deltaV.png)

좌: 선형 ΔV<sub>mac</sub>(d). 우: log |ΔV<sub>mac</sub>|, positive d side + 지수감쇄 fit (점선). x축은 ±80 Å.

### 4. v1 대비 관찰 (N = 14 단독)

| 항목 | v1 N=14 | v3 N=14 | 차이 |
|---|---|---|---|
| peak \|ΔV\| (meV) | 389 | 221 | 약 절반으로 감소 |
| d<sub>10meV</sub> (Å) | 4.57 | 5.79 | 약간 멀리 (+1.2 Å) |
| tail at edge (meV) | 13.1 | 27.98 | 두 배 증가 |
| screening λ (Å) | 10.7 | 11.28 | 거의 동일 |

- v3 분자 정정으로 **peak 약화** — 분자 자체가 단단해져 (Hf-Hf 3.43→3.23 Å) 분자 경계 sharp 감소.
- **tail은 더 큼** — perturbation이 작은 진폭으로 멀리 감. cell c도 v3가 약간 길지만 (102.5 vs 99.5 Å) tail이 두 배라는 건 long-range가 더 살아있음 의미.
- λ 거의 동일 — exp decay 자체는 비슷한 길이로 진행.

→ N = 20, 24 결과로 long-range tail 거동 확정 필요.

### 5. 다음 단계

- [ ] N = 20 SCF 완료 → row 추가
- [ ] N = 24 SCF 완료 → row 추가
- [ ] N 의존성 정리 (v1 곡선과 비교 plot)
- [ ] Threshold 결정 (10 meV vs 1 meV) → transport 셀 길이 산정
- [ ] (선택) N = 30 SCF — 1 meV 기준 cell-size 수렴 재확인
