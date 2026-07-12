SetFactory("OpenCASCADE");
// Generic D1600 fluid-domain seed. Rendered parameters are SI metres.
D = 1.6;
H = 2.0;
Sump = 0.5;
Din = 0.3;
Dout = 0.3;
Zin = 1.5;
Zout = 1.5;
Lpipe = 0.6;

// Main wet chamber plus sump.
Cylinder(1) = {0, 0, -Sump, 0, 0, H + Sump, D/2};
// Radial inlet and outlet pipe volumes. Exact boolean orientation must be validated.
Cylinder(2) = {-D/2-Lpipe, 0, Zin, Lpipe + D/2, 0, 0, Din/2};
Cylinder(3) = {0, 0, Zout, D/2+Lpipe, 0, 0, Dout/2};
BooleanUnion{ Volume{1}; Delete; }{ Volume{2,3}; Delete; }

// Candidate internals are subtracted from the fluid domain by generated design-specific scripts.
Mesh.CharacteristicLengthMin = 0.02;
Mesh.CharacteristicLengthMax = 0.12;
