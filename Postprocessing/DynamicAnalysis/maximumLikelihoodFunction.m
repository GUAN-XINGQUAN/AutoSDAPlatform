function [theta, beta] = maximumLikelihoodFunction(IM, num_gms, num_collapse)
% by Jack Baker
% 10/9/2012
%
% This function fits a lognormal CDF to observed probability of collapse 
% data using optimization on the likelihood function for the data. 
% These calculations are based on equation 11 of the following paper:
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

% by Jack Baker
% 7/15/2011


% Initial guess for the fragility function parameters theta and beta. 
% These initial choices should not need revision in most cases, but they 
% could be altered if needed.
x0 = [0.8 0.4];

% Run optimization
options = optimset('MaxFunEvals',100000, 'GradObj', 'off'); %maximum 1000 iterations, gradient of the function not provided
x = fminsearch(@mlefit, x0, options, num_gms, num_collapse, IM) ;
theta = x(1);
beta = x(2);

% objective function to be optimized
function [loglik] = mlefit(theta, num_gms, num_collapse, IM)

% estimated probabilities of collapse, given the current fragility functionparameter estimates
p = normcdf(log(IM), log(theta(1)), theta(2)); 

% likelihood of observing num_collapse(i) collapses, given num_gms
% observations, using the current fragility function parameter estimates
likelihood = binopdf(num_collapse', num_gms', p'); % 

% sum negative log likelihood (we take the nevative value because we want
% the maximum log likelihood, and the function is searching for a minimum)
loglik = -sum(log(likelihood));



