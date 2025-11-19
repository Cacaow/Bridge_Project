import numpy as np
import matplotlib.pyplot as plt

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
    x0_end   = L

    for x0 in np.arange(x0_start, x0_end + dx_step, dx_step):

        # Compute axle locations for current train position
        x_loads = []
        P_loads = []

        for i in range(len(axle_positions)):
            xi = x0 + axle_positions[i]
            if 0 <= xi <= L:
                x_loads.append(xi)
                P_loads.append(P_train[i])

        num_loads = len(x_loads)
        if num_loads == 0:
            continue   # no active loads → skip

        # Convert to numpy arrays
        x_loads = np.array(x_loads)
        P_loads = np.array(P_loads)

        # Compute reactions: simply supported
        total_load = 0.0
        moment_sum = 0.0
        for i in range(num_loads):
            total_load += P_loads[i]
            moment_sum += P_loads[i] * x_loads[i]

        RB = moment_sum / L
        RA = total_load - RB

        # Compute SFD + BMD for this train position
        SFD = np.zeros(n+1)
        BMD = np.zeros(n+1)

        for i in range(len(x)):
            xi = x[i]

            # Start with left reaction
            S = RA

            # Subtract axle loads to the left of point xi
            for j in range(num_loads):
                if xi >= x_loads[j]:
                    S -= P_loads[j]

            SFD[i] = S

            # Integrate shear to get bending moment
            if i == 0:
                BMD[i] = 0
            else:
                dx = x[i] - x[i-1]
                BMD[i] = BMD[i-1] + SFD[i-1] * dx

        # Update envelopes
        for i in range(n+1):
            if abs(SFD[i]) > SFD_max[i]:
                SFD_max[i] = abs(SFD[i])
            if abs(BMD[i]) > BMD_max[i]:
                BMD_max[i] = abs(BMD[i])

    return x, SFD_max, BMD_max


# ----- Example usage -----
"""
L = 1200
n = 1200
P = 400

axles = [52, 228, 392, 568, 732, 908]

x, SFD_env, BMD_env = compute_envelope(L, n, P_train, axles)

# Plot results
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(x, SFD_env)
plt.title("Shear Force Envelope")
plt.grid()

plt.subplot(1,2,2)
plt.plot(x, BMD_env)
plt.title("Bending Moment Envelope")
plt.grid()

plt.show()
"""