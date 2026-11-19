# Life Cycle Assessment of space missions - exercise

ETH Zürich, MSc Space Systems, Core Course 1 - lecture *Life Cycle Assessment*, 25 November 2026
Karin Treyer, Paul Scherrer Institute (karin.treyer@psi.ch)

In the afternoon you do a screening LCA of **FireSat II**, the course mission, with the open-source LCA
framework [Brightway](https://docs.brightway.dev) and its graphical interface
[Activity Browser](https://github.com/LCA-ActivityBrowser/activity-browser).

## Before the course day

1. Follow [docs/INSTALL.md](docs/INSTALL.md).
2. Run `notebooks/00_setup_check.ipynb` until it prints `All good`.
3. Problems? [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md), then the TAs.

## On the course day

- [EXERCISE.md](EXERCISE.md) gives all instructions. 
- `notebooks/01_firesat_lca.ipynb` does the LCA.
- `data/FireSat2_LCI.xlsx` contains the FireSat II inventory your team improves; and you use it to note down goal&scope and document your work.

## Repository structure

| Folder | Content |
|---|---|
| `data/` | FireSat II foreground inventory (Excel file with data prepared in Brightway import format) |
| `notebooks/` | `00_setup_check`, `01_firesat_lca`, and `lca_helpers.py` |
| `envs/` | Python environment you need (`requirements.txt`, `environment.yml`) |
| `docs/` | installation and troubleshooting |

## Data and licences

- **ecoinvent 3.12** is used under the ETH teaching license for this course only. By participating in this exercise, you consent to not use the database outside this course and any work performed within the ETH space master. Do not share the project archive.
- **ESA LCA database 1.3.0b, 25 aggregated datasets**: unfortunately, due to legal restrictions, we cannot
  share the ESA LCA database with you. You can see the **names** of the 25 ESA datasets we use and calculate
  LCIA scores with them, but not their **content**: each one is an aggregated dataset ("system process") that
  holds only the sum of the elementary flows of its whole supply chain - no bill of materials, no supply chain,
  no documentation. During the lecture we show on screen what the full datasets look like. Do not share.
- FireSat II numbers come from Wertz & Larson, *Space Mission Analysis and Design* (SMAD), as compiled in the
  course's FireSat II Mission Briefing.
- Method background: ESA (2025) *Space system life cycle assessment (LCA) guidelines*, ESSB-HB-U-005 Issue 2;
  ISO 14040/14044.

