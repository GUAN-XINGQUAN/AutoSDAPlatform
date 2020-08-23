
# DynamicAnalysisCollapseSolver #########################################################
#
# This Solver is used for Collapse "hunting"
# Time Controlled Algorithm that keeps original run
#
# Developed by Dimitrios G. Lignos, Ph.D
#
# First Created: 04/20/2010
# Last Modified: 05/06/2010
#
# Uses:
# 1. dt            : Ground Motion step
# 2. dt_anal_Step  : Analysis time step
# 3. GMtime        : Ground Motion Total Time
# 4. numStories    : DriftLimit
# 
# Subroutines called:
# MaxDriftTester: Checks after loss of convergence the drifts 
#                 and garantees convergence for collapse
# Sequence of Algorithms used:
# 1. Newton with dt
# 2. Newton with initial tangent and original dt
# 3. Newton with initial tangent and original dt/2
# 4. Newton with initial tangent and original dt/10
# 5. Newton with line search and and original dt/10
# 6. Broyden with 20 sub-iterations and original dt/10
#
# Integrator Used: Modified Implicit: Hilbert Hughes Taylor with Increment Reduction
# #######################################################################################


proc DynamicAnalysisCollapseSolver {dt dt_anal_Step GMtime numStories DriftLimit FloorNodes h1 htyp startTime} {
global CollapseFlag;                                        # global variable to monitor collapse
source MaxDriftTester.tcl;                                  # For Collapse Studies
set CollapseFlag "NO"
set maxRunTime 14400;
wipeAnalysis
constraints Transformation
numberer RCM
set UmfPackLvalueFact 30
system UmfPack -lvalueFact $UmfPackLvalueFact
# system SparseSPD
test EnergyIncr 1.0e-6 300 0
algorithm Newton
integrator Newmark 0.50 0.25
analysis Transient
set dt_analysis $dt_anal_Step;    			                # timestep of analysis
set NumSteps [expr round(($GMtime + 0.0)/$dt_analysis)];	# number of steps in analysis
set startT [clock seconds];
# puts "$startT"
set ok [analyze $NumSteps $dt_analysis];
# Check Max Drifts for Collapse by Monitoring the CollapseFlag Variable
MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
if  {$CollapseFlag == "YES"} {
	set ok 0
}

# Check run time to see if it is in excess of maximum allotted time
set currentT [clock seconds];
set runTime [expr $currentT - $startT];
if  {$runTime > $maxRunTime} {
	set ok 0
}

 if {$ok != 0} {
	puts "Analysis did not converge..."
	set TmaxAnalysis $GMtime;
	# The analysis will be time-controlled and is done for the remaining time
	set ok 0;
	set controlTime [getTime];
	
	while {$controlTime < [expr round(0.90*$TmaxAnalysis)] || $ok !=0 } {
		MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
		if  {$CollapseFlag == "YES"} {
			set ok 0; break;
		} else {
			set ok 1
		}
		# Check run time to see if it is in excess of maximum allotted time
		set currentT [clock seconds];
		set runTime [expr $currentT - $startT];
		if  {$runTime > $maxRunTime} {
			set ok 0; break;
		}	

	    
		# Get Control Time inside the loop
		set controlTime [getTime]
		
		if {$ok != 0} {
			puts "Run Newton with 1/2 of step.."
			test EnergyIncr 1.0e-3 100   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis/2.0))]
			puts $NewRemainSteps
		    puts $remainTime
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze 100 [expr $dt_analysis/2.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		
		if {$ok != 0 } {		
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-3 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {
			puts "Run Newton with Initial Tangent with 1/2 of original step.."
			test EnergyIncr 1.0e-2 100 0			
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis/2.0))]
			algorithm Newton -initial
			set ok [analyze 100 [expr $dt_analysis/2.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {			
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-2 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}				
		if {$ok != 0 } {
			puts "Newton with line Search and 1/2 of the original step .."
			test EnergyIncr 1.0e-2 100 0
			algorithm NewtonLineSearch 0.50
			set ok [analyze 100 [expr $dt_analysis/2.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}				
		}
		if {$ok != 0 } {			
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-2 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}				
		if {$ok != 0 } {
			puts "Newton Initial with 1/2 of step and Displacement Control Convergence.."
			test NormDispIncr 1.0e-2 100  0
			algorithm Newton -initial
			set ok [analyze 100 [expr $dt_analysis/2.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {			
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-2 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}		
		if {$ok != 0 } {
			puts "Newton Initial with 1/2 of step energy Control Convergence and HTTP Inegrator.."
			test EnergyIncr 1.0e-2 100  0
			algorithm Newton -initial
			integrator HHTHSIncrReduct 0.5 0.95
			set ok [analyze 100 [expr $dt_analysis/2.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}			
		}
		if {$ok != 0 } {			
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-2 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes  $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}		
		if {$ok != 0 } {			
			puts "Run Newton with Initial Tangent with original step.."
			test EnergyIncr 1.0e-2 100   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton -initial
			integrator Newmark 0.50 0.25
			set ok [analyze 100 [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {			
			puts "Go Back to Newton with tangent Tangent and original step.."
			test EnergyIncr 1.0e-2 50   0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis))]
			algorithm Newton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_analysis]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}		
		if {$ok != 0 } {
			puts "Newton with 1/10 of step and do only 1 step.."
			test NormDispIncr 1.0e-1 100  0
			set controlTime [getTime]
			set remainTime [expr $TmaxAnalysis - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_analysis/10))]
			algorithm Newton -initial
			set ok [analyze 1 [expr $dt_analysis/10.0]]
			MaxDriftTester $numStories $DriftLimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}			
		}
		set controlTime [getTime]		
	}
 }
}
