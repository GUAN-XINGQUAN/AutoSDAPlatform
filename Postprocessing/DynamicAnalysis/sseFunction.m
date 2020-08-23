function [theta, beta] = sseFunction(IM, num_gms, num_collapse)
% by Jack Baker
% 10/9/2012
%
% This function fits a lognormal CDF to observed probability of collapse 
% data by minimizing the sum of squared errors between the observed and
% predicted fractions of collapse. This approach is investigated in
% equation 12 of the following paper.
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

% Initial guess for the fragility function parameters theta and beta. 
% These initial choices should not need revision in most cases, but they 
% could be altered if needed.
x0 = [0.8 0.4]; % initial parameter estimates

% Run optimization
options = optimset('MaxFunEvals',1000, 'GradObj', 'off'); %maximum 1000 iterations, gradient of the function not provided
x = fminsearch(@ssefit, x0, options, num_gms, num_collapse, IM) ;
theta = x(1);
beta = x(2);


% objective function to be optimized
function [sse] = ssefit(x, num_gms, num_collapse, IM)

% estimated probabilities of collapse, given the current fragility functionparameter estimates
if x(1)<0 % don't let median of fragility function go below zero
    x(1)=0;
end
p = normcdf(log(IM), log(x(1)), x(2)); % predicted probabilities

sse = sum( (p - num_collapse./num_gms).^2); % sum of squared errors between estimated and observed probabilities
