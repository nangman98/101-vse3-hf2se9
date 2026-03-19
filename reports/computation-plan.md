# VSe3/Hf2Se9 구조 생성 + 계산 전체 계획

## 배경: TP vs TAP 배위

MX₃ 1D chain에서 금속 M은 위·아래 두 개의 X₃ 삼각형 사이에 위치한다.
두 삼각형의 상대적 배향에 따라 배위 구조가 결정된다.

**TP (Trigonal Prismatic)**
- 위·아래 삼각형이 **정렬** (같은 방향)
- 삼각기둥 배위 → 주기: c = d_MM, 4 atoms/cell
- STEM 관측으로 VSe3에서 TP 구조 최초 확인

**TAP (Trigonal Anti-Prismatic)**
- 인접 삼각형이 **60° 회전** (엇갈림)
- 팔면체(octahedral) 배위 → 주기: c = 2×d_MM, 8 atoms/cell
- 대부분의 MX₃ chain 물질(NbSe₃, TaSe₃ 등)이 TAP

```
TP 배위 (side view)        TAP 배위 (side view)

  Se  Se  Se                 Se  Se  Se
    \ | /                      \ | /
     V                          V
    / | \                      / | \
  Se  Se  Se                 Se   Se   Se  ← 60° 회전
    \ | /                      \ | /
     V                          V
    / | \                      / | \
  Se  Se  Se                 Se  Se  Se  ← 원래 방향
```

**핵심 질문**: VSe3에서 TP가 TAP보다 에너지적으로 안정한가? → DFT E(TP) vs E(TAP) 비교

---

## Context

이전 연구자의 접근: Python으로 기하학적 파라미터(d_VSe, d_VV)에서 구조를 처음부터 구성.
VSe3 TP는 수렴했으나, **이종접합(VSe3-Hf2Se9-VSe3) relaxation에서 Hf2Se9 구조 붕괴** 발생.
원인 추정: Hf 원자 사이 vdW 결합이 유지되지 않고, 구조가 틀어지거나 원자가 너무 가까워져서 붙음.

구조 파라미터(결합 길이, 격자 상수)로 처음부터 구성하되, 파라미터 값은 archive relaxed 결과 또는 문헌에서 가져온다.

---

## Phase 1: 단위 구조 준비

### MX₃ chains (01-04) — 파라미터 기반 구성

`build_vse3.py`의 `build_chain(d_MX, d_MM, structure)` 함수로 구성.
두 파라미터(M-X 결합 길이, M-M 거리)만으로 TP/TAP chain 기하학이 결정된다.

**파라미터 소스**: 문헌 기반 초기 추정
- VSe3: d_VSe = 2.45 Å (공유결합 반지름 합, Cordero 2008), d_VV = 3.09 Å (NbSe₃ b축 스케일링, Hodeau 1978 + Shannon 1976)
- VTe3: 공유결합 반지름 비 ×1.15 — d_VTe = 2.82 Å, d_VV = 3.55 Å
- V = Vanadium(23), Se = Selenium(34), Te = Tellurium(52)

| Case | 구조 | 파라미터 | atoms/cell |
|------|------|---------|-----------|
| 01 | VSe3 TP | d_VSe=2.45, d_VV=3.09 | 4 |
| 02 | VSe3 TAP | 동일, 60° 회전 | 8 |
| 03 | VTe3 TP | d_VTe=2.82, d_VV=3.55 | 4 |
| 04 | VTe3 TAP | 동일, 60° 회전 | 8 |

### Hf₂Se₉ (05-06) — archive relaxed 좌표

Hf₂Se₉는 11 atoms(2 Hf + 9 Se)의 복잡한 배위 구조로, 단순 파라미터로 구성 불가.
Archive relaxed 좌표를 초기 구조로 사용한다 (Hf = Hafnium).

| Case | 구조 | 소스 | 핵심 값 |
|------|------|------|---------|
| 05 | Hf2Se9 molecule | archive XV | Hf-Hf=3.80 Å, 25 Å cubic |
| 06 | Hf2Se9 chain | archive XV | Hf-Hf=3.71 Å, c=8.42 Å |

---

## Phase 2: Relaxation (SIESTA on Stampede3)

### 공통 세팅
- XC: PBE + Grimme vdW
- MeshCutoff: 500 Ry
- k-point: 1×1×8 (chain), Gamma (molecule)
- Force tolerance: 0.01 eV/Å
- Variable cell: T (c only)
- `stress 1 2 4 5 6` constraint

### 케이스별 주의사항

| Case | 예상 난이도 | 비고 |
|------|------------|------|
| 01 VSe3 TP | 쉬움 | 이미 relaxed → 거의 즉시 수렴 예상 |
| 02 VSe3 TAP | 중간 | 새 구조, 수렴 모니터링 필요 |
| 03 VTe3 TP | 중간 | 스케일링 → relaxation으로 보정 |
| 04 VTe3 TAP | 중간 | 위와 동일 |
| 05 Hf2Se9 mol | 쉬움 | 이미 relaxed |
| 06 Hf2Se9 chain | 중간~어려움 | 이전에 여러 시도 (charge, basis 변경 등) |

---

## Phase 3: Band/PDOS (relaxation 완료 후)

- Relaxed struct.fdf 복사 → band-pdos 디렉토리
- SCF만 (MD.Steps 0), BandLines + PDOS 설정
- **핵심 결과**: E(TP) vs E(TAP) per atom → TP 안정성 검증

---

## Phase 4: 이종접합 (이전 실패 원인 해결)

### 이전 문제
- Hf2Se9의 Hf 원자가 relaxation 중 VSe3 쪽으로 끌려가거나, Hf-Hf vdW gap 붕괴
- separation test(1-5 Å)를 했지만 최적 거리에서도 구조 불안정

### 개선된 접근법
1. **단계적 relaxation**: VSe3 고정 → Hf2Se9만 relax → 전체 relax (작은 MaxDispl)
2. **Geometry Constraints 강화**: VSe3 원자 좌표 고정
3. **vdW 보정 검토**: Grimme D3(BJ) 또는 vdW-DF2 (Hf의 D2 C6/R0 부정확 가능)
4. **separation test 재수행**: Relaxed 구조로 조립, 1.5-4.0 Å, 0.25 Å 간격, single-point 먼저

---

## Phase 5: Transport (후순위)

- Electrode: VSe3 3uc
- Junction: VSe3-Hf2Se9-VSe3
- TBtrans I-V curve

---

## 코드 (`VSe3-Hf2Se9/02-code/`)

### build_vse3.py — MX₃ chain 구조 생성기

기하학적 파라미터(d_MX, d_MM)에서 TP/TAP chain 구조를 처음부터 구성.

```
입력: d_MX (M-X 결합 길이), d_MM (M-M 거리), structure ("TP" or "TAP")
출력: cell, atoms, species

기하학 (d_MX, d_MM → 전체 구조 결정):
  h = d_MM / 2             M에서 X₃ 평면까지 거리
  r = sqrt(d_MX² - h²)     X₃ 삼각형 외접원 반지름
  d_XX = r × sqrt(3)       X-X 거리

주요 함수:
  build_chain(d_MX, d_MM, structure, M, X) → cell, atoms, species, info
```

### convert_xv.py — XV 파일 변환기

SIESTA relaxation 결과 `siesta.XV` (Bohr) → `struct.fdf` + `struct.xsf` (Å) 변환.
Hf₂Se₉처럼 파라미터 구성이 불가한 구조에 사용.

### generate_structures.py — 전체 구조 일괄 생성

6개 계산 케이스를 `03-calc/`에 생성.

```
실행: python3 generate_structures.py
생성: 03-calc/{01~06}-*/struct.fdf, struct.xsf, input.fdf

파이프라인:
  파라미터(d_VSe, d_VV) ──build_chain──→ 01-VSe3-TP, 02-VSe3-TAP
  파라미터(d_VTe, d_VV) ──build_chain──→ 03-VTe3-TP, 04-VTe3-TAP
  archive XV ──convert_xv──→ 05-Hf2Se9-mol, 06-Hf2Se9-chain
```

### 유틸리티 (build_tap.py, scale_te.py)

기존 구조에서 TAP 파생 또는 칼코겐 스케일링 시 사용 가능한 보조 도구.

---

## 검증 체크리스트

- [ ] 각 struct.xsf → VESTA 시각화로 구조 확인
- [ ] V-Se ≈ 2.46 Å / V-Te ≈ 2.83 Å (물리적 범위 내)
- [ ] Se₃/Te₃ 삼각형이 정삼각형 (편차 < 0.05 Å)
- [ ] TAP: 인접 삼각형이 정확히 60° 회전
- [ ] Hf-Hf 거리 ≈ 3.8 Å (vdW gap 유지)
- [ ] Relaxation 수렴: force < 0.01 eV/Å
- [ ] TP vs TAP 에너지 차이: 물리적으로 합리적 (수십~수백 meV/atom)
