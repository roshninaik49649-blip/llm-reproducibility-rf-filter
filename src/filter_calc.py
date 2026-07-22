"""
filter_calc.py

Step 2 of the pipeline: take the extracted parameters (JSON from
extract_params.py) and simulate an approximate band-pass filter
frequency response, so it can be compared against the response
reported in the original paper.

This uses a simple Chebyshev band-pass prototype via scikit-rf as a
stand-in for the actual hairpin filter's electromagnetic behaviour --
good enough to test whether the *extracted parameters* (order, center
frequency, bandwidth) are sufficient to get you "in the right ballpark",
which is exactly the reproducibility question the CNRS thesis asks at
a larger scale.

Usage:
    python filter_calc.py --params data/paper1_params.json --output data/paper1_response.csv

You already know this domain -- feel free to replace the Chebyshev
prototype with your own hairpin synthesis equations from your thesis
for a more faithful reproduction.
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd
import skrf as rf


def simulate_response(params: dict, n_points: int = 501) -> pd.DataFrame:
    order = params.get("filter_order")
    f0_ghz = params.get("center_frequency_ghz")
    bw_mhz = params.get("bandwidth_mhz")

    missing = [
        name
        for name, val in [
            ("filter_order", order),
            ("center_frequency_ghz", f0_ghz),
            ("bandwidth_mhz", bw_mhz),
        ]
        if val is None
    ]
    if missing:
        raise ValueError(
            f"Cannot simulate: missing required parameters {missing}. "
            "This is itself a useful data point for your reproducibility "
            "analysis -- note which fields the LLM failed to extract."
        )

    f0 = f0_ghz * 1e9
    bw = bw_mhz * 1e6
    f_low = f0 - bw / 2
    f_high = f0 + bw / 2

    freq = rf.Frequency(
        start=(f0 - 3 * bw) / 1e9,
        stop=(f0 + 3 * bw) / 1e9,
        npoints=n_points,
        unit="GHz",
    )

    # Chebyshev band-pass prototype as an approximation.
    # ripple_db is a placeholder -- refine using insertion_loss/return_loss
    # from the extracted params if you want a closer match.
    media = rf.media.DefinedGammaZ0(frequency=freq, z0=50)
    ripple_db = 0.1
    bp = media.cheby1(
        order=int(order),
        ripple=ripple_db,
        fl=f_low / 1e9,
        fh=f_high / 1e9,
        freq=freq,
        filter_type="bandpass",
    )

    s21_db = 20 * np.log10(np.abs(bp.s[:, 1, 0]))

    return pd.DataFrame({"frequency_ghz": freq.f / 1e9, "s21_db": s21_db})


def main():
    parser = argparse.ArgumentParser(description="Simulate filter response from extracted params")
    parser.add_argument("--params", required=True, help="Path to extracted params JSON")
    parser.add_argument("--output", required=True, help="Path to write CSV response")
    args = parser.parse_args()

    with open(args.params, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed = data.get("parsed")
    if parsed is None:
        sys.exit(
            "No parsed parameters available (extraction step failed to "
            "produce valid JSON). Check the 'raw' field in the params file."
        )

    df = simulate_response(parsed)
    df.to_csv(args.output, index=False)
    print(f"Simulated response saved to {args.output}")


if __name__ == "__main__":
    main()
