# vdW 보정 방법 비교: Grimme D2 vs vdW-DF2

Hf₂Se₉ relaxation에서 vdW 보정 방법에 따라 결과가 크게 달라지는 원인을 정리한다.

## Grimme D2 (경험적 사후 보정)

$$E_{DFT-D2} = E_{DFT}^{PBE} + E_{disp}$$

$$E_{disp} = -s_6 \sum_{i<j} \frac{C_6^{ij}}{r_{ij}^6} f_{damp}(r_{ij})$$

- **PBE** exchange-correlation 위에 분산력 항을 사후 보정으로 더한다.
- $C_6$ 계수: **원소별 고정값** — 화학 환경(결합 상태, 배위수)에 무관.
- $f_{damp}$: 근거리에서 이중 카운팅을 방지하는 damping function.
- $s_6$: functional에 따른 전역 스케일링 팩터 (PBE: $s_6 = 0.75$).
- SCF에 영향 없음: 전자 밀도는 PBE로 수렴한 후 에너지/force에만 보정 추가.

**한계**: Hf처럼 다양한 산화 상태와 배위 환경을 갖는 전이금속에서 고정 $C_6$가 부정확할 수 있다.

## vdW-DF2 (비경험적, self-consistent)

$$E_{vdW-DF2} = E_x^{revPBE} + E_c^{LDA} + E_c^{nl}$$

$$E_c^{nl} = \frac{1}{2}\int\int n(\mathbf{r})\,\Phi(\mathbf{r}, \mathbf{r}')\,n(\mathbf{r}') \,d\mathbf{r}\,d\mathbf{r}'$$

- Exchange: **revPBE** (PBE가 아님 — 더 repulsive).
- 비국소 상관 $E_c^{nl}$: **전자 밀도 $n(\mathbf{r})$로부터 직접 계산**.
- Kernel $\Phi(\mathbf{r}, \mathbf{r}')$: 두 점 사이의 거리와 밀도 기울기에 의존 → 화학 환경에 따라 자동 조절.
- SCF 루프 안에서 self-consistent하게 작동 → force에도 정확히 반영.
- 경험적 파라미터 없음.

## 핵심 차이

| | Grimme D2 | vdW-DF2 |
|---|---|---|
| Exchange functional | PBE | **revPBE** |
| vdW 보정 | 사후 보정 ($C_6/r^6$, 고정 계수) | self-consistent (밀도 기반 kernel) |
| 환경 의존성 | 없음 (원소별 고정) | 있음 (밀도 기울기에 의존) |
| Force | 해석적 gradient 근사 | self-consistent force |
| 계산 비용 | 저렴 (PBE + 보정항) | 비쌈 (비국소 적분) |

## Hf₂Se₉에 대한 영향

### Exchange 차이 (PBE vs revPBE)

vdW-DF2의 revPBE exchange는 PBE보다 **repulsive**하다:
- PBE: exchange enhancement factor가 큰 밀도 기울기에서 saturate
- revPBE: saturate하지 않고 계속 증가 → 원자 간 반발이 더 강함

이 차이가 vdW gap에서 결정적:
- D2(PBE): exchange repulsion이 약함 → vdW attraction과 균형 → 안정
- vdW-DF2(revPBE): exchange repulsion이 강함 → vdW gap이 팽창하는 방향으로 밀림

### Molecule vs Chain 차이

| | 05-mol (molecule) | 06-chain (chain) |
|---|---|---|
| 초기 Hf-Hf | 3.62 Å | 3.62 Å |
| 현재 Hf-Hf | 3.97 Å (+10%) | 4.56 Å (+26%) |
| Force | 0.027 eV/Å (거의 수렴) | 0.39 eV/Å (불안정) |

Molecule은 고립계라 vdW gap 하나만 기술하면 되지만, chain은 주기적 반복으로 vdW 상호작용이 누적된다. revPBE의 추가 repulsion이 chain에서는 **누적 효과**로 팽창을 가속시킨다.

### Phase A에서 검증할 내용

| 비교 | 질문 |
|---|---|
| A1 (PBE, no vdW) vs A3 (vdW-DF2) | vdW 보정 자체가 필요한가? |
| A2 (PBE+D2) vs A3 (vdW-DF2) | exchange 차이(PBE vs revPBE)가 원인인가? |
| A2 (PBE+D2) vs A4 (PBE+D3) | D2 vs D3 — 환경 의존 $C_6$가 차이를 만드는가? |
| A4 (SIESTA PBE+D3) vs A5 (VASP PBE+D3) | 같은 functional인데 basis(NAO vs PAW)가 문제인가? |

## VSe3 TP/TAP — functional 통일 필요

현재 계산별 vdW method가 통일되지 않은 상태:

| 계산 | Method | Exchange |
|---|---|---|
| 01-vse3-tp (relax, band) | vdW-DF2 (LMKLL) | revPBE |
| 02-vse3-tap (relax, band) | vdW-DF2 (LMKLL) | revPBE |
| 07-hetero | vdW-DF2 (LMKLL) | revPBE |
| Hf2Se9 stability A2 | PBE+D2 | PBE |

### 왜 문제인가

이종접합(hetero) 구조에서 VSe3 부분과 Hf2Se9 부분이 다른 functional로 relaxed된 격자상수를 쓰면:
- Exchange 차이 (revPBE vs PBE) → 격자상수 mismatch
- 같은 functional이어야 힘/에너지가 self-consistent

### 계획

1. Hf2Se9 stability test에서 최적 vdW functional 확정 (예: PBE+D2 또는 PBE+D3)
2. VSe3 TP/TAP relaxation을 같은 설정으로 재계산 (`relax-d2/` 디렉토리 준비 완료)
3. 재계산된 구조로 hetero 재조립

### 준비된 입력 파일

- `03-calc/01-vse3-tp/relax-d2/` — PBE+D2 설정
- `03-calc/02-vse3-tap/relax-d2/` — PBE+D2 설정

## 참고

- vdW-DF2 원문: Lee et al., Phys. Rev. B 82, 081101(R) (2010)
- Grimme D2: Grimme, J. Comput. Chem. 27, 1787 (2006)
- 이전 VASP MD (DFT-D3)에서는 Hf-Hf = 3.82 Å 유지 → D3에서는 양호했음
