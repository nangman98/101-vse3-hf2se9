# Project Status

## Overview

VSe3 1D chain의 TP 구조 안정성을 DFT로 검증하고, Hf₂Se₉ 이종접합 transport 계산을 수행한다.

## Current focus

- **A2 PBE+D2 v4-prescf**: Perlmutter CPU 노드에서 실행 중 (Job 50892449, PD 대기)
  - 3단계 전략: prescf → relax → verify ([상세](VSe3-Hf2Se9/03-calc/05-hf2se9-mol/stability-test/A2-pbe-d2-convergence-strategy.md))
- **Heterostructure energy scan**: Stampede3 skx-dev에서 실행 중
  - d_3.0: DF2/D2 완료, d_2.5/3.5/4.0: 실행 중 (Jobs 2993128-2993130)
- Hf₂Se₉ stability test Phase A/B 진행 중
- VSe3 vdW-DF2 / PBE+D2 비교 완료

**Updated**: 2026-04-03

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
| A2 | PBE+D2 | — | — | ❌ SCF 미수렴 | r3/r4/v2: SCF 설정 문제 |
| A2-v3 | PBE+D2 (archive 설정) | 4.30 (미수렴) | — | 🔄 진행 중 | SCF 수렴 성공, OOM으로 중단 → 3노드 재제출 |
| A3 | vdW-DF2 | 3.967 | +10% | ✅ 13 steps | |
| A4 | PBE+D3(BJ) | 3.857 | +7% | ✅ 14 steps | |
| A5 | PBE+D3 (VASP) | — | — | 🔄 진행 중 | lmp_cnt에서 restart, step 41 |
| A6 | HSE06+D3 (VASP) | — | — | 🔄 대기 | A5 후 순차 실행 |

→ A2 SCF 실패 상세: [a2-scf-debug.md](reports/hf2se9-stability/a2-scf-debug.md)

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

## 3. Phase C: CNT + MD (준비 단계)

→ 계획: [phase-c-cnt-md.md](reports/hf2se9-stability/phase-c-cnt-md.md)

| Hf₂Se₉@CNT(9,9) oblique | top view |
|---|---|
| <img src="reports/hf2se9-stability/hf2se9-cnt99-oblique.png" width="300"> | <img src="reports/hf2se9-stability/hf2se9-cnt99-top.png" width="200"> |

- CNT 직경 스캔 (single-point) → 최적 직경 결정 → DFT relaxation + Classical MD
- Phase A~D 확정 후 시작

---

## 4. Not Started

| Step | Description | Blocked by |
|------|-------------|------------|
| Phase D | DFT+U scan (U=0~7 eV on Hf 5d) | Phase A+B 결과 |
| Phase C 계산 | CNT 직경 스캔 + DFT relax + Classical MD | Phase A~D + force field 확인 |
| Hf₂Se₉ band/PDOS | chain: band, mol: PDOS | Relaxation |
| 이종접합 조립 | VSe3-Hf₂Se₉-VSe3 | Functional 통일 + Hf₂Se₉ relax |
| Transport | Electrode + Junction + I-V | 이종접합 |

---

## 문서 색인

### 계획

| 문서 | 내용 |
|------|------|
| [computation-plan.md](reports/computation-plan.md) | 전체 계산 계획 (Phase 1~5) |
| [hf2se9-stability.md](reports/hf2se9-stability/hf2se9-stability.md) | Hf₂Se₉ 안정성 테스트 (Phase A~D 설계, 결과 테이블) |
| [phase-c-cnt-md.md](reports/hf2se9-stability/phase-c-cnt-md.md) | Phase C: CNT + MD 계획 |

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
