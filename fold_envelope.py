import numpy as np
from SB_calculations import SFD_BMD 

def compute_envelope(L, n, P_train, axle_positions, dx_step=1):
    """
    Compute shear force and bending moment envelopes for a train
    moving across a simply supported bridge — NO zip() used.
    """

    x = np.linspace(0, L, n+1)
    SFD_max = np.zeros(n+1)
    BMD_max = np.zeros(n+1)

    # Train moves from left of the bridge to the far right
    x0_start = -max(axle_positions)
    x0_end = L

    for x0 in np.arange(x0_start, x0_end + dx_step, dx_step):

        # Compute axle locations for current train position
        x_loads = []

        for i in range(len(axle_positions)):
            xi = x0 + axle_positions[i]
            if 0 <= xi <= L:
                x_loads.append(xi)

        num_loads = len(x_loads)
        if num_loads == 0:
            continue   # no active loads → skip

        # Convert to numpy arrays
        x_loads = np.array(x_loads)
        P_loads = np.array(P_train)

        SFD, BMD = SFD_BMD(L, n, P_loads, x0)

        # Update envelopes
        for i in range(n+1):
            if abs(SFD[i]) > SFD_max[i]:
                SFD_max[i] = abs(SFD[i])
            if abs(BMD[i]) > BMD_max[i]:
                BMD_max[i] = abs(BMD[i])
    """
    # Plot results
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.plot(x, SFD_max)
    plt.title("Shear Force Envelope")
    plt.grid()

    plt.subplot(1,2,2)
    plt.plot(x, BMD_max)
    plt.title("Bending Moment Envelope")
    plt.grid()

    plt.show()
    """
    return SFD_max, BMD_max


# ----- Example usage -----



