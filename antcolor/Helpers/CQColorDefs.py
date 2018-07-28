import numpy as np
import math

####################
#### CQColorDefs includes defs for calculating the distance between colors and additional conversions between spaces
################

#r1 is the ant color, r2 is the color to find the distance from
def rgbdist(r1, g1, b1, r2, g2, b2):
    floorval = math.sqrt(pow((r2 - 127.5), 2) + pow((g2 - 127.5), 2) + pow((b2 - 127.5), 2)) #floorval is the distance of the color from the midpoint of the colorspace
    distance = math.sqrt(pow((r1 - r2), 2) + pow((g1 - g2), 2) + pow((b1 - b2), 2))
    if (distance > floorval):
        distance = floorval
    distance = -(distance / floorval) + 1 #220.836478
    return distance

#accepts hues h1 and h2 as degrees 0-360
#distance of 60 degrees of hue = 1 = distance from white/black
def hsvdist(h1,s1,v1,h2,s2,v2):
    dh = abs(h1 - h2) / 60
    ds = abs(s1 - s2)
    dv = abs(v1 - v2)
    dist = math.sqrt(dh * dh + ds * ds + dv * dv)
    if (dist > 1):
        dist = 1
    dist = -(dist) + 1
    return dist

#defs to convert between CMYK and RGB
rgb_scale = 255
cmyk_scale = 100
def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy)
    m = (m - min_cmy)
    y = (y - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

#WIP Matlab conversion for estimating spectra from RGB coordinates
def ILSS(B11=None, B12=None, sRGB=None):
    # This is the Iterative Least Slope Squared (ILSS) algorithm for generating
    # a "reasonable" reflectance curve from a given sRGB color triplet.
    # The reflectance spans the wavelength range 380-730 nm in 10 nm increments.

    # It solves min sum(rho_i+1 - rho_i)^2 s.t. T rho = rgb, K1 rho = 1, K0 rho = 0,
    # using Lagrangian formulation and iteration to keep all rho (0-1].

    # B11 is upper-left 36x36 part of inv([D,T';T,zeros(3)])
    # B12 is upper-right 36x3 part of inv([D,T';T,zeros(3)])
    # sRGB is a 3-element vector of target D65-referenced sRGB values in 0-255 range,
    # rho is a 36x1 vector of reflectance values (0->1] over wavelengths 380-730 nm,

    # Written by Scott Allen Burns, 4/26/15.
    # Licensed under a Creative Commons Attribution-ShareAlike 4.0 International
    # License (http://creativecommons.org/licenses/by-sa/4.0/).
    # For more information, see http://www.scottburns.us/subtractive-color-mixture/

    rho = np.ones(36, 1) / 2# initialize output to 0.5
    rhomin = 0.00001# smallest refl value

    # handle special case of (255,255,255)
    if all(sRGB == 255):
        rho = np.ones(36, 1)
        return
        end

        # handle special case of (0,0,0)
        if all(sRGB == 0):
            rho = rhomin * np.ones(36, 1)
            return
            end

            # compute target linear rgb values
            sRGB = sRGB(mslice[:]) / 255        # convert to 0-1 column vector
            rgb = np.zeros(3, 1)
            # remove gamma correction to get linear rgb
            for i in mslice[1:3]:
                if sRGB(i) < 0.04045:
                    rgb(i).lvalue = sRGB(i) / 12.92
                else:
                    rgb(i).lvalue = ((sRGB(i) + 0.055) / 1.055) ** 2.4
                    end
                    end

                    R = B12 * rgb

                    # iteration to get all refl 0-1
                    maxit = 10                # max iterations
                    count = 0                # counter for iteration
                    while ((any(rho > 1) or any(rho < rhomin)) and count <= maxit) or count == 0:

                        # create K1 matrix for fixed refl at 1
                        fixed_upper_logical = rho >= 1
                        fixed_upper = find(fixed_upper_logical)
                        num_upper = length(fixed_upper)
                        K1 = zeros(num_upper, 36)
                        for i in mslice[1:num_upper]:
                            K1(i, fixed_upper(i)).lvalue = 1
                            end

                            # create K0 matrix for fixed refl at rhomin
                            fixed_lower_logical = rho <= rhomin
                            fixed_lower = find(fixed_lower_logical)
                            num_lower = length(fixed_lower)
                            K0 = zeros(num_lower, 36)
                            for i in mslice[1:num_lower]:
                                K0(i, fixed_lower(i)).lvalue = 1
                                end

                                # set up linear system
                                K = mcat([K1, OMPCSEMI, K0])
                                C = B11 * K.cT / (K * B11 * K.cT)                            # M*K'*inv(K*M*K')
                                rho = R - C * (K * R - mcat([ones(num_upper, 1), OMPCSEMI, rhomin * ones(num_lower, 1)]))
                                rho(fixed_upper_logical).lvalue = 1                            # eliminate FP noise
                                rho(fixed_lower_logical).lvalue = rhomin                            # eliminate FP noise

                                count = count + 1
                                end
                                if count >= maxit:
                                    disp(mcat([mstring('No solution found after '), num2str(maxit), mstring(' iterations.')]))
                                    end
