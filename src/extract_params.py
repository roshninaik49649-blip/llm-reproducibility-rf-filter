"""
extract_params.py

Step 1 of the pipeline: send the text of a paper (or a relevant excerpt,
e.g. the methods / design section) to an LLM and ask it to extract the
filter design parameters as structured JSON.

Usage:
    python extract_params.py --input data/paper1.txt --output data/paper1_params.json

Notes for a Python beginner:
- `argparse` just reads command-line flags like --input and --output.
- We ask the model to return ONLY JSON (no prose) so it's easy to parse
  reliably with `json.loads`.
- Wrap the parse in try/except because LLMs occasionally add stray text
  even when told not to; if parsing fails, we save the raw text so you
  can inspect what went wrong (this "failure" is itself useful data for
  your write-up).
"""

import argparse
import json
import os
import sys

import anthropic

EXTRACTION_PROMPT = """You are extracting RF band-pass filter design
parameters from a scientific paper excerpt. Read the text below and
extract the following fields if present. If a field is not stated,
use null. Do not guess or hallucinate values.

Fields to extract:
- filter_type (e.g. "hairpin", "interdigital", "combline")
- filter_order (integer, number of poles/stages)
- center_frequency_ghz (float)
- bandwidth_mhz (float)
- insertion_loss_db (float)
- return_loss_db (float)
- substrate_material (string, if given)
- substrate_dielectric_constant (float, if given)
- notes (string: anything ambiguous, e.g. "two candidate values given
  in text and figure disagree")

Respond with ONLY a JSON object. No markdown fences, no explanation.

PAPER EXCERPT:
---
{paper_text}
---
"""


def extract_params(paper_text: str) -> dict:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_PROMPT.format(paper_text=paper_text),
            }
        ],
    )

    raw_text = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    try:
        return {"parsed": json.loads(raw_text), "raw": raw_text}
    except json.JSONDecodeError:
        # Extraction "failed" to parse cleanly -- keep the raw output so
        # you can look at it and note the failure mode in your write-up.
        return {"parsed": None, "raw": raw_text}


def main():
    parser = argparse.ArgumentParser(description="Extract filter params via LLM")
    parser.add_argument("--input", required=True, help="Path to paper text excerpt")
    parser.add_argument("--output", required=True, help="Path to write JSON result")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Input file not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        paper_text = f.read()

    result = extract_params(paper_text)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    if result["parsed"] is None:
        print(f"WARNING: could not parse JSON cleanly. Raw output saved to {args.output}")
    else:
        print(f"Extracted parameters saved to {args.output}")
        print(json.dumps(result["parsed"], indent=2))


if __name__ == "__main__":
    main()
