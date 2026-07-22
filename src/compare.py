"""
compare.py

Step 3 of the pipeline: compare the simulated response (from
filter_calc.py) against a reference response digitized from the
original paper's plot, and produce a simple reproducibility metric
plus a plot.

Getting the reference data:
Use a free tool like WebPlotDigitizer (https://automeris.io/) to click
along the curve in the paper's published S21 plot and export it as CSV
with columns matching `frequency_ghz,s21_db`.

Usage:
    python compare.py --simulated data/paper1_response.csv --reference data/paper1_reference.csv
"""

import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compare(simulated: pd.DataFrame, reference: pd.DataFrame) -> dict:
    # Interpolate simulated response onto the reference's frequency grid
    # so we can compare point-by-point even if sampling differs.
    interp_s21 = np.interp(
        reference["frequency_ghz"],
        simulated["frequency_ghz"],
        simulated["s21_db"],
    )

    error = interp_s21 - reference["s21_db"].values
    rmse_db = float(np.sqrt(np.mean(error**2)))
    max_error_db = float(np.max(np.abs(error)))

    return {
        "rmse_db": rmse_db,
        "max_abs_error_db": max_error_db,
        "interpolated_simulated": interp_s21,
    }


def plot_comparison(simulated, reference, interp_s21, output_path):
    plt.figure(figsize=(8, 5))
    plt.plot(simulated["frequency_ghz"], simulated["s21_db"], label="Simulated (from extracted params)")
    plt.plot(reference["frequency_ghz"], reference["s21_db"], "o", label="Reference (digitized from paper)", markersize=3)
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("S21 (dB)")
    plt.title("Reproduced vs. Reported Filter Response")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Comparison plot saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compare simulated vs reference filter response")
    parser.add_argument("--simulated", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--plot-output", default="comparison_plot.png")
    args = parser.parse_args()

    simulated = pd.read_csv(args.simulated)
    reference = pd.read_csv(args.reference)

    result = compare(simulated, reference)
    print(f"RMSE: {result['rmse_db']:.2f} dB")
    print(f"Max absolute error: {result['max_abs_error_db']:.2f} dB")

    plot_comparison(simulated, reference, result["interpolated_simulated"], args.plot_output)


if __name__ == "__main__":
    main()
