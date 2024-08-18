def calculate_velocities(directions): 
    
    # Separate function to reuse for each direction
    def velocities_for_direction(movements):
        velocities = {}
        
        # Iterate over each track
        for track in movements.keys():            
            velocities[track] = []
            
            # Iterate over each segment
            for index, segment in enumerate(movements[track]):
                
                # Only considering segments > 3 elements
                segment_length = len(segment['x'])
                if segment_length > 3:
                    
                    # Calculate velocity for this segment
                    delta_distance = segment['x'][segment_length - 1] - segment['x'][0]
                    delta_time = segment['y'][segment_length - 1] - segment['y'][0]
                    velocity = delta_distance / delta_time
                    
                    velocities[track].append(velocity)

        return velocities
    
    left_velocities = velocities_for_direction(directions['left'])
    right_velocities = velocities_for_direction(directions['right'])
    return {'left': left_velocities, 'right': right_velocities}

def combine_velocities(velocities, min_velocity):
    velocity_lists_left = [velocities['left'][track] for track in velocities['left'].keys() if len(velocities['left'][track]) > 0]
    combined_velocities_left = [item for sublist in velocity_lists_left for item in sublist]
    combined_velocities_left = [item for item in combined_velocities_left if item < -min_velocity]

    velocity_lists_right = [velocities['right'][track] for track in velocities['right'].keys() if len(velocities['right'][track]) > 0]
    combined_velocities_right = [item for sublist in velocity_lists_right for item in sublist]
    combined_velocities_right = [item for item in combined_velocities_right if item > min_velocity]
    return combined_velocities_left, combined_velocities_right