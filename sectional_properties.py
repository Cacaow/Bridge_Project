from fold_envelope import compute_envelope 
import math
import numpy as np

t_glue = 1.27
w_glue = 5
E = 4000
mu = 0.2
S_tens = 30
S_comp = 6
T_max = 4
T_gmax = 2

def prop(h_web, tfw, bfw, d_web, a_web, tft, bft, t_web, graphs=None):
    """Compute factors of safety for a section.

    `graphs`, if provided, should be the tuple returned by
    `compute_envelope` -> `(x, SFD_env, BMD_env)` so the heavy envelope
    calculation can be performed once and reused across many calls.
    """
    # Area calculations
    A_top = tfw * tft                       # Area of top flange
    A_bottom = bfw * bft                    # Area of bottom flange
    A_web = 2 * ((h_web - bft - t_glue) * t_web)             # Area of both webs
    A_glue = 2 * w_glue * t_glue            # Area of glue tabs
    A_total = A_top + A_bottom + A_web + A_glue      # Total area

    # Centroid calculations
    y_top = h_web + bft + tft/2             # Centroid location of top flange
    y_bot = bft/2                           # Centroid location of bottom flange
    y_web = bft + h_web/2                   # Centroid location of webs
    y_glue = bft + h_web - t_glue/2         # Centroid location of glue tabs

    ybar = (A_top * y_top + A_bottom * y_bot + A_web * y_web + A_glue * y_glue) / A_total   # Centroidal axis location

    # Second moment of area calculations
    I_top = (tfw * tft**3 / 12) + (A_top * (y_top - ybar)**2)   # Second moment of area of top flange
    I_bottom = (bfw * bft**3 / 12) + (A_bottom * (y_bot - ybar)**2) # Second moment of area of bottom flange
    I_web = 2 * ((t_web * (h_web - bft - t_glue)**3 / 12) + (A_web/2 * (y_web - ybar)**2))   # Second moment of area of both webs
    I_glue = 2 * ((w_glue * t_glue**3 / 12) + (A_glue/2 * (y_glue - ybar)**2)) # Second moment of area of glue tabs
    I_total = I_top + I_bottom + I_web + I_glue    # Total second moment of area

    #Q at centroid
    Q_cent = A_bottom*(ybar- bft/2) + (t_web*(ybar - bft))*((ybar - bft)/2)*2

    #Stress calculations
    SFD_env, BMD_env = graphs
    S_top = abs(BMD_env) * (tft + h_web + bft - ybar) / I_total
    S_bot = abs(BMD_env) * ybar / I_total
    T_cent = abs(SFD_env) * Q_cent / (I_total * t_web * 2)
    T_glue = abs(SFD_env) * A_top * (y_top - ybar) / (I_total * t_web * 2)

    #Thin Plate Buckling Calculations

    ### Top Flange Buckling ###
    #case 1: Compresion in the top flange between the webs
    k1 = 4
    t1 = tft
    b1 = d_web
    S_b1 = (k1 * math.pi**2 * E) / (12 * (1 - mu**2)) * (t1 / b1)**2

    #case 2: Compression in the tips of the top flange
    k2 = 0.425
    t2 = tft
    b2 = (tfw - d_web - 2 * t_web) / 2
    S_b2 = (k2 * math.pi**2 * E) / (12 * (1 - mu**2)) * (t2 / b2)**2

    #case 3: Buckling in webs due to flexural stress
    k3 = 6
    t3 = t_web
    b3 = bft + h_web - ybar
    S_b3 = (k3 * math.pi**2 * E) / (12 * (1 - mu**2)) * (t3 / b3)**2

    #case 4: Shear stress in the diaphrams/webs
    k_shear = 5
    tV = t_web
    hV = h_web
    aV = a_web
    T_b = (k_shear * math.pi**2 * E) / (12 * (1 - mu**2)) * ((tV / hV)**2 + (tV / aV)**2)

    #FOS
    FOS_tens = S_tens / max(S_bot)
    FOS_comp = S_comp / max(S_top)
    FOS_shear = T_max / max(T_cent)
    FOS_glue = T_gmax / max(T_glue)
    FOS_buckling1 = S_b1 / max(S_top)
    FOS_buckling2 = S_b2 / max(S_bot)
    FOS_buckling3 = S_b3 / max(S_top)
    FOS_buckling4 = T_b / max(T_cent)

    FOS_glue = 10000000

    FOS = [FOS_tens, FOS_comp, FOS_shear, FOS_glue, FOS_buckling1, FOS_buckling2, FOS_buckling3, FOS_buckling4]
    
    #Vfail and Mfail
    Mf_tens = FOS[0] * np.abs(BMD_env)
    Mf_comps = FOS[1] * np.abs(BMD_env)

    Vf_shear = FOS[2] * np.abs(SFD_env)

    Mf_buckling1 = FOS[4] * np.abs(BMD_env)
    Mf_buckling2 = FOS[5] * np.abs(BMD_env)
    Mf_buckling3 = FOS[6] * np.abs(BMD_env)
    Vf_buckling4 = FOS[7] * np.abs(SFD_env)

    buckle = [Mf_buckling1, Mf_buckling2, Mf_buckling3, Vf_buckling4]

    return FOS, buckle





