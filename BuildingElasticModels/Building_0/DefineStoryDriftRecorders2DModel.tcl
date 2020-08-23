# Define story drift recorders


cd	$baseDir/$dataDir/StoryDrifts

recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Story1.out	-time	-iNode	111	-jNode	121	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Story2.out	-time	-iNode	121	-jNode	131	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Story3.out	-time	-iNode	131	-jNode	141	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Roof.out	-time	-iNode	111	-jNode	141	-dof	1	-perpDirn	2; 
