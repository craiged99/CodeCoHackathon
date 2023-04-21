import numpy as np
import math


#Add a columns for key passes, progressive passes, and prgressive carries into the dataset

#Input the original StatsBomb dataset (e.g.'ManCity Hackathon Json Files/ManCity_Arsenal_events.json')
    
def add_col(X):
    
    player_pass = X.copy()
    
    player_pass['pass'].replace('', np.nan, inplace=True)
    player_pass.dropna(subset=['pass'], inplace=True)
            
    
    
    pass_data_array = np.array(player_pass[['pass']])
    pos = np.array(player_pass[['location']])
    
    big_dict = {}
    successful = 0
    long = 0
    short_suc = 0
    long_suc = 0
    prog_pass = 0
    prog_suc = 0
    
    prog_passes_index = []
    
    for i in range(len(pass_data_array)):
        
        little_dict = {}
        
        ID = player_pass.iloc[i]['id']
        
         
        try:
            little_dict['recipient'] = pass_data_array[i][0]['recipient']['name']
        except:
            pass
        
        
        try:
            x = pass_data_array[i][0]['outcome']['name']
            little_dict['outcome'] = 'Fail'
        except:
            little_dict['outcome'] = 'Clear'
            successful = successful + 1
            
        
        little_dict['length'] = pass_data_array[i][0]['length']
        if pass_data_array[i][0]['length'] < 27:
            little_dict['pass_type'] = 'short'
            
            if little_dict['outcome'] == 'Clear':
                short_suc = short_suc + 1
            
        else:
            little_dict['pass_type'] = 'long'
            long = long+1
            
            if little_dict['outcome'] == 'Clear':
                long_suc = long_suc + 1
            
                
            
        little_dict['angle'] = pass_data_array[i][0]['angle']
        
        
        little_dict['start_x'] = pos[i][0][0]
        little_dict['start_y'] = pos[i][0][1]
        
        little_dict['end_x'] = pass_data_array[i][0]['end_location'][0]
        little_dict['eny_y'] = pass_data_array[i][0]['end_location'][1]
         
         
        #little_dict['body_part'] = pass_data_array[i][0]['body_part']['name']
    
        little_dict['minute'] = player_pass.iloc[i]['minute']
        little_dict['play_pattern'] = player_pass.iloc[i]['play_pattern']
        
        
        
        
        #Progressive Passes
        if abs(pass_data_array[i][0]['angle']) < 1.5708 and math.cos(abs(pass_data_array[i][0]['angle']))*pass_data_array[i][0]['length'] > 15 and pos[i][0][0] > 48:
            little_dict['progressive pass'] = 'True'
            
            prog_pass = prog_pass + 1
            row_index_prog = player_pass.iloc[i]['index']-1
            
            prog_passes_index.append(row_index_prog)
            
            
            
            
            if little_dict['outcome'] == 'Clear':
                prog_suc = prog_suc + 1
            
        
        else:
            little_dict['progressive pass'] = 'False'
        
        
         
        big_dict[ID] = little_dict
        
       
    player_shots = X.copy()   
       
    player_shots['shot'].replace('', np.nan, inplace=True)
    player_shots.dropna(subset=['shot'], inplace=True)
    
    
    shots_in_match = np.array(player_shots[['shot']])
    
    
    #Key_passes / xA
    assists = 0
    xa = 0
    key_pass = 0
    key_pass_index = []
    
    for i in range(len(shots_in_match)):
        try:
            assist_id = shots_in_match[i][0]['key_pass_id']
            player_assist = X[np.isin(X['id'], assist_id)]['player'].values[0]['name']
        
            key_pass = key_pass + 1
            
            big_dict[assist_id]['key_pass'] = 'True'
            big_dict[assist_id]['xA'] = shots_in_match[i][0]['statsbomb_xg']
            
            row_index = X[np.isin(X['id'], assist_id)].index[0]
            
            key_pass_index.append(row_index)
            
            
            if shots_in_match[i][0]['outcome']['name'] == 'Goal':
                big_dict[assist_id]['assist'] = 'True'
                assists=assists+1
            
            else:
                big_dict[assist_id]['assist'] = 'False'
                
                
                
        except:
            pass
        
    X.loc[key_pass_index, 'key_pass'] = True
    X.loc[prog_passes_index, 'prog_pass'] = True
    
    
    
    player_carries = X.copy()
    
    player_carries['carry'].replace('', np.nan, inplace=True)
    player_carries.dropna(subset=['carry'], inplace=True)
    
    
        
    
    carry_data_array = np.array(player_carries[['carry']])
    pos = np.array(player_carries[['location']])
    
    big_dict = {}
    
    total_distance = 0
    prog_carry = 0
    
    prog_carry_index = []
    
    for i in range(len(pos)):
        
        ID = player_carries.iloc[i]['id']
        
        little_dict = {}
    
    
        little_dict['start_x'] = pos[i][0][0]
        little_dict['start_y'] = pos[i][0][1]
        
        
        little_dict['end_x'] = carry_data_array[0][0]['end_location'][0]
        little_dict['end_y'] = carry_data_array[0][0]['end_location'][1]
        
        distance = np.sqrt((abs(carry_data_array[0][0]['end_location'][0]-pos[i][0][0])**2) + 
                           (abs(carry_data_array[0][0]['end_location'][1]-pos[i][0][1])**2))
        
        if carry_data_array[i][0]['end_location'][0]-pos[i][0][0] >= 5.5 and pos[i][0][0] >48:
            prog_carry = prog_carry+1
            
            row_index_prog_car = player_carries.iloc[i]['index']-1
            
            prog_carry_index.append(row_index_prog_car)
        
        little_dict['distance'] = distance
        
        total_distance = total_distance + distance
        
        big_dict[ID] = little_dict
        
    
    X.loc[prog_carry_index, 'prog_carry'] = True
    
    return X
    
    
    
    
    
    
    
    
    
    
