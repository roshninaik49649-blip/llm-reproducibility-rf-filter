% FILTER SPECIFICATIONS

fc = 1.42e9;          % Center frequency
BW = 90e6;            % Bandwidth
FBW = BW/fc;          % Fractional bandwidth

% SUBSTRATE

sub = dielectric('FR4');
sub.EpsilonR = 4.2;
sub.Thickness = 0.8e-3;
sub.LossTangent = 0.02;

% CREATE HAIRPIN FILTER

hairpin = filterHairpin;
hairpin.FilterOrder = 7;
hairpin.Substrate = sub;

% DESIGN FILTER

design(hairpin,fc,'FBW',FBW,'RippleFactor',0.1);

% FREQUENCY SWEEP

freq = linspace(1.25e9,1.55e9,501);

S = sparameters(hairpin,freq);

% PLOT S PARAMETERS

figure
rfplot(S,2,1)
hold on
rfplot(S,1,1)
grid on
title('7th Order Hairpin Bandpass Filter')

legend('S21','S11')

% SHOW PHYSICAL LAYOUT

figure
show(hairpin)

% PCB MODEL

pcb = pcbComponent(hairpin);

figure
show(pcb)

% EXPORT GERBER FILES FOR MANUFACTURING

gerberWrite(pcb,'Hairpin_1420MHz_Filter')
