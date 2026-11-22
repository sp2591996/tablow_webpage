# Contributing

## Workflow

1. Get the latest code: `git checkout main` then `git pull`.
2. Create a branch: `git checkout -b feature/short-description` (for example `feature/add-monocef`).
3. Edit only `_build/` or `assets/`. Never hand-edit the generated HTML.
4. Rebuild: `python _build/build.py`, then preview with `python -m http.server 8765`.
5. Check the page on desktop and on a phone-sized window (375 px wide).
6. Commit both your source change and the regenerated pages:
   `git add -A` then `git commit -m "Add Monocef 200 pair"`.
7. Push: `git push -u origin feature/short-description`.
8. Open a pull request on GitHub into `main` and fill in the checklist.
9. After approval, merge. Delete the branch.

`main` is protected: changes go in only through an approved pull request.

## Adding a medicine pair

Add a pair in `_build/data_v4.py` (copy an existing `_pair(...)` entry), with brand and substitute names, MRPs and their source and date, pack, units and usage. Add a new salt to `SALTS` and `MORE` if needed, and new companies to `COMPANIES` and `COMPANY_MORE`. Rebuild and check the new branded, generic, salt and company pages.

## Content rules

- No "#1", "best-selling" or "most prescribed" claims for any brand.
- No lists of a company's other brands.
- No "prescription needed", "upload first" or "check with your doctor before switching" near a buy button. Insulin and levothyroxine keep their safety notes.
- Savings are per year and must match across the hero, price table and calculator.
- Prices need a source and date in the data file.
