# Perturbation Range 측정 계획

> **Log**
> - `2026-04-19` — 계획 수립, N = 8/10/12/14 SCF (Perlmutter).
> - `2026-04-21` — N = 8/10/12/14 완료, 분석.
> - `2026-04-22` — N = 20 완료 (Perlmutter, cell 137 Å), 분석 반영.
>
> **Tags**: `#perturbation` `#transport-cell-design` `#VSe3` `#Hf2Se9` `#1D-chain` `#hartree-potential`

## 목적

Transport 셀의 **scattering region 최소 길이**를 정량적으로 결정한다.

`VSe3 + Hf2Se9 분자` 시스템과 `VSe3-only` 시스템의 self-consistent potential을 각각 계산하고, 두 potential의 차이 `ΔV(z)`가 분자로부터 멀어지면서 감쇄하는 길이를 측정한다. 이 길이가 **분자 유무가 전자 구조에 유의미한 영향을 주는 공간 범위**이며, electrode / device 길이 산정의 하한이 된다.

1D chain은 screening이 약해 perturbation이 bulk 3D 대비 멀리 살아남을 가능성이 있으므로, 사전 측정 없이 셀 길이를 추정하는 것은 부정확하다.

## 원리

Kohn-Sham 방정식의 해는 local charge density와 electrostatic potential의 self-consistent 해이다. 분자를 삽입하면 근방 전자 밀도가 재분포되어 Hartree / XC potential이 변하고, 그 변화는 z축을 따라 서서히 감쇄한다.

두 시스템의 planar-averaged potential을 각각

$$
\bar{V}^\text{with}(z) = \frac{1}{A_{xy}} \iint V^\text{with}(x,y,z)\, dx\, dy
$$

으로 정의하고,

$$
\Delta V(z) = \bar{V}^\text{with}(z) - \bar{V}^\text{without}(z)
$$

를 macroscopic average로 한 번 더 부드럽게 한다 (lattice period 하나 window로 이동 평균). Macroscopic averaged `ΔV_mac(z)`가 **threshold 이하로 감쇄하는 z 거리**가 perturbation range이다.

- 기준 threshold: `|ΔV_mac| < 10 meV` (~0.4 kB·T @ 300 K) 를 기본값으로 둔다. 더 엄격히 잡으려면 `1 meV`.
- 감쇄 양상이 exponential에 가까우면 `ΔV_mac(z) ≈ A·exp(-z/λ)` 로 fit해서 screening length `λ` 추출.

## 두 시스템 설정

### System A: VSe3 + Hf2Se9 분자 (`+molecule`)

- 현재 완료된 relaxed 구조 `11-hetero-h-relax/gap-d3.5/relaxed.xsf` 를 base로, **VSe3 사슬을 z축으로 크게 확장**한다.
- 대칭 배치: 중심에 Hf2Se9 분자 1개, 양쪽으로 VSe3 N·unit cell 씩. H termination은 분자 양쪽 Se3 faces에 유지.
- 처음 N은 **N = 8 ~ 10 unit cell 씩** 로 시작 (VSe3 unit cell c ≈ 3.35 Å → 양쪽 27 ~ 34 Å). 감쇄 관찰 후 필요하면 더 늘림.

### System B: VSe3-only (`-molecule`)

- System A에서 Hf2Se9 분자 (Hf 2개 + Se 9개)를 **완전히 제거**.
- 나머지는 System A와 **정확히 동일** — 같은 cell vectors, 같은 VSe3 원자 위치, 같은 H 위치.
- 셀 크기와 원자 위치가 동일해야 planar average 후 z 좌표가 정합한다.
- H의 dangling bond 중성화 효과는 양쪽 시스템에 모두 들어가므로 차이에서 상쇄된다.

⚠️ 확인 필요:
- System B에서 H를 **유지**할지, 분자 제거와 함께 **H도 제거**할지. 유지하는 쪽이 "분자 유무만" 분리한 clean한 비교가 되므로 **기본은 H 유지**를 제안.
- 분자 쪽 H 3개 (원래 Hf2Se9 terminal Se에 붙었던 H가 있는지) — 현재 구조 확인 필요.

## SCF 계산 설정

두 시스템 모두 동일 조건 (차이가 분자 유무만 되도록):

```fdf
SystemLabel              siesta
%include                 struct.fdf

XC.functional            VDW
XC.authors               LMKLL
MeshCutoff               500.0 Ry
ElectronicTemperature    300 K
OccupationFunction       MP
OccupationMPOrder        1

%block kgrid_Monkhorst_Pack
      1      0     0        0.0
      0      1     0        0.0
      0      0     1        0.0
%endblock kgrid_Monkhorst_Pack

SolutionMethod           diagon
Diag.ParallelOverK       T

MD.Steps                 0            # SCF only, no relaxation

MaxSCFIterations         1500
SCF.DM.Converge          T
SCF.DM.Tolerance         1.0d-8
SCF.MustConverge         T
SCF.Mix                  Hamiltonian
SCF.Mixer.Method         Pulay
SCF.Mixer.Weight         0.2
SCF.Mixer.History        10

# Grid I/O
SaveElectrostaticPotential  T     # → ElectrostaticPotential.grid.nc
SaveTotalPotential          T     # → TotalPotential.grid.nc (V_KS)
SaveRho                     F     # 굳이 필요 없음
```

- **k-grid z = 1**이 핵심: 긴 셀이면 band folding으로 충분. z방향 dispersion을 보려는 목적이 아님.
- `MD.Steps 0`: relaxation 없이 single-point SCF 한 번.
- 두 시스템 모두 같은 SCF tolerance, 같은 mixer.

## 후처리 (planar + macroscopic average)

1. `ElectrostaticPotential.grid.nc` 두 파일 읽기 (sisl)
2. (x, y) 평면 평균으로 `V(z)` 1D profile 생성
3. macroscopic average: window = VSe3 unit cell c (~3.35 Å) 크기로 이동 평균
4. `ΔV_mac(z) = V_mac^A(z) − V_mac^B(z)` 계산
5. 플롯: `V^A`, `V^B`, `ΔV`, `ΔV_mac` 4개 곡선 (또는 그룹)
6. Threshold 교차점 z*에서 `z_perturb = z* − z_molecule` 읽기

스크립트 초안 (sisl 기반):

```python
import sisl
import numpy as np
import matplotlib.pyplot as plt

def planar_avg(gridfile):
    g = sisl.get_sile(gridfile).read_grid()
    V = g.grid             # shape (Nx, Ny, Nz)
    z = np.linspace(0, g.lattice.cell[2,2], V.shape[2])
    return z, V.mean(axis=(0, 1))

def macroscopic_avg(z, V, period):
    dz = z[1] - z[0]
    w = int(period / dz)
    kernel = np.ones(w) / w
    return np.convolve(V, kernel, mode='same')

z1, V1 = planar_avg("system_A/ElectrostaticPotential.grid.nc")
z2, V2 = planar_avg("system_B/ElectrostaticPotential.grid.nc")
assert np.allclose(z1, z2), "z grids must match"

period = 3.353   # VSe3 unit c
V1m = macroscopic_avg(z1, V1, period)
V2m = macroscopic_avg(z1, V2, period)
dV = V1 - V2
dVm = V1m - V2m

# molecule center (Hf2Se9 average z)
z_mol = 12.5   # cell 중심에 배치했다면 cell_z / 2

fig, ax = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
ax[0].plot(z1, V1, alpha=0.4, label='V_A (+mol)')
ax[0].plot(z2, V2, alpha=0.4, label='V_B (-mol)')
ax[0].plot(z1, V1m, lw=2, label='V_A macro')
ax[0].plot(z2, V2m, lw=2, label='V_B macro')
ax[0].set_ylabel('V (eV)')
ax[0].legend()

ax[1].plot(z1, dV, alpha=0.3, label='ΔV raw')
ax[1].plot(z1, dVm, lw=2, label='ΔV macro')
ax[1].axhline(0.010, ls='--', c='gray')
ax[1].axhline(-0.010, ls='--', c='gray')
ax[1].axvline(z_mol, ls=':', c='red', label='molecule center')
ax[1].set_ylabel('ΔV (eV)')
ax[1].set_xlabel('z (Å)')
ax[1].legend()
plt.savefig('perturbation_range.png', dpi=200, bbox_inches='tight')
```

## Transport 셀 길이 결정

측정된 perturbation range `z_perturb`로부터:

- **Scattering region 최소 반쪽 길이** = `z_perturb` (분자 한쪽 기준)
- **Scattering region 전체 최소 길이** = `2 · z_perturb` + 분자 길이
- **Electrode 길이**: 별도 결정. Electrode와 scattering region 경계에서 potential이 bulk VSe3와 충분히 맞아야 하므로 electrode 자체도 `~ z_perturb` 이상.
- **Device cell 총 길이** ≥ `2 · z_perturb + L_molecule + 2 · L_electrode`

## 실행 단계

| 단계 | 작업 | 출력 |
|---|---|---|
| 1 | System A/B 구조 생성 (python script, Hf2Se9 제거 = System B) | `system_A/struct.fdf`, `system_B/struct.fdf` |
| 2 | 두 시스템 SCF (SaveElectrostaticPotential T, MD.Steps 0) | `*/ElectrostaticPotential.grid.nc` |
| 3 | Planar + macroscopic average 후처리 | `perturbation_range.png`, `ΔV(z)` 데이터 |
| 4 | Threshold 교차점 / 지수감쇄 fit | `z_perturb`, 필요시 `λ_screen` |
| 5 | 결과 해석 → transport 셀 길이 결정 | 이 문서 업데이트 |

## 결정 필요 사항

1. **System B의 H passivation 유지 여부** — 유지가 기본, 사용자 확인.
2. **초기 VSe3 unit cell 개수 (N)** — 양쪽 8개 (총 17 unit cell + 분자)로 시작 vs 더 작게.
3. **Threshold 기준** — 10 meV (~0.4 kT) vs 1 meV.
4. **Potential 종류** — Hartree만 (`ElectrostaticPotential`) vs Kohn-Sham 전체 (`TotalPotential`). 두 개 다 저장해서 비교하는 것을 제안.

## 주의사항

- 두 SCF에 들어가는 **cell 벡터 / z-grid 개수 / 공간 origin** 이 완전히 동일해야 `V_A(z) − V_B(z)` 가 물리적으로 의미 있다.
- `ElectrostaticPotential` 에는 ion-core electrostatic 도 포함되므로 원자 위치가 살짝 다르면 차이가 실질적으로 무한대(절대값 기준 수십 eV)로 튐. 두 시스템의 원자 좌표가 정확히 일치하도록 구조 생성 스크립트를 작성.
- H 유지할 경우, System B에서 남은 H의 "상대측 Hf2Se9가 사라진" 영향으로 H 자리가 완전 passivate가 아닐 수 있다 (dangling-like state). 이는 `ΔV`에 국소 기여로 반영된다. 해석 시 "분자 유무" + "H 환경 변화"로 분리 가능.

---

## Results & 해석 (`2026-04-22`)

### 1. 측정한 양

$$
\Delta\bar{V}_\mathrm{mac}(d) \;=\; \big[\bar{V}^{A}(z) - \bar{V}^{B}(z)\big]_\mathrm{mac} \;-\; c_0,
\qquad d = z - z_\mathrm{mol}
$$

여기서 `c_0`는 셀 양 끝(가장 분자에서 먼 ~3 Å 구간)에서 평균한 상수 — A/B 총 전자수가 달라 생기는 gauge 어긋남 제거. macro window = VSe3 주기 `a = 3.135 Å`. `z_mol` = Hf 두 원자 z 평균.

### 2. 핵심 수치

| N | cell c (Å) | half_length (Å) | gauge `c_0` (meV) | peak \|ΔV\| (meV) | `d_10meV` (Å) | `d_1meV` (Å) | tail at edge (meV) | λ fit (Å) |
|---|---|---|---|---|---|---|---|---|
| 8  | 61.9  | 30.9 | −37.9 | 405 | 4.65 | —    | 15.1 | 5.9  |
| 10 | 74.4  | 37.1 | −37.4 | 392 | 4.58 | —    | 15.4 | 7.5  |
| 12 | 87.0  | 43.4 | −34.7 | 387 | 4.57 | —    | 14.2 | 9.0  |
| 14 | 99.5  | 49.7 | −31.8 | 389 | 4.57 | —    | 13.1 | 10.7 |
| 20 | 137.1 | 68.5 | −24.5 | 384 | 4.57 | 38.7 |  9.8 | 17.4 |

(`d_1meV` 칸의 `—`는 셀 크기 한계로 `|ΔV_mac| < 1 meV` 영역이 잡히지 않음을 의미.)

### 3. 피겨 부위별 의미

![ΔV(d) profile](perturbation-range-deltaV.png)

| 부위 | 의미 |
|---|---|
| (A) 좌 패널 d≈0 −400 meV spike | 분자 자리 자체. 원자 종류가 다르므로 ΔV 큰 게 당연. **해석 대상 아님** — 분자 위치 마커 |
| (B) d = 0 ~ 5 Å 가파른 감쇄 | 분자 직접 영향권. `d ≈ 4.6 Å`에서 10 meV 아래로 → VSe3 격자주기(3.14 Å)의 약 1.5배. 모든 N에서 동일 |
| (C) 우 패널 log plot V자 cusp | ΔV가 부호 바뀌는 자리. 진짜 0 아님. **1D Friedel-like 진동**의 흔적 (1D는 screening이 약해 진동 꼬리가 멀리 감) |
| (D) 셀 끝 tail | N = 8→14에서 `15.1 → 13.1 meV`로 정체하다가 N = 20에서 `9.8 meV`로 떨어짐. cell-size 약의존성 확인 |
| (E) 좌 패널 분자 근방 곡선 겹침 | 분자 주변 모양이 cell 크기에 무관 → **N = 8부터 분자가 자기 image 안 느낌** |

### 4. 측정값

| 측정 항목 | 값 | 신뢰도 |
|---|---|---|
| 분자 직접 영향권 (10 meV 기준) | `d_10meV ≈ 4.6 Å` (≈ 1.5 VSe3 주기) | **높음** — 다섯 N 모두 일치 |
| 1 meV 기준 영향권 | `d_1meV ≈ 38.7 Å` (N = 20에서만 관찰) | **중간** — 더 긴 셀에서 재확인 필요 |
| 진동 tail 크기 | `15.1 → 15.4 → 14.2 → 13.1 → 9.8 meV` (N = 8→20) | — cell-size에 약하게 의존 |
| Screening length λ | `5.9 → 7.5 → 9.0 → 10.7 → 17.4 Å` (N에 따라 증가) | **낮음** — 단순 exponential fit이 진동 tail에 부적합 |

### 5. Transport 셀 길이 — 측정한 N 기반

- Primary decay (`|ΔV_mac| < 10 meV`) 는 `d ≈ 4.6 Å`에서 모든 N이 동일하게 달성 — 분자 영향권은 N = 8부터 수렴.
- 이전 (N ≤ 14) 관측에서 "cell-size 무관 floor" 로 보였던 꼬리는 N = 20에서 `13.1 → 9.8 meV` 로 25% 감소. 완전한 floor는 아니며 약의존. **1D Friedel-like 진동이지만 cell 크기에 따라 조금씩 죽어 감**.
- 1 meV 기준으로는 N = 20 (분자 한쪽 `d ≈ 68 Å` 가능) 에서 `d_1meV ≈ 38.7 Å` 확보. 1 meV 기준을 고수하려면 scattering 반쪽 ≥ 40 Å.

### 6. 한 문장 결론

> Hf2Se9 분자의 영향은 VSe3 체인을 `d ≈ 4.6 Å`까지 10 meV 이상으로 흔들고, 그 너머에서는 cell 크기에 약하게 의존하는 1D 진동 꼬리로 남는다. 10 meV 기준이면 N = 8 setup 으로 충분, 1 meV 기준이면 최소 N = 20 (분자 한쪽 ≥ 40 Å) 이 필요.

### 7. 다음 단계

- [x] N = 8 / 10 / 12 / 14 SCF 완료
- [x] N = 20 SCF 완료, cell-edge tail 10 meV 이하 확인, `d_1meV ≈ 38.7 Å`
- [ ] Threshold 결정 (10 meV vs 1 meV)
- [ ] 결정된 N으로 transport device 셀 조립 → electrode/scattering 분리
- [ ] (선택) N = 30 SCF — 1 meV 기준의 cell-size 수렴 재확인

