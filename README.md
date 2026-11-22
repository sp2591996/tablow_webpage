# Tablow product pages (prototype)

Static HTML prototypes for Tablow's medicine pages: branded pages that steer to a cheaper same-salt **Smart Switch**, generic (substitute) buy pages, salt pages, company pages, a hub (`index.html`) and an internal guidelines page (`guidelines.html`).

Prices are placeholders and medical content is a draft awaiting pharmacist and legal review.

## Folder structure

| Path | What it is | Edit it? |
|---|---|---|
| `_build/build.py` | Page templates and the generator | Yes |
| `_build/data.py`, `data_v4.py`, `data_more.py` | Medicines, prices, salts, companies, FAQs | Yes |
| `_build/guidelines_body.html` | Text of the internal guidelines page | Yes |
| `assets/tablow.css`, `assets/app.js` | Styles and page behaviour | Yes |
| `index.html`, `guidelines.html`, `medicines/`, `salt/`, `company/`, `seo/` | **Generated** by `build.py` | No, rebuild instead |

## Build and preview

Needs Python 3.10+ (no packages to install).

```bash
python _build/build.py          # regenerates every page
python -m http.server 8765      # then open http://localhost:8765
```

On Windows, if `₹` causes a print error, run `set PYTHONIOENCODING=utf-8` first.

## Making a change

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: branch → edit `_build/` or `assets/` → rebuild → pull request → review → merge.

## Page rules (summary)

The full rules are in `guidelines.html`. The most important:

- The top of the page is worth the most: the first screen shows why to switch, that it is the same medicine, the yearly saving and one Add to cart button.
- The brand is never promoted. It can be bought only through the "Want [brand] instead?" path, which needs a tick to enable.
- No friction copy near the buy button. Prescription medicines say a Tablow doctor calls after the order.
- No popularity or ranking claims ("#1", "best-selling"), and no lists of a company's other brands.
- Savings are always shown per year, on one formula shared by the hero, table and calculator.
