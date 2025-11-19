from SB_calculations import SFD_BMD
from sectional_properties import prop
from fold_envelope import compute_envelope
import math

## VARIABLE NAMES

#manual input variables:
#upper_flange_thickness: number of layers for the upper flange (int)
#lower_flange_thickness: number of layers for lower flange (int)
#webbing_thickness: number of layers for webbings (int)
#upper_flange_step, lower_flange_step, distance_between_webbing_step: how much each loop increments by (lower = more accurate) (int)
#upper_flange_bound, lower_flange_bound: max values for upper, lower flange (int)
 
#important custom variables
#dimensions: list containing all possible design dimensions (nested list)

#constants
#E = 4000 MPa
#mu = 0.2
#sigma_t = 30 MPa
#sigma_c = 6 MPa
#tau_m = 4 MPa 
#tau_g = 2 MPa

#L: length of bridge
#n: ????
# P: weight of train

#upper_flange_height: height of upper flange (int)
#lower_flange_height: height of lower flange (int)
#webbing_width: width of webbing  (int)

#variables in loop 
#best_min_FOS: value of the minimum FOS for the best design (float)
#best_dimensions: dimensions for the best design (list)
#y: ybar, defined by y_bar_and_I() function called in loop (float)
#inertia: I-value, defined by y_bar_and_I() function called in loop (float)


#initalize values
L = 1200
n = 1200
dx = L/n
x = [i*dx for i in range(n)]
P = 400

x_train = [52, 228, 392, 568, 732, 908]
P_train = [P/6]*6


## MANUAL INPUTS

# number of layers for specific members
upper_flange_thickness = 1
lower_flange_thickness = 1
webbing_thickness = 1 

# how much each loop increments by (lower = more accurate)
upper_flange_step = 20
lower_flange_step = 20
distance_between_webbing_step = 20

# upper bounds of dimensions
upper_flange_bound = 300
lower_flange_bound = 300


## loop to create list of all viable dimensions, in mm

dimensions = []

for height in range(20, 200, 20):
    for upper_flange_length in range(100, upper_flange_bound, upper_flange_step):
        for lower_flange_length in range(60, lower_flange_bound, lower_flange_step):
            for distance_between_webbing in range(50,max(upper_flange_length+1,lower_flange_length+1), distance_between_webbing_step):
                diaphragm_area = 813 * 1016 - 1250 * (upper_flange_length * upper_flange_thickness + lower_flange_length * lower_flange_thickness + 2*height*webbing_thickness)
                dimension = [height, upper_flange_length, lower_flange_length, distance_between_webbing, diaphragm_area]
                if diaphragm_area >= 0:
                    dimensions.append(dimension)



## CIV CALCULATIONS

#constants (i think were missing some if u guys can add it)
E = 4000 #MPa
mu = 0.2
sigma_t = 30 #MPa
sigma_c = 6 #MPa
tau_m = 4 #MPa 
tau_g = 2 #MPa

L = 1200 #mm
n = 1200 
P = 1000 #N

upper_flange_height = 1.27 * upper_flange_thickness
lower_flange_height = 1.27 * lower_flange_thickness
webbing_width = 1.27 * webbing_thickness

##add BMD and SFD function here???

# takes input of a list, dimension, returns ybar (in mm) and I (in mm^4) values
def y_bar_and_I(dimension):
    A_web = webbing_width * dimension[0] ## area of ONE of the webbings
    A_upper = upper_flange_height * dimension[1]
    A_lower = lower_flange_height * dimension[2]

    y_lower = lower_flange_height / 2
    y_web = lower_flange_height + dimension[0] / 2
    y_upper = lower_flange_height + dimension[0] + upper_flange_height/2

    A_total = A_web + A_upper + A_lower

    ybar = (1/A_total) * (2*A_web*y_web + A_upper*y_upper + A_lower*y_lower)

    ## I calculations

    d_upper = y_upper - ybar
    d_lower = ybar - y_lower
    d_web = abs(ybar - y_web)

    I_web = ((webbing_width * dimension[0]**3) / 12) + A_web * d_web**2
    I_upper = ((dimension[1] * upper_flange_height**3) / 12) + A_upper * d_upper**2
    I_lower = ((dimension[2] * lower_flange_height**3) / 12) + A_lower * d_lower**2

    inertia = I_web + I_lower + I_upper

    return ybar, inertia


def FOS(): ##add this
    None



## FINDING OPTIMAL DESIGN (loop)

best_min_FOS = 0
best_dimensions = []
print("here")

# Precompute expensive envelope once and reuse for all section checks
# compute_envelope returns (x, SFD_env, BMD_env)
graphs = compute_envelope(L, n, P_train, x_train, dx)

for dim in dimensions: 
    # correct unpacking: ybar, inertia
    #ybar, inertia = y_bar_and_I(dim)
    #FOS = FOS(dim, inertia, y) ## change depending on what parameters u want to add in FOS function
    #SFD_BMD(L, n, P_train, x) 
    
    # pass precomputed graphs to avoid recomputing envelope each iteration
    FoS = prop(dim[0], dim[1], dim[2], L, n, P_train, x_train, dx, graphs=graphs)
    
    min_FOS = min(FoS)

    if min_FOS > best_min_FOS:
        best_min_FOS = min_FOS
        best_dimensions = dim

Load_Capacity = P * best_min_FOS
print("the best dimensions are:", best_dimensions)
print("the min FOS of this design is:", best_min_FOS)
print("the load capacity of this design is:", Load_Capacity)
