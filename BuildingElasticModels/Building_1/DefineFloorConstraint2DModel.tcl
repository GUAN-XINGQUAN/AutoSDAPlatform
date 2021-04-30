# This file will be used to define floor constraint 

set	ConstrainDOF	1;	# Nodes at same floor level have identical lateral displacement 

# Level 2 
equalDOF	121	221	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	121	321	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	121	421	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	121	521	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	121	62	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 3 
equalDOF	131	231	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	131	331	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	131	431	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	131	531	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	131	63	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 4 
equalDOF	141	241	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	141	341	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	141	441	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	141	541	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	141	64	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 5 
equalDOF	151	251	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	151	351	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	151	451	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	151	551	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	151	65	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 6 
equalDOF	161	261	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	161	361	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	161	461	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	161	561	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	161	66	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 7 
equalDOF	171	271	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	171	371	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	171	471	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	171	571	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	171	67	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 8 
equalDOF	181	281	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	181	381	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	181	481	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	181	581	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	181	68	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 9 
equalDOF	191	291	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	191	391	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	191	491	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	191	591	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	191	69	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 10 
equalDOF	1101	2101	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1101	3101	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1101	4101	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1101	5101	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1101	610	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 11 
equalDOF	1111	2111	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1111	3111	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1111	4111	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1111	5111	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1111	611	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 12 
equalDOF	1121	2121	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1121	3121	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1121	4121	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1121	5121	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1121	612	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 13 
equalDOF	1131	2131	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1131	3131	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1131	4131	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1131	5131	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1131	613	$ConstrainDOF;	# Pier 1 to Leaning column

# puts "Floor constraint defined"