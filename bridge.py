from sectional_properties import prop
from fold_envelope import compute_envelope
from optimize import optimize

## Please consult the README file for variable definitions

#initalize values
L = 1260
n = 1260
dx = L/n
P = 400

x_train = [52, 228, 392, 568, 732, 908]
P_train = [P/6]*6

## MANUAL INPUTS

# number of layers for specific members
tf_thickness = 2
bf_thickness = 1
webbing_thickness = 1 


## CIV CALCULATIONS

#constants
E = 4000 #MPa
mu = 0.2

# Precompute expensive envelope once and reuse for all section checks
# compute_envelope returns (SFD_env, BMD_env)
graphs = compute_envelope(L, n, P_train, x_train, dx)

#optimize(400, webbing_thickness, 5, tf_thickness, bf_thickness, webbing_thickness, 10000, graphs)


#DESIGN 0 CALCULATIONS
#Note: comment out optimize() call above to run this section alone
#FoS, buckling_FOS = prop(75, 100, 80, 77.46, 400, 1.27, 1,27, graphs)
#print("Initial FOS values are:", FoS)
#print("Initial buckling FOS values are:", buckling_FOS)
#min_FOS = min(FoS)
#print("Initial min FOS is:", min_FOS)

tft = 1.27 * tf_thickness
bft = 1.27 * bf_thickness
t_web = 1.27 * webbing_thickness


FoS, buckling_FOS = prop(137, 110, 70, 50, 140, tft, bft, t_web, graphs=graphs,
)

#print("Initial FOS values are:", FoS)
#print("Initial buckling FOS values are:", buckling_FOS)
min_FOS = min(FoS)
print("Initial min FOS is:", min_FOS)
print("the load capacity of this design is:", P * min_FOS)
