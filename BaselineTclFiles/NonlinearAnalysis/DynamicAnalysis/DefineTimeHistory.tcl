# Source dynamic solver and associated analysis parameters
source DynamicAnalysisCollapseSolver.tcl
source DefineDynamicAnalysisParameters2DModel.tcl

# Ground motion parameters
set GM_dt $dt; #($eqNumber);
set GM_numPoints $numPoints; #($eqNumber);
# set GM_FileName "Histories/[lindex $eqFileName $eqNumber-1]";
set GM_FileName "$rootDir/Histories/[lindex $eqFileName $eqNumber-1]";  # Used for running a batch of building models
set Gaccel "Series -dt $GM_dt -filePath $GM_FileName -factor $scalefactor"

# Use the following command for absolute acceleration
timeSeries Path 2 -dt $GM_dt -filePath $GM_FileName -factor $scalefactor

# Source the recorder to record absolute acceleration
source DefineAllRecorders.tcl

pattern UniformExcitation  2   1  -accel   $Gaccel
		
# Call Dynamic Analysis Solver and run for collapse tracing
set currentTime [getTime];
set dtAn [expr 1.0*$GM_dt];		# timestep of initial analysis	
set GMtime [expr $GM_dt*$GM_numPoints];
set firstTimeCheck [clock seconds];
		
#                            input Motion  simul. step  duration numStories Drift Limit    List Nodes    StoryH 1   StoryH Typical    Analysis Start Time
DynamicAnalysisCollapseSolver    $GM_dt  	$dtAn       $GMtime  $NStories     0.10   	   $FloorNodes   $HFirstStory    $HTypicalStory          $firstTimeCheck

