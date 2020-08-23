# Define analysis series
set AnalysisLoadType [list EigenValue DeadLoad LiveLoad EarthquakeLoad GravityEarthquake]

# Loop over all the analysis types
foreach LoadType $AnalysisLoadType {

puts "Analysis type is $LoadType"

# Define model builder
model BasicBuilder -ndm 2 -ndf 3

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

# Defining beam elements
source DefineBeams2DModel.tcl

# Defining column elements
source DefineColumns2DModel.tcl

# Defining rotational springs for leaning columns
source DefineLeaningColumnSpring.tcl

# Defining masses
source DefineMasses2DModel.tcl

# Perform eigen value analysis
if {$LoadType == "EigenValue"} {
	source EigenValueAnalysis.tcl
	}

# Defining all recorders
if {$LoadType != "EigenValue"} {
	source DefineAllRecorders2DModel.tcl
	}
	
# Defining gravity dead load
if {$LoadType == "DeadLoad"} {
	source DefineGravityDeadLoads2DModel.tcl
	source PerformLoadsAnalysis.tcl
	}

# Defining gravity live load
if {$LoadType == "LiveLoad"} {
	source DefineGravityLiveLoads2DModel.tcl
	source PerformLoadsAnalysis.tcl
	}

# Defining earthquake load
if {$LoadType == "EarthquakeLoad"} {
	source DefineEarthquakeLaterLoads2DModel.tcl
	source PerformLoadsAnalysis.tcl
	}
	
# Defining the load cases for checking drift
if {$LoadType == "GravityEarthquake"} {
	source DefineGravityEarthquakeLoads2DModel.tcl
	source PerformLoadsAnalysis.tcl
}

# Clear the memory
wipe all

# Create a blank line among different analysis
puts " "
}