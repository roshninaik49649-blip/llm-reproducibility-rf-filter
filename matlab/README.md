# MATLAB Filter Design Code

This folder contains the original MATLAB code developed during my MSc
thesis for a hairpin microstrip band-pass filter targeting the 1.42 GHz
hydrogen line, used in a radio astronomy receiver front end.

## Files

- **`hairpin_1420MHz_design.m`** — Core filter design and S-parameter
  simulation. Defines a 7th-order hairpin band-pass filter (FBW-based
  Chebyshev design, ripple factor 0.1) on an FR4 substrate (εr = 4.4,
  thickness 0.8 mm), centered at 1.42 GHz with a 90 MHz bandwidth. Sweeps
  frequency from 1.2–1.6 GHz and plots the resulting S-parameters.

- **`hairpin_pcb_layout_gerber.m`** — Extends the design into a full PCB
  layout: converts the filter to a `pcbComponent`, builds a PCB stack
  (FR4 dielectric + ground plane), adds a via fence and SMA edge
  connectors, and exports manufacturing-ready Gerber files.

## Requirements

- MATLAB (R2023a or later recommended)
- RF PCB Toolbox / Antenna Toolbox (for `filterHairpin`, `pcbComponent`,
  `pcbStack`, `gerberWrite`)

## Usage

```matlab
% Run the core design + simulation
run('hairpin_1420MHz_design.m')

% Run the PCB layout + Gerber export
run('hairpin_pcb_layout_gerber.m')
```

## Relation to this repository

This code represents the ground-truth, hand-designed instrumentation
work that motivated the rest of this repository: the central question
explored elsewhere here is whether a large language model can extract
and reproduce design parameters like these directly from a written
paper, rather than from source code.
