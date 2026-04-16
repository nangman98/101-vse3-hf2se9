# H Termination Plan: VSe3-Hf2Se9 Heterostructure

## Background

### 문제

08-hetero-v2 (vdW-DF2)와 09-hetero-d2 (PBE+D2)에서 separation energy가 d = 2.5 ~ 4.0 A 전 구간에서 단조 감소한다. 실험에서 관측되는 ~3.5 A 부근의 minimum을 재현하지 못함.

| d (A) | vdW-DF2 비대칭 (eV) | vdW-DF2 대칭 (eV) | PBE+D2 대칭 (eV) |
|-------|---------------------|--------------------|-------------------|
| 2.5   | -3.73               | -6.21              | -8.31             |
| 3.0   | -2.00               | -4.10              | -4.89             |
| 3.5   | -0.84               | -1.61              | -1.84             |
| 4.0   | 0.00                | 0.00               | 0.00              |

### 가설 (2026-04-07 미팅, 교수님 제안)

VSe3를 chain에서 잘라낸 단면의 Se에 dangling bond가 남아 있어, 인터페이스에서 비물리적으로 강하게 결합한다. Hf2Se9 molecule은 closed-shell이라 자체적으로 안정하므로, 문제는 VSe3 측에 한정된다.

**검증 방법**: VSe3 측 Se에만 H를 붙인 구조 / 안 붙인 구조를 모두 계산하여 separation energy curve를 비교한다. H termination이 있을 때 실험 부근의 minimum이 나타나면 가설이 지지됨.

---

## Archive 참고: 이전 H termination 시도 (2025-08)

`archive/101_VSe3-Hf2Se9/PPT_summary_aug25/005_Hydrogen/`

### 구조

- VSe3(6uc) + **H(3개)** + Hf2Se9 + **H(3개)** + VSe3(6uc) = **68 atoms**
- H를 VSe3 / Hf2Se9 **양쪽 모두**에 부착
- Se-H 거리: ~1.0 A (Se 바로 위/아래에 배치)
- Species: V(1), Se(2), H(3), Hf(4)

### 계산 설정

- PBE + Grimme D2, MeshCutoff 500 Ry, kgrid 1x1x4
- Broyden MD 1500 steps (relaxation)
- Separation scan: **0.4 ~ 0.8 A** (5개 포인트)

### 결과

- 0.4 ~ 0.8 A 범위에서 **여전히 단조 감소** (에너지 ~920 eV → 0 eV)
- 이 범위는 repulsive wall에 해당 — separation이 너무 작아서 minimum을 볼 수 없었음

### 교훈

1. Separation 범위가 너무 좁았음 (0.4-0.8 A) → **2.0-4.5 A로 확장 필요**
2. H를 양쪽 모두 붙였음 → 미팅 결정에 따라 **VSe3 측만** H termination
3. PBE+D2 사용 → 현재 기준 functional인 **vdW-DF2로 통일**
4. 6uc electrode → 현재 기준 **3uc**

또한 `archive/101_VSe3-Hf2Se9/005_PPT/005_Hf2Se9_H/`에 Hf2Se9 molecule 양쪽 Se3에 H를 붙인 구조도 있음 (17 atoms: 2Hf + 9Se + 6H, Se-H ~1.0 A).

---

## 계획

### Phase 1: H termination separation scan (single-point)

아카이브의 실패를 반복하지 않도록, 적절한 separation 범위에서 H 있음/없음을 직접 비교한다.

#### 구조 설계

**10-hetero-h-term** (H termination 있음):
- VSe3(3uc) 좌측 electrode — **끝 Se3에 H 3개 부착** — gap — Hf2Se9 — gap — **끝 Se3에 H 3개 부착** — VSe3(3uc) 우측 electrode
- H는 VSe3 측 인터페이스 Se3에만 부착 (Hf2Se9는 그대로)
- Se-H 거리: ~1.46 A (H2Se 실험값 기반, archive는 1.0 A였으나 이는 짧음)
- H 배치: Se에서 gap 쪽으로 (z 방향 바깥쪽)
- 원자 수: 38 (기존) + 6 H = **44 atoms**
- Species 추가: H (species 4)

**비교 대상: 08-hetero-v2** (H 없음, 이미 완료):
- 동일 vdW-DF2, 동일 VSe3/Hf2Se9 relaxed 좌표
- d = 2.5, 3.0, 3.5, 4.0 A 결과 이미 있음

#### Separation 범위

| d (A) | 비고 |
|-------|------|
| 2.0   | repulsive wall 확인 (archive가 놓친 영역) |
| 2.5   | 기존 결과와 비교 |
| 3.0   | 기존 결과와 비교 |
| 3.5   | 실험 예상 equilibrium |
| 4.0   | 기존 결과와 비교 |
| 4.5   | 약한 상호작용 한계 |

→ 총 **6개 single-point** 계산

#### Functional

- **vdW-DF2** (LMKLL) — 08-hetero-v2와 직접 비교 가능
- PBE+D2는 보조로 고려하되, 우선순위는 vdW-DF2

#### 계산 설정

| Parameter | Value | 비고 |
|-----------|-------|------|
| XC.functional | VDW | |
| XC.authors | LMKLL | vdW-DF2 |
| MeshCutoff | 500 Ry | |
| kgrid | 1x1x4 | |
| MD.Steps | 0 | single-point (relaxation 아님) |
| SCF.DM.Tolerance | 1.0d-4 | |
| SCF.Mixer.Weight | 0.3 | |

### Phase 2: H termination + relaxation

Phase 1에서 minimum이 확인되면:

1. Minimum 부근 separation에서 **Broyden relaxation** 수행
   - MD.Steps: 500
   - MD.MaxForceTol: 0.01 eV/Ang
   - Geometry.Constraints: cell 고정, electrode 원자 고정 (인터페이스 + Hf2Se9만 relax)
2. Relaxed 구조에서 Hf-Hf 거리, Se-Se 인터페이스 거리 확인
3. H 있음/없음 relaxed 구조 비교

### Phase 3: Transport 계산

Phase 2에서 안정 구조가 나오면 transport 계산으로 직행 (2026-04-07 미팅 결정):

1. Electrode 계산 (VSe3 bulk, H 없음)
2. TranSIESTA device 계산 (H termination 포함 heterostructure)
3. TBtrans I-V curve

---

## 구현 사항

### build_hetero_v2.py 수정

`--h-term` 플래그 추가:

1. VSe3 좌측 electrode 마지막 Se3 → H 3개 추가 (Se에서 +Se-H 거리만큼 z 증가)
2. VSe3 우측 electrode 첫 Se3 → H 3개 추가 (Se에서 -Se-H 거리만큼 z 감소)
3. Species에 H 추가: `('H', 1)` → species index 4
4. write_struct_fdf, write_xsf 등에서 H species 처리

### Se-H 거리

- Archive에서 사용한 값: 1.0 A
- H2Se 실험 bond length: 1.46 A
- **1.46 A 사용** (또는 relaxation에서 자연스럽게 조정되도록)

### Grimme parameter (PBE+D2 사용 시)

Archive `005_Hydrogen/grimme.fdf`에서 재사용:

```
  H-H:  C6 =   1.45, R0 = 2.002
  V-H:  C6 =  12.74, R0 = 2.563
  Se-H: C6 =  13.79, R0 = 2.772
  Hf-H: C6 =  39.76, R0 = 2.788
```

현재 grimme.fdf (species 1=Hf, 2=Se, 3=V)에 species 4=H 추가 필요.

### Pseudopotential

H.psml 필요 — HPC에 있는지 확인 필요 (PseudoDojo 또는 기존 라이브러리).

---

## 디렉토리 구조

```
03-calc/
├── 08-hetero-v2/          # (기존) vdW-DF2, H 없음 — 비교 기준
│   ├── d_2.5/
│   ├── d_3.0/
│   ├── d_3.5/
│   └── d_4.0/
├── 10-hetero-h-term/      # (신규) vdW-DF2, H termination
│   ├── d_2.0/
│   ├── d_2.5/
│   ├── d_3.0/
│   ├── d_3.5/
│   ├── d_4.0/
│   └── d_4.5/
└── 11-hetero-h-relax/     # (Phase 2) H termination + relaxation
    └── d_X.X/             # minimum 부근
```

---

## 예상 결과 시나리오

### A. H termination으로 minimum 출현

- H가 VSe3 Se dangling bond를 passivate → 비물리적 강한 결합 제거
- Separation energy curve에 ~3.5 A 부근 minimum 출현
- → 가설 지지, Phase 2 relaxation → Phase 3 transport로 진행

### B. H termination에도 단조 감소 유지

- Dangling bond가 주 원인이 아님
- 다른 가능성 검토 필요:
  - Cell size 효과 (electrode 길이 부족)
  - Functional 한계
  - 구조 자체의 문제 (Se3 orientation 등)

---

## 우선순위와 의존관계

```
Phase 1: single-point scan (10-hetero-h-term)
  ├── build_hetero_v2.py 수정 (--h-term 플래그)
  ├── H.psml 확보
  └── HPC 제출 (6 jobs, vdW-DF2)
      │
      ▼
  결과 분석: minimum 유무 확인
      │
      ├── minimum 있음 → Phase 2 relaxation
      │                    │
      │                    ▼
      │               Phase 3 transport
      │
      └── minimum 없음 → 원인 재검토
```
