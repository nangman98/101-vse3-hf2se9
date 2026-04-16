# H Termination Plan — VSe3–Hf2Se9 Heterostructure

**Status**: Plan (2026-04-13). 구조 생성 완료 (gap, tilt 모드), bond 모드 재구성 예정. 계산 미제출.

**관련 문서**:
- 이전 plan (superseded): [h-termination.md](h-termination.md)
- 미팅 결정 근거: [meetings/2026-04-07/2026-04-07.md](../../meetings/2026-04-07/2026-04-07.md)
- 전체 stability plan: [reports/hf2se9-stability/hf2se9-stability.md](../hf2se9-stability/hf2se9-stability.md)

---

## 1. 문제 정의

08-hetero-v2 (vdW-DF2) + 09-hetero-d2 (PBE+D2): separation energy가 d = 2.5 ~ 4.0 Å 전 구간에서 **단조 감소**. 실험에서 관측되는 ~3.5 Å minimum 재현 안 됨.

| d (Å) | vdW-DF2 비대칭 (eV) | vdW-DF2 대칭 (eV) | PBE+D2 대칭 (eV) |
|---|---|---|---|
| 2.5 | −3.73 | −6.21 | −8.31 |
| 3.0 | −2.00 | −4.10 | −4.89 |
| 3.5 | −0.84 | −1.61 | −1.84 |
| 4.0 | 0.00 | 0.00 | 0.00 |

### 가설 (2026-04-07 미팅)

VSe3를 chain에서 잘라낸 단면의 Se에 **dangling bond**가 남아 있어, 인터페이스에서 비물리적으로 강한 결합을 형성한다. Hf₂Se₉ molecule은 closed-shell이므로 문제는 VSe3 측에 한정.

**검증 방법**: VSe3 interface Se에만 H를 붙인 구조 / 안 붙인 구조의 separation energy curve 비교.

---

## 2. 화학적 배경 — Dangling bond의 실체

### VSe3 TP chain의 국소 구조 (vdW-DF2 relaxed)

| 항목 | 값 | 출처 |
|---|---|---|
| c-axis (chain 주기) | 3.1145 Å | `01-vse3-tp/relax/STRUCT_OUT` |
| V-Se bond length | **2.508 Å** | [STATUS.md §1](../../STATUS.md#1-vse3-tp-vs-tap) |
| V 위치 (xy) | chain 축 (12.5, 12.5) | `build_hetero_v2.py` |
| Se 위치 (xy) | (12.5, 14.47), (10.80, 11.52), (14.20, 11.52) | 동일 |
| Se의 xy offset from V | 1.97 Å (radial out) | 좌표 계산 |
| V-Se-V 각도 (z-axis에서) | 2 × arctan(1.97/1.557) = 2 × 51.7° = **103.4°** | `c/2 = 1.557 Å`, 위 값 |

각 Se는 **V 2개**와 bond (z = Se_z ± c/2 위치). Trigonal prism geometry.

### Hetero 셀에서 잘린 위치

z축 적층: `Se3_boundary | [V Se3] × 3 | gap | Hf₂Se₉ | gap | [Se3 V] × 3 | (PBC wrap)`

- **Left electrode 마지막 Se3** (z = 3c = 9.343 Å): 정상적이면 z = 3.5c = 10.900 Å에 **다음 V**가 있어야 하지만 gap+molecule이 대신 자리잡음
- **Right electrode 첫 Se3**: 대칭적으로 아래쪽 V 잃음
- 따라서 **사라진 V의 방향**이 dangling bond 방향

### 사라진 V의 위치 (각 interface Se에 대해)

Left side (z = 3c = 9.343 Å) 기준:
```
V_missing = (12.5, 12.5, 3c + c/2) = (12.5, 12.5, 10.900)
Se → V_missing 벡터 = (−Δx, −Δy, +c/2)    # Δ = Se의 xy offset
|벡터| = sqrt(1.97² + 1.557²) = 2.508 Å    # bulk V-Se와 일치 ✓
방향 = (−0.785, 0 or ±0.866·(−0.866 or 0.866), +0.621)
z축에서 기울기 = arccos(0.621) = 51.7°
방향성: chain 안쪽 (inward, radial) + gap 쪽 (+z)
```

Right side는 대칭 (z-부호 반대).

---

## 3. H 배치 모드 정의

### Mode `bond` (primary, 물리적 근거 기반)

H가 사라진 V의 방향으로 배치 → H-Se bond가 원래 V-Se bond의 방향과 일치. Local trigonal prism geometry partial 보존.

```python
for each interface Se at (sx, sy, sz):
    V_missing = (chain_cx, chain_cy, sz ± c/2)     # +c/2=left, −c/2=right
    bond_vec = V_missing - (sx, sy, sz)
    unit_vec = bond_vec / |bond_vec|               # |bond_vec| = 2.508 Å
    H_pos = Se + d_SeH × unit_vec
```

**H 좌표 샘플 (d = 3.5 Å, d_SeH = 1.460 Å)**:

| Se | Se 좌표 | H 좌표 | 방향 |
|---|---|---|---|
| Se1 (apex) | (12.50, 14.47, 9.343) | (12.50, 13.33, 10.249) | z축에서 51.7°, −y 방향 |
| Se2 | (10.80, 11.52, 9.343) | (11.79, 12.09, 10.249) | +x, +y |
| Se3 | (14.20, 11.52, 9.343) | (13.21, 12.09, 10.249) | −x, +y |

모든 H가 **chain 안쪽 + gap 쪽**으로 향함. Right side는 부호 반전.

### Mode `gap` (sensitivity test, optional)

H가 pure +z/−z 방향. Chain 기하 무시, Se의 "가장 단순한 passivation" 가정.
- H_pos = Se + d_SeH × (0, 0, ±1)
- 물리적 근거: 없음. Archive 관례 답습.

### Mode `tilt` (sensitivity test, optional)

H가 z축에서 45° 기울어지고 radial **outward** 방향. Chain 바깥쪽 vdW 이웃 (bulk에서 인접 chain Se가 있던 자리)을 모사.
- H_pos = Se + d_SeH × [sin45° · r̂_radial_out(xy) + cos45° · ẑ]
- 물리적 근거: bulk VSe3에서 인접 chain Se가 제공했을 vdW 상호작용을 H로 대체. 단, vdW 이웃은 bond가 아니므로 정당성 약함.

---

## 4. d(Se-H) 값 확정

**d(Se-H) = 1.460 Å (고정)**

**근거**:
- **NIST CCCBDB**: H₂Se 분자의 experimental r₀ = **1.460 Å**
  - URL: [https://cccbdb.nist.gov/exp2x.asp?casno=7783075](https://cccbdb.nist.gov/exp2x.asp?casno=7783075&charge=0)
  - Citation: 1998Kuc = K. Kuchitsu (ed.), *Landolt-Börnstein: Structure Data of Free Polyatomic Molecules*, Vol. II/25A (Springer, 1998)
- **Solid-state Se passivation 관례**: MoSe2, CdSe DFT 논문에서는 Se-H를 **relax**하는 것이 표준. 최종 값은 대체로 1.46~1.52 Å 범위로 수렴.
  - Reference: [ACS Omega MoSe2 polymorphs study](https://pubs.acs.org/doi/10.1021/acsomega.2c08217), [Nature Sci. Rep. pseudo-H passivation](https://www.nature.com/articles/srep20055)

**왜 고정?**
- Single-point 스캔 목적: d(hetero gap) 1개 변수만 변화시켜 separation curve 해석 단순화
- H만 relax하면 각 gap마다 d(Se-H)가 조금씩 달라져 **gap vs energy** 비교가 오염됨
- 1.46 Å는 실험값이므로 DFT starting point으로 bias 없음

---

## 5. 실행 계획

### Phase 1: bond 모드 단독 single-point scan (primary)

**디렉토리 구조**:
```
03-calc/10-hetero-h-term/
├── bond/              # ← primary run
│   ├── d_2.0/
│   ├── d_2.5/
│   ├── d_3.0/
│   ├── d_3.5/
│   ├── d_4.0/
│   └── d_4.5/
├── gap/   (기존 생성됨, deprecated — sensitivity 필요 시 재활용)
└── tilt/  (기존 생성됨, deprecated — sensitivity 필요 시 재활용)
```

**구조 스펙** (각 `d_X.X/`):
- 44 atoms: 6V + 2Hf + 30Se + 6H
- Cell: 25 × 25 × (2·n_elec·c + 2·d + h_mol) Å
- Species: 1=Hf, 2=Se, 3=V, 4=H

**SIESTA 설정**:
- Functional: vdW-DF2 (LMKLL) — 08-hetero-v2와 직접 비교
- MeshCutoff: 500 Ry
- k-grid: 1 × 1 × 4
- SCF.DM.Tolerance: 1.0 × 10⁻⁴
- MD.Steps: 0 (single-point)
- SystemLabel: `siesta`
- Pseudopotential: `V.psml`, `Se.psml`, `Hf.psml` + **`H.psml`** (vdW-DF2 호환)
  - 확보 경로 미확정: 누리온 기존 psml 확인 → PseudoDojo v0.4 vdW-DF2 set에서 다운로드

### Phase 2 (조건부): minimum이 나오면 진행

- Minimum 부근 (d ≈ 3.0~3.5 Å 예상) relaxation
  - MD.Steps: 500, MaxForceTol: 0.01 eV/Å
  - Constraints: cell 고정, electrode V/Se 고정, **H + Hf₂Se₉만 relax**
- 비교 항목: Hf-Hf 거리, Se-Se interface 거리, H 위치 변화

### Phase 3 (조건부): Sensitivity test if reviewer/paper 요구

- `gap/`, `tilt/` 재사용하여 `bond`와 같은 조건으로 scan
- 세 곡선 비교 → 결과의 robustness 판단

### Phase 4 (조건부): 정합되는 구조에서 Transport 계산 (2026-04-07 미팅 결정)

---

## 6. 예상 시나리오 및 판정 기준

| 시나리오 | 판정 | 후속 |
|---|---|---|
| A. bond 모드에서 d ≈ 3.5 Å 부근 minimum 출현 | 가설 지지 | Phase 2 relaxation → Phase 4 transport |
| B. bond에서도 단조 감소 | 가설 reject | 원인 재검토: cell size, electrode 길이, functional, 구조 자체 |
| C. bond에서 이상한 minimum (d < 2.5 Å 등) | H-Hf₂Se₉ 충돌 영향 가능 | gap/tilt 비교로 H 방향 민감도 확인 |

---

## 7. 작업 목록

- [ ] **H.psml 확보** — 누리온에서 기존 psml 확인, 없으면 PseudoDojo vdW-DF2 set 다운로드
- [ ] **`build_hetero_v2.py`에 `bond` 모드 추가** — 현재 `gap`/`tilt` 뒤에 `bond` 추가, default 변경
- [ ] **`03-calc/10-hetero-h-term/bond/d_{2.0~4.5}/` 생성** — 6 디렉토리, 각 4 파일
- [ ] **xsf 시각 검증** — VESTA에서 H 위치, chain 기하 확인 (1 case 선택)
- [ ] **PBS 스크립트 작성** (6 jobs, vdW-DF2, 누리온 long8n or long12n)
- [ ] **사용자 승인 후 제출** — 철칙: qsub 전 승인
- [ ] **결과 분석 및 본 문서 업데이트**

---

## 8. 아카이브 참고 (왜 이전 시도가 실패했는가)

`archive/101_VSe3-Hf2Se9/PPT_summary_aug25/005_Hydrogen/`:
- Separation 범위: 0.4 ~ 0.8 Å (repulsive wall만 sampling) → 현재 계획: **2.0 ~ 4.5 Å**
- H 양쪽 모두 (VSe3 + Hf₂Se₉) → 현재 계획: **VSe3만** (미팅 결정)
- d(Se-H) ~1.0 Å (너무 짧음, 실제 bond 길이 아님) → 현재 계획: **1.460 Å (NIST 값)**
- Functional PBE+D2 → 현재 계획: **vdW-DF2** (08-hetero-v2와 비교)
- Electrode 6 uc → 현재 계획: **3 uc**

---

## 9. References

1. NIST CCCBDB H₂Se experimental data: [https://cccbdb.nist.gov/exp2x.asp?casno=7783075](https://cccbdb.nist.gov/exp2x.asp?casno=7783075&charge=0)
2. K. Kuchitsu (ed.), *Landolt-Börnstein: Structure Data of Free Polyatomic Molecules*, Vol. II/25A, Springer (1998) — NIST citation tag `1998Kuc`.
3. Pseudo-H passivation (일반 방법론): Z. Li et al., *Sci. Rep.* **6**, 20055 (2016). [https://www.nature.com/articles/srep20055](https://www.nature.com/articles/srep20055)
4. MoSe2 polymorphs (Se-H relaxation 관례 reference): *ACS Omega* (2022). [https://pubs.acs.org/doi/10.1021/acsomega.2c08217](https://pubs.acs.org/doi/10.1021/acsomega.2c08217)
5. 2026-04-07 미팅 노트 (가설 제안 context): [meetings/2026-04-07/2026-04-07.md](../../meetings/2026-04-07/2026-04-07.md)
