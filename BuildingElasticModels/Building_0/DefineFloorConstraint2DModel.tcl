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

# puts "Floor constraint defined"