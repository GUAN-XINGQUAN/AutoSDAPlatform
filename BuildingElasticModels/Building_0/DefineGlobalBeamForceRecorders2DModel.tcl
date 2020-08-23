# Define global beam force recorders


cd	$baseDir/$dataDir/GlobalBeamForces

# Beam element global force recorders
recorder	Element	-file	GlobalXBeamForcesLevel2.out	-time	-ele	2121221	2221321	2321421	2421521	force; 
recorder	Element	-file	GlobalXBeamForcesLevel3.out	-time	-ele	2131231	2231331	2331431	2431531	force; 
recorder	Element	-file	GlobalXBeamForcesLevel4.out	-time	-ele	2141241	2241341	2341441	2441541	force; 
