function rho=LSS(sRGB) 
  % This is the Least Slope Squared (LSS) algorithm for generating a "reasonable" reflectance curve from a given sRGB color triplet. 
  % The reflectance spans the wavelength range 380-730 nm in 10 nm increments. 
 % It solves min sum(rho_i+1 - rho_i)^2 s.t. T rho = rgb, % using Lagrangian approach. 
 % B12 is upper-right 36x3 part of inv([D,T';T,zeros(3)]) % sRGB is a three-element vector of target D65-referenced sRGB values %      in 0-255 range, % rho is a 36x1 vector of reflectance values over wavelengths 380-730 nm, 
 % Written by Scott Allen Burns, 4/25/15. 
 % Licensed under a Creative Commons Attribution-ShareAlike 4.0 International 
 % License (http://creativecommons.org/licenses/by-sa/4.0/). 
 % For more information, see  % http://www.scottburns.us/subtractive-color-mixture/ 
 
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
        
 % compute target linear rgb values 
 sRGB=sRGB(:)/255; 
 
 % convert to 0-1 column vector 
 rgb=zeros(3,1); 
 
 % remove gamma correction to get linear rgb 
 for i=1:3     
   if sRGB(i)<0.04045         
     rgb(i)=sRGB(i)/12.92;     
   else         
     rgb(i)=((sRGB(i)+0.055)/1.055)^2.4;     
   end 
 end 
 
rho=B12*rgb; 