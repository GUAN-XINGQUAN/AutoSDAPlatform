# Define gravity live loads


# Assign uniform beam dead load values (kip/inch)
set	BeamDeadLoadFloor2	0.108125; 
set	BeamDeadLoadFloor3	0.108125; 
set	BeamDeadLoadFloor4	0.108125; 
set	BeamDeadLoadFloor5	0.108125; 
set	BeamDeadLoadFloor6	0.108125; 
set	BeamDeadLoadFloor7	0.108125; 
set	BeamDeadLoadFloor8	0.108125; 
set	BeamDeadLoadFloor9	0.108125; 
set	BeamDeadLoadFloor10	0.108125; 
set	BeamDeadLoadFloor11	0.108125; 
set	BeamDeadLoadFloor12	0.108125; 
set	BeamDeadLoadFloor13	0.108125; 

# Assign uniform beam live load values (kip/inch)
set	BeamLiveLoadFloor2	0.037500; 
set	BeamLiveLoadFloor3	0.037500; 
set	BeamLiveLoadFloor4	0.037500; 
set	BeamLiveLoadFloor5	0.037500; 
set	BeamLiveLoadFloor6	0.037500; 
set	BeamLiveLoadFloor7	0.037500; 
set	BeamLiveLoadFloor8	0.037500; 
set	BeamLiveLoadFloor9	0.037500; 
set	BeamLiveLoadFloor10	0.037500; 
set	BeamLiveLoadFloor11	0.037500; 
set	BeamLiveLoadFloor12	0.037500; 
set	BeamLiveLoadFloor13	0.037500; 

# Assign point dead load values on leaning column: kip
set	LeaningColumnDeadLoadFloor2	864.000000; 
set	LeaningColumnDeadLoadFloor3	864.000000; 
set	LeaningColumnDeadLoadFloor4	864.000000; 
set	LeaningColumnDeadLoadFloor5	864.000000; 
set	LeaningColumnDeadLoadFloor6	864.000000; 
set	LeaningColumnDeadLoadFloor7	864.000000; 
set	LeaningColumnDeadLoadFloor8	864.000000; 
set	LeaningColumnDeadLoadFloor9	864.000000; 
set	LeaningColumnDeadLoadFloor10	864.000000; 
set	LeaningColumnDeadLoadFloor11	864.000000; 
set	LeaningColumnDeadLoadFloor12	864.000000; 
set	LeaningColumnDeadLoadFloor13	864.000000; 

# Assign point live load values on leaning column (kip)
set	LeaningColumnLiveLoadFloor2	324.000000; 
set	LeaningColumnLiveLoadFloor3	324.000000; 
set	LeaningColumnLiveLoadFloor4	324.000000; 
set	LeaningColumnLiveLoadFloor5	324.000000; 
set	LeaningColumnLiveLoadFloor6	324.000000; 
set	LeaningColumnLiveLoadFloor7	324.000000; 
set	LeaningColumnLiveLoadFloor8	324.000000; 
set	LeaningColumnLiveLoadFloor9	324.000000; 
set	LeaningColumnLiveLoadFloor10	324.000000; 
set	LeaningColumnLiveLoadFloor11	324.000000; 
set	LeaningColumnLiveLoadFloor12	324.000000; 
set	LeaningColumnLiveLoadFloor13	324.000000; 

# Assign lateral load values caused by earthquake (kip)
set	LateralLoad	[list	0.700160	2.548103	5.424912	9.273357	14.055461	19.742977	26.313537	33.748694	42.032797	51.152288	61.095227	71.850967];


# Define uniform loads on beams
# Load combinations:
# 101 Dead load only
# 102 Live load only
# 103 Earthquake load only
# 104 Gravity and earthquake (for calculation of drift)
pattern	Plain	102	Constant	{# Level2
eleLoad	-ele	2121221	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2221321	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2321421	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2421521	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor2]; 

# Level3
eleLoad	-ele	2131231	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2231331	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2331431	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2431531	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor3]; 

# Level4
eleLoad	-ele	2141241	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2241341	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2341441	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2441541	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor4]; 

# Level5
eleLoad	-ele	2151251	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2251351	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2351451	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2451551	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor5]; 

# Level6
eleLoad	-ele	2161261	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor6]; 
eleLoad	-ele	2261361	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor6]; 
eleLoad	-ele	2361461	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor6]; 
eleLoad	-ele	2461561	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor6]; 

# Level7
eleLoad	-ele	2171271	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor7]; 
eleLoad	-ele	2271371	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor7]; 
eleLoad	-ele	2371471	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor7]; 
eleLoad	-ele	2471571	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor7]; 

# Level8
eleLoad	-ele	2181281	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor8]; 
eleLoad	-ele	2281381	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor8]; 
eleLoad	-ele	2381481	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor8]; 
eleLoad	-ele	2481581	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor8]; 

# Level9
eleLoad	-ele	2191291	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor9]; 
eleLoad	-ele	2291391	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor9]; 
eleLoad	-ele	2391491	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor9]; 
eleLoad	-ele	2491591	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor9]; 

# Level10
eleLoad	-ele	211012101	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor10]; 
eleLoad	-ele	221013101	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor10]; 
eleLoad	-ele	231014101	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor10]; 
eleLoad	-ele	241015101	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor10]; 

# Level11
eleLoad	-ele	211112111	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor11]; 
eleLoad	-ele	221113111	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor11]; 
eleLoad	-ele	231114111	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor11]; 
eleLoad	-ele	241115111	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor11]; 

# Level12
eleLoad	-ele	211212121	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor12]; 
eleLoad	-ele	221213121	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor12]; 
eleLoad	-ele	231214121	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor12]; 
eleLoad	-ele	241215121	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor12]; 

# Level13
eleLoad	-ele	211312131	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor13]; 
eleLoad	-ele	221313131	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor13]; 
eleLoad	-ele	231314131	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor13]; 
eleLoad	-ele	241315131	-type	-beamUniform	[expr -1*$BeamLiveLoadFloor13]; 



# Define point loads on leaning column
load	62	0	[expr -1*$LeaningColumnLiveLoadFloor2]	0; 
load	63	0	[expr -1*$LeaningColumnLiveLoadFloor3]	0; 
load	64	0	[expr -1*$LeaningColumnLiveLoadFloor4]	0; 
load	65	0	[expr -1*$LeaningColumnLiveLoadFloor5]	0; 
load	66	0	[expr -1*$LeaningColumnLiveLoadFloor6]	0; 
load	67	0	[expr -1*$LeaningColumnLiveLoadFloor7]	0; 
load	68	0	[expr -1*$LeaningColumnLiveLoadFloor8]	0; 
load	69	0	[expr -1*$LeaningColumnLiveLoadFloor9]	0; 
load	610	0	[expr -1*$LeaningColumnLiveLoadFloor10]	0; 
load	611	0	[expr -1*$LeaningColumnLiveLoadFloor11]	0; 
load	612	0	[expr -1*$LeaningColumnLiveLoadFloor12]	0; 
load	613	0	[expr -1*$LeaningColumnLiveLoadFloor13]	0; 

}
# puts "Live load defined"