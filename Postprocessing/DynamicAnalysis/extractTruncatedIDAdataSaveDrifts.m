% This file is used to extract partial IDA data
% Developed by GUAN, XINGQUAN at UCLA, Sept. 2017

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Explanations:                                                           %
% The advantage of this file is that it saves all the drifts of structure %
% subjected to each EQ;                                                   %
% The disadvantage: time-consuming because of eval function               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear;
clf;


% Define the data stroage location
workDir = [pwd];
modelDir = 'E:\Models-3 with results\PT connection frame\DynamicAnalysis\ModelIDAOutput';

% Go to the data location
cd(modelDir);

% Define the basic variables
NumEQ = 44;                         % Number of earthquakes
Scale = 29:29:435;                  % Scale factots for earthquakes
NumStory = 6;                       % Number of stories
SaMCE = 0.690;                      % Acceleration of MCE

% Loop over the number of earthquakes
for i = 1:NumEQ;
    % Loop over the number of all scales
    for j=1:length(Scale);
        % Loop over the number of stories
        for k = 1:NumStory;
            pathEQ = sprintf('EQ_%i',i);
            pathScale = sprintf('Scale_%i',Scale(j));
            fileLocation = strcat(modelDir,'\',pathEQ,'\',pathScale,'\','StoryDrifts');
            cd(fileLocation);
            driftFile = sprintf('Story%i.out',k);
            Drift = load(driftFile);
            StoryDrift(:,k) = Drift(:,2);
            eval(['EQ_',num2str(i),'_Scale_',num2str(Scale(j)),'_Drift','=','StoryDrift;']);
        end
        eval(['EQMaxDrift','(',num2str(i),',',num2str(j),')', ...
            '=','max(max(abs(','EQ_',num2str(i),'_Scale_',num2str(Scale(j)),'_Drift)));']);
        clear pathEQ pathScale fileLocation driftFile Drift StoryDrift;
    end
end

figure(1);
IM = Scale/100*SaMCE;
for i = 1:NumEQ;
    plot(EQMaxDrift(i,:),IM);
    hold on;
end
