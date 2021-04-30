# This file will be used to define all nodal masses 

# Define floor weights and each nodal mass 
set	Floor2Weight	1163.70; 
set	Floor3Weight	1163.70; 
set	Floor4Weight	1163.70; 
set	Floor5Weight	1163.70; 
set	Floor6Weight	1163.70; 
set	Floor7Weight	1163.70; 
set	Floor8Weight	1163.70; 
set	Floor9Weight	1163.70; 
set	Floor10Weight	1163.70; 
set	Floor11Weight	1163.70; 
set	Floor12Weight	1163.70; 
set	Floor13Weight	1163.70; 
set	FrameTributaryMassRatio	0.5; 
set	TotalNodesPerFloor	5; 
set	NodalMassFloor2	[expr $Floor2Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor3	[expr $Floor3Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor4	[expr $Floor4Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor5	[expr $Floor5Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor6	[expr $Floor6Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor7	[expr $Floor7Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor8	[expr $Floor8Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor9	[expr $Floor9Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor10	[expr $Floor10Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor11	[expr $Floor11Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor12	[expr $Floor12Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor13	[expr $Floor13Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 


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

# Level 5 
mass	151	$NodalMassFloor5	$Negligible	$Negligible
mass	251	$NodalMassFloor5	$Negligible	$Negligible
mass	351	$NodalMassFloor5	$Negligible	$Negligible
mass	451	$NodalMassFloor5	$Negligible	$Negligible
mass	551	$NodalMassFloor5	$Negligible	$Negligible

# Level 6 
mass	161	$NodalMassFloor6	$Negligible	$Negligible
mass	261	$NodalMassFloor6	$Negligible	$Negligible
mass	361	$NodalMassFloor6	$Negligible	$Negligible
mass	461	$NodalMassFloor6	$Negligible	$Negligible
mass	561	$NodalMassFloor6	$Negligible	$Negligible

# Level 7 
mass	171	$NodalMassFloor7	$Negligible	$Negligible
mass	271	$NodalMassFloor7	$Negligible	$Negligible
mass	371	$NodalMassFloor7	$Negligible	$Negligible
mass	471	$NodalMassFloor7	$Negligible	$Negligible
mass	571	$NodalMassFloor7	$Negligible	$Negligible

# Level 8 
mass	181	$NodalMassFloor8	$Negligible	$Negligible
mass	281	$NodalMassFloor8	$Negligible	$Negligible
mass	381	$NodalMassFloor8	$Negligible	$Negligible
mass	481	$NodalMassFloor8	$Negligible	$Negligible
mass	581	$NodalMassFloor8	$Negligible	$Negligible

# Level 9 
mass	191	$NodalMassFloor9	$Negligible	$Negligible
mass	291	$NodalMassFloor9	$Negligible	$Negligible
mass	391	$NodalMassFloor9	$Negligible	$Negligible
mass	491	$NodalMassFloor9	$Negligible	$Negligible
mass	591	$NodalMassFloor9	$Negligible	$Negligible

# Level 10 
mass	1101	$NodalMassFloor10	$Negligible	$Negligible
mass	2101	$NodalMassFloor10	$Negligible	$Negligible
mass	3101	$NodalMassFloor10	$Negligible	$Negligible
mass	4101	$NodalMassFloor10	$Negligible	$Negligible
mass	5101	$NodalMassFloor10	$Negligible	$Negligible

# Level 11 
mass	1111	$NodalMassFloor11	$Negligible	$Negligible
mass	2111	$NodalMassFloor11	$Negligible	$Negligible
mass	3111	$NodalMassFloor11	$Negligible	$Negligible
mass	4111	$NodalMassFloor11	$Negligible	$Negligible
mass	5111	$NodalMassFloor11	$Negligible	$Negligible

# Level 12 
mass	1121	$NodalMassFloor12	$Negligible	$Negligible
mass	2121	$NodalMassFloor12	$Negligible	$Negligible
mass	3121	$NodalMassFloor12	$Negligible	$Negligible
mass	4121	$NodalMassFloor12	$Negligible	$Negligible
mass	5121	$NodalMassFloor12	$Negligible	$Negligible

# Level 13 
mass	1131	$NodalMassFloor13	$Negligible	$Negligible
mass	2131	$NodalMassFloor13	$Negligible	$Negligible
mass	3131	$NodalMassFloor13	$Negligible	$Negligible
mass	4131	$NodalMassFloor13	$Negligible	$Negligible
mass	5131	$NodalMassFloor13	$Negligible	$Negligible

# puts "Nodal mass defined"