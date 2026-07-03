"""Exercise 1: Loading Programs — loading.py

Data analysis tool demonstrating mastery of package management with both pip
and Poetry. Uses pandas (data manipulation), numpy (numerical computation and
to generate the simulated Matrix data — not hardcoded lists or range()), and
matplotlib (visualization). Handles missing dependencies gracefully and shows
the difference between pip and Poetry dependency management. requests is
optional (only if fetching real data from an external API).

Authorized: pandas, requests, matplotlib, numpy, sys, importlib.
"""

from __future__ import annotations

import sys
from importlib import import_module
from importlib.metadata import version, PackageNotFoundError
from importlib.util import find_spec
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


DATA_POINTS = 1000
OUTPUT_FILE = "matrix_analysis.png"
REQUIRED = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def check_dependencies() -> list[str]:
    print("Checking dependencies:")
    missing: list[str] = []
    for name, message in REQUIRED.items():
        if find_spec(name) is None:
            print(f"[MISSING] {name} - not installed")
            missing.append(name)
            continue
        try:
            print(f"[OK] {name} ({version(name)}) - {message}")
        except PackageNotFoundError:
            print(f"[OK] {name} (unknown version) - {message}")
    return missing


def report_missing(missing: list[str]) -> None:
    print()
    print(f"Missing dependencies: {', '.join(missing)}")
    print("Install them with either tool:")
    print("  pip install -r requirements.txt   # pip")
    print("  poetry install                    # Poetry")


def prepare_data() -> pd.DataFrame:
    import numpy as np
    import pandas as pd
    print("Analyzing Matrix data...")
    rng = np.random.default_rng()
    data = rng.normal(0, 1, DATA_POINTS)
    df = pd.DataFrame({"value": data})
    df["rolling_mean"] = df["value"].rolling(window=50).mean()
    df["cumulative"] = df["value"].cumsum()
    return df


def visualize_data(df: pd.DataFrame) -> None:
    matplotlib = import_module("matplotlib")
    matplotlib.use("Agg")
    plt = import_module("matplotlib.pyplot")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["value"], alpha=0.4, label="signal")
    ax.plot(df.index, df["rolling_mean"], color="red",
            label="rolling mean (50)")
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("data point")
    ax.set_ylabel("value")
    ax.legend()
    fig.savefig(OUTPUT_FILE)
    plt.close(fig)


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    missing = check_dependencies()
    if missing:
        report_missing(missing)
        sys.exit(1)
    print()
    df = prepare_data()
    print(f"Processing {DATA_POINTS} data points...")
    visualize_data(df)
    print("Generating visualization...")
    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
