function rho=ILLSS(sRGB)
% This is the Iterative Least Log Slope Squared (ILLSS) algorithm for generating
% a "reasonable" reflectance curve from a given sRGB color triplet.
% The reflectance spans the wavelength range 380-730 nm in 10 nm increments.

% It solves min sum(z_i+1 - z_i)^2 s.t. T exp(z) = rgb, K z = 0, where
% z=log(reflectance), using Lagrangian approach and Newton's method.
% Clips values >1 and repeats optimization until all reflectance <=1.

% T is 3x36 matrix converting reflectance to linear rgb over the range 380-730 nm,
% sRGB is a 3 element vector of target D65 referenced sRGB values in 0-255 range,
% rho is a 36x1 vector of reflectance values (0->1] over wavelengths 380-730 nm,

% Written by Scott Allen Burns, 4/11/15.
% Licensed under a Creative Commons Attribution-ShareAlike 4.0 International
% License (http://creativecommons.org/licenses/by-sa/4.0/).
% For more information, see http://www.scottburns.us/subtractive-color-mixture/

% initialize T
T = [5.47813E-05, 0.000184722, 0.000935514, 0.003096265, 0.009507714, 0.017351596, 0.022073595, 0.016353161, 0.002002407, -0.016177731, -0.033929391, 0.046158952, -0.06381706, -0.083911194, -0.091832385, -0.08258148, 0.052950086, -0.012727224, 0.037413037, 0.091701812, 0.147964686, 0.181542886, 0.210684154, 0.210058081, 0.181312094, 0.132064724, 0.093723787, 0.057159281, 0.033469657, 0.018235464, 0.009298756, 0.004023687, 0.002068643, 0.00109484, 0.000454231, 0.000255925;
    -4.65552E-05, -0.000157894, -0.000806935, -0.002707449, -0.008477628, 0.016058258, -0.02200529, -0.020027434, -0.011137726, 0.003784809, 0.022138944, 0.038965605, 0.063361718, 0.095981626, 0.126280277, 0.148575844, 0.149044804, 0.14239936, 0.122084916, 0.09544734, 0.067421931, 0.035691251, 0.01313278, -0.002384996, -0.009409573, -0.009888983, -0.008379513, 0.005606153, -0.003444663, -0.001921041, -0.000995333, -0.000435322, 0.000224537, -0.000118838, -4.93038E-05, -2.77789E-05;
     0.00032594, 0.001107914, 0.005677477, 0.01918448, 0.060978641, 0.121348231, 0.184875618, 0.208804428, 0.197318551, 0.147233899, 0.091819086, 0.046485543, 0.022982618, 0.00665036, -0.005816014, -0.012450334, -0.015524259, 0.016712927, -0.01570093, -0.013647887, -0.011317812, -0.008077223, 0.005863171, -0.003943485, -0.002490472, -0.001440876, -0.000852895, 0.000458929, -0.000248389, -0.000129773, -6.41985E-05, -2.71982E-05, 1.38913E-05, -7.35203E-06, -3.05024E-06, -1.71858E-06]
% initialize output to zeros
rho=zeros(36,1);

% handle special case of (0,0,0)
if all(sRGB==0)
    rho=0.0001*ones(36,1);
    return
end

% handle special case of (255,255,255)
if all(sRGB==255)
    rho=ones(36,1);
    return
end

% 36x36 difference matrix having 4 on main diagonal and -2 on off diagonals,
% except first and last main diagonal are 2.
D=full(gallery('tridiag',36,-2,4,-2));
D(1,1)=2;
D(36,36)=2;

% compute target linear rgb values
sRGB=sRGB(:)/255; % convert to 0-1 column vector
rgb=zeros(3,1);
% remove gamma correction to get linear rgb
for i=1:3
    if sRGB(i)<0.04045
        rgb(i)=sRGB(i)/12.92;
    else
        rgb(i)=((sRGB(i)+0.055)/1.055)^2.4;
    end
end

% outer iteration to get all refl <=1
maxouter=10;
outer_count=0; % counter for outer iteration
while (any(rho>1) && outer_count<=maxouter) || all(rho==0)
    
    % create K matrix for fixed refl constraints
    fixed_refl=find(rho>=1)';
    numfixed=length(fixed_refl);
    K=zeros(numfixed,36);
    for i=1:numfixed
        K(i,fixed_refl(i))=1;
    end
    
    % initialize
    z=zeros(36,1); % starting point all zeros
    lambda=zeros(3,1); % starting point for lambda
    mu=zeros(numfixed,1); % starting point for mu
    maxit=50; % max number of iterations
    ftol=1.0e-8; % function solution tolerance
    deltatol=1.0e-8; % change in oper pt tolerance
    count=0; % iteration counter
    
    % Newton's method iteration
    while count <= maxit
        r=exp(z);
        v=-diag(r)*T'*lambda; % 36x1
        m1=-T*r; % 3x1
        m2=-T*diag(r); % 3x36
        F=[D*z+v+K'*mu;m1+rgb;K*z]; % function vector
        J=[D+diag(v),[m2',K'];[m2;K],zeros(numfixed+3)]; % Jacobian matrix
        delta=J\(-F); % solve Newton system of equations J*delta = -F
        z=z+delta(1:36); % update z
        lambda=lambda+delta(37:39); % update lambda
        mu=mu+delta(40:end);
        if all(abs(F)<ftol) % check if functions satisfied
            if all(abs(delta)<deltatol) % check if variables converged
                % solution found
                disp(['Inner loop solution found after ',num2str(count),' iterations'])
                rho=exp(z);
                break
            end
        end
        count=count+1;
    end
    if count>=maxit
        disp(['No inner loop solution found after ',num2str(maxit),' iterations.'])
    end
    outer_count=outer_count+1;
end
if outer_count<maxouter
    disp(['Outer loop solution found after ',num2str(outer_count),' iterations'])
else
    disp(['No outer loop solution found after ',num2str(maxouter),' iterations.'])
end