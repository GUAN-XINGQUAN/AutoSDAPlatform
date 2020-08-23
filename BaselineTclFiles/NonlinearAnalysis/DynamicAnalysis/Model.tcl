wipe all;

# Defining model builder
model BasicBuilder -ndm 2 -ndf 3;

# Define the periods to use for the Rayleigh damping calculations
set periodForRayleighDamping_1 **firstModePeriod**;	# Mode 1 period - NEEDS to be UPDATED
set periodForRayleighDamping_2 **thirdModePeriod**;	# Mode 3 period - NEEDS to be UPDATED

# Defining variables
source DefineVariables.tcl

# Defining functions and procedures
source DefineFunctionsAndProcedures.tcl

# Defining nodes
source DefineNodes2DModel.tcl

# Defining node fixities
source DefineFixities2DModel.tcl

# Defining floor constraint
source DefineFloorConstraint2DModel.tcl

# Defining beam hinge material models
source DefineBeamHingeMaterials2DModel.tcl

# Defining column hinge material models
source DefineColumnHingeMaterials2DModel.tcl

# Defining beam elements
source DefineBeams2DModel.tcl

# Defining column elements
source DefineColumns2DModel.tcl

# Defining beam hinges
source DefineBeamHinges2DModel.tcl

# Defining column hinges
source DefineColumnHinges2DModel.tcl

# Defining masses
source DefineMasses2DModel.tcl

# Defining elements in panel zone
source DefinePanelZoneElements.tcl

# Defining springs in panel zone
source DefinePanelZoneSprings.tcl

# Defining gravity loads
source DefineGravityLoads2DModel.tcl

# Perform gravity analysis
source PerformGravityAnalysis.tcl

# Defining damping
source DefineDamping2DModel.tcl

# Define ground motion scale factor
set scalefactor [expr $g*$scale/100*$MCEScaleFactor];

# Run Time History
source DefineTimeHistory.tcl

puts "Analysis Completed"
