"""Generate SVG peak-memory plots from the technote CSV data."""

import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "_static"
MIB = 1024 * 1024


def read_csv(name):
    with (STATIC / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def save_bars(labels, values, title, path, *, rotation=0, width=9):
    fig, ax = plt.subplots(figsize=(width, 5))
    bars = ax.bar(range(len(labels)), values, color="#4477AA")
    ax.set_title(title)
    ax.set_ylabel("Peak memory (MiB)")
    ax.set_xticks(range(len(labels)), labels, rotation=rotation, ha="right" if rotation else "center")
    ax.bar_label(bars, fmt="%.0f", padding=3)
    ax.margins(y=0.12)
    fig.tight_layout()
    fig.savefig(STATIC / path, format="svg")
    plt.close(fig)


def main():
    local = defaultdict(list)
    for row in read_csv("test-memory.csv"):
        key = (row["runner"], row["python"])
        local[key].append(int(row["max_rss_bytes"]) / MIB)
    save_bars(
        [f"{runner}\nPython {python}" for runner, python in local],
        [median(values) for values in local.values()],
        "Local build peak memory",
        "local-build-memory.svg",
        rotation=25,
        width=11,
    )

    ci = read_csv("ci-pipeline-memory.csv")
    save_bars(
        [f"{row['test_runner']}\n{row['mode']}\n{row['package_builder']}" for row in ci],
        [float(row["pipeline_peak_mib"]) for row in ci],
        "CI pipeline peak memory",
        "ci-pipeline-memory.svg",
        rotation=40,
        width=14,
    )

    solver = defaultdict(list)
    for row in read_csv("conda-solver-memory.csv"):
        solver[row["solver"]].append(int(row["max_rss_bytes"]) / MIB)
    save_bars(
        list(solver),
        [median(values) for values in solver.values()],
        "Conda solver peak memory",
        "conda-solver-memory.svg",
    )


if __name__ == "__main__":
    main()
