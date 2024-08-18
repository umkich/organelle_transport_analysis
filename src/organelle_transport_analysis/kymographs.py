import csv

# Function to read data from the excel file in a specific format
def get_kymo(input_file_name, head_distances={}):
    kymo = {}

    with open(input_file_name, 'r') as file:
        csvreader = csv.reader(file)
        index = -1
        for row in csvreader:
            if index == -1:
                for i in range(0, len(row) // 2):
                    kymo[i] = {}
                    kymo[i]['type'] = 'polyline'
                    kymo[i]['width'] = 0
                    kymo[i]['position'] = 0
                    kymo[i]['y'] = [] # Timeframe
                    kymo[i]['x'] = [] # Position
                    if str(row[i * 2]).split('_')[0] in head_distances:
                        kymo[i]['distance_to_head'] = head_distances[str(row[i * 2]).split('_')[0]]
                    else:
                        kymo[i]['distance_to_head'] = -1
            else:
                track_index = 0
                for column in row:
                    if column != '':
                        if track_index % 2 == 0:
                            kymo[track_index // 2]['y'].append(float(column))
                        else:
                            kymo[track_index // 2]['x'].append(float(column))
                    track_index = track_index + 1
            index = index + 1
    return kymo

def get_kymo_by_distance(kymo, distance_from, distance_to):
    result = {}
    for track in kymo.keys():
        if kymo[track]['distance_to_head'] >= distance_from and kymo[track]['distance_to_head'] < distance_to:
            result[track] = kymo[track]
    return result

## Removing values with different positions for the same timeframe by finding the average
def remove_duplicates(kymo):
    
    # Iterate over tracks
    for track in kymo.keys():
        
        sum_of_repeats = 0
        number_of_repeats = 0
        index_to_insert = 0
        length = len(kymo[track]['y'])
        
        # Iterate over points in the track
        for j in range(0, length):
            
            if j < length-1 and kymo[track]['y'][j] == kymo[track]['y'][j+1]:
                # If current and next point have the same timeframe value (y),
                # record it and sum the positions
                number_of_repeats = number_of_repeats + 1
                sum_of_repeats = sum_of_repeats + kymo[track]['x'][j]
            else:
                # If current and next point have different timeframe values (y),
                # and if any repeats were recorded, calculate the average position
                # and record it
                if number_of_repeats > 0:
                    kymo[track]['y'][index_to_insert] = kymo[track]['y'][j]
                    kymo[track]['x'][index_to_insert] = ((sum_of_repeats + kymo[track]['x'][j]) 
                                                         / (number_of_repeats + 1))
                    sum_of_repeats = 0
                    number_of_repeats = 0
                else:
                    kymo[track]['y'][index_to_insert] = kymo[track]['y'][j]
                    kymo[track]['x'][index_to_insert] = kymo[track]['x'][j]
                index_to_insert = index_to_insert + 1
        
        # Update the track points' arrays
        kymo[track]['y'] = kymo[track]['y'][:index_to_insert]
        kymo[track]['x'] = kymo[track]['x'][:index_to_insert]
    return kymo

def adjust_units(kymo, distance_coefficient, time_coefficient):
    for track in kymo.keys():
        kymo[track]['x'] = [value * distance_coefficient for value in kymo[track]['x']]
        kymo[track]['y'] = [value * time_coefficient for value in kymo[track]['y']]
    return kymo