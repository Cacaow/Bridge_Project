import math

# --------------------------
# Load envelope function
# --------------------------
def computeLoadEnvelopes(L, n, x_train, P_train):
    """
    Computes shear force (SFD) and bending moment (BMD) envelopes
    for a simply supported beam of length L.
    Returns:
        SFDmax : list of max absolute shear force at each division (length n+1)
        BMDmax : list of max absolute bending moment at each division (length n+1)
    """
    x = [float(L) * i / float(n) for i in range(n + 1)]
    SFDmax = [0.0] * (n + 1)
    BMDmax = [0.0] * (n + 1)
    x0_start = -max(x_train)
    x0_end = float(L)
    n_train = int(math.floor(x0_end - x0_start)) + 1

    for i in range(n_train):
        x0 = x0_start + float(i)
        x_load = [x0 + float(xp) for xp in x_train]

        sumP = 0.0
        sumPx = 0.0
        for k in range(len(x_load)):
            xl = x_load[k]
            if 0.0 <= xl <= L:
                sumP += float(P_train[k])
                sumPx += float(P_train[k]) * xl

        if sumP > 0.0:
            RB = sumPx / float(L)
            RA = sumP - RB
        else:
            RA = 0.0
            RB = 0.0

        w = [0.0] * (n + 1)
        w[0] = float(RA)
        w[-1] += float(RB)

        for k in range(len(x_load)):
            xl = x_load[k]
            if 0.0 <= xl <= L:
                closest_idx = 0
                min_dist = abs(x[0] - xl)
                for j in range(1, n + 1):
                    d = abs(x[j] - xl)
                    if d < min_dist:
                        min_dist = d
                        closest_idx = j
                w[closest_idx] -= float(P_train[k])

        SF = [0.0] * (n + 1)
        SF[0] = float(w[0])
        for j in range(1, n + 1):
            SF[j] = SF[j - 1] + float(w[j])

        BM = [0.0] * (n + 1)
        for j in range(1, n + 1):
            dx = x[j] - x[j - 1]
            BM[j] = BM[j - 1] + 0.5 * dx * (SF[j] + SF[j - 1])

        for j in range(n + 1):
            SFDmax[j] = max(SFDmax[j], abs(SF[j]))
            BMDmax[j] = max(BMDmax[j], abs(BM[j]))

    return SFDmax, BMDmax
