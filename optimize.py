from sectional_properties import prop

# how much each loop increments by (lower = more accurate)
tf_step = 5
bf_step = 5
distance_between_webbing_step = 5

# upper bounds of dimensions
tf_bound = 150
bf_bound = 100

def optimize(P, t_web, distance_between_webbing_step, tf_thickness, bf_thickness, webbing_thickness, scrap, graphs):
    ## loop to create list of all viable dimensions, in mm
    dimensions = []

    ## FINDING OPTIMAL DESIGN (loop)
    best_min_FOS = 0
    best_dimensions = []
    tf_height = 1.27 * tf_thickness
    bf_height = 1.27 * bf_thickness
    webbing_width = 1.27 * webbing_thickness

    for height in range(20-int((tf_height + bf_height) + 10), 150, 20):
        for bf_length in range(60, bf_bound, bf_step):
            for tf_length in range(100, tf_bound, tf_step):
                for distance_between_webbing in range(50,max(tf_length+1,bf_length+1), distance_between_webbing_step):
                    total_diaphragm_area = 813 * 1016 - 1260 * (tf_length * tf_thickness + bf_length * bf_thickness + 2*height*t_web)
                    if total_diaphragm_area > 2 * distance_between_webbing * height + scrap:
                        diaphragm_spacing = 1260/((total_diaphragm_area-scrap) // (distance_between_webbing * height))
                        dimension = [height, tf_length, bf_length, distance_between_webbing, diaphragm_spacing, total_diaphragm_area]
                        dimensions.append(dimension)
    for dim in dimensions: 
        
        # pass precomputed graphs to avoid recomputing envelope each iteration
        FoS, buckling_FOS = prop(dim[0] - 10 , dim[1], dim[2], dim[3], dim[4], tf_height, bf_height, webbing_width, graphs=graphs)
        
        min_FOS = min(FoS)

        if min_FOS > best_min_FOS:
            Factors_of_Safety = FoS
            best_min_FOS = min_FOS
            best_dimensions = dim
            best_buckling_FOS = buckling_FOS
            diaphragm_remaining = dim[5]
        

    Load_Capacity = P * best_min_FOS
    print("the best dimensions are:", best_dimensions)
    print("the min FOS of this design is:", best_min_FOS)
    print("the load capacity of this design is:", Load_Capacity)
    print("FOS values are:", Factors_of_Safety)
    print("diaphragm area leftover", diaphragm_remaining)
    print("the buckling FOS values are:", best_buckling_FOS)