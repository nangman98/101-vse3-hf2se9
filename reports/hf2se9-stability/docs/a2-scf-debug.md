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

## 현재 상태

A2 molecule에서 SCF 미수렴 — 4회 시도(r3, r4, v2, v3) 모두 실패.
원인 미확인. archive의 chain PBE+D2 계산(Weight 0.1, History 15, Tol 1e-8)은 수렴했으므로, PBE+D2 자체가 불가능한 것은 아님.

### 관측된 사실
- A1(PBE), A3(vdW-DF2), A4(PBE+D3): 같은 molecule에서 SCF 수렴 성공
- A2(PBE+D2): 같은 molecule에서 SCF 수렴 실패 (SCF 설정 변경해도)
- Archive chain PBE+D2: 수렴 성공 (c = 8.417 Å)
- VSe3 PBE+D2: TP/TAP 모두 수렴 성공

### 참고: archive와의 차이

| | archive chain (성공) | 현재 A2 molecule (실패) |
|---|---|---|
| 시스템 | chain (k=1×1×8) | molecule (Gamma) |
| Weight | 0.1 | 0.3 → 0.15 → 0.1 |
| Tolerance | 1e-8 | 1e-10 → 1e-6 → 1e-8 |
| History | 15 | 10 → 10 → 15 |
