# This file will be used to define all nodal masses 

# Define floor weights and each nodal mass 
set	Floor2Weight	2289.00; 
set	Floor3Weight	2289.00; 
set	Floor4Weight	2289.00; 
set	FrameTributaryMassRatio	0.5; 
set	TotalNodesPerFloor	5; 
set	NodalMassFloor2	[expr $Floor2Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor3	[expr $Floor3Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor4	[expr $Floor4Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 


# Level 2 
mass	121	$NodalMassFloor2	$Negligible	$Negligible
mass	221	$NodalMassFloor2	$Negligible	$Negligible
mass	321	$NodalMassFloor2	$Negligible	$Negligible
mass	421	$NodalMassFloor2	$Negligible	$Negligible
mass	521	$NodalMassFloor2	$Negligible	$Negligible

# Level 3 
mass	131	$NodalMassFloor3	$Negligible	$Negligible
mass	231	$NodalMassFloor3	$Negligible	$Negligible
mass	331	$NodalMassFloor3	$Negligible	$Negligible
mass	431	$NodalMassFloor3	$Negligible	$Negligible
mass	531	$NodalMassFloor3	$Negligible	$Negligible

# Level 4 
mass	141	$NodalMassFloor4	$Negligible	$Negligible
mass	241	$NodalMassFloor4	$Negligible	$Negligible
mass	341	$NodalMassFloor4	$Negligible	$Negligible
mass	441	$NodalMassFloor4	$Negligible	$Negligible
mass	541	$NodalMassFloor4	$Negligible	$Negligible

# puts "Nodal mass defined"