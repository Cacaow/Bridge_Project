from SB_calculations import SFD_BMD
from sectional_properties import prop
from fold_envelope import compute_envelope
import math

## VARIABLE NAMES


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
upper_flange_thickness = 2
lower_flange_thickness = 1
webbing_thickness = 1 

# how much each loop increments by (lower = more accurate)
upper_flange_step = 5
lower_flange_step = 5
distance_between_webbing_step = 5

# upper bounds of dimensions
upper_flange_bound = 150
lower_flange_bound = 150


## loop to create list of all viable dimensions, in mm

dimensions = []

for height in range(20-int((1.27*(upper_flange_thickness + lower_flange_thickness))), 150, 20):
    for lower_flange_length in range(60, lower_flange_bound, lower_flange_step):
        for upper_flange_length in range(100, upper_flange_bound, upper_flange_step):
            for distance_between_webbing in range(50,max(upper_flange_length+1,lower_flange_length+1), distance_between_webbing_step):
                total_diaphragm_area = 813 * 1016 - 1250 * (upper_flange_length * upper_flange_thickness + lower_flange_length * lower_flange_thickness + 2*height*webbing_thickness)
                if total_diaphragm_area > 0:
                    diaphragm_spacing = 1250/(total_diaphragm_area / (distance_between_webbing * height))
                    dimension = [height, upper_flange_length, lower_flange_length, distance_between_webbing, diaphragm_spacing, total_diaphragm_area]
                    dimensions.append(dimension)



## CIV CALCULATIONS

#constants (i think were missing some if u guys can add it)
E = 4000 #MPa
mu = 0.2
sigma_t = 30 #MPa
sigma_c = 6 #MPa
tau_m = 4 #MPa 
tau_g = 2 #MPa


upper_flange_height = 1.27 * upper_flange_thickness
lower_flange_height = 1.27 * lower_flange_thickness
webbing_width = 1.27 * webbing_thickness

## FINDING OPTIMAL DESIGN (loop)

best_min_FOS = 0
best_dimensions = []

# Precompute expensive envelope once and reuse for all section checks
# compute_envelope returns (x, SFD_env, BMD_env)
graphs = compute_envelope(L, n, P_train, x_train, dx)
#FoS, buckling_FOS = prop(75, 100, 80, 77.46, 400, graphs=graphs)
#print("Initial FOS values are:", FoS)
#print("Initial buckling FOS values are:", buckling_FOS)
#min_FOS = min(FoS)
#print("Initial min FOS is:", min_FOS)

for dim in dimensions: 
    # correct unpacking: ybar, inertia
    #ybar, inertia = y_bar_and_I(dim)
    #FOS = FOS(dim, inertia, y) ## change depending on what parameters u want to add in FOS function
    #SFD_BMD(L, n, P_train, x) 
    
    # pass precomputed graphs to avoid recomputing envelope each iteration
    FoS, buckling_FOS = prop(dim[0], dim[1], dim[2], dim[3], dim[4], graphs=graphs)
    
    min_FOS = min(FoS)

    if min_FOS > best_min_FOS:
        min_FOS = min(FoS)
        best_min_FOS = min_FOS
        best_dimensions = dim
        best_buckling_FOS = buckling_FOS
        diaphragm_remaining = dim[5]

Load_Capacity = P * best_min_FOS
print("the best dimensions are:", best_dimensions)
print("the min FOS of this design is:", best_min_FOS)
print("the load capacity of this design is:", Load_Capacity)
print("FOS values are:", FoS)
#print("diaphragm area leftover", diaphragm_remaining)
#print("the buckling FOS values are:", best_buckling_FOS)