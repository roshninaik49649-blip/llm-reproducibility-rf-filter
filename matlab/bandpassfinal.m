% Hairpin Microstrip Filter Design - 1.42 GHz


% 1. Filter Specifications
fc = 1.42e9;        % center frequency
BW = 90e6;          % bandwidth
FBW = BW/fc;        % fractional bandwidth

% 2. Substrate Definition
sub = dielectric('FR4');
sub.EpsilonR = 4.4;
sub.Thickness = 0.8e-3;
sub.LossTangent = 0.02;

% 3. Create Hairpin Filter
hp = filterHairpin;
hp.FilterOrder = 7;
hp.Substrate = sub;

design(hp,fc,'FBW',FBW,'RippleFactor',0.1);

% 4. Adjust Geometry (stable values)
hp.CoupledLineLength = 26.5e-3;
hp.CoupledLineWidth  = 1.5e-3;
hp.CoupledLineSpacing = [0.5e-3 0.8e-3];
hp.PortLineWidth = 1.5e-3;

% 5. Visualize Filter
figure
show(hp)
axis equal
grid on
title('Hairpin Filter Geometry')


% 7. Convert to PCB Component
c = pcbComponent(hp);

% 8. Board Dimensions
boardLen = 0.12;   % 120 mm
boardWid = 0.035;   % 90 mm

gnd = antenna.Rectangle( ...
    'Length',boardLen,...
    'Width',boardWid);

% 9. Create PCB Stack
p = pcbStack;

p.BoardThickness = 0.8e-3;

topLayer = c.Layers{1};

subLayer = dielectric('FR4');
subLayer.EpsilonR = 4.4;
subLayer.Thickness = 0.8e-3;

p.Layers = {topLayer,subLayer,gnd};

p.BoardShape = gnd;

% 10. Feed Locations (keep traces inside board)

% 11. Optional Via Fence (supported in your MATLAB)

viaSpacing = 7e-3;
x = -boardLen/2:viaSpacing:boardLen/2;


%  Feed locations from the filter component
p.FeedLocations = c.FeedLocations;
p.FeedDiameter = 1e-3;
pY = boardWid/2 - 2e-3;
botY = -boardWid/2 + 2e-3;

topVias = [x' repmat(topY,length(x),1)];
botVias = [x' repmat(botY,length(x),1)];

viaXY = [topVias ; botVias];

startLayer = ones(size(viaXY,1),1);
stopLayer  = 3*ones(size(viaXY,1),1);

p.ViaLocations = [viaXY startLayer stopLayer];
p.ViaDiameter = 0.8e-3;

% 12. PCB Layout Check
figure
show(p)
axis equal
title('PCB Layout')

% 13. Current Distribution
%figure
%current(p,fc)
%title('Surface Current')

% 14. Define Gerber Writer
writer = PCBServices.PCBWayWriter;
writer.Filename = 'LastHairpin_Filter_1420MHz';

% 15. Define SMA Connectors
C1 = PCBConnectors.SMAEdge_Samtec;
C2 = PCBConnectors.SMAEdge_Samtec;

C1.EdgeLocation = 'west';
C2.EdgeLocation = 'east';

C1.ExtendBoardProfile = false;
C2.ExtendBoardProfile = false;

% 16. Generate Gerber Files
[PW,g] = gerberWrite(p,writer,{C1,C2});

disp('Gerber files generated successfully')
