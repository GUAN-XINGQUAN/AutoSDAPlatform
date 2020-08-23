clear all
close all
tic

% Define path to base directory where MATLAB files are located
MATLABFilesLocation = pwd;

% Define building ID
BuildingID = '1C2-M-R';

% Define path to base directory
BaseDirectory = strcat('C:\Users\henry\Documents\UCLA\RESEARCH\',...
    'ActiveProjects\PEER_CEA_Project\PilotStudy');


% Define location of EDP data
EDPDataDirectory = strcat(BaseDirectory,'\',BuildingID,...
    '\EDPDataDirectory\');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                           Define Key Variables                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Number of ground motions
numberOfGroundMotions = 44;

% Define ground motion intensities
SaMCE = 1.5;

% Define IDA Scales
IDAScales = 5:5:100;
IDAScales = IDAScales';

% Define IDA Sas
IDASas = SaMCE*IDAScales/100;

% Go to location where where EDPs are located
cd(EDPDataDirectory)
load IDAEDPs2DModel

% Extract collapse data
collapseDrift = 1;
collapedCases = zeros(length(IDAEDPs2DModel.maxStoryDrifts(1,1,:)),1);
% Loop over the number of ground motion intensities
for i = 1:length(IDAEDPs2DModel.maxStoryDrifts(1,1,:))
    nonCollapsedGMs{i} = [];
    collapsedStories{i} = [];
    nonCollapseCases = 1;
    % Loop over the number of ground motions
    for j = 1:length(IDAEDPs2DModel.maxStoryDrifts(1,:,1))
        % Initialize variable
        collapseOccurred = 0;
        % Loop over the number of stories
        for k = 1:length(IDAEDPs2DModel.maxStoryDrifts(:,1,1))
            if IDAEDPs2DModel.maxStoryDrifts(k,j,i) > collapseDrift
                collapseOccurred = 1;
                collapsedStories{i}(j) = k;
            end
        end
        if collapseOccurred == 1
            collapedCases(i,1) = collapedCases(i,1) + 1;            
        else
            nonCollapsedGMs{i}(nonCollapseCases) = j;
            nonCollapseCases = nonCollapseCases + 1;
        end
    end
end

% Compute collapse fragility parameters
cd(MATLABFilesLocation)
[thetaCollapse, betaCollapse] = generateFragiltyParameters(...
    collapedCases,IDASas,numberOfGroundMotions,'MLE')
    

 % Extract demolition data
demolitionResidualDrift = 0.01;
demolitionCases = zeros(length(IDAEDPs2DModel.residualStoryDrifts(...
    1,1,:)),1);
% Loop over the number of ground motion intensities
for i = 1:length(IDAEDPs2DModel.residualStoryDrifts(1,1,:))
    % Loop over the number of ground motions
    for j = 1:length(IDAEDPs2DModel.residualStoryDrifts(1,:,1))
        % Initialize variable
        demolitionOccurred = 0;
        % Loop over the number of stories
        for k = 1:length(IDAEDPs2DModel.residualStoryDrifts(:,1,1))
            if IDAEDPs2DModel.residualStoryDrifts(k,j,i) > ...
                    demolitionResidualDrift
                demolitionOccurred = 1;
            end
        end
        if demolitionOccurred == 1
            demolitionCases(i,1) = demolitionCases(i,1) + 1;
        end
    end
end

% Compute demolition fragility parameters
cd(MATLABFilesLocation)
[thetaDemolition, betaDemolition] = generateFragiltyParameters(...
    demolitionCases,IDASas,numberOfGroundMotions,'Probit');


% Compute fragility functions using estimated parameters
SaLevels = 0:.01:2*SaMCE;
SaLevels = SaLevels';
LognormalCollapseProbabilities = normcdf((log(SaLevels/thetaCollapse))/...
    betaCollapse);
LognormalDemolitionProbabilities = normcdf((log(SaLevels/...
    thetaDemolition))/betaDemolition);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                         Generate Fragility Curves                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% % Fragility Curve
% figure1 = figure('Units','pixels','Position', [100 100 500 375]);
% axes1 = axes('Parent',figure1,'FontSize',14);
% ylim(axes1,[0 1]);
% hold on;
% 
% % Create initial plot of data
% LinePlot = line(SaLevels,LognormalCollapseProbabilities);
% set(LinePlot,'Color',[0 0 1],'LineStyle','-','LineWidth',3); 
% LinePlot = line(SaLevels,LognormalDemolitionProbabilities);
% set(LinePlot,'Color',[1 0 0],'LineStyle','--','LineWidth',3);
%     
% % Add Legend
% hLegend = legend('Collapse','Demolition','location','Best');
% legend boxoff  
% set(hLegend,'color','none');
% 
% % Add axes labels
% xlabel({'Sa_T_1 (g)'},'FontSize',14);
% ylabel({'Probability of Exceedance'},'FontSize',14);
% set(gca,'FontName','Helvetica','FontSize',14);

cd(EDPDataDirectory)
save('nonCollapsedGMs.mat','nonCollapsedGMs','-mat')

plot(IDASas,collapedCases/numberOfGroundMotions,...
    'Marker','square','LineStyle','none'); 
toc


