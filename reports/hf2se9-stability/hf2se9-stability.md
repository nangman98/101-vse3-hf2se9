# Hf₂Se₉ 안정성 체계적 검토 계획

> **Status**: Phase A 진행 중 (A1✅ A2❌탈락 A3✅ A4✅ A5/A6 Running), Phase B 진행 중
> **Updated**: 2026-03-30

## 관련 문서

| 문서 | 내용 |
|------|------|
| [stability-comparison-method.md](docs/stability-comparison-method.md) | Functional 간 비교 방법론 — total energy 비교 불가, 실험 일치도 기준 |
| [vdw-methods-comparison.md](docs/vdw-methods-comparison.md) | vdW-DF2 vs D2 물리적 차이, revPBE exchange 문제, functional 통일 필요성 |
| [a2-scf-debug.md](docs/a2-scf-debug.md) | A2 (PBE+D2) SCF 수렴 실패 분석 — 원인, 시도 이력, 해결책 |
| [phase-c-cnt-md.md](docs/phase-c-cnt-md.md) | Phase C: CNT confinement + MD 계획 — CNT 선택, 구조 생성, MD 설정, JACS 캡슐화 근거, 실행 스캐폴드 |
| [failure-analysis.md](../initial-structures/failure-analysis.md) | 이전 Hf₂Se₉ relaxation 실패 원인 (cell 팽창, 구조 붕괴) |

## 배경

이전 연구에서 Hf₂Se₉ relaxation이 반복적으로 실패했다 (cell 팽창 16~53%, 구조 붕괴).
실패 원인 분석: [failure-analysis.md](../initial-structures/failure-analysis.md)

핵심 문제: DFT 설정(functional, basis, vdW 보정)에 따라 결과가 극적으로 달라지며,
어떤 설정이 올바른지 체계적으로 검증한 적이 없음.

실험(STEM)에서 Hf₂Se₉ 존재는 거의 확실하므로, **DFT에서 이를 재현할 수 있는 설정을 찾는 것**이 목표.

## 목표

Hf₂Se₉ molecule relaxation이 안정적으로 수렴하는 DFT 설정을 찾는다.
네 가지 축(exchange, basis, DFT+U, CNT)을 **독립적으로** 검토하여 실패 원인을 분리한다.

## 판단 기준

**중요**: 서로 다른 functional 간 total energy 직접 비교는 불가. 비교 방법론은 [`stability-comparison-method.md`](docs/stability-comparison-method.md) 참조.

핵심 판단 순서: (1) 수렴 여부 → (2) 구조 유지 → (3) 실험값과 구조 파라미터 비교

| 기준 | 성공 | 실패 |
|------|------|------|
| Hf-Hf 거리 | 3.5~3.8 Å 유지 (TEM: 3.6 Å) | < 3.0 Å (붕괴) 또는 > 5.0 Å (분해) |
| Force 수렴 | < 0.01 eV/Å | 미수렴 (1000 steps 이상) |
| 구조 | confacial bioctahedron 유지 | Se₃ 삼각형 변형, Hf 이탈 |
| 실험 일치도 | Hf-Hf 편차 < 5% | 편차 > 10% |

## 테스트 시스템

**Hf₂Se₉ molecule** (11 atoms, 25 Å cubic, Gamma only)
- 가장 가벼움 → 여러 설정을 빠르게 스캔 가능
- molecule에서 안정적인 설정을 찾은 후 chain → 이종접합으로 확장

## 판단 흐름

```
Step 1: vdW-DF2 molecule relaxation (SIGTERM 종료, step 39, force 0.045 eV/Å)
  ↓ 안정 → chain(06) → VSe3-Hf2Se9 이종접합 → transport
  ↓ 불안정 ↓
Step 2: Phase A — Exchange scan (어떤 functional이 문제인지)
  ↓ SIESTA vs VASP 비교로 코드 문제 분리
  ↓
Step 3: Phase B — Basis scan (SIESTA basis 품질 문제인지)
  ↓
Step 4: Phase D — DFT+U scan (Hf 5d 강상관 효과인지)
  ↓
Step 5: Phase C — CNT에 넣어서 relax + MD
  ↓ CNT confinement가 안정화하는지
  ↓
Step 6: 그래도 불안정 → VSe3 TP chain만으로 논문 마무리
```

---

## Axis 1: Exchange-Correlation Functional + vdW (Phase A)

**고정**: Basis EnergyShift 0.01 Ry (136 meV), U=0, CNT 없음.
**변수**: functional + vdW 보정 방법.

| # | Dir | Functional | vdW | 코드 | 목적 |
|---|-----|-----------|-----|------|------|
| A1 | `A1-pbe-novdw/` | PBE | 없음 | SIESTA | baseline — vdW 없이도 구조가 유지되는지 |
| A2 | `A2-pbe-d2/` | PBE + Grimme D2 | fdf2grimme | SIESTA | 이전 방식 재현 |
| A3 | `A3-vdw-df2/` | vdW-DF2 (LMKLL) | 내장 | SIESTA | relax/ step 39 SIGTERM 종료 → 재제출 필요 |
| A4 | `A4-pbe-d3bj/` | PBE + D3(BJ) | SIESTA DFT-D3 | SIESTA | 배위수 의존 C6 보간 |
| A5 | `A5-vasp-pbe-d3/` | PBE + D3(BJ) | IVDW=12 | VASP | plane-wave 참조값 — SIESTA basis 문제 분리 |
| A6 | `A6-vasp-hse-d3/` | HSE06 + D3(BJ) | IVDW=12 | VASP | hybrid functional — exchange 정확도 효과 |

**핵심 비교**:
- A1 vs A3: vdW 보정 자체가 필요한가?
- A2 vs A3 vs A4: D2 / vdW-DF2 / D3(BJ) 중 어느 쪽이 Hf₂Se₉에 적합한가?
- A4 vs A5: **SIESTA vs VASP** — 같은 PBE+D3인데 결과가 다르면 NAO basis 문제 확정
- A5 vs A6: PBE vs HSE — exchange-correlation 자체가 문제인지 확인

**이전 결과 참고**: VASP MD (DFT-D3)에서 Hf-Hf = 3.82 Å 유지 → D3에서는 양호했음.
이전 PPT(`Hf2Se9-VSe3 Aug 2025.pptx`)에서 SIESTA(PBE)는 실험 일치, PW 기반(QE, VASP)은 불일치라는 역방향 결과도 있었으므로 코드 비교가 중요.

## Axis 2: Basis Set (Phase B, SIESTA only)

**고정**: Phase A 최적 functional, U=0, CNT 없음.
**변수**: PAO.EnergyShift (orbital 범위 결정).

EnergyShift가 작을수록 basis가 크고 정확하지만, BSSE(basis set superposition error)도 커진다.
vdW gap 에너지(~수십 meV)가 BSSE 오차 범위 내이면 결과가 불안정해진다.

| # | Dir | EnergyShift | Basis 크기 | 목적 |
|---|-----|------------|-----------|------|
| B1 | `B1-eshft-010/` | 10 meV | 매우 큼 | 이전 실패 설정(16% 팽창) 재현 확인 |
| B2 | `B2-eshft-030/` | 30 meV | 큼 | 중간 |
| B3 | `B3-eshft-050/` | 50 meV | 보통 | 이전 "안정" 설정 재현 확인 |
| B4 | `B4-eshft-100/` | 100 meV | 작음 | BSSE 감소 |
| B5 | `B5-eshft-200/` | 200 meV | 최소 | 극단적 — 경향 확인 |

**핵심 비교**:
- B1~B5 수렴 트렌드: Hf-Hf 거리가 basis 크기에 따라 단조롭게 변하는지
- B1(팽창 재현) vs B3(안정 재현): 이전 결과와 일치하는지
- 수렴점: 어느 EnergyShift에서 결과가 안정화되는지 → 최적값 결정

## Axis 3: DFT+U (Phase D, Hubbard correction)

**고정**: Phase A+B 최적, CNT 없음.
**변수**: Hubbard U 값.

Hf는 5d 전자를 가지며, PBE는 d-electron의 localization을 과소평가할 수 있다.
이전에 DFT+U를 시도한 적 있으나(archive `003_Hf2Se9_DFT+U`, U=1~7 eV) 체계적이지 않았음.

U를 키우면 d-electron이 localize되어 Hf-Se bonding 성격이 변할 수 있고,
이것이 vdW gap 안정성에 영향을 줄 수 있다.

| # | Dir | U (eV) | 적용 orbital | 목적 |
|---|-----|--------|-------------|------|
| D1 | `D1-u0/` | 0 | — | baseline (= Phase A+B 최적) |
| D2 | `D2-u1/` | 1 | Hf 5d | 약한 보정 |
| D3 | `D3-u3/` | 3 | Hf 5d | 중간 보정 |
| D4 | `D4-u5/` | 5 | Hf 5d | 강한 보정 (이전 시도값) |
| D5 | `D5-u7/` | 7 | Hf 5d | 과보정 — 경향 확인 |
| D6 | `D6-u3-se4p/` | 3 | Se 4p | Se에도 U가 필요한지 테스트 |

**핵심 비교**:
- D1~D5: U 증가에 따른 Hf-Hf 거리 트렌드
- U가 vdW gap 안정화에 기여하는지 (d-electron localization → bonding 변화)
- D5 vs D6: Hf-d vs Se-p 중 어디에 U가 더 효과적인지
- 밴드갭 변화: U에 따라 금속/반도체 전이 여부

## Axis 4: CNT 역할 (Phase C)

**고정**: Phase A~D 최적 설정.
**변수**: CNT 유무 + relaxation vs MD.

실험에서 Hf₂Se₉는 CNT 안에서 합성/관찰됨. CNT가 물리적으로 구조를 안정화하는 역할을 할 수 있다.
이전에는 CNT 포함 계산을 해보지 않았음 → 남아있는 핵심 과제.

| # | 시스템 | 방법 | 목적 |
|---|--------|------|------|
| C1 | Hf₂Se₉ molecule (isolated) | Relaxation | baseline (Phase A~D 결과) |
| C2 | Hf₂Se₉ molecule in CNT | Relaxation | CNT confinement가 구조를 안정화하는지 |
| C3 | Hf₂Se₉ molecule in CNT | MD (300K) | 열적 안정성 — DFT relaxation이 놓치는 효과 |
| C4 | Hf₂Se₉ chain (isolated) | Relaxation | chain 형성 시 안정성 변화 |
| C5 | Hf₂Se₉ chain in CNT | Relaxation | 실험 조건에 가장 가까운 시스템 |

**핵심 비교**:
- C1 vs C2: CNT confinement 효과 정량화
- C2 vs C3: 0K relaxation vs finite-T MD — local minimum 문제인지
- C1 vs C4: molecule → chain 시 안정성 변화 (chain 간 vdW 상호작용)

**CNT 선택**: 실험에서 Hf₂Se₉가 관찰된 CNT 직경 참고. ASE로 적절 직경 CNT 생성.

**문헌 근거 보강**:
- ACS Nano 2025 VSe3@CNT: 실험 구조를 confined phase로 해석
- JACS 2021 NbTe3/VTe3/TiTe3@CNT (`10.1021/jacs.0c10175`): bulk 비안정 MX3도 CNT 안에서 안정화 가능, `vacuum vs encapsulated` 비교와 `CNT fixed + guest relax` 프로토콜 제시

**현재 구현 상태**:
- 구조 초안: `VSe3-Hf2Se9/03-calc/phase-c/`
- 초기 입력 스캐폴드: `VSe3-Hf2Se9/03-calc/05-hf2se9-mol/stability-test/phase-c/`
- 생성 스크립트: `VSe3-Hf2Se9/02-code/setup_phase_c.py`

---

## 실행 계획

### 디렉토리 구조

모든 테스트: `03-calc/05-hf2se9-mol/stability-test/`

```
stability-test/
├── run-phaseA.pbs / .sh      A1→A2→A4 (SIESTA, long큐 3노드 128MPI)
├── run-phaseB.pbs / .sh      B1→B5 (SIESTA, flat큐 3노드 128MPI)
├── run-vasp.sh               A5→A6 (VASP, jobvasp continuous job용)
├── A1~A4 (SIESTA), A5~A6 (VASP)
├── B1~B5 (SIESTA)
└── D1~D6 (SIESTA)           ← A+B 결과 확정 후 제출
```

### 잡 구성

| 잡 | 큐 | 노드 | MPI | 내용 | 비고 |
|---|---|---|---|---|---|
| `run-phaseA.pbs` | long | 3 | 128 | A1 → A2 → A4 | A2: fdf2grimme 런타임 생성 |
| `run-phaseB.pbs` | flat | 3 | 128 | B1 → B2 → B3 → B4 → B5 | Phase A와 동시 제출 가능 |
| `run-vasp.sh` → jobvasp | continuous | 1 | 64 | A5 → A6 | `/scratch/x3251a05/job/jobvasp/run.sh`로 복사, POTCAR 자동 생성 |
| Phase D (미정) | flat | 3 | 128 | D1 → ... → D6 | A+B 최적 설정 반영 후 제출 |

### 실행 순서

```
Phase A + B 동시 제출 (SIESTA long+flat)
  + A5/A6 VASP 제출 (jobvasp)
    ↓ 결과 분석: 최적 XC + EnergyShift 확정
Phase D: DFT+U scan (D1~D6, 최적 설정 반영)
    ↓
Phase C: CNT 테스트 (C1~C5, 구조 생성 필요)
```

Phase A~D는 molecule(11 atoms, Gamma)이므로 각 테스트 수 시간 내 완료 가능.
Phase A와 B는 독립적 → 동시 제출.
Phase D는 A+B 결과 의존 → 순차 제출.

## 결과 정리 테이블 (계산 후 채울 것)

| Test | Functional | Basis | U (eV) | CNT | Hf-Hf (Å) | 수렴 | 비고 |
|------|-----------|-------|--------|-----|-----------|------|------|
| A1 | PBE | 136 meV (0.01 Ry) | 0 | X | **3.857** | ✅ 14 steps | vdW 없어도 구조 유지 |
| A2 | PBE+D2 | 136 meV (0.01 Ry) | 0 | X | — | ❌ SCF 미수렴 (3회 실패, 원인 미확인) | [상세](docs/a2-scf-debug.md) |
| A3 | vdW-DF2 | 136 meV (0.01 Ry) | 0 | X | **3.967** | ✅ 13 steps | = 05-mol relax, revPBE exchange |
| A4 | PBE+D3(BJ) | 136 meV (0.01 Ry) | 0 | X | **3.857** | ✅ 14 steps | = A1과 동일 (D3는 isolated mol에 효과 없음) |
| A5 | PBE+D3 (VASP) | PAW | 0 | X | — | — | normal큐 재제출 (MKL 수정) |
| A6 | HSE06+D3 (VASP) | PAW | 0 | X | — | — | normal큐 재제출 (MKL 수정) |
| B1 | (best) | 10meV | 0 | X | — | — | |
| B2 | (best) | 30meV | 0 | X | — | — | |
| B3 | (best) | 50meV | 0 | X | — | — | |
| B4 | (best) | 100meV | 0 | X | — | — | |
| B5 | (best) | 200meV | 0 | X | — | — | |
| D1 | (best) | (best) | 0 | X | — | — | |
| D2 | (best) | (best) | 1 | X | — | — | |
| D3 | (best) | (best) | 3 | X | — | — | |
| D4 | (best) | (best) | 5 | X | — | — | |
| D5 | (best) | (best) | 7 | X | — | — | |
| D6 | (best) | (best) | 3(Se) | X | — | — | |
| C1 | (best) | (best) | (best) | X | — | — | |
| C2 | (best) | (best) | (best) | O | — | — | |
| C3 | (best) | (best) | (best) | O+MD | — | — | |
| C4 | (best) | (best) | (best) | X (chain) | — | — | |
| C5 | (best) | (best) | (best) | O (chain) | — | — | |
