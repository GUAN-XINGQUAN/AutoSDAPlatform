% This function is used to extract story drifts from IDA results

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This file doesn't save any drifts history subjected to each EQ. Instead,%
% it saves the maximum drifts and residual drifts directly.               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [ maxDriftEachStory,residualDriftEachStory ] = ...
    extractStoryDriftsFromIDA( modelDir,NumStory,NumEQ,Scale )

cd(modelDir);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find the maximum drifts of each story and residual of each story at each%
% intensity level of each ground motion                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Loop over the number of all scales
for j=1:length(Scale);
    % Loop over the number of earthquakes
    for i = 1:NumEQ;
        % Loop over the number of stories
        for k = 1:NumStory;
            pathEQ=sprintf('EQ_%i',i);
            pathScale = sprintf('Scale_%i',Scale(j));
            fileDir = strcat(modelDir,'\',pathEQ,'\',pathScale,'\','StoryDrifts');
            cd(fileDir);
            fileID = sprintf('Story%i.out',k);
            drifts = load(fileID);
            % maxDriftEachStory{i,1}(j,k) = max(abs(drifts(:,2)));
            % residualDriftEachStory{i,1}(j,k) = abs(drifts(end,2));
            maxDriftEachStory{j,1}(i,k) = max(abs(drifts(:,2)));
            residualDriftEachStory{j,1}(i,k) = abs(drifts(end,2));
        end
    end
end

end

