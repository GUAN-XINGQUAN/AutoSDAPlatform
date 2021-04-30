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
pattern	Plain	103	Linear	{

load	121	[lindex $LateralLoad 0] 0.0 0.0;	# Level2
load	131	[lindex $LateralLoad 1] 0.0 0.0;	# Level3
load	141	[lindex $LateralLoad 2] 0.0 0.0;	# Level4
load	151	[lindex $LateralLoad 3] 0.0 0.0;	# Level5
load	161	[lindex $LateralLoad 4] 0.0 0.0;	# Level6
load	171	[lindex $LateralLoad 5] 0.0 0.0;	# Level7
load	181	[lindex $LateralLoad 6] 0.0 0.0;	# Level8
load	191	[lindex $LateralLoad 7] 0.0 0.0;	# Level9
load	1101	[lindex $LateralLoad 8] 0.0 0.0;	# Level10
load	1111	[lindex $LateralLoad 9] 0.0 0.0;	# Level11
load	1121	[lindex $LateralLoad 10] 0.0 0.0;	# Level12
load	1131	[lindex $LateralLoad 11] 0.0 0.0;	# Level13

}
# puts "Earthquake load defined"