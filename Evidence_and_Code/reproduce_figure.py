"""Plot selected published odds ratios. The program performs no pooled estimation."""
import csv
import hashlib
import json
from pathlib import Path
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

HERE = Path(__file__).resolve().parent
OUT = HERE / "generated"
OUT.mkdir(exist_ok=True)
TRIALS = HERE / "trials.csv"
ESTIMATES = HERE / "figure_inputs.csv"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def display_number(n):
    return f"{n:.2f}"


def render(rows):
    plt.rcParams.update({
        "font.family": ["Liberation Serif", "DejaVu Serif"],
        "font.size": 10.5, "axes.labelsize": 11.5, "pdf.fonttype": 42, "ps.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "text.color": "#181818", "axes.labelcolor": "#181818",
    })
    fig = plt.figure(figsize=(6.48, 4.04))
    ax = fig.add_axes((.43, .16, .29, .73))
    ax.set(xscale="log", xlim=(.14, 1.75), ylim=(-.65, len(rows)-.28))
    ax.set_yticks([])
    ax.set_xticks([.15, .25, .5, 1., 1.5], ["0.15", "0.25", "0.5", "1", "1.5"])
    ax.xaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis="x", length=3, color="#282828", pad=4)
    ax.set_xlabel("Published odds ratio (log scale)", labelpad=5)
    ax.axvline(1, linestyle="--", color="#636363", lw=.85, zorder=1)
    for i, row in enumerate(rows):
        y = len(rows)-1-i
        mid, lo, hi = (float(row[key]) for key in ("estimate","lower_95_ci","upper_95_ci"))
        assert 0 < lo <= mid <= hi
        symbol = "D" if row["followup"] == "6 years" else "o"
        ax.errorbar(mid, y, xerr=[[mid-lo],[hi-mid]], fmt=symbol, ms=4.8,
                    lw=1.12, elinewidth=1.12, capsize=2.8, color="#222222", zorder=3)
        fig_y = ax.transData.transform((1, y))[1]/fig.bbox.height
        fig.text(.018, fig_y+.012, row["label"], ha="left", va="center",
                 fontweight="bold", fontsize=10.6)
        fig.text(.018, fig_y-.031, f'{row["endpoint"]}, {row["followup"]}',
                 ha="left", va="center", fontsize=9.55)
        fig.text(.751, fig_y, f'{display_number(mid)}  [{display_number(lo)}, {display_number(hi)}]',
                 ha="left", va="center", fontsize=10.4)
    fig.text(.018, .929, "Program and outcome", ha="left", va="center",
             fontweight="bold", fontsize=11.5)
    fig.text(.751, .929, "OR [95% CI]", ha="left", va="center",
             fontweight="bold", fontsize=11.5)
    for ext, kwargs in (("eps",{}),("pdf",{}),("png",{"dpi":600}),
                        ("tiff",{"dpi":600,"pil_kwargs":{"compression":"tiff_lzw"}})):
        fig.savefig(OUT/f"Figure_1_Published_Odds_Ratios.{ext}",facecolor="white", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    trials = read_csv(TRIALS)
    ids = {r["trial_id"] for r in trials}
    rows = read_csv(ESTIMATES)
    assert len(trials) == len(ids) == 9 and len({r["country"] for r in trials}) == 7
    assert len(rows) == 6 and {r["measure"] for r in rows} == {"OR"}
    assert {r["trial_id"] for r in rows}.issubset(ids)
    assert sum(r["trial_id"] == "PA03" for r in rows) == 2
    (OUT/"run_metadata.json").write_text(json.dumps({
        "command":"python reproduce_figure.py",
        "python":platform.python_version(),
        "matplotlib":matplotlib.__version__,
        "input_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (TRIALS, ESTIMATES)},
        "trials":len(trials),
        "countries":len({r["country"] for r in trials}),
        "published_estimates_plotted":len(rows),
    },indent=2)+"\n",encoding="utf-8")
    render(rows)
