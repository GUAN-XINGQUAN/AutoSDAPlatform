# Clear the memory
wipe all

# Define model builder
model BasicBuilder -ndm 2 -ndf 3

# Define pushover analysis parameters
# Following parameters will be updated using regular expression in Python
set IDctrlNode **ControlNode**
set IDctrlDOF **ControlDOF**
set Dincr **DisplacementIncrement**
set Dmax **DisplacementMaximum**

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

# Defining all recorders
source DefineAllRecorders.tcl

# Define gravity loads
source DefineGravityLoads2DModel.tcl

# Perform gravity analysis
source PerformGravityAnalysis.tcl

# Defining pushover loading
source DefinePushoverLoading2DModel.tcl

# Defining model run time parameters
set startT [clock seconds]

# Run pushover analysis
source RunStaticPushover.tcl

# Defining model run time parameters
set endT [clock seconds]
set RunTime [expr $endT - $startT]
puts "Run Time = $RunTime Seconds"