# Functional 간 구조 안정성 비교 방법론

서로 다른 exchange-correlation functional(PBE, vdW-DF2, PBE+D2, PBE+D3 등)로 계산한 결과에서 "어떤 functional이 더 좋은가"를 판단하는 방법을 정리한다.

## 핵심 원칙: Total energy는 functional 간 비교 불가

각 functional은 exchange-correlation energy($E_{xc}$)를 다르게 근사하므로 **절대 total energy의 크기를 functional 간에 비교하는 것은 의미가 없다**.

예시:
- A1(PBE): $E_{tot}$ = −12345.678 eV
- A3(vdW-DF2): $E_{tot}$ = −12300.123 eV
- → "PBE가 45 eV 더 낮으니까 더 안정" ❌ **틀림**

이유:
1. 각 functional은 고유한 systematic bias를 가진다 (GGA는 exchange를 과대, correlation을 과소평가하는 경향)
2. vdW-DF2는 revPBE exchange를 사용하고, D2는 PBE exchange를 사용 → 에너지 reference 자체가 다름
3. vdW 보정항($E_{disp}$)의 크기와 부호가 method마다 다름

## 비교 가능한 것들

### 1. 구조 파라미터 vs 실험 (가장 중요)

DFT relaxed 구조를 실험(TEM, XRD, STEM 등)과 직접 비교한다. **실험값에 가장 가까운 구조를 주는 functional이 이 물질에 가장 적합하다**.

Hf₂Se₉에 적용:

| 파라미터 | TEM 실험값 | 비교 방법 |
|----------|-----------|----------|
| Hf-Hf 거리 | 3.6 Å | 가장 핵심. 3.5~3.8 Å 범위가 성공 |
| 분자 전체 길이 | ~7.2 Å | Se₃ 삼각형 끝~끝 |
| Se₃ 삼각형 폭 | 3.6~4.2 Å | TEM 이미지에서 추정 |
| vdW gap (chain) | ~3.5 Å | chain 계산에서만 비교 가능 |
| confacial bioctahedron | 유지 | 구조 붕괴 여부 |

**현재 결과**:

| Functional | Hf-Hf (Å) | Δ(실험) | 전체 길이 | 판정 |
|-----------|-----------|---------|----------|------|
| A1: PBE | 3.857 | +7% | 6.70 Å | 구조 유지, 약간 팽창 |
| A3: vdW-DF2 | 3.967 | +10% | 6.98 Å | 구조 유지, 더 팽창 |
| A4: PBE+D3 | 3.857 | +7% | 6.70 Å | = A1 (mol에서 D3 효과 없음) |
| A2: PBE+D2 | — | — | — | 아직 미완 |

→ 현재까지는 **PBE 계열(A1, A4)이 vdW-DF2(A3)보다 실험에 더 가까움**.

### 2. 같은 Functional 내에서 상대 에너지 비교

**같은 functional 내에서는** total energy 비교가 유효하다:

- TP vs TAP: 같은 functional(vdW-DF2)로 계산 → ΔE = 41 meV/atom, TP가 안정
- Molecule vs chain: 같은 functional로 binding energy 비교 가능
- Hetero separation test: 같은 functional에서 거리별 에너지 → 최적 vdW gap

주의: **다른 functional 간 ΔE를 비교하면 안 된다**.
- vdW-DF2에서 TP-TAP = 41 meV vs PBE+D2에서 TP-TAP = ? meV → 각각 독립적으로 해석

### 3. Binding Energy / Cohesive Energy

고립된 구성 요소 대비 결합 에너지를 비교하면 functional 간 간접 비교가 가능하다:

$$E_{bind} = E_{chain} - n \cdot E_{molecule}$$

또는 molecule 내 결합:

$$E_{cohesive} = E_{molecule} - \sum E_{atoms}$$

같은 functional 안에서 계산한 binding energy를 실험값(승화열 등)과 비교하면 vdW 기술 능력을 평가할 수 있다.

### 4. 수렴성 및 구조 안정성

| 기준 | 좋음 | 나쁨 |
|------|------|------|
| Force 수렴 | < 0.01 eV/Å, < 50 steps | 미수렴 / 1000 steps |
| 구조 유지 | confacial bioctahedron 유지 | Se₃ 변형, Hf 이탈 |
| Cell 안정 | c축 변화 < 5% | 16~53% 팽창 (이전 실패) |

특정 functional에서 구조가 아예 수렴하지 않거나 붕괴하면, 그 functional은 이 물질에 부적합하다고 판단할 수 있다.

## Hf₂Se₉ Stability Test 판단 흐름

```
Step 1: 수렴하는가?
  ├─ No → 이 functional은 부적합
  └─ Yes ↓

Step 2: 구조가 유지되는가? (confacial bioctahedron)
  ├─ No → 부적합
  └─ Yes ↓

Step 3: 실험과 얼마나 가까운가?
  ├─ Hf-Hf: 3.6 Å 기준으로 편차(%) 순위 매김
  ├─ 전체 길이: 7.2 Å 기준
  └─ vdW gap (chain): ~3.5 Å 기준 ↓

Step 4: 실험 일치도 + 수렴 안정성이 가장 좋은 functional 선택
  └─ 이 functional로 VSe3도 재계산 → hetero 통일
```

## 주의사항

### Molecule vs Chain 결과가 다를 수 있다

Molecule에서 좋은 결과를 주는 functional이 chain에서도 좋다는 보장이 없다:
- D3(BJ)는 isolated molecule에서는 PBE와 동일 (분자 간 vdW가 없으므로)
- Chain에서는 분자 간 vdW가 작용하므로 D3 효과가 나타남
- → Molecule 스크리닝 후 **chain에서 반드시 재검증** 필요

### SIESTA vs VASP 결과 차이

같은 functional이라도 코드(basis set)에 따라 다를 수 있다:
- SIESTA: NAO basis (EnergyShift 의존)
- VASP: PAW + plane-wave (ENCUT 의존)
- A4(SIESTA PBE+D3) vs A5(VASP PBE+D3) 비교로 코드 의존성 분리

### 문헌 벤치마크 참고

- vdW-DF2는 일반적으로 격자상수를 **과대평가**하는 경향 (revPBE exchange의 repulsive 성격)
- PBE+D2는 layered 물질에서 격자상수 정확도가 높은 편 (0.3~0.5% 편차)
- PBE+D3(BJ)는 배위수 의존 C₆를 사용하여 다양한 화학 환경에 더 유연

## 참고 문헌

- Grimme et al., J. Comput. Chem. 27, 1787 (2006) — DFT-D2
- Lee et al., Phys. Rev. B 82, 081101(R) (2010) — vdW-DF2
- Grimme et al., J. Chem. Phys. 132, 154104 (2010) — DFT-D3
- Goerigk et al., Phys. Chem. Chem. Phys. 19, 32184 (2017) — GMTKN55 benchmark
