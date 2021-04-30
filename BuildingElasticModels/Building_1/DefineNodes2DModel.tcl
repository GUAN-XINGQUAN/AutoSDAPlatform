# This file will be used to define all nodes 
# Units: inch 


# Set bay width and story height 
set	BayWidth	[expr 30.00*12]; 
set	FirstStory	[expr 13.00*12]; 
set	TypicalStory	[expr 13.00*12]; 


# Define nodes at corner of frames 
# Level 1 
node	111	[expr 0*$BayWidth]	[expr 0*$FirstStory];	 # Column #1 
node	211	[expr 1*$BayWidth]	[expr 0*$FirstStory];	 # Column #2 
node	311	[expr 2*$BayWidth]	[expr 0*$FirstStory];	 # Column #3 
node	411	[expr 3*$BayWidth]	[expr 0*$FirstStory];	 # Column #4 
node	511	[expr 4*$BayWidth]	[expr 0*$FirstStory];	 # Column #5 

# Level 2 
node	121	[expr 0*$BayWidth]	[expr 1*$FirstStory];	 # Column #1 
node	221	[expr 1*$BayWidth]	[expr 1*$FirstStory];	 # Column #2 
node	321	[expr 2*$BayWidth]	[expr 1*$FirstStory];	 # Column #3 
node	421	[expr 3*$BayWidth]	[expr 1*$FirstStory];	 # Column #4 
node	521	[expr 4*$BayWidth]	[expr 1*$FirstStory];	 # Column #5 

# Level 3 
node	131	[expr 0*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #1 
node	231	[expr 1*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #2 
node	331	[expr 2*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #3 
node	431	[expr 3*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #4 
node	531	[expr 4*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #5 

# Level 4 
node	141	[expr 0*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #1 
node	241	[expr 1*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #2 
node	341	[expr 2*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #3 
node	441	[expr 3*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #4 
node	541	[expr 4*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #5 

# Level 5 
node	151	[expr 0*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #1 
node	251	[expr 1*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #2 
node	351	[expr 2*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #3 
node	451	[expr 3*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #4 
node	551	[expr 4*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #5 

# Level 6 
node	161	[expr 0*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	 # Column #1 
node	261	[expr 1*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	 # Column #2 
node	361	[expr 2*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	 # Column #3 
node	461	[expr 3*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	 # Column #4 
node	561	[expr 4*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	 # Column #5 

# Level 7 
node	171	[expr 0*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	 # Column #1 
node	271	[expr 1*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	 # Column #2 
node	371	[expr 2*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	 # Column #3 
node	471	[expr 3*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	 # Column #4 
node	571	[expr 4*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	 # Column #5 

# Level 8 
node	181	[expr 0*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	 # Column #1 
node	281	[expr 1*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	 # Column #2 
node	381	[expr 2*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	 # Column #3 
node	481	[expr 3*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	 # Column #4 
node	581	[expr 4*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	 # Column #5 

# Level 9 
node	191	[expr 0*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	 # Column #1 
node	291	[expr 1*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	 # Column #2 
node	391	[expr 2*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	 # Column #3 
node	491	[expr 3*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	 # Column #4 
node	591	[expr 4*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	 # Column #5 

# Level 10 
node	1101	[expr 0*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	 # Column #1 
node	2101	[expr 1*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	 # Column #2 
node	3101	[expr 2*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	 # Column #3 
node	4101	[expr 3*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	 # Column #4 
node	5101	[expr 4*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	 # Column #5 

# Level 11 
node	1111	[expr 0*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	 # Column #1 
node	2111	[expr 1*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	 # Column #2 
node	3111	[expr 2*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	 # Column #3 
node	4111	[expr 3*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	 # Column #4 
node	5111	[expr 4*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	 # Column #5 

# Level 12 
node	1121	[expr 0*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	 # Column #1 
node	2121	[expr 1*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	 # Column #2 
node	3121	[expr 2*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	 # Column #3 
node	4121	[expr 3*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	 # Column #4 
node	5121	[expr 4*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	 # Column #5 

# Level 13 
node	1131	[expr 0*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	 # Column #1 
node	2131	[expr 1*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	 # Column #2 
node	3131	[expr 2*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	 # Column #3 
node	4131	[expr 3*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	 # Column #4 
node	5131	[expr 4*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	 # Column #5 

# puts "Nodes at frame corner defined" 

# Define nodes for leaning column 
node	61	[expr 5*$BayWidth]	[expr 0*$FirstStory]; 	# Level 1
node	62	[expr 5*$BayWidth]	[expr 1*$FirstStory]; 	# Level 2
node	63	[expr 5*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Level 3
node	64	[expr 5*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Level 4
node	65	[expr 5*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Level 5
node	66	[expr 5*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	# Level 6
node	67	[expr 5*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	# Level 7
node	68	[expr 5*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	# Level 8
node	69	[expr 5*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	# Level 9
node	610	[expr 5*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	# Level 10
node	611	[expr 5*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	# Level 11
node	612	[expr 5*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	# Level 12
node	613	[expr 5*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	# Level 13

# puts "Nodes for leaning column defined" 

# Define extra nodes needed to define leaning column springs 
node	622	[expr 5*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node below floor level 2
node	624	[expr 5*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node above floor level 2
node	632	[expr 5*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node below floor level 3
node	634	[expr 5*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node above floor level 3
node	642	[expr 5*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node below floor level 4
node	644	[expr 5*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node above floor level 4
node	652	[expr 5*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Node below floor level 5
node	654	[expr 5*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Node above floor level 5
node	662	[expr 5*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	# Node below floor level 6
node	664	[expr 5*$BayWidth]	[expr 1*$FirstStory+4*$TypicalStory];	# Node above floor level 6
node	672	[expr 5*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	# Node below floor level 7
node	674	[expr 5*$BayWidth]	[expr 1*$FirstStory+5*$TypicalStory];	# Node above floor level 7
node	682	[expr 5*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	# Node below floor level 8
node	684	[expr 5*$BayWidth]	[expr 1*$FirstStory+6*$TypicalStory];	# Node above floor level 8
node	692	[expr 5*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	# Node below floor level 9
node	694	[expr 5*$BayWidth]	[expr 1*$FirstStory+7*$TypicalStory];	# Node above floor level 9
node	6102	[expr 5*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	# Node below floor level 10
node	6104	[expr 5*$BayWidth]	[expr 1*$FirstStory+8*$TypicalStory];	# Node above floor level 10
node	6112	[expr 5*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	# Node below floor level 11
node	6114	[expr 5*$BayWidth]	[expr 1*$FirstStory+9*$TypicalStory];	# Node above floor level 11
node	6122	[expr 5*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	# Node below floor level 12
node	6124	[expr 5*$BayWidth]	[expr 1*$FirstStory+10*$TypicalStory];	# Node above floor level 12
node	6132	[expr 5*$BayWidth]	[expr 1*$FirstStory+11*$TypicalStory];	# Node below floor level 13

# puts "Extra nodes for leaning column springs defined"
