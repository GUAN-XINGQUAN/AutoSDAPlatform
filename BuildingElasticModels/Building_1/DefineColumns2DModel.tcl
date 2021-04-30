# This file will be used to define columns 


# Define exterior column section sizes 
set	ExteriorColumnStory1	[SectionProperty W14X455]; 
set	ExteriorColumnStory2	[SectionProperty W14X455]; 
set	ExteriorColumnStory3	[SectionProperty W14X342]; 
set	ExteriorColumnStory4	[SectionProperty W14X342]; 
set	ExteriorColumnStory5	[SectionProperty W14X311]; 
set	ExteriorColumnStory6	[SectionProperty W14X311]; 
set	ExteriorColumnStory7	[SectionProperty W14X283]; 
set	ExteriorColumnStory8	[SectionProperty W14X283]; 
set	ExteriorColumnStory9	[SectionProperty W14X257]; 
set	ExteriorColumnStory10	[SectionProperty W14X257]; 
set	ExteriorColumnStory11	[SectionProperty W14X132]; 
set	ExteriorColumnStory12	[SectionProperty W14X132]; 


# Define interior column section sizes 
set	InteriorColumnStory1	[SectionProperty W14X550]; 
set	InteriorColumnStory2	[SectionProperty W14X550]; 
set	InteriorColumnStory3	[SectionProperty W14X426]; 
set	InteriorColumnStory4	[SectionProperty W14X426]; 
set	InteriorColumnStory5	[SectionProperty W14X398]; 
set	InteriorColumnStory6	[SectionProperty W14X398]; 
set	InteriorColumnStory7	[SectionProperty W14X370]; 
set	InteriorColumnStory8	[SectionProperty W14X370]; 
set	InteriorColumnStory9	[SectionProperty W14X311]; 
set	InteriorColumnStory10	[SectionProperty W14X311]; 
set	InteriorColumnStory11	[SectionProperty W14X159]; 
set	InteriorColumnStory12	[SectionProperty W14X159]; 


# Define columns
# Story 1 
element	elasticBeamColumn	3111121	111	121	[lindex $ExteriorColumnStory1 2]	$Es	[lindex $ExteriorColumnStory1 6]	$PDeltaTransf; 
element	elasticBeamColumn	3211221	211	221	[lindex $InteriorColumnStory1 2]	$Es	[lindex $InteriorColumnStory1 6]	$PDeltaTransf; 
element	elasticBeamColumn	3311321	311	321	[lindex $InteriorColumnStory1 2]	$Es	[lindex $InteriorColumnStory1 6]	$PDeltaTransf; 
element	elasticBeamColumn	3411421	411	421	[lindex $InteriorColumnStory1 2]	$Es	[lindex $InteriorColumnStory1 6]	$PDeltaTransf; 
element	elasticBeamColumn	3511521	511	521	[lindex $ExteriorColumnStory1 2]	$Es	[lindex $ExteriorColumnStory1 6]	$PDeltaTransf; 
element	elasticBeamColumn	361622	61	622	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 2 
element	elasticBeamColumn	3121131	121	131	[lindex $ExteriorColumnStory2 2]	$Es	[lindex $ExteriorColumnStory2 6]	$PDeltaTransf; 
element	elasticBeamColumn	3221231	221	231	[lindex $InteriorColumnStory2 2]	$Es	[lindex $InteriorColumnStory2 6]	$PDeltaTransf; 
element	elasticBeamColumn	3321331	321	331	[lindex $InteriorColumnStory2 2]	$Es	[lindex $InteriorColumnStory2 6]	$PDeltaTransf; 
element	elasticBeamColumn	3421431	421	431	[lindex $InteriorColumnStory2 2]	$Es	[lindex $InteriorColumnStory2 6]	$PDeltaTransf; 
element	elasticBeamColumn	3521531	521	531	[lindex $ExteriorColumnStory2 2]	$Es	[lindex $ExteriorColumnStory2 6]	$PDeltaTransf; 
element	elasticBeamColumn	3624632	624	632	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 3 
element	elasticBeamColumn	3131141	131	141	[lindex $ExteriorColumnStory3 2]	$Es	[lindex $ExteriorColumnStory3 6]	$PDeltaTransf; 
element	elasticBeamColumn	3231241	231	241	[lindex $InteriorColumnStory3 2]	$Es	[lindex $InteriorColumnStory3 6]	$PDeltaTransf; 
element	elasticBeamColumn	3331341	331	341	[lindex $InteriorColumnStory3 2]	$Es	[lindex $InteriorColumnStory3 6]	$PDeltaTransf; 
element	elasticBeamColumn	3431441	431	441	[lindex $InteriorColumnStory3 2]	$Es	[lindex $InteriorColumnStory3 6]	$PDeltaTransf; 
element	elasticBeamColumn	3531541	531	541	[lindex $ExteriorColumnStory3 2]	$Es	[lindex $ExteriorColumnStory3 6]	$PDeltaTransf; 
element	elasticBeamColumn	3634642	634	642	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 4 
element	elasticBeamColumn	3141151	141	151	[lindex $ExteriorColumnStory4 2]	$Es	[lindex $ExteriorColumnStory4 6]	$PDeltaTransf; 
element	elasticBeamColumn	3241251	241	251	[lindex $InteriorColumnStory4 2]	$Es	[lindex $InteriorColumnStory4 6]	$PDeltaTransf; 
element	elasticBeamColumn	3341351	341	351	[lindex $InteriorColumnStory4 2]	$Es	[lindex $InteriorColumnStory4 6]	$PDeltaTransf; 
element	elasticBeamColumn	3441451	441	451	[lindex $InteriorColumnStory4 2]	$Es	[lindex $InteriorColumnStory4 6]	$PDeltaTransf; 
element	elasticBeamColumn	3541551	541	551	[lindex $ExteriorColumnStory4 2]	$Es	[lindex $ExteriorColumnStory4 6]	$PDeltaTransf; 
element	elasticBeamColumn	3644652	644	652	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 5 
element	elasticBeamColumn	3151161	151	161	[lindex $ExteriorColumnStory5 2]	$Es	[lindex $ExteriorColumnStory5 6]	$PDeltaTransf; 
element	elasticBeamColumn	3251261	251	261	[lindex $InteriorColumnStory5 2]	$Es	[lindex $InteriorColumnStory5 6]	$PDeltaTransf; 
element	elasticBeamColumn	3351361	351	361	[lindex $InteriorColumnStory5 2]	$Es	[lindex $InteriorColumnStory5 6]	$PDeltaTransf; 
element	elasticBeamColumn	3451461	451	461	[lindex $InteriorColumnStory5 2]	$Es	[lindex $InteriorColumnStory5 6]	$PDeltaTransf; 
element	elasticBeamColumn	3551561	551	561	[lindex $ExteriorColumnStory5 2]	$Es	[lindex $ExteriorColumnStory5 6]	$PDeltaTransf; 
element	elasticBeamColumn	3654662	654	662	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 6 
element	elasticBeamColumn	3161171	161	171	[lindex $ExteriorColumnStory6 2]	$Es	[lindex $ExteriorColumnStory6 6]	$PDeltaTransf; 
element	elasticBeamColumn	3261271	261	271	[lindex $InteriorColumnStory6 2]	$Es	[lindex $InteriorColumnStory6 6]	$PDeltaTransf; 
element	elasticBeamColumn	3361371	361	371	[lindex $InteriorColumnStory6 2]	$Es	[lindex $InteriorColumnStory6 6]	$PDeltaTransf; 
element	elasticBeamColumn	3461471	461	471	[lindex $InteriorColumnStory6 2]	$Es	[lindex $InteriorColumnStory6 6]	$PDeltaTransf; 
element	elasticBeamColumn	3561571	561	571	[lindex $ExteriorColumnStory6 2]	$Es	[lindex $ExteriorColumnStory6 6]	$PDeltaTransf; 
element	elasticBeamColumn	3664672	664	672	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 7 
element	elasticBeamColumn	3171181	171	181	[lindex $ExteriorColumnStory7 2]	$Es	[lindex $ExteriorColumnStory7 6]	$PDeltaTransf; 
element	elasticBeamColumn	3271281	271	281	[lindex $InteriorColumnStory7 2]	$Es	[lindex $InteriorColumnStory7 6]	$PDeltaTransf; 
element	elasticBeamColumn	3371381	371	381	[lindex $InteriorColumnStory7 2]	$Es	[lindex $InteriorColumnStory7 6]	$PDeltaTransf; 
element	elasticBeamColumn	3471481	471	481	[lindex $InteriorColumnStory7 2]	$Es	[lindex $InteriorColumnStory7 6]	$PDeltaTransf; 
element	elasticBeamColumn	3571581	571	581	[lindex $ExteriorColumnStory7 2]	$Es	[lindex $ExteriorColumnStory7 6]	$PDeltaTransf; 
element	elasticBeamColumn	3674682	674	682	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 8 
element	elasticBeamColumn	3181191	181	191	[lindex $ExteriorColumnStory8 2]	$Es	[lindex $ExteriorColumnStory8 6]	$PDeltaTransf; 
element	elasticBeamColumn	3281291	281	291	[lindex $InteriorColumnStory8 2]	$Es	[lindex $InteriorColumnStory8 6]	$PDeltaTransf; 
element	elasticBeamColumn	3381391	381	391	[lindex $InteriorColumnStory8 2]	$Es	[lindex $InteriorColumnStory8 6]	$PDeltaTransf; 
element	elasticBeamColumn	3481491	481	491	[lindex $InteriorColumnStory8 2]	$Es	[lindex $InteriorColumnStory8 6]	$PDeltaTransf; 
element	elasticBeamColumn	3581591	581	591	[lindex $ExteriorColumnStory8 2]	$Es	[lindex $ExteriorColumnStory8 6]	$PDeltaTransf; 
element	elasticBeamColumn	3684692	684	692	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 9 
element	elasticBeamColumn	31911101	191	1101	[lindex $ExteriorColumnStory9 2]	$Es	[lindex $ExteriorColumnStory9 6]	$PDeltaTransf; 
element	elasticBeamColumn	32912101	291	2101	[lindex $InteriorColumnStory9 2]	$Es	[lindex $InteriorColumnStory9 6]	$PDeltaTransf; 
element	elasticBeamColumn	33913101	391	3101	[lindex $InteriorColumnStory9 2]	$Es	[lindex $InteriorColumnStory9 6]	$PDeltaTransf; 
element	elasticBeamColumn	34914101	491	4101	[lindex $InteriorColumnStory9 2]	$Es	[lindex $InteriorColumnStory9 6]	$PDeltaTransf; 
element	elasticBeamColumn	35915101	591	5101	[lindex $ExteriorColumnStory9 2]	$Es	[lindex $ExteriorColumnStory9 6]	$PDeltaTransf; 
element	elasticBeamColumn	36946102	694	6102	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 10 
element	elasticBeamColumn	311011111	1101	1111	[lindex $ExteriorColumnStory10 2]	$Es	[lindex $ExteriorColumnStory10 6]	$PDeltaTransf; 
element	elasticBeamColumn	321012111	2101	2111	[lindex $InteriorColumnStory10 2]	$Es	[lindex $InteriorColumnStory10 6]	$PDeltaTransf; 
element	elasticBeamColumn	331013111	3101	3111	[lindex $InteriorColumnStory10 2]	$Es	[lindex $InteriorColumnStory10 6]	$PDeltaTransf; 
element	elasticBeamColumn	341014111	4101	4111	[lindex $InteriorColumnStory10 2]	$Es	[lindex $InteriorColumnStory10 6]	$PDeltaTransf; 
element	elasticBeamColumn	351015111	5101	5111	[lindex $ExteriorColumnStory10 2]	$Es	[lindex $ExteriorColumnStory10 6]	$PDeltaTransf; 
element	elasticBeamColumn	361046112	6104	6112	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 11 
element	elasticBeamColumn	311111121	1111	1121	[lindex $ExteriorColumnStory11 2]	$Es	[lindex $ExteriorColumnStory11 6]	$PDeltaTransf; 
element	elasticBeamColumn	321112121	2111	2121	[lindex $InteriorColumnStory11 2]	$Es	[lindex $InteriorColumnStory11 6]	$PDeltaTransf; 
element	elasticBeamColumn	331113121	3111	3121	[lindex $InteriorColumnStory11 2]	$Es	[lindex $InteriorColumnStory11 6]	$PDeltaTransf; 
element	elasticBeamColumn	341114121	4111	4121	[lindex $InteriorColumnStory11 2]	$Es	[lindex $InteriorColumnStory11 6]	$PDeltaTransf; 
element	elasticBeamColumn	351115121	5111	5121	[lindex $ExteriorColumnStory11 2]	$Es	[lindex $ExteriorColumnStory11 6]	$PDeltaTransf; 
element	elasticBeamColumn	361146122	6114	6122	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 12 
element	elasticBeamColumn	311211131	1121	1131	[lindex $ExteriorColumnStory12 2]	$Es	[lindex $ExteriorColumnStory12 6]	$PDeltaTransf; 
element	elasticBeamColumn	321212131	2121	2131	[lindex $InteriorColumnStory12 2]	$Es	[lindex $InteriorColumnStory12 6]	$PDeltaTransf; 
element	elasticBeamColumn	331213131	3121	3131	[lindex $InteriorColumnStory12 2]	$Es	[lindex $InteriorColumnStory12 6]	$PDeltaTransf; 
element	elasticBeamColumn	341214131	4121	4131	[lindex $InteriorColumnStory12 2]	$Es	[lindex $InteriorColumnStory12 6]	$PDeltaTransf; 
element	elasticBeamColumn	351215131	5121	5131	[lindex $ExteriorColumnStory12 2]	$Es	[lindex $ExteriorColumnStory12 6]	$PDeltaTransf; 
element	elasticBeamColumn	361246132	6124	6132	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# puts "Columns defined"