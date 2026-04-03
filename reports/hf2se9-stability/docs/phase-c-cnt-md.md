# Phase C: CNT Confinement + MD 계획

> **Status**: 구조 설계 + molecule@CNT 입력 스캐폴드 작성
> **Updated**: 2026-04-03
> **관련**: [hf2se9-stability.md](hf2se9-stability.md) — Axis 4

## 배경

실험에서 Hf₂Se₉는 CNT 안에서 합성/관찰됨 (STEM). CNT confinement가 구조를 물리적으로 안정화하는 역할을 할 수 있다. 이전에 CNT 포함 계산은 수행한 적 없음.

DFT relaxation (0K)에서 안정적인 구조라도, 유한 온도(300K)에서는 local minimum을 넘어 다른 구조로 전이할 수 있다. MD로 열적 안정성을 검증해야 함.

## 왜 Phase C가 필요한가

자유 Hf₂Se₉가 실험 구조를 잘 재현하지 못하는 상황에서, CNT는 단순 배경이 아니라 **구조 선택 조건**일 수 있다.
즉 질문은 "자유 분자가 왜 안 맞는가"에서 끝나지 않고, **"실험에서 보인 Hf₂Se₉가 confinement-stabilized species인가"**로 확장되어야 한다.

현재까지의 로컬 결과는 이 해석과 잘 맞는다.

- isolated molecule은 PBE / PBE+D3 / vdW-DF2에서 모두 Hf-Hf가 실험 3.6 Å보다 길다
- isolated chain은 더 악화되며 vdW gap과 Hf-Hf가 실험보다 커진다
- heterostructure나 주변 cage가 있으면 "움직이지 못해서 맞아 보이는" kinetic trapping 가능성이 있다

따라서 Phase C의 목적은 단순히 "CNT에 넣으면 맞는가"가 아니라 아래 두 가지를 분리하는 것이다.

1. CNT가 **실제로** Hf₂Se₉ geometry를 실험값 방향으로 안정화하는가
2. 아니면 CNT가 단지 **움직임을 막아서** metastable geometry를 가둔 것인가

## 문헌 근거: CNT가 구조 선택을 바꿀 수 있음

### 직접 참고 1: VSe3 CNT 논문 (ACS Nano 2025, `10.1021/acsnano.4c04184`)

- 논문 초안/요약 기준으로 핵심 메시지는 `single-chain phase` 자체가 CNT 안에서 구현되고 식별된다는 점이다
- 즉 자유계와 CNT 내부 구조를 동일시하지 않고, **confined phase**로 취급한다
- Hf₂Se₉ 해석도 같은 프레임이 필요하다

### 직접 참고 2: NbTe3/VTe3/TiTe3@CNT (JACS 2021, `10.1021/jacs.0c10175`)

이 논문은 현재 Phase C 판단에 더 직접적이다.

- bulk에서 안정하지 않거나 보고되지 않은 MX₃ 조성도 CNT 안에서는 few/single chain으로 합성 가능하다고 제시한다
- DFT에서 `isolated chain in vacuum`과 `chain@CNT`를 분리해서 다룬다
- encapsulated 계산에서는 **CNT 원자를 고정하고 내부 chain만 relax**하는 프로토콜을 사용한다
- 논문 해석의 중심은 "자유계 절대 정답"이 아니라, **vacuum vs encapsulated 비교**이다

Hf₂Se₉에 주는 직접적인 시사점:

- 자유 Hf₂Se₉가 안 맞아도 바로 탈락시킬 이유는 없다
- 첫 CNT 계산은 `CNT fixed + Hf₂Se₉ only relax`로 시작하는 것이 타당하다
- 판단 지표는 TP/TAP 같은 상전이보다 `Hf-Hf`, `Se₃ 폭`, `bioctahedron 유지`, `CNT-wall 거리`, `oval distortion`로 바꿔야 한다
- 따라서 Phase C는 free-standing 정답 찾기보다는 **free vs confined 비교 실험**으로 설계해야 한다

## CNT 선택

### 실험 조건

- Source: Sigma-Aldrich SWCNT (#704113) + Cheap Tubes (90% SW-DW)
- 전처리: 510°C air 15min (tube opening)
- 합성: 650-900°C, 5일, 진공 ~10⁻⁶ Torr
- CNT 직경: 혼합 SWCNT/DWCNT, 정확한 chirality 미특정

### 문헌 참고 (유사 물질 CNT encapsulation)

| 물질 | CNT 내경 | 구조 | 출처 |
|------|---------|------|------|
| CsI | 0.73 nm | 1D linear chain | Kashtiban 2021 |
| CsI | 0.8-1.1 nm | 2×1 double helix | Kashtiban 2021 |
| Se | DWCNT narrow | double helix | Fujimori 2013 |
| HgI₂ | ~0.8 nm | helical 2×1 layer | Sloan 2003 |

### Hf₂Se₉ 크기 추정

| 파라미터 | 값 | 출처 |
|----------|---|------|
| Se₃ 삼각형 폭 | ~2.9 Å (DFT), 3.6-4.2 Å (TEM) | Phase A 결과 |
| Molecule 전체 직경 | ~5.8-8.4 Å | Se₃ 폭 × 2 |
| 분자-CNT 간 vdW gap | ~3.0-3.5 Å | 문헌 (CsI, I₂) |

**필요 CNT 내경**: molecule 직경 + 2 × vdW gap ≈ 5.8 + 6.0 = **~12 Å (1.2 nm)**

### 후보 CNT chirality

| Chirality | 직경 (Å) | 적합도 | 비고 |
|-----------|---------|--------|------|
| (9,9) armchair | 12.20 | ★★★ | 내경 ~12 Å, 좁은 fit |
| (10,10) armchair | 13.56 | ★★☆ | 여유 있는 fit |
| (15,0) zigzag | 11.74 | ★★★ | 약간 좁음 |
| (16,0) zigzag | 12.53 | ★★★ | 적정 |
| (12,8) chiral | 13.65 | ★★☆ | 문헌(Yao 2016) |

**추천**: **(9,9)** 또는 **(16,0)** — Hf₂Se₉ 직경에 맞는 tight fit.
두 가지 chirality로 비교하면 confinement 강도 의존성도 확인 가능.

## Step 0: CNT 직경 스캔 (single-point)

Relaxation 전에 **어떤 CNT 직경이 가장 안정적인지** 먼저 확인해야 한다.
다양한 chirality의 CNT에 Hf₂Se₉를 넣고 single-point 에너지를 비교.

| # | CNT | 내경 (Å) | 방법 | 목적 |
|---|-----|---------|------|------|
| S1 | (8,8) | ~10.9 | Single-point | tight confinement |
| S2 | (9,9) | ~12.2 | Single-point | 중간 |
| S3 | (10,10) | ~13.6 | Single-point | 여유 |
| S4 | (15,0) | ~11.7 | Single-point | zigzag, tight |
| S5 | (16,0) | ~12.5 | Single-point | zigzag, 중간 |

비교: 같은 functional에서 total energy → 최적 직경 결정 → 해당 CNT로 relaxation/MD 진행.

실무적으로는 현재 준비된 구조를 기준으로 `(9,9)`과 `(16,0)`부터 시작한다.
즉 S2와 S5를 먼저 수행한 뒤, 필요하면 `(8,8)` 또는 `(10,10)`으로 넓힌다.

## 테스트 매트릭스

두 가지 방법을 병행:
- **DFT relaxation**: 0K 평형 구조 + CNT confinement 효과
- **MD**: 유한 온도(300K) 열적 안정성 + 구조 변화 추적

| # | 시스템 | 방법 | CNT | 목적 |
|---|--------|------|-----|------|
| C1 | Hf₂Se₉ molecule (isolated) | DFT relax | — | baseline (Phase A~D 결과) |
| C2 | Hf₂Se₉ molecule in CNT(최적) | DFT relax | (최적) | CNT confinement 효과 (0K) |
| C3 | Hf₂Se₉ molecule in CNT(최적) | MD (300K) | (최적) | 열적 안정성 |
| C4 | Hf₂Se₉ chain (isolated) | DFT relax | — | chain 안정성 (=06-chain 결과) |
| C5 | Hf₂Se₉ chain in CNT(최적) | DFT relax | (최적) | 실험 조건에 가장 가까운 시스템 (0K) |
| C6 | Hf₂Se₉ chain in CNT(최적) | MD (300K) | (최적) | chain 열적 안정성 |

### 권장 해석 순서

Phase C에서 중요한 것은 계산 수를 늘리는 것보다 비교 순서를 지키는 것이다.

1. `C1 vs C2`: confinement만으로 geometry가 실험값 쪽으로 이동하는가
2. `C2 vs C3`: 0 K local minimum인지, 300 K에서도 유지되는지
3. `C1 vs C4`: molecule과 chain 중 무엇이 자유계에서 더 불안정한가
4. `C2 vs C5`: confinement가 molecule뿐 아니라 chain에도 같은 방향으로 작용하는가

이 순서를 지키면 "진짜 안정화"와 "가둬놓은 trapping"을 최소한 1차적으로 분리할 수 있다.

## 구조 생성 방법

### CNT 생성 (ASE)

```python
from ase.build import nanotube
cnt = nanotube(9, 9, length=3)  # (9,9) armchair, 3 unit cells
```

### Hf₂Se₉@CNT 조립

1. CNT 생성 (c축 방향으로 적절 길이)
2. Hf₂Se₉ molecule/chain을 CNT 중심에 배치
3. CNT c축과 Hf₂Se₉ c축 정렬
4. CNT-molecule 간 vdW gap 확인 (최소 ~2.5 Å)
5. Vacuum 추가 (a, b 방향 ~15 Å)

### 주의사항

- **1차 계산은 CNT 원자 고정** (`Geometry.Constraints`) — Hf₂Se₉만 relax
- 구조가 잘 맞지만 CNT 변형이 과도하면 **2차 계산에서 CNT 일부 또는 전체 자유화**
- MD는 처음부터 classical force field로 가기보다, 짧은 **DFT-MD**를 우선 고려
- Hf-Se force field 신뢰성이 확보되기 전까지 classical MD 결과는 보조 자료로만 해석

## DFT Relaxation 설정

C1/C2/C4/C5: SIESTA 또는 VASP로 0K relaxation.
원칙적으로는 **Phase A~D에서 확정된 최적 functional/basis**를 사용한다.

다만 지금 바로 molecule@CNT를 시작할 경우의 임시 우선순위는 아래와 같다.

1. `PBE+D3(BJ)` 또는 `VASP PBE+D3`
2. `vdW-DF2`
3. `PBE+D2`는 참고용 재현 케이스로만 사용

이유:

- Hf 계에서 D2 파라미터 신뢰성 문제가 이미 의심된다
- A4(PBE+D3BJ)는 isolated molecule에서 적어도 비정상 붕괴를 보이지 않았다
- JACS 2021은 D2를 썼지만, Hf₂Se₉에서는 D3 또는 PW-D3가 더 안전한 시작점이다

## MD 설정

C3/C6: 유한 온도에서의 구조 안정성 검증.

### Force field 선택 (확정 필요)

| Option | 코드 | 장점 | 단점 |
|--------|------|------|------|
| ReaxFF | LAMMPS | 반응성, bond breaking 기술 가능 | Hf 파라미터 존재 여부 확인 필요 |
| COMB3 | LAMMPS | 금속-산화물 시스템 | Hf-Se 파라미터 확인 필요 |
| ML potential | VASP/custom | DFT 정확도에 근접 | training data 필요 |

Hf-Se 계에 적합한 force field 확인이 선행되어야 함.

따라서 현재 권장 순서는 다음과 같다.

1. 먼저 `DFT relax`
2. 그 다음 `짧은 VASP DFT-MD` (수 ps 수준)
3. classical MD는 force field 검증 후에만 확장

### MD 프로토콜 (force field 확정 후)

- 온도: 300 K (NVT, Langevin 또는 Nosé-Hoover)
- Time step: 1.0 fs
- 시뮬레이션 시간: 수십~수백 ps (classical MD이므로 가능)
- Cell: 고정 (NVT)

### 모니터링 지표

MD 중 매 step에서 추적:

| 지표 | 안정 | 불안정 |
|------|------|--------|
| Hf-Hf 거리 | 3.5-4.0 Å 유지 | < 3.0 또는 > 5.0 Å |
| Confacial bioctahedron | Se₃ 삼각형 유지 | 삼각형 변형/Hf 이탈 |
| Total energy | 일정 (kT 범위 요동) | 급격한 하락 (구조 전이) |
| CNT 형태 | 원형 유지 | 과도한 oval distortion |

## 실행 순서

```
Phase A+B+D 최적 functional/basis 확정
  ↓
구조 생성: CNT(9,9) + Hf₂Se₉ mol/chain
  ↓
C1: baseline (이미 완료 — Phase A 결과)
S2/S5: cnt99 / cnt160 single-point
  ↓
C2: mol@CNT relaxation (CNT 고정)
C2b: mol@(16,0) relaxation (CNT 고정)
  ↓ 직경 효과 비교
C3: best mol@CNT MD 300K 2~5 ps
  ↓
C2에서 CNT oval distortion 확인
  → 심하면 CNT도 relax 허용
  ↓
C4: chain isolated (이미 완료 — 06-chain 결과)
C5: chain@CNT relaxation
  ↓
C6: best chain@CNT MD
```

## 구현 위치

Phase C 작업 공간은 아래 두 곳으로 나눈다.

- 구조 초안/시각화: `VSe3-Hf2Se9/03-calc/phase-c/`
- 실제 안정성 테스트 입력: `VSe3-Hf2Se9/03-calc/05-hf2se9-mol/stability-test/phase-c/`

현재 molecule 기준 초기 스캐폴드는 `stability-test/phase-c/` 아래에 두며, 다음 케이스를 바로 시작점으로 사용한다.

| Case | 내용 | 상태 |
|------|------|------|
| C1-mol-isolated-reference | isolated molecule reference | scaffold |
| S2-mol-cnt99-singlepoint | 직경 스캔용 (9,9) | scaffold |
| S5-mol-cnt160-singlepoint | 직경 스캔용 (16,0) | scaffold |
| C2-mol-cnt99-relax-fixedcnt | CNT 고정 relaxation | scaffold |
| C2b-mol-cnt160-relax-fixedcnt | CNT 고정 relaxation | scaffold |

chain@CNT는 molecule 결과로 적정 직경과 functional을 고른 뒤 추가한다.

## 계산 리소스 추정

| 케이스 | 원자 수 | 코드 | 예상 시간 |
|--------|---------|------|----------|
| C2 (mol@CNT) | ~140 (11+~130 CNT) | SIESTA | ~24-48h (3노드) |
| C3 (mol@CNT MD) | ~140 | VASP | ~48h (8노드, 1000 steps) |
| C5 (chain@CNT) | ~140 | SIESTA | ~48-120h (3노드) |

## 아카이브 참고

- `archive/101_VSe3-Hf2Se9/001_Hf2Se9_singlemol/001_MD/` — VASP DFT-MD 템플릿
  - 300K NVT, Langevin, IVDW=10(D3-BJ), POTIM=1.0 fs, NSW=500
  - Hf-Hf = 3.82 Å (isolated molecule)
  - 참고: 이 아카이브는 DFT 기반 MD (VASP IBRION=0). Phase C의 classical MD와는 다른 방법.
