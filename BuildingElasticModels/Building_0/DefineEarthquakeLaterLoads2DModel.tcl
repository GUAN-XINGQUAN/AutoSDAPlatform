# Define gravity live loads


# Assign uniform beam dead load values (kip/inch)
set	BeamDeadLoadFloor2	0.132500; 
set	BeamDeadLoadFloor3	0.132500; 
set	BeamDeadLoadFloor4	0.132500; 

# Assign uniform beam live load values (kip/inch)
set	BeamLiveLoadFloor2	0.062500; 
set	BeamLiveLoadFloor3	0.062500; 
set	BeamLiveLoadFloor4	0.062500; 

# Assign point dead load values on leaning column: kip
set	LeaningColumnDeadLoadFloor2	954.000000; 
set	LeaningColumnDeadLoadFloor3	954.000000; 
set	LeaningColumnDeadLoadFloor4	954.000000; 

# Assign point live load values on leaning column (kip)
set	LeaningColumnLiveLoadFloor2	450.000000; 
set	LeaningColumnLiveLoadFloor3	450.000000; 
set	LeaningColumnLiveLoadFloor4	450.000000; 

# Assign lateral load values caused by earthquake (kip)
set	LateralLoad	[list	58.569078	127.066572	199.889973];


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

}
# puts "Earthquake load defined"