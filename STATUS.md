# Project Status

- **Phase**: planning
- **Material**: VSe3, Hf-doped VSe3 (molecule junction)

## Completed (이전 프로젝트에서 물려받은 계산)

- [x] Hf2Se9 단분자 MD (300K, 500-1000 step) — 구조 안정성 확인
- [x] Hf2Se9 1D 체인 MD + 밴드/PDOS
- [x] VSe3-Hf2Se9 이종접합 MD + 밴드/PDOS + Mulliken 분석
- [x] Transport I-V curve (Hf2Se9, Hf-doped, VSe3) — TranSIESTA
- [x] Hf 도핑 VSe3 체인 relaxation + 밴드
- [x] NbSe3 비교계 (단일체인, 이종접합, Hf 도핑)
- [x] B3LYP 광학물성 (neutral, charged)
- [x] 코드 비교: SIESTA(LDA/PBE) vs QE(LDA/PBE/B3LYP)
- [x] 이전 계산 리뷰 및 정리 → `reports/previous-calculations/`

## Pending

- [ ] VSe3 TP vs TAP 구조 안정성 DFT 계산
- [ ] Se vs Te TP/TAP 비교
- [ ] Hf 도핑 molecule 구조 → CNT 포함 MD (이전 실패 재도전)
- [ ] CNT 영향 (밴드, charge transfer)

## Open Questions

- TP vs TAP 에너지 차이 크기
- Hf 도핑 molecule이 CNT 내부에서 안정화되는지 (이전 계산에서 불안정)
- Se vs Te에 따른 TP/TAP 선호도 차이 원인

## Data Layout

| Directory | Contents |
|-----------|----------|
| `reports/previous-calculations/` | 이전 계산 상세 리뷰 |
