from fold_envelope import compute_envelope 
import math
import numpy as np

tft = 1.27 * 1
bft = 1.27 
t_web = 1.27 * 1
#a_web = 20
E = 4000
mu = 0.2
S_tens = 30
S_comp = 6
T_max = 4
T_gmax = 2

def prop(h_web, tfw, bfw, d_web, graphs=None):
    """Compute factors of safety for a section.

    `graphs`, if provided, should be the tuple returned by
    `compute_envelope` -> `(x, SFD_env, BMD_env)` so the heavy envelope
    calculation can be performed once and reused across many calls.
    """
    A_top = tfw * tft
    A_bottom = bfw * bft
    A_web = 2 * (h_web * t_web)
    A_total = A_top + A_bottom + A_web

    y_top = h_web + bft + tft/2
    y_bot = bft/2
    y_web = bft + h_web/2

    ybar = (A_top * y_top + A_bottom * y_bot + A_web * y_web) / A_total

    I_top = (tfw * tft**3 / 12) + (A_top * (y_top - ybar)**2)
    I_bottom = (bfw * bft**3 / 12) + (A_bottom * (y_bot - ybar)**2)
    I_web = 2 * ((t_web * h_web**3 / 12) + (A_web/2 * (y_web - ybar)**2))
    I_total = I_top + I_bottom + I_web
    print("Moment of Inertia is:", I_total)

    #Q at centroid
    y_glue_top = bft + h_web
    Q_web = (h_web + tft - ybar) * t_web * (h_web + tft - ybar)
    Q_cent = A_top * (y_top - ybar) + Q_web

    #Stress calculations
    SFD_env, BMD_env = graphs
    S_top = abs(BMD_env) * (tft + h_web + bft - ybar) / I_total
    S_bot = abs(BMD_env) * ybar / I_total
    T_cent = abs(SFD_env) * Q_cent / (I_total * t_web * 2)
    T_glue = abs(SFD_env) * A_top * (y_top - ybar) / (I_total * t_web * 2)

    #Thin Plate 
    #case 1: Compresion in the top flange
    k1 = 4
    #strange calculation??
    b1 = tfw - (tfw - bfw) - (t_web/2 * 2)
    S_b1 = (k1 * math.pi**2 * E) / (12 * (1 - mu**2)) * (tft / b1)**2

    #case 2: Compression in the bottom flange
    k2 = 0.425
    b2 = (tfw - d_web - t_web * 2) / 2
    S_b2 = (k2 * math.pi**2 * E) / (12 * (1 - mu**2)) * (tft / b2)**2

    #case 3: Buckling in web
    k3 = 6
    b3 = t_web
    t3 = (h_web + bft - ybar)
    S_b3 = (k3 * math.pi**2 * E) / (12 * (1 - mu**2)) * (h_web / t_web)**2

    #case 4: Shear in web
    k_shear = 5
    T_b = (k_shear * math.pi**2 * E) / (12 * (1 - mu**2)) * ((t_web / h_web)**2 + (t_web/d_web)**2)


    #FOS
    FOS_tens = S_tens / max(S_bot)
    FOS_comp = S_comp / max(S_top)
    FOS_shear = T_max / max(T_cent)
    FOS_glue = T_gmax / max(T_glue)
    FOS_buckling1 = S_b1 / max(S_top)
    FOS_buckling2 = S_b2 / max(S_bot)
    FOS_buckling3 = S_b3 / max(S_top)
    FOS_buckling4 = T_b / max(T_cent)
    
    FOS = [FOS_tens, FOS_comp, FOS_shear, FOS_glue, FOS_buckling1, FOS_buckling2, FOS_buckling3, FOS_buckling4]
    Pfail = []
    """
    for j in FOS:
        Pfails = P_train * 6 * j
        Pfail.append(Pfails)
    """
    #Vfail and Mfail
    Mf_tens = FOS[0] * np.abs(BMD_env)
    Mf_comps = FOS[1] * np.abs(BMD_env)

    Vf_shear = FOS[2] * np.abs(SFD_env)

    Mf_buckling1 = FOS[3] * np.abs(BMD_env)
    Mf_buckling2 = FOS[4] * np.abs(BMD_env)
    Mf_buckling3 = FOS[5] * np.abs(BMD_env)
    Vf_buckling4 = FOS[6] * np.abs(SFD_env)

    buckle = [Mf_buckling1, Mf_buckling2, Mf_buckling3, Vf_buckling4]

    return FOS, buckle





