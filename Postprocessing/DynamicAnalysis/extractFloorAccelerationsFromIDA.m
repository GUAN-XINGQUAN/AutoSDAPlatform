% This function is used to extract the floor accelerations from the partial
% IDA results


function [ maxFloorAccelerations ] = ...
    extractFloorAccelerationsFromIDA( modelDir,NumStory,NumEQ,Scale )

% Go to the location where the floor accelerations are stored
cd(modelDir)

% Define the gravitational acceleration in inch/sec^2
g = 32.174*12;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find the maximum floor accelerations and store them in a .mat file      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Loop over the number of all scales
for j=1:length(Scale);
    % Loop over the number of earthquakes
    for i = 1:NumEQ;
        % Loop over the number of stories
        for k = 1:NumStory + 1;
            pathEQ=sprintf('EQ_%i',i);
            pathScale = sprintf('Scale_%i',Scale(j));
            fileDir = strcat(modelDir,'\',pathEQ,'\',pathScale,'\','NodeAccelerations');
            cd(fileDir);
            fileID = sprintf('NodeAccLevel%i.out',k);
            accelerations = load(fileID);
            maxFloorAccelerations{j,1}(i,k) =...
                max(max(abs(accelerations(:,2:size(accelerations,2)))))/g;
        end
    end
end
end

