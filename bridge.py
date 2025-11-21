from SB_calculations import SFD_BMD
from sectional_properties import prop
from fold_envelope import compute_envelope
from optimize import optimize

## Please consult the README file for variable definitions

#initalize values
L = 1260
n = 1260
dx = L/n
#x = [i*dx for i in range(n)]
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

tf_height = 1.27 * tf_thickness
bf_height = 1.27 * bf_thickness
webbing_width = 1.27 * webbing_thickness

# Precompute expensive envelope once and reuse for all section checks
# compute_envelope returns (x, SFD_env, BMD_env)
graphs = compute_envelope(L, n, P_train, x_train, dx)

optimize(400, tf_thickness, bf_thickness, webbing_thickness, 5, tf_height, bf_height, webbing_width, graphs)
#FoS, buckling_FOS = prop(75, 100, 80, 77.46, 400, graphs=graphs)
#print("Initial FOS values are:", FoS)
#print("Initial buckling FOS values are:", buckling_FOS)
#min_FOS = min(FoS)
#print("Initial min FOS is:", min_FOS)

