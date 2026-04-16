# Project Status

## Overview

VSe3 1D chain의 TP 구조 안정성을 DFT로 검증하고, Hf₂Se₉ 이종접합 transport 계산을 수행한다.

## Current focus

- **H termination 3-mode scan 완료 — gap 모드 (H⊥Se₃) 최안정**
  - bond 6/6, gap 5/6, tilt 6/6 완료 (Perlmutter, vdW-DF2, ELPA)
  - gap d=4.5만 SCF stuck → TIME LIMIT → Stampede3에서 재실행 중 (job 3027949)
  - 절대 에너지 비교 (44 atoms 동일): gap < bond (+1.1 eV) < tilt (+3.7 eV)
  - gap d=3.5~4.0 Å flat (ΔE=4 meV): H passivation이 interface 결합 완전 차단
  - **결론: relaxation은 gap 모드 (H⊥Se₃), d=3.5 Å로 진행**
  - 결과 로컬 다운 완료, 미팅노트 피겨 완성
- **Relaxation → Transport 파이프라인 확정**:
  - gap 모드 d=3.5 Å 구조에서 full relaxation → transport
  - 처음부터 transport 크기(~20uc) 셀로 1회 relax → 그대로 transport
- **CNT encapsulation**: 보류 (04-07 미팅 결정)
- **A2 PBE+D2 v5a/v5b**: 보류

**Updated**: 2026-04-15 (3-mode 비교 완료, gap d=4.5 Stampede3 재실행 중)

---

## 1. VSe3 TP vs TAP

### vdW-DF2

| | TP | TAP |
|---|---|---|
| 구조 | <img src="reports/initial-structures/vse3-tp-relaxed.png" width="200"> | <img src="reports/initial-structures/vse3-tap-relaxed.png" width="200"> |
| c (Å) | 3.114 | 5.535 |
| V-Se (Å) | 2.508 | 2.508 |
| Se₃ 폭 (Å) | 3.405 | 3.623 |
| V-V (Å) | 3.114 | 2.768 |
| E (eV/atom) | −2988.762 | −2988.721 |
| **ΔE** | **TP가 41 meV/atom 안정** | |
| Band | 금속성 | 금속성 |

### PBE+D2

| | TP | TAP |
|---|---|---|
| 구조 | <img src="reports/initial-structures/vse3-tp-d2-relaxed.png" width="200"> | <img src="reports/initial-structures/vse3-tap-d2-relaxed.png" width="200"> |
| c (Å) | 3.027 | 5.343 |
| V-Se (Å) | 2.461 | 2.458 |
| Se₃ 폭 (Å) | 3.362 | 3.574 |
| V-V (Å) | 3.027 | 2.672 |
| E (eV/atom) | −2974.713 | −2974.693 |
| **ΔE** | **TP가 20 meV/atom 안정** | |
| Band | 금속성 | 금속성 |

### Band Structure (TP)

| vdW-DF2 (c = 3.114 Å) | PBE+D2 (c = 3.027 Å) |
|---|---|
| <img src="reports/initial-structures/vse3-tp-band.png" width="300"> | <img src="reports/initial-structures/vse3-tp-band-d2.png" width="300"> |

---

## 2. Hf₂Se₉ 안정성 검토

→ 마스터 계획: [hf2se9-stability.md](reports/hf2se9-stability/hf2se9-stability.md)

### Phase A: Exchange scan (molecule)

| Test | Functional | Hf-Hf (Å) | Δ(TEM 3.6 Å) | 수렴 | 비고 |
|------|-----------|-----------|--------------|------|------|
| A1 | PBE | 3.857 | +7% | ✅ 14 steps | |
| A2 | PBE+D2 | — | — | ❌ SCF 미수렴 | r3/r4/v2/v3: SCF 설정 문제 |
| A2-v4 | PBE+D2 (Perlmutter, FD 700K) | 3.543 | −1.6% | ✅ 완료 | 비표준 occupation, 결과 해석 모호 |
| A2-v5a | PBE+D2 (MP 300K, Tol 1e-4, Weight 0.05) | — | — | ⚠️ SCF ✅ / post-SCF OOM | InitMesh 360³ 시점 OOM, 8노드 재시도 필요 |
| A2-v5b | PBE+D2 (MP 300K, Tol 1e-6) | — | — | ⚠️ SCF ✅ / post-SCF OOM | 동일, 8노드 재시도 필요 |
| A3 | vdW-DF2 | 3.967 | +10% | ✅ 13 steps | |
| A4 | PBE+D3(BJ) | 3.857 | +7% | ✅ 14 steps | |
| A5 | PBE+D3 (VASP) | — | — | 🔄 진행 중 | lmp_cnt에서 restart, step 41 |
| A6 | HSE06+D3 (VASP) | — | — | 🔄 대기 | A5 후 순차 실행 |

→ A2 SCF 실패 상세 (+ v5 OOM): [a2-scf-debug.md](reports/hf2se9-stability/docs/a2-scf-debug.md)

### Phase A 구조 비교 (molecule)

| A1: PBE | A3: vdW-DF2 | A4: PBE+D3(BJ) |
|---|---|---|
| <img src="reports/initial-structures/hf2se9-A1-pbe.png" width="200"> | <img src="reports/initial-structures/hf2se9-A3-vdwdf2.png" width="200"> | <img src="reports/initial-structures/hf2se9-A4-d3bj.png" width="200"> |

| 치수 | A1: PBE | A3: vdW-DF2 | A4: PBE+D3 | TEM |
|---|---|---|---|---|
| Hf-Hf (Å) | 3.857 (+7%) | 3.967 (+10%) | 3.857 (+7%) | 3.6 |
| 전체 길이 (Å) | 6.70 | 6.98 | 6.70 | 7.2 |
| Se₃ 폭 (Å) | ~2.9 | ~2.9 | ~2.9 | 3.6~4.2 |

### Phase B: Basis scan

| Test | EnergyShift | 상태 |
|------|------------|------|
| B1 | 10 meV | 🔄 step 43 진행 중 (27h/120h) |
| B2~B5 | 30~200 meV | 대기 (B1 후 순차) |

### Hf₂Se₉ Relaxation 결과

#### vdW-DF2

| | molecule (05) | chain (06) | TEM |
|---|---|---|---|
| 구조 | <img src="reports/initial-structures/hf2se9-mol-relaxed.png" width="200"> | <img src="reports/initial-structures/hf2se9-chain-relaxed.png" width="200"> | — |
| Hf-Hf (Å) | 3.967 (+10%) | 4.164 (+15.7%) | 3.6 |
| c축 (Å) | 25 (고정) | 13.161 | ~7.2 |
| vdW gap (Å) | — | 5.87 (+68%) | ~3.5 |
| 수렴 | ✅ | ✅ | — |

#### PBE+D2 Chain (197 steps, 미수렴)

| | PBE+D2 chain | vdW-DF2 chain | TEM |
|---|---|---|---|
| 구조 | <img src="reports/hf2se9-stability/chain-d2-197step.png" width="200"> | <img src="reports/initial-structures/hf2se9-chain-relaxed.png" width="200"> | — |
| c축 (Å) | 11.882 | 13.161 | ~7.2 |
| Hf-Hf (Å) | 4.47 | 4.164 | 3.6 |
| vdW gap (Å) | 5.59 | 5.87 | ~3.5 |
| Max force (eV/Å) | 0.094 | 0.009 ✅ | — |
| 상태 | 미수렴 (OOM) | 수렴 | — |

### 07-hetero separation test

| 구조 (gap = 3.5 Å) | Energy vs Separation |
|---|---|
| <img src="reports/initial-structures/hetero-d3.5.png" width="300"> | <img src="reports/initial-structures/hetero-energy-vs-sep.png" width="300"> |

vdW-DF2 relaxed 구조, 2.5~4.0 Å. 에너지 단조 감소 — 실험(~3.5 Å)과 일치하는 최적 분리 거리 미발견.

---

## 3. Phase C: CNT + MD (진행 중)

→ 계획: [phase-c-cnt-md.md](reports/hf2se9-stability/phase-c-cnt-md.md)

| Hf₂Se₉@CNT(9,9) oblique | top view |
|---|---|
| <img src="reports/hf2se9-stability/hf2se9-cnt99-oblique.png" width="300"> | <img src="reports/hf2se9-stability/hf2se9-cnt99-top.png" width="200"> |

### Diameter scan 진행 상황

| (n,n) | empty CNT | Hf₂Se₉@CNT | 상태 |
|------|-----------|-----------|------|
| (5,5) | ✅ NORMAL_EXIT | ✅ NORMAL_EXIT | 04-06 17:03~17:23 (누리온) |
| (6,6) | ✅ NORMAL_EXIT | ✅ NORMAL_EXIT | 04-06 17:06~17:35 |
| (7,7) | ✅ NORMAL_EXIT | ✅ NORMAL_EXIT | 04-06 17:10~17:50 |
| (8,8) | (이전 슬롯) | (이전 슬롯) | 04-06 minimum 발견 (메모리 04-06 세션 노트) |
| (9,9)~(12,12) | (이전 슬롯) | (이전 슬롯) | 04-06 새벽 슬롯 |

- 로컬 다운: `03-calc/05-hf2se9-mol/stability-test/phase-c/diameter-scan{,-ref}/`
- 다운된 파일: `struct.fdf`, `input.fdf`, `siesta.stdout`, `siesta.STRUCT_OUT`, `siesta.EIG`, `siesta.XV`, `siesta.FA`, `OUTVARS.yml`, `0_NORMAL_EXIT`, `*.xsf`, `grimme.fdf`, `FORCE_STRESS` 등
- 제외 (대용량/재생성 가능): `siesta.DM`, `siesta.xml`, `siesta.ORB_INDX`, `siesta.BONDS*`, `MMpot.*`, `*.psml`, `*.ion*`, `PARALLEL_DIST`
- **다음**: encapsulation energy = E[Hf₂Se₉@CNT] − E[CNT] − E[Hf₂Se₉] vs CNT 직경 분석 (5,5)~(12,12) 통합

---

## 4. Phase D: DFT+U scan (진행 중, 모두 미완)

누리온 `/scratch/x3251a05/VSe3-Hf2Se9/03-calc/05-hf2se9-mol/stability-test/D{1..6}-*`. 로컬에는 없음.

| Case | U (orbital) | SCF 상태 | 종료 | 비고 |
|---|---|---|---|---|
| D1-u0.stopped | U=0 (Hf 5d, control) | iter 36 dDmax=0.000033 (미수렴) | OOM SIGKILL (node7729) | `.stopped` 표시, 의도적 중단 |
| D2-u1.stuck | U=1 (Hf 5d) | iter 62 dDmax=0 ✅, 다음 step에서 0.41~0.88 발산 | OOM SIGKILL (node7729) | `.stuck` = next geom step에서 SCF 발산 |
| D3-u3 | U=3 (Hf 5d) | iter 63 dDmax=0 ✅ | OOM SIGKILL (node7706) | 04-03 + 04-05 두 번 시도, 둘 다 OOM |
| D4-u5 | U=5 (Hf 5d) | iter 63 dDmax=0 ✅ | 🔄 04-07 새벽부터 진행 중 | Hubbard local occupation `max change=0.000815`에서 38 iter째 진동 (Hubbard self-consistency 미수렴) |
| D5-u7 | U=7 (Hf 5d) | — | 미시작 | input.fdf, struct.fdf만 |
| D6-u3-se4p | U=3 (Se 4p) | — | 미시작 | input.fdf, struct.fdf만 |

**관찰**:
- D1, D3는 A2-v5와 같은 패턴 — SCF 수렴 후 post-SCF mesh 360³ 단계에서 OOM. 8노드 재시도가 동일한 해결책.
- D2 (U=1)는 OOM 외에 next geometry step에서 SCF 발산도 있음 — 별도 mixing 조정 필요할 수도.
- D4는 SCF는 dDmax=0인데 Hubbard projector self-consistency가 0.000815에서 못 떨어짐 — DFTU.PopTol(0.001)에 닿을락 말락.
- **유의미한 결과(NORMAL_EXIT) = 0개**.

## 5. H Termination (신규, 최우선)

→ 계획: [h-termination.md](reports/h-termination/h-termination.md)

| Phase | 내용 | 상태 | Blocked by |
|-------|------|------|------------|
| Phase 1 | single-point scan (d=2.0~4.5 A, vdW-DF2, H 있음) | 📋 준비 | build script 수정, H.psml |
| Phase 2 | minimum 부근 relaxation | 대기 | Phase 1 결과 |
| Phase 3 | transport 계산 | 대기 | Phase 2 안정 구조 |

## 6. Not Started / 보류

| Step | Description | Blocked by | 비고 |
|------|-------------|------------|------|
| Phase C 분석 | encapsulation energy vs CNT 직경 | 데이터 통합 | 우선순위 내림 (04-07) |
| Phase C MD | DFT relax + Classical MD | Phase C 분석 결과 | 보류 |
| Hf₂Se₉ band/PDOS | chain: band, mol: PDOS | Relaxation | |
| Transport | Electrode + Junction + I-V | H termination relax | H-term Phase 3으로 이동 |

---

## 문서 색인

### 계획

| 문서 | 내용 |
|------|------|
| [computation-plan.md](reports/computation-plan.md) | 전체 계산 계획 (Phase 1~5) |
| [hf2se9-stability.md](reports/hf2se9-stability/hf2se9-stability.md) | Hf₂Se₉ 안정성 테스트 (Phase A~D 설계, 결과 테이블) |
| [phase-c-cnt-md.md](reports/hf2se9-stability/phase-c-cnt-md.md) | Phase C: CNT + MD 계획 |
| [h-termination.md](reports/h-termination/h-termination.md) | H termination separation scan 계획 |

### 분석

| 문서 | 내용 |
|------|------|
| [failure-analysis.md](reports/initial-structures/failure-analysis.md) | 이전 Hf₂Se₉ relaxation 실패 원인 |
| [vdw-methods-comparison.md](reports/hf2se9-stability/vdw-methods-comparison.md) | vdW-DF2 vs D2 비교 |
| [stability-comparison-method.md](reports/hf2se9-stability/stability-comparison-method.md) | Functional 간 비교 방법론 |
| [a2-scf-debug.md](reports/hf2se9-stability/a2-scf-debug.md) | A2 (PBE+D2) SCF 실패 상세 |

### 미팅

| 날짜 | 내용 |
|------|------|
| [2026-03-16](meetings/2026-03-16.md) | 프로젝트 시작 |
| [2026-03-19](meetings/2026-03-19.md) | 4축 체계적 검토 계획 확정 |
| [next.md](meetings/next.md) | 다음 미팅 progress report |

### 코드

| 파일 | 내용 |
|------|------|
| `VSe3-Hf2Se9/02-code/generate_structures.py` | 전체 구조 일괄 생성 |
| `VSe3-Hf2Se9/02-code/build_vse3.py` | MX₃ chain 구조 생성기 |
| `VSe3-Hf2Se9/02-code/build_hf2se9.py` | Hf₂Se₉ confacial bioctahedron 생성기 |
| `render_structure.py` | VESTA급 3D 구조 렌더러 (pyvista) |
