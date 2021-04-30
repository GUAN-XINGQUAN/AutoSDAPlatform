# This file will be used to define all recorders 


# Setting up main folders for different load scenarios
set	baseDir	[pwd]
set	dataDir	$LoadType
file	mkdir	$dataDir
cd	$baseDir/$dataDir

# Creating all the sub-folders for different quantities
file	mkdir	StoryDrifts
file	mkdir	NodeDisplacements
file	mkdir	GlobalBeamForces
file	mkdir	GlobalColumnForces

# Source all the tcl files that define the output
cd	$baseDir
source	DefineStoryDriftRecorders2DModel.tcl

cd	$baseDir
source	DefineNodeDisplacementRecorders2DModel.tcl

cd	$baseDir
source	DefineGlobalBeamForceRecorders2DModel.tcl

cd	$baseDir
source	DefineGlobalColumnForceRecorders2DModel.tcl

cd	$baseDir
# puts "All recorders defined"