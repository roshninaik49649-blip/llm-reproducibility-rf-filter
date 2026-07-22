# LLM-Based Reproducibility of RF Instrumentation Papers

**Goal:** Test whether a large language model (LLM) can extract the key
design parameters from a published RF/instrumentation paper (e.g., a
band-pass filter design) and whether those extracted parameters are
sufficient to reproduce the reported frequency response.

This is a small-scale pilot of the same question explored in
CNRS thesis UMR8254-SYLDES-026: *"Reproductibilité de résultats
scientifiques en héliophysique au moyen de modèles de langue."*

## Pipeline

```
paper text (PDF/txt)
      │
      ▼
[1] extract_params.py   -- LLM extracts structured params -> JSON
      │
      ▼
[2] filter_calc.py       -- params -> simulated S21 response (scikit-rf)
      │
      ▼
[3] compare.py           -- overlay simulated vs. reported response,
                             compute agreement metric
```

## Setup

```bash
python -m venv venv
source venv/bin/activate          # (venv\Scripts\activate on Windows)
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
# 1. Extract parameters from a paper (plain text extract of the methods section)
python src/extract_params.py --input data/paper1.txt --output data/paper1_params.json

# 2. Simulate the filter response from extracted parameters
python src/filter_calc.py --params data/paper1_params.json --output data/paper1_response.csv

# 3. Compare against digitized values from the paper's own plot (you supply this)
python src/compare.py --simulated data/paper1_response.csv --reference data/paper1_reference.csv
```

## Suggested test papers

Start with 2-3 short, parameter-dense instrumentation papers you already
understand well — including, if possible, your own Master's thesis, since
you can verify extraction accuracy against ground truth you know by heart.
Good candidates: hairpin / interdigital / combline band-pass filter design
papers with explicit tables of dimensions, center frequency, order, and
insertion loss.

## What to report in your write-up

- Parameter-extraction accuracy (per paper, per parameter)
- Where the LLM hallucinated or missed values, and why (ambiguous units?
  values only in a figure, not text? multiple candidate values in the
  paper?)
- Agreement between simulated and reported frequency response (e.g. RMSE
  in dB across the passband, or center-frequency/bandwidth error in MHz)
- Your own assessment, as a domain expert, of *why* certain failures
  happened — this qualitative judgment is exactly the kind of insight an
  ML-only researcher wouldn't have, and it's worth highlighting in a
  cover letter.

## Notes

- No prior Python experience assumed. `extract_params.py` and
  `filter_calc.py` are deliberately short and heavily commented — read
  through them rather than just running them.
- Swap `ANTHROPIC_API_KEY` / the model string for OpenAI or a local model
  if preferred; only `extract_params.py` would need to change.
