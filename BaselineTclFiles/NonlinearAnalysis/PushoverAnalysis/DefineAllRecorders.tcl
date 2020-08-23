# This file will be used to source all files associating with recorders

# Set up output directory
set baseDir [pwd]
set dataDir PushoverOutput
file mkdir $dataDir
cd $baseDir/$dataDir

# Creating all the sub-folders for different quantities
file mkdir BaseReactions
file mkdir BeamHingeMoment
file mkdir BeamHingeDeformations
file mkdir ColumnHingeMoment
file mkdir ColumnHingeDeformations
file mkdir GlobalBeamForces
file mkdir GlobalColumnForces
file mkdir NodeDisplacements
file mkdir StoryDrifts

# Source all the tcl files that define the output
cd $baseDir
source DefineBaseReactionRecorders2DModel.tcl

cd $baseDir
source DefineBeamHingeRecorders2DModel.tcl

cd $baseDir
source DefineColumnHingeRecorders2DModel.tcl

cd $baseDir
source DefineGlobalBeamForceRecorders2DModel.tcl

cd $baseDir
source DefineGlobalColumnForceRecorders2DModel.tcl

cd $baseDir
source DefineNodeDisplacementRecorders2DModel.tcl

cd $baseDir
source DefineStoryDriftRecorders2DModel.tcl

cd $baseDir

puts "All recorders defined"