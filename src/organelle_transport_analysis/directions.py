
def calculate_movement_directions(kymo, movement_threshold, time_threshold):
    left={};
    right={};
    stat={};
    reversals={};
    
    # Initialising result dictionary
    for track in kymo.keys():
        left[track] = [];
        right[track] = [];
        stat[track] = [];
        reversals[track] = [];
    
    # Helper to save track segments in the result dictionary
    def save_track(dictionary, track_name, start_index, end_index, x_array, t_array):
        if (end_index >= start_index):
            dictionary[track_name].append({'x': x_array[start_index:end_index+1], 
                                           'y': t_array[start_index:end_index+1]});
    
    # Helper to determine if the change between two points (index_p_1, index_p_2)
    # exceeds the thresholds given (tx, ty) 
    def determine_threshold_movement(x_array, y_array, index_p_1, index_p_2, tx, ty):
        slope = (y_array[index_p_2] - y_array[index_p_1]) / (x_array[index_p_2] - x_array[index_p_1])
        y = slope * (tx - x_array[index_p_1]) + y_array[index_p_1]
        return y >= ty
    
    # Helper to switch between dictionaries based on given state
    def get_dictionary_by_state(state, left_dict, right_dict, stat_dict):
        if state == 0:
            return stat_dict
        elif state == -1:
            return left_dict
        elif state == 1:
            return right_dict
    
    # ---- Main function - iterating over all tracks ----
    for track in kymo.keys():
        #print("====================================")
        #print("Starting track " + str(track) + "...")
        
        # Initialising internal variables
        x_array = kymo[track]['x'];
        y_array = kymo[track]['y'];
        x_count = len(x_array);
        
        index = 0

        mov_t = movement_threshold
        time_t = time_threshold

        current_state = 0
        current_state_start_index = 0
        
        track_reversals_stack = []

        # Iterating over track points
        while (index < x_count):
            
            # First outside index is used to track the last point outside 
            # the movement "window" 
            first_outside_index = index - 1
            found_index = False

            # Movement direction flags: left-to-right, right-to-left and stationary
            ltr = rtl = stationary = False
            
            # Iterate until possible direction change found
            while first_outside_index >= 0 and found_index != True:
                if x_array[first_outside_index] <= x_array[index] - mov_t:
                    # Possibly moving left-to-right
                    found_index = True
                    ltr = True
                if x_array[first_outside_index] >= x_array[index] + mov_t:
                    # Possibly moving right-to-left
                    found_index = True
                    rtl = True
                if y_array[first_outside_index] <= y_array[index] - time_t:
                    # Possibly stationary
                    found_index = True
                    stationary = True
                if found_index != True:
                    # No direction change found, shift the window
                    first_outside_index = first_outside_index - 1

            # Movement change can be flagged as both rtl or ltr AND stationary,
            # so to determine the new state we need to use the thresholds
            if rtl:
                if stationary:
                    is_moving = determine_threshold_movement(x_array, 
                                                             y_array, 
                                                             first_outside_index, 
                                                             first_outside_index + 1, 
                                                             x_array[index] + mov_t, 
                                                             y_array[index] - time_t)
                    if is_moving:
                        new_state = -1
                    else:
                        new_state = 0
                else:
                    new_state = -1
            elif ltr:
                if stationary:
                    is_moving = determine_threshold_movement(x_array, 
                                                             y_array, 
                                                             first_outside_index, 
                                                             first_outside_index + 1, 
                                                             x_array[index] - mov_t, 
                                                             y_array[index] - time_t)
                    if is_moving:
                        new_state = 1
                    else:
                        new_state = 0
                else:
                    new_state = 1
            elif stationary:
                new_state = 0

            if found_index and new_state != current_state:
                dict_to_save = get_dictionary_by_state(current_state, left, right, stat)
                
                # If state change was confirmed and we are not at the very start of the track,
                # record it in the corresponding dictionary
                if current_state_start_index != 0 or first_outside_index != 0:
                    save_track(dict_to_save, track, current_state_start_index, 
                               first_outside_index, x_array, y_array)
                    
                    # If switched from one movement state to another, record the reversal
                    if first_outside_index >= current_state_start_index:
                        track_reversals_stack.append(current_state)
                    
                current_state = new_state
                current_state_start_index = first_outside_index

            index = index + 1
        
        # Save the last track fragment once the track ends
        dict_to_save = get_dictionary_by_state(current_state, left, right, stat)
        save_track(dict_to_save, track, current_state_start_index, index, x_array, y_array)
        track_reversals_stack.append(current_state)
        
        # Count only the full movement reversals - changes such as ltr->stat->ltr do not count
        track_reversals = 0
        state_switch = 0
        for state in track_reversals_stack:
            if state != 0 and state != state_switch:
                if state_switch != 0:
                    track_reversals = track_reversals + 1
                state_switch = state
        
        reversals[track] = track_reversals
        
    return {'left': left, 'right': right, 'stat': stat, 'reversals': reversals}