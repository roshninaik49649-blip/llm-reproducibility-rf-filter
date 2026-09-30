# Can LLMs reproduce RF filter designs from the literature?

A small experiment on **scientific reproducibility with large language models**:
given only the text of a published radio-frequency / microwave filter paper, can an
LLM recover enough design parameters to *reproduce the reported performance* — and
where does that reproduction break down?

This grew out of my MSc thesis work on a hand-designed 1.42 GHz hairpin band-pass
filter for a 21-cm radio telescope (see [`matlab/`](matlab/)): I know exactly how
much practical knowledge lives *between* the lines of such a paper, and I wanted to
test whether a language model can reconstruct a design from the published text alone.

## Pipeline

| Step | Script | What it does |
|---|---|---|
| 1 | `src/extract_params.py` | Sends a paper's method/design section to an LLM (Anthropic API) and extracts design parameters as structured JSON — order, centre frequency, bandwidth, substrate, coupling values |
| 2 | `src/filter_calc.py` | Converts the extracted parameters into a simulated band-pass response (Chebyshev prototype via `scikit-rf`) |
| 3 | `src/compare.py` | Compares the simulated response against a reference curve digitised from the paper's published S₂₁ plot, and returns a simple reproducibility metric + overlay figure |

```
paper text ──► extract_params.py ──► params.json ──► filter_calc.py ──► simulated S21
                                                                          │
                              reference S21 (WebPlotDigitizer) ──► compare.py ──► metric + plot
```

## Quick start
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...

python src/extract_params.py --input data/paper1.txt   --output data/paper1_params.json
python src/filter_calc.py    --params data/paper1_params.json --output data/paper1_response.csv
python src/compare.py        --simulated data/paper1_response.csv \
                             --reference data/paper1_reference.csv
```

## Status
Working prototype (v0.1). The three steps run end-to-end on a paper excerpt; the
first reproducibility results and overlay figures are being compiled.

- [x] Extraction and simulation steps implemented
- [x] Comparison metric + overlay plot
- [ ] Digitised reference curves for the test papers (WebPlotDigitizer CSVs)
- [ ] Results table across several papers (where does it succeed / fail?)
- [ ] Write-up

## Related work in this repository
The `matlab/` folder holds the **ground-truth instrumentation work** that motivated
the question: the design and PCB layout scripts for my 7th-order hairpin band-pass
filter (1.42 GHz, 90 MHz bandwidth), fabricated and measured with a Rohde & Schwarz
ZVH8 VNA. That measured data is the benchmark a reproduction would have to match.

## Why this matters
Reproducibility studies at scale (e.g. work on LLM-assisted reproduction of published
results) usually stop at text: *does the model restate the method correctly?* For an
instrumentation paper the real test is physical — can the reconstructed parameters
reproduce the measured response? This repo is a small, honest attempt at that.

---
*Author: Roshani Devendra Naik ([@roshninaik49649-blip](https://github.com/roshninaik49649-blip))*
