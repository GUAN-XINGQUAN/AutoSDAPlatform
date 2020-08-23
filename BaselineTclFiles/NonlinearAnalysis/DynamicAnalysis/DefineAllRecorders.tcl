# This file will be used to source all files associating with recorders

# Creating Output Directory
file mkdir $dataDir;

# Go into data directory
cd $baseDir/$dataDir

# Creating all the sub-folders for different ground motion
file mkdir EQ_$eqNumber
cd $baseDir/$dataDir/EQ_$eqNumber

# Creating all the sub-folders for each ground motion under different intensities
file mkdir Scale_$scale
cd $baseDir/$dataDir/EQ_$eqNumber/Scale_$scale

# Creating all the sub-folders for different output quantities: story drift and acceleration
file mkdir NodeAccelerations
file mkdir StoryDrifts

# Source all the tcl files that define the output
cd $baseDir
source DefineNodeAccelerationRecorders2DModel.tcl

cd $baseDir
source DefineStoryDriftRecorders2DModel.tcl

cd $baseDir

puts "All recorders defined"