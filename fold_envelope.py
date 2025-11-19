import numpy as np
from SB_calculations import SFD_BMD 

def compute_envelope(L, n, P_train, axle_positions, dx):
    """
    Compute the maximum shear force (SFD) and bending moment (BMD) envelopes
    for a moving train load along a simply supported bridge.
    
    L: bridge length
    n: number of divisions along the bridge
    P_train: list of axle loads
    axle_positions: list of distances of axles from train nose
    dx_step: step size for moving train (default 1 unit)
    """
    
    x = np.linspace(0, L, n+1)           # beam discretization
    SFD_max = np.zeros(n+1)               # initialize max shear envelope
    BMD_max = np.zeros(n+1)               # initialize max bending envelope
    
    # Move train from left of bridge to right
    x0_start = 0
    x0_end = L
    
    for x0 in np.arange(x0_start, x0_end + dx, dx):
        # Current axle positions
        x_loads = [x0 + xi for xi in axle_positions]
        P_loads = P_train
        
        # Only include axles on the bridge
        loads_on_bridge = [(xi, Pi) for xi, Pi in zip(x_loads, P_loads) if 0 <= xi <= L]
        if len(loads_on_bridge) == 0:
            continue
        
        graph = SFD_BMD(L, n, P_train, x0)
        
        # Update envelopes
        SFD_max = np.maximum(SFD_max, np.abs(graph[0]))
        BMD_max = np.maximum(BMD_max, np.abs(graph[1]))
    
    return SFD_max, BMD_max
