# Trial evidence and figure reproduction

These materials accompany the critical narrative review of couple-based prevention programs in sub-Saharan Africa. They contain publication-level information and published aggregate estimates. No participant-level data were collected.

- `trials.csv` contains one row per eligible randomized trial.
- `figure_inputs.csv` lists the published odds ratios, confidence limits, endpoints, follow-up times, and source locations used in Figure 1.
- `search_and_source_audit.md` documents selection decisions and details that affect interpretation.
- `recorded_queries.md` lists selected query strings from the targeted update.
- `reproduce_figure.py` validates the ledger and reproduces the artwork from the extracted values.
- `generated/run_metadata.json` records the Python and Matplotlib versions, input checksums, and verified counts.

Run `python reproduce_figure.py` with Python 3 and Matplotlib installed. The program creates EPS, PDF, PNG, and TIFF versions of the figure in `generated/`. The plot reproduces six published model estimates from four trials. Two rows are from the Bandebereho randomization and two outcomes are from the Unite for a Better Life randomization. The code produces no pooled estimate and derives no confidence intervals.
