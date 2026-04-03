# vdW 설정 검증 및 방법별 비교

## 1. vdW 방법별 설정 방식

### 핵심: 별도 파일이 필요한가?

| 방법 | SIESTA | VASP |
|------|--------|------|
| **Grimme D2** | `grimme.fdf` 필요 (**fdf2grimme로 생성**) | `IVDW=10` (자동) |
| **Grimme D3(BJ)** | SIESTA 미지원 (5.2.x 기준) | `IVDW=12` (자동) |
| **vdW-DF2 (LMKLL)** | input.fdf 설정만 (`XC.functional VDW` + `XC.authors LMKLL`) | `LUSE_VDW=.TRUE.` + `GGA=MK` + `AGGAC=0.0` |

**정리:**
- **D2만 별도 파일 필요** (SIESTA). C6/R0 파라미터가 원소쌍별로 다르고, species 번호가 struct.fdf에 종속되므로 `fdf2grimme struct.fdf > grimme.fdf`로 자동 생성해야 함.
- **vdW-DF2**: 비국소(non-local) 범함수로 전자밀도에서 직접 vdW 상호작용을 계산. 외부 파라미터 파일 없음. input.fdf에 XC 설정만 하면 됨.
- **D3(BJ)**: VASP에서만 지원 (`IVDW=12`). VASP 내장 DB에서 원소별 파라미터를 자동 적용. SIESTA에서는 별도 구현 필요 (표준 지원 아님).

### fdf2grimme 사용법 (SIESTA D2 전용)

```bash
# 누리온 SKL 노드용 (로그인 노드에서 실행 가능)
/apps/applications/SIESTA/5.2.1/intel/19.1.2/impi/19.1.2/x86-skylake/bin/fdf2grimme struct.fdf > grimme.fdf

# KNL 노드용 (컴퓨트 노드에서만)
/apps/applications/SIESTA/5.2.1/intel/19.1.2/impi/19.1.2/mic-knl/bin/fdf2grimme struct.fdf > grimme.fdf
```

- struct.fdf의 `ChemicalSpeciesLabel`을 읽어서 원소쌍별 Grimme D2 파라미터 (C6, R0) 자동 생성
- species 번호가 구조마다 다르므로 **구조마다 새로 생성해야 함**
- S6=0.75, D=20 (PBE 기본값) 자동 설정

## 2. 기존 계산 설정 검증

### SIESTA 계산

| 계산 | Functional | vdW 설정 | grimme.fdf 출처 | 검증 |
|------|-----------|---------|----------------|------|
| 01-vse3-tp/relax | vdW-DF2 | `XC.functional VDW` + `XC.authors LMKLL` | 불필요 | 정상 |
| 01-vse3-tp/relax-d2 | PBE+D2 | `%include grimme.fdf` | fdf2grimme 재실행 결과와 내용 동일 (생성 방법은 미확인) | 정상 |
| 05-hf2se9-mol/relax | vdW-DF2 | `XC.functional VDW` + `XC.authors LMKLL` | 불필요 | 정상 |
| 06-hf2se9-chain-d2 | PBE+D2 | `%include grimme.fdf` | fdf2grimme 재실행 결과와 내용 동일 (생성 방법은 미확인) | 정상 |
| 08-hetero-v2 | vdW-DF2 | `XC.functional VDW` + `XC.authors LMKLL` | 불필요 | 정상 |
| 09-hetero-d2 | PBE+D2 | `%include grimme.fdf` | **fdf2grimme 생성** (누리온에서 실행) | 정상 |

### VASP 계산

| 계산 | Functional | vdW 설정 | 파라미터 출처 | 검증 |
|------|-----------|---------|-------------|------|
| A5 PBE+D3(BJ) | PBE | `IVDW=12` | VASP 내장 DB (자동) | 정상 |
| A6 HSE06+D3(BJ) | HSE06 | `IVDW=12` | VASP 자동 감지: S6=1.0, S8=0.109, A1=0.383, A2=5.685 (OUTCAR 확인) | 정상 |

### VASP에서 D2를 안 한 이유

A5/A6은 D3(BJ)만 사용. VASP에서 D2는 `IVDW=10`으로 가능하지만, D3(BJ)가 더 정확한 최신 방법이라 D3만 테스트함. SIESTA PBE+D2와 직접 비교하려면 VASP D2(`IVDW=10`)도 돌려야 함.

## 3. VASP INCAR 설정 예시

### PBE+D2 ([VASP Wiki — DFT-D2](https://www.vasp.at/wiki/index.php/DFT-D2))

```
IVDW   = 10        # DFT-D2 활성화 (1도 동일)
# PBE 기본값 (자동 적용):
# VDW_S6 = 0.75     global scaling factor
# VDW_SR = 1.00     damping scaling factor
# VDW_D  = 20.0     damping parameter
# VDW_RADIUS = 50.0 cutoff (Ang)
```

VASP 내장 DB에서 원소별 C6/R0 자동 적용. 별도 파일 불필요.
다른 functional은 S6이 다름 (BLYP: 1.2, B3LYP: 1.05).

### PBE+D3(BJ) ([VASP Wiki — IVDW](https://www.vasp.at/wiki/index.php/IVDW))

```
IVDW = 12        # DFT-D3 with BJ damping
```

A6 OUTCAR에서 확인한 실제 적용 파라미터 (HSE06):
```
VDW_S6       =    1.0000
VDW_S8       =    0.1090
VDW_A1       =    0.3830
VDW_A2       =    5.6850
VDW_RADIUS   =   50.2022 A
VDW_CNRADIUS =   21.1671 A
```

### vdW-DF2 ([VASP Wiki — Nonlocal vdW-DF functionals](https://www.vasp.at/wiki/index.php/Nonlocal_vdW-DF_functionals))

```
GGA      = ML        # rPW86 exchange (vdW-DF2용)
LUSE_VDW = .TRUE.    # 비국소 vdW 활성화
AGGAC    = 0.0       # GGA correlation 비활성 (vdW 커널로 대체)
ZAB_VDW  = -1.8867   # vdW-DF2 파라미터 (vdW-DF1은 -0.8491)
LASPH    = .TRUE.    # 비구형 기여 (권장)
```

`vdw_kernel.bindat` 파일 필요 (VASP 설치 디렉토리에 포함).

## 4. 방법별 차이 요약 (SIESTA D3는 5.0+ 필요, [release notes](https://siesta-project.org/siesta/Documentation/Release_Notes/SIESTA-5.0.0_release_notes.html))

| | D2 (Grimme 2006) | D3(BJ) (Grimme 2011) | vdW-DF2 (Lee 2010) |
|---|---|---|---|
| **원리** | 경험적 C6/R0 파라미터 | coordination-number 의존 C6 | 비국소 상관 범함수 |
| **파라미터** | 원소별 고정 (C6, R0) | 원소+환경 의존 | 없음 (전자밀도에서 직접) |
| **SIESTA** | `%include grimme.fdf` (fdf2grimme) | 미지원 | `XC.functional VDW` |
| **VASP** | `IVDW=10` (자동) | `IVDW=12` (자동) | `LUSE_VDW=.TRUE.` |
| **외부 파일** | SIESTA만 grimme.fdf 필요 | 불필요 | 불필요 |
| **정확도** | 낮음 (고정 파라미터) | 높음 (환경 의존) | 높음 (self-consistent) |

## 5. 검증 로그

### grimme.fdf 검증: fdf2grimme 재실행 vs 기존 파일

```bash
# 01-vse3-tp/relax-d2 (Species: 1=V, 2=Se)
$ cd /scratch/x3251a05/VSe3-Hf2Se9/03-calc/01-vse3-tp/relax-d2
$ fdf2grimme struct.fdf
MM.Grimme.S6     0.75
%block MM.Potentials
  1   1 Grimme    111.94      3.124 # V
  1   2 Grimme    121.10      3.333 # V / Se
  2   2 Grimme    131.01      3.542 # Se
%endblock MM.Potentials
# → 기존 grimme.fdf와 byte-for-byte 동일

# 06-hf2se9-chain-d2 (Species: 1=Hf, 2=Se)
$ cd /scratch/x3251a05/VSe3-Hf2Se9/03-calc/06-hf2se9-chain-d2/relax
$ fdf2grimme struct.fdf
%block MM.Potentials
  1   1 Grimme   1089.41      3.574 # Hf
  1   2 Grimme    377.78      3.558 # Hf / Se
  2   2 Grimme    131.01      3.542 # Se
%endblock MM.Potentials
# → 기존 grimme.fdf와 byte-for-byte 동일

# 09-hetero-d2 (Species: 1=Hf, 2=Se, 3=V)
$ cd /scratch/x3251a05/VSe3-Hf2Se9/03-calc/09-hetero-d2/d_3.0
$ fdf2grimme struct.fdf > grimme.fdf
%block MM.Potentials
  1   1 Grimme   1089.41      3.574 # Hf
  1   2 Grimme    377.78      3.558 # Hf / Se
  1   3 Grimme    349.21      3.349 # Hf / V
  2   2 Grimme    131.01      3.542 # Se
  2   3 Grimme    121.10      3.333 # Se / V
  3   3 Grimme    111.94      3.124 # V
%endblock MM.Potentials
# → 누리온에서 fdf2grimme 실행하여 신규 생성
```

### A6 HSE06+D3(BJ) OUTCAR 발췌

경로: `05-hf2se9-mol/stability-test/A6-vasp-hse-d3/rlx1/OUTCAR`

```
IVDW         = 12
VDW_S6       =    1.0000
VDW_S8       =    0.1090
VDW_A1       =    0.3830
VDW_A2       =    5.6850
VDW_RADIUS   =   50.2022 A
VDW_CNRADIUS =   21.1671 A
```

### SIESTA input.fdf 발췌

```
# 01-vse3-tp/relax (vdW-DF2)
XC.functional            VDW
XC.authors               LMKLL

# 01-vse3-tp/relax-d2 (PBE+D2)
XC.functional            GGA
XC.authors               PBE
%include grimme.fdf

# A5 VASP INCAR (PBE+D3BJ)
IVDW    = 12

# A6 VASP INCAR (HSE06+D3BJ)
IVDW    = 12
LHFCALC = .TRUE.
HFSCREEN = 0.2
```

## 6. 출처

- vdW-DF2 설정: [SIESTA 4.1.5 Manual, Section 6.6 (p.49)](https://siesta-project.org/SIESTA_MATERIAL/Docs/Manuals/siesta-4.1.5.pdf#page=49)
- D2 / fdf2grimme: [SIESTA 4.1.5 Manual, Section 6.23 (p.109)](https://siesta-project.org/SIESTA_MATERIAL/Docs/Manuals/siesta-4.1.5.pdf#page=109)
- D3 지원: [SIESTA 5.0.0 Release Notes](https://siesta-project.org/siesta/Documentation/Release_Notes/SIESTA-5.0.0_release_notes.html)
- VASP IVDW: [VASP Wiki — IVDW](https://www.vasp.at/wiki/index.php/IVDW)
- VASP vdW-DF: [VASP Wiki — Nonlocal vdW-DF functionals](https://www.vasp.at/wiki/index.php/Nonlocal_vdW-DF_functionals)
- A6 D3(BJ) 파라미터: `A6-vasp-hse-d3/rlx1/OUTCAR`에서 직접 확인
- grimme.fdf 검증: 누리온에서 `fdf2grimme` 재실행하여 기존 파일과 동일 확인
