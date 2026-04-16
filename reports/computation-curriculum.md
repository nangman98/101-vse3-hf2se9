# VSe3/Hf₂Se₉ 계산 커리큘럼

전자 구조 → interface → transport 전체 파이프라인. 이미 한 것 / 아카이브에 있는 것 / 새로 해야 할 것 정리.

**Updated**: 2026-04-14

---

## Phase 0: 기존 계산 인벤토리

### 현재 프로젝트 (03-calc/)

| 시스템 | Functional | Relax | Band | PDOS | 비고 |
|--------|-----------|-------|------|------|------|
| VSe3 TP | vdW-DF2 | ✅ | ✅ | ✅ | 금속성 확인 |
| VSe3 TP | PBE+D2 | ✅ | ✅ | ✅ | 금속성 확인 |
| VSe3 TAP | vdW-DF2 | ✅ | ✅ | ✅ | 금속성, TP보다 41 meV/atom 불안정 |
| VSe3 TAP | PBE+D2 | ✅ | ✅ | ✅ | 금속성, TP보다 20 meV/atom 불안정 |
| Hf₂Se₉ mol | vdW-DF2 | ✅ | ❌ | ❌ | input 준비됨, 미실행 |
| Hf₂Se₉ chain | vdW-DF2 | ✅ | ❌ | ❌ | input 준비됨, 미실행 (psml 누락으로 실패 이력) |
| VTe3 TP/TAP | — | ✅ | ❌ | ❌ | input 준비됨, 미실행 |

### 아카이브 (archive/, PBE+D2 기반)

| 시스템 | Band | PDOS | Transport | 분석 노트 | 위치 |
|--------|------|------|-----------|-----------|------|
| VSe3 chain | ✅ | ✅ | — | bands.ipynb | `001_single_chain/001_VSe3/002_band/` |
| Hf₂Se₉ chain | ✅ | ✅ (7 MB) | — | bandspdos_SIESTA.ipynb | `101_/002_Hf2Se9_chain/002_bandspdos/` |
| Hf₂Se₉ molecule | ✅ | ✅ (1.8 MB) | — | bandspdos_SIESTA.ipynb | `101_/001_Hf2Se9_singlemol/002_bands/` |
| Hf₂Se₉ DFT+U | — | ✅ | — | analysis_pdos_byatoms.ipynb | `002_single_molecule/003_Hf2Se9_DFT+U/` |
| Hetero 3uc | ✅ | ✅ | — | bands_pdos.ipynb | `003_heterojunction/002_3uc/002_bands_pdos/` |
| Hetero 20uc | ✅ | ✅ (30 MB) | — | bandspdos_SIESTA.ipynb, mulliken | `101_/003_hetero/002_bandspdos/` |
| Hf-doped VSe3 | ✅ | ✅ (30 MB) | — | pdos.ipynb | `101_/PPT_summary_aug25/002_HfdopedVSe3/` |
| Transport 20uc | ✅ | ✅ (56 MB) | TSHS(electrode만) | bandspdos, mulliken | `101_/004_transport/001_bandspdos_20uc/` |
| Electrode (VSe3 3uc) | — | ✅ | ✅ TSHS | — | `006_transport/001_Hf2Se9/001_electrode/` |
| Device 0bias | — | — | stdout만 (TBtrans 미실행) | — | `006_transport/001_Hf2Se9/002_0bias/` |
| NbSe3 chain | ✅ | — | — | — | `005_NbSe3/001_single_chain/` |
| Se 4p U scan | — | ✅ | — | — | `002_single_molecule/003_DFT+U/Se4p_Utest/` |
| QE PBE/B3LYP | ✅ | ✅ | — | analysis.ipynb, pdos_QE.ipynb | `002_single_molecule/002_Hf2Se9_qe/` |
| I-V curve | — | — | 디렉토리만 | — | `101_/004_transport/002_IVcurve/` |

---

## Phase 1: 전자 구조 — 개별 시스템 (기본)

### 1A. VSe3 chain PDOS orbital 분해 (✅ 이미 완료)

- V 3d / Se 4p 분해 → Fermi level 부근 orbital 기원 확인
- 결과: 금속성, V 3d가 주도
- 위치: `03-calc/01-vse3-tp/band-pdos/` (vdW-DF2), `band-pdos-d2/` (PBE+D2)
- 아카이브: `001_single_chain/001_VSe3/002_band/` (PBE+D2)

### 1B. Hf₂Se₉ molecule PDOS (**최우선 미완료**)

- **목적: band gap 확인** — 이것이 metal/insulator junction claim의 전제
- Hf 5d / Se 4p 분해
- input 준비됨: `03-calc/05-hf2se9-mol/band-pdos/`
- **아카이브 참고**: `101_/001_Hf2Se9_singlemol/002_bands/` (PBE+D2, 완료, `bandspdos_SIESTA.ipynb`)
- 새로 돌릴 것: vdW-DF2 functional (현재 프로젝트 기준)

### 1C. Hf₂Se₉ chain band + PDOS (**미완료**)

- Chain vs molecule gap 비교 → quantum confinement 효과
- input 준비됨: `03-calc/06-hf2se9-chain/band-pdos/` (psml 누락으로 이전 실패)
- **아카이브 참고**: `101_/002_Hf2Se9_chain/002_bandspdos/` (PBE+D2, 완료)
- 새로 돌릴 것: vdW-DF2, Hf.psml/Se.psml 복사 필수

### 1D. DFT+U 파라미터 검토 (아카이브 참고)

- Hf 5d: U=1,3,5,7 eV 스캔 완료 (`002_single_molecule/003_DFT+U/case_1/`)
- Se 4p: U=6.0~6.5 eV 스캔 완료 (`003_DFT+U/Se4p_Utest/`)
- 분석 노트: `analysis_pdos_byatoms.ipynb`
- **활용**: Hf₂Se₉ gap이 PBE에서 과소평가되면 DFT+U 보정 적용

### 1E. Hf-doped VSe3 (아카이브, 참고용)

- VSe3 chain에서 V → Hf 치환
- Band + PDOS 완료: `004_hf_doped/003_bands/`
- **활용**: Hf₂Se₉ interface 근처 electronic perturbation 이해

### 1F. NbSe3 chain (아카이브, 비교 대상)

- Band 완료: `005_NbSe3/001_single_chain/002_bands/`
- **활용**: VSe3와 같은 MX₃ 계열 비교

---

## Phase 2: H termination separation scan (**진행 중**)

### 2A. Bond scan (✅ 완료)

- d=2.0~4.5 Å, 6 case, vdW-DF2
- **결과: d=3.5 Å minimum (E_sep = −0.68 eV)**, 실험 일치
- 위치: `03-calc/10-hetero-h-term/bond/`

### 2B. Gap scan (🔄 Perlmutter PD — 51534042)

- H가 pure z방향 (chain 기하 무시)
- 동일 6 case, vdW-DF2, ELPA

### 2C. Tilt scan (🔄 Perlmutter PD — 51534044)

- H가 45° outward (radial 방향)
- 동일 6 case, vdW-DF2, ELPA

### 2D. 결과 비교 → H 방향 확정

- Bond/gap/tilt 세 곡선 비교 plot
- 가장 물리적으로 합리적인 모드 선택 → Phase 3 relaxation

---

## Phase 3: Heterostructure relaxation

### 3A. 20uc급 구조 생성

- 아카이브 기준: ~174 atoms (20uc 양쪽) + H
- `build_hetero_v2.py` n_elec=20 으로 생성
- 확정된 H 방향 (Phase 2 결과) 적용

### 3B. Relaxation (Broyden, 1000 steps)

- CLAUDE.md 디폴트: Broyden, stress 1 2 4 5 6, SCF 1e-8
- 아카이브 참고: `003_heterojunction/003_20uc/001_rlx/`

### 3C. Relaxed 구조 분석

- Hf-Hf 거리 (vs TEM 3.6 Å)
- Interface Se-Se 거리, H 위치 변화
- Total energy 변화
- 구조 figure (matviz-capture)

---

## Phase 4: Heterostructure 전자 구조

### 4A. Hetero band + PDOS

- Relaxed 20uc 구조에서 single-point band + PDOS
- **아카이브 참고**: `101_/003_hetero/002_bandspdos/` (PBE+D2, 완료, 30 MB PDOS)
- PLDOS: interface 근처 local DOS → band alignment diagram
- Mulliken charge analysis (아카이브: `mulliken_analysis.ipynb`)

### 4B. H 있음/없음 비교

- 동일 구조에서 H 유무 PDOS 비교
- Dangling bond state가 gap 안에 나타나는지 확인
- Schottky barrier height 추출 (Hf₂Se₉가 반도체일 경우)

### 4C. Hf₂Se₉ 길이 효과 (아카이브 참고)

- 분자 1개 vs 2개 vs 3개 junction
- 아카이브: `arch/molecule_increase/003_molecule_3/002_bands/`
- Conductance vs molecular length → tunneling/hopping 판별

---

## Phase 5: Transport

### 5A. Electrode 계산

- VSe3 3uc bulk, k=1×1×100, SaveHS T
- **아카이브 참고**: `006_transport/001_Hf2Se9/001_electrode/` (완료, TSHS 존재)
- 새 계산 필요: vdW-DF2 functional로 재계산 (아카이브는 PBE+D2)

### 5B. Device TranSIESTA (0-bias)

- Relaxed hetero 구조 + electrode TSHS
- **아카이브 참고**: `006_transport/001_Hf2Se9/002_0bias/TS.fdf` (설정 템플릿)
- Contour: circle + tail (25+10 points), eta 10 meV

### 5C. TBtrans T(E)

- Zero-bias transmission spectrum
- **아카이브 상태**: 미실행 (006_transport에서 TBtrans 미완료)

### 5D. Eigenchannel 분석

- 어떤 orbital이 전도에 기여하는지
- siesta-eigenchannel 스킬 활용

### 5E. I-V curve (multi-bias)

- 0.1~1.0 V 범위
- **아카이브**: `101_/004_transport/002_IVcurve/` (디렉토리만)

### 5F. H 있음/없음 transport 비교

- 두 구조 모두 TranSIESTA → T(E) 비교
- Interface engineering 효과의 직접 증거

---

## Phase 6: 실험 연결

### 6A. TEM-DFT 구조 비교

- Relaxed Hf-Hf, Se₃ 폭 등 vs TEM 측정값
- Functional별 차이 표 (이미 Phase A에서 일부 완료)

### 6B. TEM image simulation (조건부)

- Multislice from DFT relaxed 구조
- HAADF-STEM simulation → Hf heavy atom contrast
- 방법론 참고: Mayock 2024 (Sb₂Se₃@CNT)

---

## 실행 우선순위

| 순서 | 작업 | 선행 조건 | HPC |
|------|------|-----------|-----|
| **1** | **Hf₂Se₉ mol PDOS (1B)** | 없음 (relaxed 구조 있음) | 누리온/Perlmutter |
| **2** | **Hf₂Se₉ chain PDOS (1C)** | Hf.psml 복사 | 누리온/Perlmutter |
| **3** | Gap/tilt 결과 분석 (2D) | 2B, 2C 완료 대기 | 로컬 |
| **4** | 20uc 구조 생성 (3A) | H 방향 확정 (2D) | 로컬 |
| **5** | 20uc relaxation (3B) | 3A | Perlmutter/누리온 |
| **6** | Hetero PDOS (4A) | 3B | Perlmutter/누리온 |
| **7** | Electrode 계산 (5A) | VSe3 relaxed (✅) | 누리온 |
| **8** | TranSIESTA 0-bias (5B) | 5A + 3B | Perlmutter |
| **9** | TBtrans + eigenchannel (5C, 5D) | 5B | 로컬/누리온 |
| **10** | I-V curve (5E) | 5B | Perlmutter |

**1번(Hf₂Se₉ mol PDOS)은 gap/tilt 대기와 무관하게 바로 시작 가능.**

---

## 아카이브 활용 가이드

| 필요할 때 | 참고 위치 | 내용 |
|-----------|-----------|------|
| PDOS 분석 스크립트 | `101_/*/bandspdos_SIESTA.ipynb` | SIESTA PDOS 파싱 + matplotlib |
| Mulliken 분석 | `101_/003_hetero/mulliken_analysis.ipynb` | 원자별 charge |
| DFT+U 설정 | `002_single_molecule/003_DFT+U/` | Hf 5d, Se 4p U 값 |
| TranSIESTA 설정 | `006_transport/001_Hf2Se9/002_0bias/TS.fdf` | contour, electrode 템플릿 |
| I-V 스크립트 | `101_/004_transport/002_IVcurve/` | multi-bias 셋업 |
| QE band (비교용) | `002_single_molecule/002_Hf2Se9_qe/` | PBE, B3LYP |
| 분자 길이 효과 | `arch/molecule_increase/` | 1~3 분자 junction |
| Separation PDOS | `003_heterojunction/004_pdos_sep/` | 거리별 PDOS |
| Hetero 20uc band | `003_heterojunction/003_20uc/bands_pdos_old/` | PBE+D2 |

---

## 외부 리소스: 튜토리얼, 도구, 논문

### GitHub / 튜토리얼

| 리소스 | URL | 활용 |
|--------|-----|------|
| **ts-tbt-sisl-tutorial** | [zerothi/ts-tbt-sisl-tutorial](https://github.com/zerothi/ts-tbt-sisl-tutorial) | CECAM 공식 TranSIESTA/TBtrans 워크숍 자료. TB_01~09 (NEGF 학습), TS_01~05 (DFT-NEGF 실전). **TS_04/05 buffer atoms 예제가 heterostructure 비등가 전극에 직접 해당** |
| **sisl** | [zerothi/sisl](https://github.com/zerothi/sisl) | Nick Papior 작성 Python 후처리. `*.TBT.nc`에서 transmission, PDOS, eigenchannel, bond-current 추출. **우리 TBtrans 후처리 전부 이걸로** |
| sisl docs | [sisl.readthedocs.io](https://sisl.readthedocs.io/) | API 문서 |
| SIESTA docs | [docs.siesta-project.org](https://docs.siesta-project.org/) | 공식 문서 |
| siesta_python | [AleksBL/siesta_python](https://github.com/AleksBL/siesta_python) | Python에서 SIESTA/TranSIESTA 구동 wrapper |

### Transport 방법론 핵심 논문

| 논문 | 요약 | 활용 |
|------|------|------|
| [Brandbyge et al., PRB 65, 165401 (2002)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.65.165401) | TranSIESTA 원본: DFT+NEGF 조합 기초 | 필수 인용 |
| [Papior et al., CPC 212, 8 (2017)](https://arxiv.org/abs/1607.04464) | 차세대 TranSIESTA: N-전극, contour 최적화, bond-current, 게이팅 | **buffer atoms, 비등가 전극 처리 방법론** |
| [Wittemeier et al., arXiv:2501.16162 (2025)](https://arxiv.org/abs/2501.16162) | SOC 포함 spinor transport | 향후 SOC 효과 필요 시 |
| [Frederiksen et al., PRB 75, 205413 (2007)](https://www.semanticscholar.org/paper/Inelastic-transport-theory-from-first-principles:-Frederiksen-Paulsson/4c6838dd01a33b4d0eb1f9fbad42634101f7a502) | 비탄성 전자-포논 산란 transport | 향후 inelastic 효과 |

### 1D Chain Transport 논문

| 논문 | 요약 | 활용 |
|------|------|------|
| [Rodrigues et al., PCCP (2017)](https://pubs.rsc.org/en/content/articlelanding/2017/CP/C7CP03080K) | Polyyne bridge + SWCNT electrode DFT-NEGF, strain 효과 | **CNT electrode + 1D bridge: 우리와 유사한 geometry** |
| [Sen & Chakrabarti, Sci. Rep. 10, 7246 (2020)](https://www.nature.com/articles/s41598-020-63363-3) | CNT electrode cut 방향 → polyene junction transport 변화 | electrode-molecule coupling 분석 참고 |
| [Kang et al., Physica E (2024)](https://www.sciencedirect.com/science/article/abs/pii/S1386947724008306) | Carbon chain@SWCNT = 1D vdW heterostructure, excitonic solar cell | 1D vdW hetero transport 개념 |

### Chalcogenide 1D Chain 논문

| 논문 | 요약 | 활용 |
|------|------|------|
| [Pham et al., Research 2023, 0066](https://spj.science.org/doi/10.34133/research.0066) | MX₃ quasi-1D 물질 종합 리뷰 (CDW, transport, 소자) | **VSe3 계열 전체 맥락 파악** |
| [Cho et al., RSC Adv. 8, 33295 (2018)](https://pubs.rsc.org/en/content/articlehtml/2018/ra/c8ra06398b) | V₂Se₉ 1D chain 합성, 구조 특성화 | V-Se 계열 실험 참고 |
| [Kim et al., ACS Omega 4, 18392 (2019)](https://pubs.acs.org/doi/10.1021/acsomega.9b02655) | V₂Se₉ indirect→direct band gap (bulk vs chain), DFT-D3/HSE06 | **band gap 비교 방법론, V-Se 전자 구조** |
| [Zhu et al., ACS Omega 5, 10601 (2020)](https://pubs.acs.org/doi/10.1021/acsomega.0c00388) | Nb₂Se₉ 1D chain → 2D sheet, band structure DFT | **M₂X₉ 구조 비교** (Nb vs Hf) |
| [Geremew et al., Nanoscale 8, 14734 (2016)](https://pubs.rsc.org/en/content/articlelanding/2016/nr/c6nr03469a) | TaSe₃ nanowire >10 MA/cm² breakdown, interconnect 응용 | 1D chalcogenide transport 실험 |

### Band Alignment / Interface 분석

| 논문 | 요약 | 활용 |
|------|------|------|
| [Afzalian et al., IEEE TED 68, 5372 (2021)](https://arxiv.org/abs/2106.07248) | HfS₂/WSe₂ vdW heterojunction TFET: PLDOS + Hartree potential → barrier 추출 | **Hf chalcogenide interface! PLDOS 방법론 직접 참고** |
| [Hinuma et al., Materials 14, 3350 (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8235794/) | DFT band offset 두 방법 비교 (individual vs alternating slab) | band alignment 계산 방법론 |
| [Shin et al., ResearchGate](https://www.researchgate.net/publication/322705290) | MX₃ (M=Zr,Hf; X=S,Se) band alignment for solar applications | **HfSe₃ band alignment — 우리 Hf₂Se₉와 직접 관련** |

### Electrode/Device 설계 Best Practice

| 항목 | 내용 | 출처 |
|------|------|------|
| Buffer atoms | scattering region 양 끝에 전극 원자 추가 → Hartree potential bulk 수렴 | [Launchpad Q&A #683010](https://answers.launchpad.net/siesta/+question/683010) |
| K-point | 전극: transport 방향 최소 20, 확신 없으면 100. Device: transverse 수렴 테스트 | [Launchpad Q&A #686603](https://answers.launchpad.net/siesta/+question/686603) |
| 전극 반복 수 | scattering region 내 전극 extension 최소 1 repeat, 2개 이상 권장 | ts-tbt-sisl-tutorial TS_04 |
| PLDOS 추출 | sisl `*.TBT.nc` → atom-resolved spectral DOS → energy vs position band diagram | [Simune Forum](https://forum.simuneatomistics.com/t/local-projected-density-of-state-using-siesta-transiesta/1755) |
| Charge transfer | Delta_rho(z) = rho(hetero) - rho(A) - rho(B), SIESTA `.RHO` grid file | Dandrea-Duke-Zunger method |

### H Passivation & Transport

| 논문 | 요약 | 활용 |
|------|------|------|
| [Li et al., Sci. Rep. 6, 20055 (2016)](https://www.nature.com/articles/srep20055) | Pseudo-H (fractional charge) passivation 방법론 | dangling bond 제거 일반 방법 |
| GNR 연구 (다수) | H passivation 유무 → transport 수 order 차이. dangling bond의 in-gap state가 spurious T(E) peak 유발 | **우리 H termination 결과 해석에 직접 적용** |
