# Previous Calculations Review

**Date**: 2026-03-16
**Updated**: 2026-03-16

## Key Finding

약 1년 전 수행된 VSe3/Hf2Se9 계산이 두 디렉토리(`101_VSe3-Hf2Se9/`, `VSe3-Hf2Se9/`)에 보존되어 있다.
VASP(MD, hybrid DFT), SIESTA(밴드/PDOS, transport), Quantum ESPRESSO(functional 비교)를 활용하여 Hf2Se9 분자/체인의 구조 안정성, 전자구조, 광학물성, 전송 특성까지 폭넓게 진행하였으나, **Hf 도핑 molecule 구조가 불안정**하여 핵심 목표였던 1D molecule junction 계산이 미완으로 남았다.

---

## Method

### 사용 코드

| 코드 | 용도 | 주요 세팅 |
|------|------|-----------|
| **VASP** | MD, relaxation, hybrid functional | ENCUT=400-500 eV, EDIFF=1e-6~1e-8, DFT-D3(BJ) |
| **SIESTA** | 밴드, PDOS, transport (TranSIESTA) | MeshCutoff=500 Ry, PBE+Grimme vdW |
| **Quantum ESPRESSO** | functional 비교 테스트 | ecutwfc=100 Ry, B3LYP/PBE/LDA |

### 공통 계산 파라미터

- **분자/체인 셀**: 25 A 큐빅 (고립 조건)
- **이종접합 셀**: 25 x 25 x 74.7 A (z방향 확장)
- **k-point**: Gamma-only (분자), 1x1x4 (체인/transport)
- **van der Waals**: IVDW=10 (DFT-D3(BJ), VASP) / Grimme (SIESTA)
- **MD**: Langevin thermostat (MDALGO=3), 300 K, timestep 0.5-2.0 fs

---

## Results

### A. 101_VSe3-Hf2Se9/ (메인 계산)

#### 001: Hf2Se9 단분자 (Single Molecule)

시스템: 2 Hf + 9 Se = 11 atoms, 25 A 큐빅셀

| 계산 | 코드 | 세팅 | 결과 |
|------|------|------|------|
| **001_MD** | VASP | NVT 300K, 500 steps, dt=2.0 fs | 분자 안정성 확인, XDATCAR 궤적 |
| **001-1_MD2** | VASP | NVT 300K, 100 steps | 추가 MD 테스트 |
| **003_MD_500step** | VASP | NVT 300K, 500 steps, dt=1.0 fs, NELM=100 | 에너지 vs step 플롯 (step.png) |
| **002_bands** | SIESTA | PBE, MeshCutoff=500 Ry | 밴드+PDOS, Fermi 근처 -2~+2 eV |

분석 도구: `extract_MD.ipynb` (MD 궤적 추출), `bandspdos_SIESTA.ipynb` (밴드 시각화)

#### 002: Hf2Se9 체인 (1D Chain)

시스템: Hf2Se9 단위를 1D으로 연장한 체인 구조

| 계산 | 코드 | 세팅 | 결과 |
|------|------|------|------|
| **000_generate** | - | rotate.py로 체인 방향 정렬 | struct.xsf, initial.xsf |
| **001_MD** | VASP | NVT 300K, 500 steps, dt=2.0→1.0 fs, ISIF=3 | 체인 안정성, ICONST 제약조건 |
| **003_MD1000step** | VASP | NVT 300K, 1000 steps, dt=1.0→0.5 fs | 장시간 궤적, data/ 디렉토리에 추출 데이터 |
| **002_bandspdos** | SIESTA | PBE+Grimme, MeshCutoff=500 Ry | 밴드(bands.png)+PDOS |

#### 003: VSe3-Hf2Se9 이종접합 (Heterostructure)

시스템: V20Se72Hf2 = 94 atoms, VSe3 monolayer(3층) + Hf2Se9 흡착

| 계산 | 코드 | 세팅 | 결과 |
|------|------|------|------|
| **001_MD** | VASP | NVT 300K, 100 steps, ISIF=2(셀 고정), NELM=300 | 이종접합 안정성 |
| **002_bandspdos** | SIESTA | PBE, MeshCutoff=500 Ry | 밴드+PDOS (31-58 MB 대용량) |
| **002b_bandspdos** | SIESTA | 대안 설정 | 밴드+PDOS 비교 |
| **003_checkU** | - | Hubbard U 파라미터 테스트 | DFT+U 적절값 탐색 |
| **004_CNT_Hf2Se9** | SIESTA | CNT+Hf2Se9 구조 | cnt.ipynb 분석 |

Mulliken 전하 분석: `mulliken_analysis.ipynb`, `mulliken_data.txt`

#### 004: 전송 특성 (Transport)

시스템: Hf2Se9 체인 20 unit cell 기반 molecular junction

| 계산 | 코드 | 세팅 | 결과 |
|------|------|------|------|
| **001_electrode** | SIESTA | 전극 참조 계산 | siesta.TSHS (반무한 전극용) |
| **001_bandspdos_20uc** | SIESTA | 20 unit cell 밴드+PDOS | siesta.PDOS (58 MB), Mulliken 분석 |
| **002_IVcurve** | TranSIESTA + TBtrans | 7개 전압점 (0.00-0.30 V) | 전송계수 vs 에너지, I-V 곡선 |

I-V 계산 세부:
- 각 전압별: SCF(SIESTA) → TranSIESTA(전극 결합) → TBtrans(전송계수)
- k-point: 1x1x4, Electronic Temperature: 400 K
- 에너지 contour: -75 ~ +20 eV, 0.01 eV 간격
- 병렬: SIESTA 1024코어, TBtrans 64코어
- 스크립트: `job_siesta.sh`, `execute_tb.sh`

#### 005: 광학물성 (Hybrid Functional)

목적: ionization potential, electron affinity, exciton binding energy

| 계산 | 코드 | 세팅 | 상태 |
|------|------|------|------|
| **B3LYP neutral** | VASP | AEXX=0.20, GGA=91, ALGO=Damped, ENCUT=400 eV | 완료 |
| **B3LYP neutral (old struct)** | VASP | 대안 구조에서 B3LYP | 완료 |
| **B3LYP e-doped (old struct)** | VASP | 전자 도핑 (EA 계산용) | 완료 |
| **HSE06 neutral** | VASP | AEXX=0.25, HFSCREEN=0.2 | **미완 (빈 디렉토리)** |
| **HSE06 e-doped** | VASP | HSE06 전자 도핑 | **미완** |
| **PBE, LDA** | VASP | 표준 functional 비교용 | **미완** |
| **Hf2Se9-H (수소화)** | SIESTA | Grimme vdW | 구조 최적화 |

#### PPT_summary_aug25: 광학물성 요약

| 디렉토리 | 시스템 |
|----------|--------|
| 001_VSe3chain | VSe3 체인 |
| 002_HfdopedVSe3 | Hf 도핑 VSe3 |
| 003_Hf2Se9_mol | Hf2Se9 분자 |
| 004_Hf2Se9_chain | Hf2Se9 체인 |
| 005_Hydrogen | 수소화 변종 |

#### 2509: 코드/basis set 테스트

| 계산 | 코드 | 내용 |
|------|------|------|
| 2-B3LYP | QE | exx_fraction=0.25, tot_charge=-1 (음이온), ecutwfc=100 Ry |
| 3-Hf2Se9-siesta | SIESTA | basis set 수렴 테스트 (10 meV cutoff) |
| 1-Hf2Se9-LDA | QE | LDA 테스트 (빈 디렉토리) |

---

### B. VSe3-Hf2Se9/ (보조 계산)

#### 001: 단일 체인 (Single Chain)

| 계산 | 시스템 | 코드 | 내용 |
|------|--------|------|------|
| 001_VSe3/001_rlx | VSe3 체인 | SIESTA | 구조 relaxation |
| 001_VSe3/002_band | VSe3 체인 | SIESTA | 밴드 구조 |
| 002_Hf2Se9/001_rlx | Hf2Se9 체인 | SIESTA | 구조 relaxation |
| 002_Hf2Se9/002_band | Hf2Se9 체인 | SIESTA | 밴드 구조 |

#### 002: 단분자 (Single Molecule)

| 계산 | 내용 |
|------|------|
| 001_Hf2Se9/001_rlx | Hf2Se9 분자 relaxation |
| 002_Hf2Se9_qe | QE로 PBE, B3LYP 비교 |
| 003_Hf2Se9_DFT+U | Hubbard U 테스트 (U=1,3,7 eV), Se 4p U 탐색 |

#### 003: 이종접합 (Heterojunction)

체계적 구조 탐색 수행:

| 계산 | 내용 |
|------|------|
| 001_separation_test | VSe3-Hf2Se9 층간 거리 스크리닝 |
| 002_angle_dependence_test | 배향 각도 효과 |
| 002_3uc/001_rlx | 3 unit cell 이종접합 relaxation |
| 002_3uc/002_bands_pdos | 3 unit cell 밴드+PDOS |
| 003_20uc/001_rlx | 20 unit cell 이종접합 relaxation |
| 004_pdos_sep/001_5ang | 5 A 층간 거리에서 PDOS |

#### 004: Hf 도핑 VSe3 (Hf-doped Chain)

| 계산 | 내용 |
|------|------|
| 001_separation_test | 도핑 원자 간 거리 최적화 |
| 002_rlx | 구조 relaxation |
| 003_bands | 밴드 구조 |

#### 005: NbSe3 비교계 (Comparative System)

VSe3와 동일한 계산 프로토콜을 NbSe3에 적용:

| 계산 | 내용 |
|------|------|
| 001_single_chain | NbSe3 체인 relaxation + band |
| 002_heterojunction | NbSe3/Hf2Se9 이종접합 (구조 테스트 + relaxation) |
| 003_hf_doped | Hf 도핑 NbSe3 |

#### 006: 전송 계산 (Transport)

3개 시스템에 대해 동일한 transport 프로토콜 적용:

| 시스템 | 하위 계산 |
|--------|-----------|
| 001_Hf2Se9 | electrode → 0bias → IVcurve |
| 002_Hfdoped | electrode → 0bias → IVcurve |
| 003_VSe3 | electrode → 0bias → IVcurve |

#### Hf2Se9_vasp_HSE06: VASP HSE06 계산

| 항목 | 값 |
|------|-----|
| Functional | HSE06 (AEXX=0.25, HFSCREEN=0.2) |
| ENCUT | 500 eV |
| EDIFF | 1e-8 |
| NELM | 100 |
| NCORE | 2 |
| ISYM | 0 (대칭 없음) |
| 상태 | restart/ 서브디렉토리에서 WAVECAR 기반 재시작 |

#### Hf2Se9_mol_compare: 코드 간 비교

5개 조합으로 동일 구조 계산하여 코드/functional 차이 검증:

| 번호 | 코드 | Functional |
|------|------|-----------|
| 001 | SIESTA | LDA |
| 002 | SIESTA | PBE |
| 003 | QE | LDA |
| 004 | QE | PBE |
| 005 | QE | B3LYP |

#### Hf2Se9_chain/: 체인 추가 연구

다양한 전하 상태에서의 체인 relaxation (tot_charge=-2 등)

---

## Discussion

### 완료된 것

1. **Hf2Se9 단분자/체인 구조 안정성**: MD 300K에서 안정 확인
2. **VSe3-Hf2Se9 이종접합**: 구조 최적화, 밴드/PDOS, Mulliken 전하 분석
3. **Transport**: I-V 곡선 (0-0.3 V), Hf2Se9/Hf-doped/VSe3 3개 시스템
4. **Hf 도핑 VSe3**: 체인 relaxation + 밴드
5. **NbSe3 비교계**: 단일체인, 이종접합, Hf 도핑 동일 프로토콜
6. **광학물성**: B3LYP(VASP) neutral/charged 완료
7. **코드 비교**: SIESTA(LDA/PBE) vs QE(LDA/PBE/B3LYP) 완료

### 미완/실패

1. **Hf 도핑 molecule 구조**: 불안정하여 수렴 실패 → **CNT 내부 MD로 재시도 필요**
2. **HSE06 계산**: 디렉토리 생성만 되고 실제 계산 미수행
3. **PBE/LDA 광학물성 비교**: 미수행
4. **VSe3 TP vs TAP 비교**: 당시 미수행 → 현재 프로젝트 핵심 과제

### 현재 프로젝트에 활용 가능한 데이터

| 이전 데이터 | 활용 방안 |
|-------------|-----------|
| VSe3 체인 relaxation/band (001_single_chain) | TP 구조 기준점, 초기 구조 참고 |
| Hf 도핑 체인 (004_hf_doped) | molecule junction 재계산 시 참고 |
| NbSe3 비교 (005_NbSe3) | Se vs Te 비교 연구 시 프로토콜 참고 |
| Transport 프로토콜 (006_transport) | 향후 transport 계산 시 입력 파일 재활용 |
| DFT+U 테스트 (002_single_molecule/003) | U 파라미터 선정 참고 |
