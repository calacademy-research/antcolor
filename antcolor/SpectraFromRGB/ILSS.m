function rho=ILSS(sRGB) #B11,B12,sRGB
% This is the Iterative Least Slope Squared (ILSS) algorithm for generating
% a "reasonable" reflectance curve from a given sRGB color triplet.
% The reflectance spans the wavelength range 380-730 nm in 10 nm increments.

% It solves min sum(rho_i+1 - rho_i)^2 s.t. T rho = rgb, K1 rho = 1, K0 rho = 0,
% using Lagrangian formulation and iteration to keep all rho (0-1].

% B11 is upper-left 36x36 part of inv([D,T';T,zeros(3)])
% B12 is upper-right 36x3 part of inv([D,T';T,zeros(3)])
% sRGB is a 3-element vector of target D65-referenced sRGB values in 0-255 range,
% rho is a 36x1 vector of reflectance values (0->1] over wavelengths 380-730 nm,

% Written by Scott Allen Burns, 4/26/15.
% Licensed under a Creative Commons Attribution-ShareAlike 4.0 International
% License (http://creativecommons.org/licenses/by-sa/4.0/).
% For more information, see http://www.scottburns.us/subtractive-color-mixture/

% initialize T
T = [5.47813E-05, 0.000184722, 0.000935514, 0.003096265, 0.009507714, 0.017351596, 0.022073595, 0.016353161, 0.002002407, -0.016177731, -0.033929391, 0.046158952, -0.06381706, -0.083911194, -0.091832385, -0.08258148, 0.052950086, -0.012727224, 0.037413037, 0.091701812, 0.147964686, 0.181542886, 0.210684154, 0.210058081, 0.181312094, 0.132064724, 0.093723787, 0.057159281, 0.033469657, 0.018235464, 0.009298756, 0.004023687, 0.002068643, 0.00109484, 0.000454231, 0.000255925;
    -4.65552E-05, -0.000157894, -0.000806935, -0.002707449, -0.008477628, 0.016058258, -0.02200529, -0.020027434, -0.011137726, 0.003784809, 0.022138944, 0.038965605, 0.063361718, 0.095981626, 0.126280277, 0.148575844, 0.149044804, 0.14239936, 0.122084916, 0.09544734, 0.067421931, 0.035691251, 0.01313278, -0.002384996, -0.009409573, -0.009888983, -0.008379513, 0.005606153, -0.003444663, -0.001921041, -0.000995333, -0.000435322, 0.000224537, -0.000118838, -4.93038E-05, -2.77789E-05;
     0.00032594, 0.001107914, 0.005677477, 0.01918448, 0.060978641, 0.121348231, 0.184875618, 0.208804428, 0.197318551, 0.147233899, 0.091819086, 0.046485543, 0.022982618, 0.00665036, -0.005816014, -0.012450334, -0.015524259, 0.016712927, -0.01570093, -0.013647887, -0.011317812, -0.008077223, 0.005863171, -0.003943485, -0.002490472, -0.001440876, -0.000852895, 0.000458929, -0.000248389, -0.000129773, -6.41985E-05, -2.71982E-05, 1.38913E-05, -7.35203E-06, -3.05024E-06, -1.71858E-06]
D = [.499755; 0.546482; 0.827549; 0.91486; 0.934318; 0.866823; 1.04865; 1.17008; 1.17812; 1.14861; 1.15923; 1.08811; 1.09354; 1.07802; 1.0479; 1.07689; 1.04405; 1.04046; 1.00000; 0.963342; 0.95788; 0.886856; 0.900062; 0.895991; 0.876987; 0.832886; 0.836992; 0.800268; 0.802146; 0.822778; 0.782842; 0.697213; 0.716091; 0.74349; 0.61604; 0.698856]
B11 = inv([D,T';T,zeros(3)])
B12 = [0.0933, -0.1729, 1.0796;
        0.0933, -0.1728, 1.0796; 
        0.0932, -0.1725, 1.0794; 
        0.0927, -0.1710, 1.0783; 
        0.0910, -0.1654, 1.0744; 
        0.0854, -0.1469, 1.0615; 
        0.0723, -0.1031, 1.0308; 
        0.0487, -0.0223, 0.9736; 
        0.0147, 0.0980, 0.8873; 
        -0.0264, 0.2513, 0.7751; 
        -0.0693, 0.4234, 0.6459; 
        -0.1080, 0.5983, 0.5097; 
        -0.1374, 0.7625, 0.3749; 
        -0.1517, 0.9032, 0.2486; 
        -0.1437, 1.0056, 0.1381; 
        -0.1080, 1.0581, 0.0499; 
        -0.0424, 1.0546, -0.0122; 
        0.0501, 0.9985, -0.0487;
        0.1641, 0.8972, -0.0613; 
        0.2912, 0.7635, -0.0547; 
        0.4217, 0.6129, -0.0346; 
        0.5455, 0.4616, -0.0071; 
        0.6545, 0.3238, 0.0217; 
        0.7421, 0.2105, 0.0474; 
        0.8064, 0.1262, 0.0675; 
        0.8494, 0.0692, 0.0814; 
        0.8765, 0.0330, 0.0905; 
        0.8922, 0.0121, 0.0957; 
        0.9007, 0.0006, 0.0987; 
        0.9052, -0.0053, 0.1002; 
        0.9073, -0.0082, 0.1009; 
        0.9083, -0.0096, 0.1012; 
        0.9088, -0.0102, 0.1014; 
        0.9090, -0.0105, 0.1015; 
        0.9091, -0.0106, 0.1015; 
        0.9091, -0.0107, 0.1015]
        
rho=ones(36,1)/2; % initialize output to 0.5
rhomin=0.00001; % smallest refl value

% handle special case of (255,255,255)
if all(sRGB==255)
    rho=ones(36,1);
    return
end

% handle special case of (0,0,0)
if all(sRGB==0)
    rho=rhomin*ones(36,1);
    return
end

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

R=B12*rgb;

% iteration to get all refl 0-1
maxit=10; % max iterations
count=0; % counter for iteration
while ( (any(rho>1) || any(rho<rhomin)) && count<=maxit ) || count==0
    
    % create K1 matrix for fixed refl at 1
    fixed_upper_logical = rho>=1;
    fixed_upper=find(fixed_upper_logical);
    num_upper=length(fixed_upper);
    K1=zeros(num_upper,36);
    for i=1:num_upper
        K1(i,fixed_upper(i))=1;
    end
    
    % create K0 matrix for fixed refl at rhomin
    fixed_lower_logical = rho<=rhomin;
    fixed_lower=find(fixed_lower_logical);
    num_lower=length(fixed_lower);
    K0=zeros(num_lower,36);
    for i=1:num_lower
        K0(i,fixed_lower(i))=1;
    end
    
    % set up linear system
    K=[K1;K0];
    C=B11*K'/(K*B11*K'); % M*K'*inv(K*M*K')
    rho=R-C*(K*R-[ones(num_upper,1);rhomin*ones(num_lower,1)]);
    rho(fixed_upper_logical)=1; % eliminate FP noise
    rho(fixed_lower_logical)=rhomin; % eliminate FP noise
    
    count=count+1;
end
if count>=maxit
    disp(['No solution found after ',num2str(maxit),' iterations.'])
end