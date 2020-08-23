##############################################################################################################################
# 	RunIDAtoCollapse														                             		             #
#	This module runs incremental dynamic analyses for a given model for a specified number of ground motions to collapse     #
# 														             														 #
# 	Created by: Henry Burton, Stanford University, October 7, 2012									                         #
#   Revised by: Xingquan Guan, University of California, Los Angeles, April 2019                                             #
#								     						                                                                 #
# 	Units: kips, inches, seconds                                                                                             #
##############################################################################################################################

# Clear all memory 
wipe all;

# Ground motion scales to run
set allScales {100};

# Scale factor is required in order to anchor median ground motion Sa to MCE level
set MCEScaleFactor 1.0;

# Define the total number of ground motions
set numGMs 240;

# Define the building models' names (the name of the building model folder)
set modelNames {}
set modelNameFile [open BuildingIDs.txt r];
while {[gets $modelNameFile line] >= 0} {
	set name Building_$line
	lappend modelNames $name
}
puts "Model names defined"

# Define the total number of models for dynamic analysis
set numModels [llength $modelNames];

# Defining a variable to record the stating time
set AllStartTime [clock seconds];

# Set the root directory
set rootDir [pwd];

# Set the data output directory name
set dataDir IDAOutput

# Initializing processor information
# set np [getNP];  # Getting the number of processors
# set pid [getPID];  # Getting the processor ID number

# Setting up a vector of ground motion IDs
set groundMotionIDs {}; 
set numberOfGroundMotionIDs $numGMs; 
for {set gm 1} {$gm <= $numberOfGroundMotionIDs} {incr gm} {
	lappend groundMotionIDs $gm
}
puts "Ground motion ID's defined"

# Setting up a vector with the number of steps in each ground motion record
set groundMotionNumPoints {}; 
set pathToTextFile $rootDir/GroundMotionInfo;
set groundMotionNumPointsFile [open $pathToTextFile/GMNumPoints.txt r];
while {[gets $groundMotionNumPointsFile line] >= 0} {
	lappend groundMotionNumPoints $line;
}
close $groundMotionNumPointsFile;
puts "Ground motion number of steps defined"

# Setting up a vector with the names for each ground motion record txt file
set eqFileName {};
set eqFile [open $pathToTextFile/GMFileNames.txt r];
while {[gets $eqFile line] >= 0} {
	lappend eqFileName $line;
}
close $eqFile
puts "Ground motion file names defined"

# Setting up a vector with the time step for each ground motion record
set groundMotionTimeStep {}; 
set groundMotionTimeStepFile [open $pathToTextFile/GMTimeSteps.txt r];
while {[gets $groundMotionTimeStepFile line] >= 0} {
	lappend groundMotionTimeStep $line;
}
close $groundMotionTimeStepFile;
puts "Ground motion time steps defined"

# Total number of analysis for al models
set numSimulations [expr $numGMs*$numModels];

# Define a series of integers to denote the number of each simulation
set RunIDs {}; 
for {set ID 0} {$ID < $numSimulations} {incr ID} {
	lappend RunIDs $ID
} 
puts "Routine ID's defined"

# Specify which ground motion you want to run. The number is between 1 and 240.
# set globalCounter [lindex $argv 0];
set globalCounter 200;

set groundMotionNumber $globalCounter

# Each glorbal counter corresponds to one building subjected to one ground motion
for {set modelIndex 0} {$modelIndex < $numModels} {incr modelIndex} {
	# Define the base folder for each model
	set baseDir "$rootDir/[lindex $modelNames $modelIndex]/DynamicAnalysis"
	
	
	# foreach groundMotionNumber $groundMotionIDs {
	#if {[expr {$groundMotionNumber % $np}] == $pid} {
		set eqNumber $groundMotionNumber;
		set dt [lindex $groundMotionTimeStep [expr $groundMotionNumber - 1]];
		set numPoints [lindex $groundMotionNumPoints [expr $groundMotionNumber - 1]];

		# Run IDA until maximum scale is reached
		foreach scale $allScales {	
			cd $baseDir
			source Model.tcl
			wipe;
		}
		
		puts "********************************"
		puts "Current ModelIndex: $modelIndex."
		puts "Current GMIndex: $eqNumber."
		puts "********************************"
		
	#	}
	#}
}