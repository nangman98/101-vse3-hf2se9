# Rules

## Key files
- `README.md` — project summary for humans. Keep it concise.
- `STATUS.md` — current project status for you. **Keep this up to date** whenever work progresses.
- `CLAUDE.md` — this file. Rules for you.

## Calculation workspace (`VSe3-Hf2Se9/`)
- HPC 계산 디렉토리. rsync/upload로 Stampede3에 동기화.
- `01-data/` — 참조 구조 데이터
- `02-code/` — 구조 생성 스크립트
- `03-calc/` — 계산 케이스 디렉토리
  - One directory per case: `{nn}-{case-name}/` (e.g., `01-vse3-tp-relax/`)
  - 각 케이스: struct.fdf, input.fdf, (grimme.fdf는 계산 시 생성)
- 계산 결과는 연구 디렉토리(`reports/`)에 정리

## Archive (`archive/`)
- 이전 계산 참고 데이터 (gitignored)
- `101_VSe3-Hf2Se9/`, `VSe3-Hf2Se9/` (old), tar files, raw meeting notes

## Reports (`reports/`)
- One directory per topic: `reports/{report-name}/`
- Main document: `reports/{report-name}/{report-name}.md`
- Plot scripts, figures, supporting files go in the same directory
- Image paths in the report are relative: `![caption](figure.png)`
- Report sections: Key Finding, Method, Results, Discussion
- Cross-cutting docs (e.g., computation plan) can be top-level files in `reports/`

## Meetings (`meetings/`)
- One file per meeting: `meetings/{YYYY-MM-DD}.md`
- Contains both:
  - **Progress report** (written before meeting)
  - **After-meeting notes** (discussion, decisions, action items, related issues)

## Conventions
- Filenames: lowercase, hyphenated
- Dates: YYYY-MM-DD
