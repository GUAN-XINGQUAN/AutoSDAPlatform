# This file will be used to define beam elements 


# Define beam section sizes 
set	BeamLevel2	[SectionProperty W30X191]; 
set	BeamLevel3	[SectionProperty W30X191]; 
set	BeamLevel4	[SectionProperty W30X148]; 
set	BeamLevel5	[SectionProperty W30X148]; 
set	BeamLevel6	[SectionProperty W30X148]; 
set	BeamLevel7	[SectionProperty W30X148]; 
set	BeamLevel8	[SectionProperty W27X146]; 
set	BeamLevel9	[SectionProperty W27X146]; 
set	BeamLevel10	[SectionProperty W24X131]; 
set	BeamLevel11	[SectionProperty W24X131]; 
set	BeamLevel12	[SectionProperty W24X76]; 
set	BeamLevel13	[SectionProperty W24X76]; 


# Define beams 
# Level 2
element	elasticBeamColumn	2121221	121	221	[lindex $BeamLevel2 2]	$Es	[lindex $BeamLevel2 6]	$LinearTransf; 
element	elasticBeamColumn	2221321	221	321	[lindex $BeamLevel2 2]	$Es	[lindex $BeamLevel2 6]	$LinearTransf; 
element	elasticBeamColumn	2321421	321	421	[lindex $BeamLevel2 2]	$Es	[lindex $BeamLevel2 6]	$LinearTransf; 
element	elasticBeamColumn	2421521	421	521	[lindex $BeamLevel2 2]	$Es	[lindex $BeamLevel2 6]	$LinearTransf; 
element	truss	252162	521	62	$AreaRigid	$TrussMatID; 

# Level 3
element	elasticBeamColumn	2131231	131	231	[lindex $BeamLevel3 2]	$Es	[lindex $BeamLevel3 6]	$LinearTransf; 
element	elasticBeamColumn	2231331	231	331	[lindex $BeamLevel3 2]	$Es	[lindex $BeamLevel3 6]	$LinearTransf; 
element	elasticBeamColumn	2331431	331	431	[lindex $BeamLevel3 2]	$Es	[lindex $BeamLevel3 6]	$LinearTransf; 
element	elasticBeamColumn	2431531	431	531	[lindex $BeamLevel3 2]	$Es	[lindex $BeamLevel3 6]	$LinearTransf; 
element	truss	253163	531	63	$AreaRigid	$TrussMatID; 

# Level 4
element	elasticBeamColumn	2141241	141	241	[lindex $BeamLevel4 2]	$Es	[lindex $BeamLevel4 6]	$LinearTransf; 
element	elasticBeamColumn	2241341	241	341	[lindex $BeamLevel4 2]	$Es	[lindex $BeamLevel4 6]	$LinearTransf; 
element	elasticBeamColumn	2341441	341	441	[lindex $BeamLevel4 2]	$Es	[lindex $BeamLevel4 6]	$LinearTransf; 
element	elasticBeamColumn	2441541	441	541	[lindex $BeamLevel4 2]	$Es	[lindex $BeamLevel4 6]	$LinearTransf; 
element	truss	254164	541	64	$AreaRigid	$TrussMatID; 

# Level 5
element	elasticBeamColumn	2151251	151	251	[lindex $BeamLevel5 2]	$Es	[lindex $BeamLevel5 6]	$LinearTransf; 
element	elasticBeamColumn	2251351	251	351	[lindex $BeamLevel5 2]	$Es	[lindex $BeamLevel5 6]	$LinearTransf; 
element	elasticBeamColumn	2351451	351	451	[lindex $BeamLevel5 2]	$Es	[lindex $BeamLevel5 6]	$LinearTransf; 
element	elasticBeamColumn	2451551	451	551	[lindex $BeamLevel5 2]	$Es	[lindex $BeamLevel5 6]	$LinearTransf; 
element	truss	255165	551	65	$AreaRigid	$TrussMatID; 

# Level 6
element	elasticBeamColumn	2161261	161	261	[lindex $BeamLevel6 2]	$Es	[lindex $BeamLevel6 6]	$LinearTransf; 
element	elasticBeamColumn	2261361	261	361	[lindex $BeamLevel6 2]	$Es	[lindex $BeamLevel6 6]	$LinearTransf; 
element	elasticBeamColumn	2361461	361	461	[lindex $BeamLevel6 2]	$Es	[lindex $BeamLevel6 6]	$LinearTransf; 
element	elasticBeamColumn	2461561	461	561	[lindex $BeamLevel6 2]	$Es	[lindex $BeamLevel6 6]	$LinearTransf; 
element	truss	256166	561	66	$AreaRigid	$TrussMatID; 

# Level 7
element	elasticBeamColumn	2171271	171	271	[lindex $BeamLevel7 2]	$Es	[lindex $BeamLevel7 6]	$LinearTransf; 
element	elasticBeamColumn	2271371	271	371	[lindex $BeamLevel7 2]	$Es	[lindex $BeamLevel7 6]	$LinearTransf; 
element	elasticBeamColumn	2371471	371	471	[lindex $BeamLevel7 2]	$Es	[lindex $BeamLevel7 6]	$LinearTransf; 
element	elasticBeamColumn	2471571	471	571	[lindex $BeamLevel7 2]	$Es	[lindex $BeamLevel7 6]	$LinearTransf; 
element	truss	257167	571	67	$AreaRigid	$TrussMatID; 

# Level 8
element	elasticBeamColumn	2181281	181	281	[lindex $BeamLevel8 2]	$Es	[lindex $BeamLevel8 6]	$LinearTransf; 
element	elasticBeamColumn	2281381	281	381	[lindex $BeamLevel8 2]	$Es	[lindex $BeamLevel8 6]	$LinearTransf; 
element	elasticBeamColumn	2381481	381	481	[lindex $BeamLevel8 2]	$Es	[lindex $BeamLevel8 6]	$LinearTransf; 
element	elasticBeamColumn	2481581	481	581	[lindex $BeamLevel8 2]	$Es	[lindex $BeamLevel8 6]	$LinearTransf; 
element	truss	258168	581	68	$AreaRigid	$TrussMatID; 

# Level 9
element	elasticBeamColumn	2191291	191	291	[lindex $BeamLevel9 2]	$Es	[lindex $BeamLevel9 6]	$LinearTransf; 
element	elasticBeamColumn	2291391	291	391	[lindex $BeamLevel9 2]	$Es	[lindex $BeamLevel9 6]	$LinearTransf; 
element	elasticBeamColumn	2391491	391	491	[lindex $BeamLevel9 2]	$Es	[lindex $BeamLevel9 6]	$LinearTransf; 
element	elasticBeamColumn	2491591	491	591	[lindex $BeamLevel9 2]	$Es	[lindex $BeamLevel9 6]	$LinearTransf; 
element	truss	259169	591	69	$AreaRigid	$TrussMatID; 

# Level 10
element	elasticBeamColumn	211012101	1101	2101	[lindex $BeamLevel10 2]	$Es	[lindex $BeamLevel10 6]	$LinearTransf; 
element	elasticBeamColumn	221013101	2101	3101	[lindex $BeamLevel10 2]	$Es	[lindex $BeamLevel10 6]	$LinearTransf; 
element	elasticBeamColumn	231014101	3101	4101	[lindex $BeamLevel10 2]	$Es	[lindex $BeamLevel10 6]	$LinearTransf; 
element	elasticBeamColumn	241015101	4101	5101	[lindex $BeamLevel10 2]	$Es	[lindex $BeamLevel10 6]	$LinearTransf; 
element	truss	25101610	5101	610	$AreaRigid	$TrussMatID; 

# Level 11
element	elasticBeamColumn	211112111	1111	2111	[lindex $BeamLevel11 2]	$Es	[lindex $BeamLevel11 6]	$LinearTransf; 
element	elasticBeamColumn	221113111	2111	3111	[lindex $BeamLevel11 2]	$Es	[lindex $BeamLevel11 6]	$LinearTransf; 
element	elasticBeamColumn	231114111	3111	4111	[lindex $BeamLevel11 2]	$Es	[lindex $BeamLevel11 6]	$LinearTransf; 
element	elasticBeamColumn	241115111	4111	5111	[lindex $BeamLevel11 2]	$Es	[lindex $BeamLevel11 6]	$LinearTransf; 
element	truss	25111611	5111	611	$AreaRigid	$TrussMatID; 

# Level 12
element	elasticBeamColumn	211212121	1121	2121	[lindex $BeamLevel12 2]	$Es	[lindex $BeamLevel12 6]	$LinearTransf; 
element	elasticBeamColumn	221213121	2121	3121	[lindex $BeamLevel12 2]	$Es	[lindex $BeamLevel12 6]	$LinearTransf; 
element	elasticBeamColumn	231214121	3121	4121	[lindex $BeamLevel12 2]	$Es	[lindex $BeamLevel12 6]	$LinearTransf; 
element	elasticBeamColumn	241215121	4121	5121	[lindex $BeamLevel12 2]	$Es	[lindex $BeamLevel12 6]	$LinearTransf; 
element	truss	25121612	5121	612	$AreaRigid	$TrussMatID; 

# Level 13
element	elasticBeamColumn	211312131	1131	2131	[lindex $BeamLevel13 2]	$Es	[lindex $BeamLevel13 6]	$LinearTransf; 
element	elasticBeamColumn	221313131	2131	3131	[lindex $BeamLevel13 2]	$Es	[lindex $BeamLevel13 6]	$LinearTransf; 
element	elasticBeamColumn	231314131	3131	4131	[lindex $BeamLevel13 2]	$Es	[lindex $BeamLevel13 6]	$LinearTransf; 
element	elasticBeamColumn	241315131	4131	5131	[lindex $BeamLevel13 2]	$Es	[lindex $BeamLevel13 6]	$LinearTransf; 
element	truss	25131613	5131	613	$AreaRigid	$TrussMatID; 

# puts "Beams defined"