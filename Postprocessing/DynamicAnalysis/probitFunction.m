function [theta, beta] = probitFunction(IM, num_gms, num_collapse)
% by Jack Baker
% 10/9/2012
%
% This function fits a lognormal CDF to observed probability of collapse 
% data using Probit regression. The probit regression function is used here 
% to do the fitting, since it is based on MLE and the lognormal CDF 
% function. Matlab's probit regrssion % function requires the Stats toolbox.
% These calculations are based on the following paper:
%
% Baker, J. W. (2013). “Efficient analytical fragility function fitting 
% using dynamic structural analysis.” Earthquake Spectra, (in review).
%
%
% INPUTS:
% IM            1xn           IM levels of interest
% num_gms       1x1 or 1xn    number of ground motions used at each IM level
% num_collapse 	1xn           number of collapses observed at each IM level
% 
% OUTPUTS:
% theta         1x1           median of fragility function
% beta          1x1           lognormal standard deviation of fragility function


% reshape vectors into colum vectors
IM = IM(:);
num_gms = num_gms(:);
num_collapse = num_collapse(:);
if ~isequal(size(num_gms), size(num_collapse)); % if num_gms is scalar
    num_gms = num_gms * ones(size(num_collapse)); % build a vector of appropriate size
end

% probit regression
Y = [num_collapse num_gms]; % vector of number of collapses and number of records at each level
[b,d] = glmfit(log(IM),Y,'binomial','link', 'probit');

% convert probit coefficients to lognormal distribution parameters
theta = exp(-b(1)/b(2));
beta = 1/b(2);



