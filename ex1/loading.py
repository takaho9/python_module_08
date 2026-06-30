"""Exercise 1: Loading Programs — loading.py

Data analysis tool demonstrating mastery of package management with both pip
and Poetry. Uses pandas (data manipulation), numpy (numerical computation and
to generate the simulated Matrix data — not hardcoded lists or range()), and
matplotlib (visualization). Handles missing dependencies gracefully and shows
the difference between pip and Poetry dependency management. requests is
optional (only if fetching real data from an external API).

Authorized: pandas, requests, matplotlib, numpy, sys, importlib.
"""

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
