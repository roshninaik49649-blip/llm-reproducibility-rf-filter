# LLM-Based Reproducibility of RF Instrumentation Papers

**Goal:** Test whether a large language model (LLM) can extract the key
design parameters from a published RF/instrumentation paper (e.g., a
band-pass filter design) and whether those extracted parameters are
sufficient to reproduce the reported frequency response.


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
# 1. Extract parameters 
python src/extract_params.py --input data/paper1.txt --output data/paper1_params.json

# 2. Simulate the filter response from extracted parameters
python src/filter_calc.py --params data/paper1_params.json --output data/paper1_response.csv

# 3. Compare against digitized values
python src/compare.py --simulated data/paper1_response.csv --reference data/paper1_reference.csv
```







