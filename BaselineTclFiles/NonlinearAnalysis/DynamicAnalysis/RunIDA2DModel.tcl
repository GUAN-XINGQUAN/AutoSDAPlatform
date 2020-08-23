##############################################################################################################################
# RunIDAToCollapse															                             		             #
#	This module runs incremental dynamic analyses for a given model for a specified number of ground motions to collapse     #
# 														             														 #
# 	Created by: Henry Burton, Stanford University, October 7, 2012									                         #
#	Revised by: Xingquan Guan, University of California, Los Angeles, April 2019						                     #
#																														     #
# Units: kips, inches, seconds                                                                                               #
##############################################################################################################################

# Clear all memory
wipe all;

# Set the base directory and output folder
set baseDir [pwd];
set dataDir IDAOutput;

# Initializing processor information
set np [getNP];   # Getting the number of processors
set pid [getPID]; # Getting the processor ID number

# Setting up a vector of ground motion IDs
set groundMotionIDs {}; 
set numberOfGroundMotionIDs **NumberOfGroundMotions**; 
for {set gm 1} {$gm <= $numberOfGroundMotionIDs} {incr gm} {
	lappend groundMotionIDs $gm
}
puts "Ground motion ID's defined"

# Setting up a vector with the number of steps in each ground motion record
set groundMotionNumPoints {}; 
set pathToTextFile $baseDir/GroundMotionInfo;
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

# Ground motion scales to run
set allScales {**IntensityScales**};

# Scale factor is required in order to anchor median ground motion Sa to MCE level
set MCEScaleFactor **MCEScaleFactor**;

# Defining a variable to record the stating time
set IDAStartT [clock seconds];

# Looping over all ground motions
foreach groundMotionNumber $groundMotionIDs {
	if {[expr {$groundMotionNumber % $np}] == $pid} {
		set eqNumber $groundMotionNumber;
		set dt [lindex $groundMotionTimeStep [expr $groundMotionNumber - 1]];
		set numPoints [lindex $groundMotionNumPoints [expr $groundMotionNumber - 1]];
	
		# Run IDA until maximum scale is reached
		foreach scale $allScales {	
			cd $baseDir
			source Model.tcl
			wipe;
		}
	}
}

# Display the running time for IDA
set IDAEndT [clock seconds];
set IDARunTime [expr ($IDAEndT - $IDAStartT)/3600];
puts "Run Time = $IDARunTime Hours"
