% Specifications
fc = 1.42e9;           % Center frequency
BW = 90e6;             % Bandwidth
FBW = BW/fc;           % Fractional Bandwidth
N = 7;                 % Filter order
Z0 = 50;               % Characteristic impedance

% Substrate Definition (FR4)
sub = dielectric('FR4');
sub.EpsilonR = 4.4;
sub.LossTangent = 0.02;
sub.Thickness = 0.8e-3;
FBW = 0.04;
h = sub.Thickness;
er = sub.EpsilonR;

% Create Hairpin Filter
hairpin = filterHairpin;
hairpin.FilterOrder = N;
hairpin.Substrate = sub;

% Design Filter
design(hairpin,fc,'FBW',FBW,'RippleFactor',0.1);

% Frequency Sweep
freq = linspace(1.2e9,1.6e9,401);
S = sparameters(hairpin,freq);

% Plot S Parameters
figure
rfplot(S,2,1)
hold on
rfplot(S,1,1)
grid on
legend('S21 (Insertion Loss)','S11 (Return Loss)')
title('7th Order Hairpin Bandpass Filter')

% Show Layout
figure
show(hairpin)


% THEORETICAL CALCULATIONS

disp('--------------------------------')
disp('FILTER DESIGN PARAMETERS')
disp('--------------------------------')

fprintf('Center Frequency = %.2f GHz\n',fc/1e9)
fprintf('Bandwidth = %.0f MHz\n',BW/1e6)
fprintf('Fractional Bandwidth = %.4f\n',FBW)

% Effective Dielectric Constant
eeff = (er+1)/2 + (er-1)/2*(1/sqrt(1+12*h/0.003));

fprintf('\nEffective Dielectric Constant = %.3f\n',eeff)

% Guided Wavelength
c = 3e8;
lambda = c/fc;
lambda_g = lambda/sqrt(eeff);

fprintf('Guided Wavelength = %.2f mm\n',lambda_g*1000)

% Resonator Length
L = lambda_g/2;

fprintf('Resonator Length ≈ %.2f mm\n',L*1000)

% Chebyshev Prototype Values
g = [1 1.4029 1.5963 2.1349 1.5963 2.1349 1.5963 1.4029 1];

% External Quality Factor
Qe = g(1)*g(2)/FBW;

fprintf('\nExternal Q = %.2f\n',Qe)

% Coupling Coefficients
disp(' ')
disp('Coupling Coefficients')

for i=1:N-1
    
    k = FBW/sqrt(g(i+1)*g(i+2));
    
    fprintf('k%d%d = %.4f\n',i,i+1,k)
    
end

% Physical Dimensions from MATLAB
disp(' ')
disp('Hairpin Filter Physical Dimensions')
disp(hairpin)

% Approximate Spacing Estimate
disp(' ')
disp('Approximate Resonator Spacing')

for i=1:N-1
    
    k = FBW/sqrt(g(i+1)*g(i+2));
    
    s = (0.2/k)*1e-3;  
    
    fprintf('Spacing %d-%d ≈ %.2f mm\n',i,i+1,s*1000)
    
end
