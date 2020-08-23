% This function is used to generate fragility paremeters various 
% approaches
function [theta, beta] = generateFragilityParameters(...
    numberOfLimitStateOccurrences,SpectraIntensities,...
    numberOfGroundMotions,FittingMethod)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                      Compute MLE Lognormal Parameters                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if strcmp(FittingMethod,'MLE') == 1
        % Computing MLE parameters
        [theta, beta] = maximumLikelihoodFunction(SpectraIntensities,...
            numberOfGroundMotions,numberOfLimitStateOccurrences);
    elseif strcmp(FittingMethod,'Probit') == 1    
        % Computing probit regression
        [theta, beta] = probitFunction(SpectraIntensities,...
            numberOfGroundMotions,numberOfLimitStateOccurrences);
    elseif strcmp(FittingMethod,'SSE') == 1
        % Computing minimum sum of squares regression
        [theta, beta] = sseFunction(SpectraIntensities,...
            numberOfGroundMotions,numberOfLimitStateOccurrences);
    end


end

