import numpy as np

def SFD_BMD(L, n, P_train, x0):
    """
    Compute Shear Force Diagram (SFD) and Bending Moment Diagram (BMD)
    for a bridge with a moving train load.
    
    L: bridge length (m)
    n: number of divisions
    P_train: array of axle loads [kN]
    x0: position of first axle (m)
    P: total load magnitude (for reaction calculation, optional)
    """
    
    # Beam discretization
    x = np.linspace(0, L, n+1)
    
    # Axle positions
    x_loads = [x0, x0+176, x0+340, x0+516, x0+680, x0+856]
    
    # Only consider loads on the bridge
    x_loads = [xi for xi in x_loads if xi <= L]
    P_loads = P_train[:len(x_loads)]  # make sure same length
    
    # Compute reactions (simply assuming simply supported)
    total_load = sum(P_loads)
    RA = total_load * (L - np.mean(x_loads)) / L
    RB = total_load - RA
    
    # Initialize arrays
    SFD = np.zeros(len(x))
    BMD = np.zeros(len(x))
    
    # Compute Shear Force and Bending Moment
    for i in range(len(x)):
        xi = x[i]
        S = RA  # left reaction
        # subtract loads to the left of xi
        for j in range(len(x_loads)):
            if xi >= x_loads[j]:
                S -= P_loads[j]
        SFD[i] = S
        
        # compute Bending Moment using trapezoidal integration
        if i == 0:
            BMD[i] = 0
        else:
            dx = x[i] - x[i-1]
            BMD[i] = BMD[i-1] + SFD[i-1] * dx
    
    return SFD, BMD