# Project Status

## Overview

VSe3 1D chain의 TP 구조 안정성을 DFT로 검증하고, Hf₂Se₉ 이종접합 transport 계산을 수행한다.

## Current focus

1순위 relaxation 누리온 실행 중 (01, 02, 05, 06) → long+flat 큐 동시 제출, vdW-DF2

## Completed

| Step | Description | Data | Report |
|------|-------------|------|--------|
| 구조 구성 | VSe3 TP/TAP 초기 구조 (문헌 파라미터 기반) | `03-calc/01-vse3-tp/`, `02-vse3-tap/` | — |
| 구조 구성 | VTe3 TP/TAP 초기 구조 (×1.15 스케일) | `03-calc/03-vte3-tp/`, `04-vte3-tap/` | — |
| 구조 구성 | Hf₂Se₉ mol/chain 초기 구조 (confacial bioctahedron) | `03-calc/05-hf2se9-mol/`, `06-hf2se9-chain/` | — |
| 실패 분석 | 이전 Hf₂Se₉ relaxation 실패 원인 조사 | — | `reports/initial-structures/failure-analysis.md` |

## In progress

| Step | Description | Data | Status |
|------|-------------|------|--------|
| Relaxation 1순위 | VSe3 TP/TAP + Hf₂Se₉ mol/chain (vdW-DF2) | `03-calc/{01,02,05,06}/relax/` | 누리온 long+flat 제출 |

## Not started

| Step | Description | Data | Blocked by |
|------|-------------|------|------------|
| Relaxation 2순위 | VTe3 TP/TAP (vdW-DF2) | `03-calc/{03,04}/relax/` | 1순위 완료 |
| Band/PDOS | 전체 6개 시스템 | `03-calc/{01~06}/band-pdos/` | Relaxation |
| 이종접합 | VSe3-Hf₂Se₉-VSe3 조립 + relaxation | — | Hf₂Se₉ relax |
| Transport | Electrode + Junction + I-V | — | 이종접합 |

## Key files

| File | Description |
|------|-------------|
| `reports/computation-plan.md` | 전체 계산 계획 |
| `reports/initial-structures/failure-analysis.md` | Hf₂Se₉ 실패 원인 + vdW 방법 비교 |
| `VSe3-Hf2Se9/02-code/generate_structures.py` | 전체 구조 생성 스크립트 |
| `VSe3-Hf2Se9/02-code/build_vse3.py` | MX₃ chain 구조 생성기 |
| `VSe3-Hf2Se9/02-code/build_hf2se9.py` | Hf₂Se₉ confacial bioctahedron 생성기 |
