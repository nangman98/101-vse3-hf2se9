# Rules

## Key files
- `README.md` — project summary for humans. Keep it concise.
- `STATUS.md` — current project status for you. **Keep this up to date** whenever work progresses.
- `CLAUDE.md` — this file. Rules for you.

## Data (`data/`)
- One directory per calculation case: `{nnn}-{case-name}/` (e.g., `001-bulk-relax/`, `002-slab-n4-vac25/`)
- Scripts and input files go in the case directory

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
