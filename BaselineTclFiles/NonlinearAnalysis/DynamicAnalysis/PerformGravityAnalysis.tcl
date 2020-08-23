##############################################################################################################################
# PerformGravityAnalysis									                            									 #
#	This file will apply a previously defined gravity load to the frame						     							 #
#	This file should be executed before running the EQ or pushover							     							 #
# 														            													     #
# Created by: Henry Burton, Stanford University, 2010									     								 #
# Revised by: XINGQUAN GUAN, UCLA, 2018																						 #
#								     						             												     #
# Units: kips, inches, seconds                                                                                               #
##############################################################################################################################

# Gravity-analysis parameters -- load-controlled static analysis
set Tol 1.0e-8; 									# Covergence tolerance for test
variable constraintsTypeGravity Plain;				# Default
if {[info exists RigidDiaphragm] == 1} {
	if {$RigidDiaphragm=="ON"} {
		variable constraintsTypeGravity Lagrange;	# 3D model: try different constraints
	};												# If rigid diaphragm is on
};													# If rigid diaphragm exists
constraints $constraintsTypeGravity;				# How it handles boundary conditions
numberer RCM; 										# Renumber dof's to minimize band-width (optimization)
system BandGeneral; 								# How to store and solve the system of equations in the analysis (large model: try UmfPack)

# set UmfPackLvalueFact 40
# system UmfPack -lvalueFact $UmfPackLvalueFact
# system SparseSPD

test EnergyIncr $Tol 6 ; 							# Determine if convergence has been achieved at the end of an iteration step
algorithm Newton;									# Use Newton's solution algorithm: updates tangent stiffness at every iteration
set NstepGravity 5;  								# Apply gravity in 5 steps
set DGravity [expr 1./$NstepGravity]; 				# Load increment;
integrator LoadControl $DGravity;					# Determine the next time step for an analysis
analysis Static;									# Define type of analysis static or transient
analyze $NstepGravity;								# Apply gravity


# ------------------------------------------------- maintain constant gravity loads and reset time to zero
loadConst -time 0.0
set Tol 1.0e-6;										# reduce tolerance after gravity loads
puts "Gravity Performed Successfully"