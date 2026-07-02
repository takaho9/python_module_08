"""Exercise 1: Loading Programs — loading.py

Data analysis tool demonstrating mastery of package management with both pip
and Poetry. Uses pandas (data manipulation), numpy (numerical computation and
to generate the simulated Matrix data — not hardcoded lists or range()), and
matplotlib (visualization). Handles missing dependencies gracefully and shows
the difference between pip and Poetry dependency management. requests is
optional (only if fetching real data from an external API).

Authorized: pandas, requests, matplotlib, numpy, sys, importlib.
"""

from importlib.metadata import version, PackageNotFoundError
from importlib import import_module
try:
    import numpy as np
    import pandas as pd
except PackageNotFoundError as e:
    print(f"PackageNotFoundError: {e.name} not found")


DATA_POINTS = 1000
OUTPUT_FILE = "matrix_analysis.png"

def check_dependencies() -> None:
    print("Checking dependencies")
    print(f"[OK] pandas ({version('pandas')}) - Data manipulation ready")
    print(f"[OK] numpy ({version('numpy')}) - Numerical computation ready")
    print(f"[OK] matplotlib ({version('matplotlib')}) - Visualization ready")

def prepare_data() -> pd.DataFrame:
    print("Analyzing Matrix data...")
    rng = np.random.default_rng()
    data = rng.normal(0, 1, DATA_POINTS)
    df = pd.DataFrame({"value": data})
    df["rolling_mean"] = df["value"].rolling(window=50).mean()
    df["cumulative"] = df["value"].cumsum()
    return df

def visualize_data(df: pd.DataFrame) -> None:
    try:
        matplotlib = import_module("matplotlib")
    except PackageNotFoundError as e:
        print(f"PackageNotFoundError: {e.name} not found")
    matplotlib.use("Agg")
    try:
        plt = import_module("matplotlib.pyplot")
    except PackageNotFoundError as e:
        print(f"PacakgeNotFoundError: {e.name} not found")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["value"], alpha=0.4, label="signal")
    ax.plot(df.index, df["rolling_mean"], color="red", label="rolling mean (50)")
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("data point")
    ax.set_ylabel("value")
    ax.legend()
    fig.savefig(OUTPUT_FILE)
    plt.close(fig)

def main() -> None:
    print("LOADING STATUS: Loading")
    print()
    check_dependencies()
    df = prepare_data()
    visualize_data(df)
    

    print(f"Processing {DATA_POINTS} data points...")
    print("Generating visualization...")


if __name__ == "__main__":
    main()

# --- Expected behavior ---
# $> python loading.py
#
# LOADING STATUS: Loading programs...
#
# Checking dependencies:
# [OK] pandas (2.1.0) - Data manipulation ready
# [OK] numpy (1.25.0) - Numerical computation ready
# [OK] requests (2.31.0) - Network access ready
# [OK] matplotlib (3.7.2) - Visualization ready
#
# Analyzing Matrix data...
# Processing 1000 data points...
# Generating visualization...
#
# Analysis complete!
# Results saved to: matrix_analysis.png
#
# Note: the requests line only appears if you fetch data from an API.
