# A2 (PBE+D2) SCF 수렴 실패 분석

## 문제

Phase A stability test에서 A2 (PBE+D2)만 SCF가 수렴하지 않는다.
A1 (PBE), A3 (vdW-DF2), A4 (PBE+D3)는 동일한 SCF 설정으로 수렴 완료.

## 실행 이력

| 시도 | 큐 / 노드 | 결과 |
|------|-----------|------|
| r1 | flat 1노드 | `-A` 플래그 누락 → 미실행 |
| r2 | flat 2노드 | 동일 에러 |
| r3 | flat 3노드 64MPI | **step 68에서 SCF_NOT_CONV** (1500 iter, dDmax=3.9×10⁻⁴) |
| r4 | debug 2노드 (DM restart) | **step 0에서 SCF_NOT_CONV** (1500 iter, dDmax=2.4×10⁻³, 악화) |
| v2 | debug 2노드 (Tol 1e-6, Weight 0.15) | 진행 중 |

## 다른 케이스와의 비교

| 케이스 | Functional | SCF/step | 마지막 dDmax | Geom steps | 결과 |
|--------|-----------|----------|-------------|------------|------|
| A1 (PBE) | PBE | ~55 | 0.000000 | 14 | ✅ 수렴 |
| A3 (vdW-DF2) | vdW-DF2 | — | — | 13 | ✅ 수렴 |
| A4 (PBE+D3) | PBE+D3(BJ) | ~55 | 0.000000 | 14 | ✅ 수렴 |
| **A2 (PBE+D2)** | **PBE+D2** | **1500** | **3.9×10⁻⁴** | **68 (미완)** | **❌ SCF 미수렴** |

공통 설정: `SCF.DM.Tolerance 1e-10`, `SCF.Mixer.Weight 0.3`, `MaxSCFIterations 1500`

## 원인 분석

### 1. SCF.DM.Tolerance 1e-10이 과도하게 타이트

`SCF.DM.Tolerance`는 이전 density matrix와 새 density matrix의 차이(dDmax)가 이 값 이하일 때 "수렴"으로 판정하는 기준이다.

- A1/A4: dDmax가 0까지 떨어져서 1e-10 통과
- A2: dDmax가 3.9×10⁻⁴에서 진동하며 더 안 떨어짐
- Relaxation에서 force 정확도 0.01 eV/Å를 얻으려면 **1e-4~1e-5면 충분**

### 2. Grimme D2의 고정 C₆가 geometry를 불리한 방향으로 유도

D2와 D3(BJ)는 모두 사후 보정이지만, **SCF 자체에는 영향을 주지 않는다** — force와 total energy에만 보정이 더해진다. 그러나:

- D2의 force가 geometry optimizer(Broyden)를 통해 **원자 위치를 변경**
- 68 step 동안 D2 force에 의해 이동한 geometry에서 **Hf 5d 오비탈이 near-degenerate**
- Near-degenerate 상태 → charge sloshing (전하가 SCF iteration마다 왔다갔다)
- dDmax가 ~10⁻⁴에서 진동하며 10⁻¹⁰에 도달 불가

A1/A4가 14 step만에 수렴한 반면 A2가 68 step까지 간 것도 이 문제를 보여준다: D2의 고정 C₆ 계수가 Hf에 대해 부정확하여 PES(potential energy surface)가 거칠어졌다.

### 3. DM restart가 오히려 악화시킴

| | r3 (원본) | r4 (DM restart) |
|---|---|---|
| Geom step | 68 | 0 |
| dDmax | 3.9×10⁻⁴ | **2.4×10⁻³** (6배 악화) |

미수렴 DM(step 68에서 1e-10 못 맞추고 abort된 시점)으로 restart → 오히려 SCF 초기 조건이 나빠짐.

### 4. D3(BJ) 결과

A4(PBE+D3) = A1(PBE): STRUCT_OUT이 동일. Isolated molecule에서 D3(BJ) 보정이 구조에 영향을 주지 않았음.

## 해결: A2-v2

변경점 (2개만):

| 파라미터 | A2 원본 | A2-v2 |
|----------|--------|-------|
| `SCF.DM.Tolerance` | 1.0d-10 | **1.0d-6** |
| `SCF.Mixer.Weight` | 0.3 | **0.15** |

- **Tolerance 1e-6**: relaxation force 정확도에 충분. 1e-10은 이 계에서 도달 불가.
- **Weight 0.15**: 새 density를 15%만 반영 → charge sloshing 억제, 수렴 안정화.

나머지 설정(basis, functional, k-grid, optimizer 등)은 원본과 동일.

## SCF 파라미터 의미 정리

### SCF.DM.Tolerance

매 SCF iteration에서 density matrix 변화량(dDmax)이 이 값보다 작으면 "수렴":

| 값 | 정밀도 수준 | 용도 |
|----|-----------|------|
| 1e-4 | Force ~0.01 eV/Å | Relaxation (최소한) |
| 1e-5~1e-6 | Force ~0.001 eV/Å | Relaxation (권장) |
| 1e-8~1e-10 | 절대 에너지 비교 | Single-point, phonon |

### SCF.Mixer.Weight

매 SCF iteration에서 새 density matrix를 섞는 비율:

```
DM_mixed = (1 - weight) × DM_old + weight × DM_new
```

| 값 | 성격 | 적합한 경우 |
|----|------|-----------|
| 0.3~0.5 | 공격적 | 수렴이 쉬운 계 |
| 0.1~0.2 | 보수적 | 전이금속, near-degeneracy |
| 0.01~0.05 | 매우 보수적 | 수렴이 극히 어려운 계 |

## A2-v2 결과 (2026-03-30)

A2-v2도 **실패**.

| | r3 (원본) | r4 (DM restart) | v2 (Tol 1e-6, Weight 0.15) |
|---|---|---|---|
| Geom step | 68 | 0 | **19** |
| SCF iter | 1500 | 1500 | 1500 |
| dDmax | 3.9×10⁻⁴ | 2.4×10⁻³ | **1.4×10⁻²** |
| Tolerance | 1e-10 | 1e-10 | 1e-6 |

dDmax가 시도마다 **악화** (0.0004 → 0.002 → 0.014). Tolerance를 1e-6으로 완화하고 Weight를 0.15로 보수적으로 해도 step 19에서 dDmax=0.014로 1e-6에 한참 미달.

## A2-v3 결과 (2026-03-30, archive 설정)

| 파라미터 | A2-v3 |
|---------|-------|
| SCF.DM.Tolerance | 1e-8 |
| SCF.Mixer.Weight | 0.1 |
| SCF.Mixer.History | 15 |
| DM/XV restart | 없음 (fresh start) |

27 steps 진행 후 OOM kill. Hf-Hf = 4.30 Å, max force = 0.396 eV/Å. 수렴과는 거리가 먼 상태.
archive chain 계산(PBE+D2, 같은 SCF 설정)은 수렴한 적 있으므로, molecule과 chain의 시스템 차이가 관련될 수 있으나 확인 안 됨.

## A2-v4 결과 (Perlmutter, 2026-04-03)

SCF 수렴을 위해 설정을 크게 변경:

| 파라미터 | 표준 설정 | v4-prescf | v4-relax |
|---------|----------|-----------|---------|
| OccupationFunction | MP | **FD** | **FD** |
| ElectronicTemperature | 300 K | **1000 K** | **700 K** |
| PAO.EnergyShift | default | **10 meV** | **10 meV** |
| SCF.DM.Tolerance | — | 1e-4 | 1e-4 |
| SCF.Mixer.Weight | — | 0.05 | 0.05 |

- prescf: SCF only (MD.Steps 0), DM 생성 → 완료
- relax: prescf DM으로 restart, 344 steps → 완료
- Hf-Hf = 3.543 Å (TEM 3.6 Å의 -1.6%)

**문제**: FD 700K + EnergyShift 10meV는 표준 설정이 아님. 이 결과가 D2 때문인지 설정 차이 때문인지 분리 불가.

## 전체 시도 요약

| 버전 | DM.Tolerance | Weight | Occup/Temp | 실제 DM 수렴 | 결과 |
|------|-------------|--------|-----------|-------------|------|
| v1 (r3) | 1e-10 | 0.3 | MP 300K | ~5e-5에서 진동 | 1500 SCF 후 abort |
| v1 (r4) | 1e-10 | 0.3 | MP 300K (DM restart) | 2.4e-3 (악화) | abort |
| v2 | 1e-6 | 0.15 | MP 300K | ~0.014 (악화) | abort |
| v3 | 1e-8 | 0.1 | MP 300K | ~1e-4에서 진동 | OOM |
| v4 | 1e-4 | 0.05 | **FD 700K** | 수렴 | 완료 (비표준 설정) |
| **v5a** | **1e-4** | **0.05** | **MP 300K** | ✅ 수렴 (iter 25, 0.000088) | post-SCF InitMesh OOM |
| **v5b** | **1e-6** | **0.05** | **MP 300K** | ✅ 1e-6 도달 (iter 33, 0.000001) | post-SCF InitMesh OOM |

### 관측된 사실
- A1(PBE), A3(vdW-DF2), A4(PBE+D3): 같은 molecule에서 SCF 수렴 성공
- A2(PBE+D2): 같은 molecule에서 SCF 수렴 실패 (표준 설정으로 4회)
- A2-v4(PBE+D2): FD 700K + EnergyShift 10meV로 변경 시 수렴 성공
- Archive chain PBE+D2: 수렴 성공 (c = 8.417 Å)
- VSe3 PBE+D2: TP/TAP 모두 수렴 성공

### 참고: archive와의 차이

| | archive chain (성공) | 현재 A2 molecule (실패) |
|---|---|---|
| 시스템 | chain (k=1×1×8) | molecule (Gamma) |
| Weight | 0.1 | 0.3 → 0.15 → 0.1 |
| Tolerance | 1e-8 | 1e-10 → 1e-6 → 1e-8 |
| History | 15 | 10 → 10 → 15 |

## A2-v5 계획 (표준 설정 + 보수적 mixing)

v4에서 Weight 0.05가 효과적이었으므로, 표준 occupation(MP 300K)을 유지하면서 Weight 0.05로 재시도.

| 파라미터 | v5a | v5b |
|---------|-----|-----|
| OccupationFunction | MP | MP |
| ElectronicTemperature | 300 K | 300 K |
| SCF.DM.Tolerance | **1e-4** | **1e-6** |
| SCF.MustConverge | **T** | **F** |
| SCF.Mixer.Weight | 0.05 | 0.05 |
| SCF.Mixer.History | 15 | 15 |
| MaxSCFIterations | 500 | 500 |

- v5a (1e-4, MustConverge T): 확실히 수렴 가능
- v5b (1e-6, MustConverge F): 1e-6 도달 시도, 실패해도 다음 geometry step으로 진행

## A2-v5 결과 (2026-04-07)

누리온 lmp_cnt continuous job (slot `run.20260406-170356.log`)에서 v5a → v5b 순차 실행. **둘 다 SCF는 수렴했지만 post-SCF mesh 초기화 시점에 OOM kill**.

| | v5a (Tol 1e-4, MustConverge T) | v5b (Tol 1e-6, MustConverge F) |
|---|---|---|
| 노드 | 4노드 × 32 rank = 128 MPI | 동일 |
| SCF iter 도달 | 25 | 33 |
| 마지막 dDmax | `0.000088` | `0.000001` |
| SCF 상태 | ✅ 수렴 (1e-4 만족, iter 25) | ✅ 1e-6 도달 (iter 33) |
| Wall time | ~3h 50m (17:50 → 21:39) | ~5h (21:39 → 02:35) |
| 죽은 위치 | post-SCF `InitMesh 360³` | post-SCF `InitMesh 360³` |
| 종료 | exit=255, SIGKILL (node7740 모든 rank) | 동일 |

경로: `/scratch/x3251a05/VSe3-Hf2Se9/03-calc/05-hf2se9-mol/stability-test/A2-pbe-d2-v5a` (및 `-v5b`)

### 핵심 발견

**SCF 자체는 더 이상 문제가 아니다.** SCF.Mixer.Weight 0.05 + History 15 + MP 300K (표준 occupation)로 PBE+D2 수렴이 가능함이 확인됨. v4의 비표준 FD 700K + EnergyShift 10 meV가 필요하지 않았다.

### 죽은 메커니즘

stdout 패턴 (v5a, v5b 동일):

```
scf:   25  ...  0.000088 ...    ← SCF 수렴
outcell: Cell vector modules (Ang): 25.000000 25.000000 25.000000
outcell: Cell volume (Ang**3)     : 15625.0000
InitMesh: MESH = 360 x 360 x 360 = 46656000
InitMesh: Mesh cutoff (required, used) = 500.000  573.095 Ry
[BAD TERMINATION ... KILLED BY SIGNAL: 9 ... node7740]
```

원인: 25³ Å³ 박스 + MeshCutoff 500 Ry → **mesh 360³ = 46.6M grid points**. SCF 동안에는 sparse density matrix 위주로 동작하다가, post-SCF에서 forces/stress 계산용 dense mesh를 다시 잡는 시점에 한 노드 메모리(KNL ~96GB)를 초과. 4노드 × 32 rank = 128 MPI에서 mesh 분산이 부족.

### 다음 단계 후보

| 옵션 | 변경 | 효과 | 비고 |
|---|---|---|---|
| (1) 노드 ↑ | 4 → **8노드** (256 rank) | mesh 분산 ↑, mesh 자체는 동일 | 가장 안전, SCF 설정 그대로 |
| (2) MeshCutoff ↓ | 500 → 400 Ry | 360³ → ~288³ (≈ 24M, 절반) | 정확도 약간 손실 |
| (3) 박스 ↓ | 25 → 20 Å | 360³ → 288³ (≈ 24M) | molecule 분리 거리 확인 필요 |

**권장**: (1) 8노드 재제출. v5 SCF 설정 (Weight 0.05, History 15, MP 300K, Tol 1e-4) 그대로 유지.
