clc;
clear;


%% Define basic variables and working directory
currentDir = [pwd];
% baseDir = 'D:\AutoSAD';
baseDir = 'C:\Users\XINGQUAN GUAN\Desktop\AutoSAD_v1'

%% Extract pushover curve
buildingID = 0;
pushoverDir = strcat(baseDir, '\BuildingNonlinearModels\Building_', ...
    num2str(buildingID), '\PushoverAnalysis\PushoverOutput');
driftDir = strcat(pushoverDir, '\StoryDrifts');
forceDir = strcat(pushoverDir, '\BaseReactions');
    
cd (driftDir);
tempDrift = importdata('Roof.out');
roofDrift = tempDrift(:,2);

cd (forceDir);
tempForce = importdata('XReactions.out');
baseReaction = sum(tempForce(:,2:end), 2)*(-1);

cd (currentDir)
    
plot(roofDrift, baseReaction, 'linewidth', 2);
xlim([0, 0.10])
xlabel('Roof drift', 'fontname', 'times new roman', 'fontsize', 12)
ylabel('Base reaction (kip)', 'fontname', 'times new roman', 'fontsize', 12)
set(gca, 'fontname', 'times new roman', 'fontsize', 12)