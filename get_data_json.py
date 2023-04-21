from statsbombpy import sb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch, VerticalPitch
from scipy.ndimage import gaussian_filter
import seaborn as sns
import math

'''
Get the raw data for each player for a certain time in a game. This data is used later
to look for anomlies etc.

Some data is basic, other data (key_passes, etc) have been manually coded into the data
generation

All this data is compiled in the 'game_all_data' function at the bottom.
'''

#Get player heatmap

def player_heatmap(player,match,X):
    
    pitch = VerticalPitch()

    
    player_pos = np.array(X[['location']])
    
    
    Xdata = []
    Ydata = []
    
    
    for i in range(len(player_pos)):
        
        try:
            Xdata.append(player_pos[i][0][0])
            Ydata.append(player_pos[i][0][1])
        except:
            pass
        
        #plt.plot(player_pos[i][0][0],80-player_pos[i][0][1],marker='x',color='red')
    
    
    
    stats = pitch.bin_statistic(Xdata, Ydata,bins=(20, 20))
    stats['statistic'] = gaussian_filter(stats['statistic'], 1)
    
    return stats

#Get shooting data
    
def player_shots(player,match,X):
    

    player_shots = X.copy()
    
    player_shots['shot'].replace('', np.nan, inplace=True)
    player_shots.dropna(subset=['shot'], inplace=True)
    
    
        
    length = len(player_shots)-1
    
    for i in range(len(player_shots)):
        
        I = length - i
        
        index_val = player_shots.index[I]
        
        player_name = player_shots.iloc[I]['player']['name']
        
        if player_name != player:
            player_shots = player_shots.drop(index=index_val)
            


    
    shot_data_array = np.array(player_shots[['shot']])
    pos = np.array(player_shots[['location']])
     
    

    
    big_dict = {}
    on_target = 0
    goals = 0
    total_xg = 0
    
    for i in range(len(pos)):
        
        little_dict = {}
        
        ID = player_shots.iloc[i]['id']

        try:
            assist = shot_data_array[i][0]['key_pass_id']
            player_assist = X[np.isin(X['id'], assist)]['player'].values[0]
            little_dict['shot_assist'] = player_assist
        except:
            pass
         
        little_dict['start_x'] = pos[i][0][0]
        little_dict['start_y'] = pos[i][0][1]
        
        little_dict['end_x'] = shot_data_array[i][0]['end_location'][0]
        little_dict['eny_y'] = shot_data_array[i][0]['end_location'][1]
         
        little_dict['xg'] = shot_data_array[i][0]['statsbomb_xg']
        total_xg = total_xg + shot_data_array[i][0]['statsbomb_xg']
         
        little_dict['body_part'] = shot_data_array[i][0]['body_part']['name']
        little_dict['outcome'] = shot_data_array[i][0]['outcome']['name']
        
        little_dict['minute'] = player_shots.iloc[i]['minute']
        little_dict['play_pattern'] = player_shots.iloc[i]['play_pattern']
        
        if little_dict['outcome'] == 'Saved' or little_dict['outcome'] == 'Saved Off T' or little_dict['outcome'] == 'Saved To Post':
            on_target = on_target+1
            
        if little_dict['outcome'] == 'Goal':
            goals = goals+1
            little_dict['goal'] = 'True'
            
        else:
            little_dict['goal'] = 'False'
         
        big_dict[ID] = little_dict


    no_of_shots = len(shot_data_array)
    
    
    
    
    overall_data = {'number_shots':no_of_shots,'shots_on_target':on_target,
                    'goals':goals,'total_xg':total_xg
                    }
    
    big_dict['overall'] = overall_data
        

    return big_dict


#Get passing data - including key passes and progressive passes

def player_pass_data(player,match,X):
    

    player_pass = X.copy()
    
    player_pass['pass'].replace('', np.nan, inplace=True)
    player_pass.dropna(subset=['pass'], inplace=True)
    
    
        
    length = len(player_pass)-1
    
    for i in range(len(player_pass)):
        
        I = length - i
        
        index_val = player_pass.index[I]
        
        player_name = player_pass.iloc[I]['player']['name']
        
        if player_name != player:
            player_pass = player_pass.drop(index=index_val)
            
    
    
    pass_data_array = np.array(player_pass[['pass']])
    pos = np.array(player_pass[['location']])
    
    big_dict = {}
    successful = 0
    long = 0
    short_suc = 0
    long_suc = 0
    prog_pass = 0
    prog_suc = 0

    for i in range(len(pos)):
        
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

    
    for i in range(len(shots_in_match)):
        try:
            assist_id = shots_in_match[i][0]['key_pass_id']
            player_assist = X[np.isin(X['id'], assist_id)]['player'].values[0]['name']
            if player_assist == player:
                xa = xa + shots_in_match[i][0]['statsbomb_xg']
                key_pass = key_pass + 1
                
                big_dict[assist_id]['key_pass'] = 'True'
                big_dict[assist_id]['xA'] = shots_in_match[i][0]['statsbomb_xg']
                
                if shots_in_match[i][0]['outcome']['name'] == 'Goal':
                    big_dict[assist_id]['assist'] = 'True'
                    assists=assists+1
                
                else:
                    big_dict[assist_id]['assist'] = 'False'
                    
                    
                
        except:
            pass
        
    no_of_passes = len(pass_data_array)
    no_long_passes = long
    no_short_passes = no_of_passes-no_long_passes
    
    try:
        suc_passes = (successful/no_of_passes)*100
    except:
        suc_passes = 0
        pass
    
    try:
        suc_short = (short_suc/no_short_passes)*100
    except:
        suc_short = 0
        pass
    
    try:
        suc_long = (long_suc/no_long_passes)*100
    except:
        suc_long = 0
        pass
    
    try:
        suc_prog = (prog_suc/prog_pass)*100
    except:
        suc_prog = 0
        pass
    
    
    overall_data = {'number_passes':no_of_passes,'successful_passes':suc_passes,
                    'number_short_passes':no_short_passes,'successful_short_passes':suc_short,
                    'number_long_passes':no_long_passes,'successful_long_passes':suc_long,
                     'xA':xa,'key_passes':key_pass,'progressive_passes':prog_pass,
                     'successful_progressive_passes':suc_prog,'assists':assists}
    
    big_dict['overall'] = overall_data
    
    return big_dict

#Get dribbling data

def player_dribbles(player,match,X):
    
    player_dribbles = X.copy()
    
    player_dribbles['dribble'].replace('', np.nan, inplace=True)
    player_dribbles.dropna(subset=['dribble'], inplace=True)
    
    
    length = len(player_dribbles)-1
    
    for i in range(len(player_dribbles)):
        
        I = length - i
        
        index_val = player_dribbles.index[I]
        
        player_name = player_dribbles.iloc[I]['player']['name']
        
        if player_name != player:
            player_dribbles = player_dribbles.drop(index=index_val)
    
    
    dribble_data_array = np.array(player_dribbles[['dribble']])
    pos = np.array(player_dribbles[['location']])
    
    big_dict = {}
    complete = 0
    
    for i in range(len(pos)):
        
        ID = player_dribbles.iloc[i]['id']
        
        little_dict = {}

         
        little_dict['start_x'] = pos[i][0][0]
        little_dict['start_y'] = pos[i][0][1]
        
        if dribble_data_array[i][0]['outcome']['name'] == 'Complete':
            complete = complete+1
        
        
        
        
        big_dict[ID] = little_dict
        
    
    
    no_of_dribble = len(dribble_data_array)
    
    no_of_suc = complete
        
    overall_data = {'number_take_ons':no_of_dribble,'successful_take_ons':no_of_suc}
    
    big_dict['overall'] = overall_data
    
    return big_dict


#Get carry data - include progressive carries

def player_carries(player,match,X):
    
    player_carries = X.copy()
    
    player_carries['carry'].replace('', np.nan, inplace=True)
    player_carries.dropna(subset=['carry'], inplace=True)
    
    length = len(player_carries)-1
    
    for i in range(len(player_carries)):
        
        I = length - i
        
        index_val = player_carries.index[I]
        
        player_name = player_carries.iloc[I]['player']['name']
        
        if player_name != player:
            player_carries = player_carries.drop(index=index_val)
    
    
    carry_data_array = np.array(player_carries[['carry']])
    pos = np.array(player_carries[['location']])
    
    big_dict = {}
    
    total_distance = 0
    prog_carry = 0
    for i in range(len(pos)):
        
        ID = player_carries.iloc[i]['id']
        
        little_dict = {}


        little_dict['start_x'] = pos[i][0][0]
        little_dict['start_y'] = pos[i][0][1]
        
        
        little_dict['end_x'] = carry_data_array[0][0]['end_location'][0]
        little_dict['end_y'] = carry_data_array[0][0]['end_location'][1]
        
        distance = np.sqrt((abs(carry_data_array[0][0]['end_location'][0]-pos[i][0][0])**2) + 
                           (abs(carry_data_array[0][0]['end_location'][1]-pos[i][0][1])**2))
        
        if carry_data_array[i][0]['end_location'][0]-pos[i][0][0] >= 5.5 and carry_data_array[i][0]['end_location'][0] > 72:
            prog_carry = prog_carry+1
        
        little_dict['distance'] = distance
        
        total_distance = total_distance + distance
        
        big_dict[ID] = little_dict
        
    
    
    no_of_carries = len(carry_data_array)
    
        
    overall_data = {'number_carries':no_of_carries,'total distance_with_ball':total_distance,
                    'progressive carries':prog_carry}
    
    big_dict['overall'] = overall_data
    
    return big_dict


#get aeiral data

def player_aerial(player,match,X):
    
    player_aerial = X.copy()
    
    player_aerial['duel'].replace('', np.nan, inplace=True)
    player_aerial.dropna(subset=['duel'], inplace=True)
    
    length = len(player_aerial)-1

    
    for i in range(len(player_aerial)):
        
        I = length - i
        
        index_val = player_aerial.index[I]
        
        type_of_duel = player_aerial.iloc[I]['duel']['type']['name']
        
        if type_of_duel != 'Aerial Lost':
            player_aerial = player_aerial.drop(index=index_val)
            
    player_aerial_clear = X.copy()
    
    player_aerial_clear['clearance'].replace('', np.nan, inplace=True)
    player_aerial_clear.dropna(subset=['clearance'], inplace=True)
    
    length = len(player_aerial_clear)-1

    
    for i in range(len(player_aerial_clear)):
        
        I = length - i
        
        index_val = player_aerial_clear.index[I]
        try:
            type_of_duel = player_aerial_clear.iloc[I]['clearance']['aerial_won'] == True
            
        
        except:
            player_aerial_clear = player_aerial_clear.drop(index=index_val)
            
            
    player_aerial_shot = X.copy()
    
    player_aerial_shot['shot'].replace('', np.nan, inplace=True)
    player_aerial_shot.dropna(subset=['shot'], inplace=True)
    
    length = len(player_aerial_shot)-1
       
    
    for i in range(len(player_aerial_shot)):
        
        I = length - i
        
        index_val = player_aerial_shot.index[I]
        try: 
            player_aerial_shot['shot'].iloc[I]['aerial_won']== True
            
            
        
        except:
            player_aerial_shot = player_aerial_shot.drop(index=index_val)
            
    player_aerial_misco = X.copy()
    
    player_aerial_misco['miscontrol'].replace('', np.nan, inplace=True)
    player_aerial_misco.dropna(subset=['miscontrol'], inplace=True)
    
    length = len(player_aerial_misco)-1
       
    
    for i in range(len(player_aerial_misco)):
        
        I = length - i
        
        index_val = player_aerial_misco.index[I]
        if player_aerial_misco.iloc[I]['miscontrol']['aerial_won'] == True:
            pass
            
            
        
        else:
            player_aerial_misco = player_aerial_misco.drop(index=index_val)
       
   
    player_aerial_pass = X.copy()
    
    player_aerial_pass['pass'].replace('', np.nan, inplace=True)
    player_aerial_pass.dropna(subset=['pass'], inplace=True)
    
   
    length = len(player_aerial_pass)-1

    
    for i in range(len(player_aerial_pass)):
        
        I = length - i
        
        index_val = player_aerial_pass.index[I]
        
        
        try:
            type_of_pass = player_aerial_pass['pass'].iloc[I]['aerial_won'] == True
            
        
        except:
            player_aerial_pass = player_aerial_pass.drop(index=index_val)
            
    
    player_aerial_won = pd.concat([player_aerial_clear,player_aerial_misco,player_aerial_pass,player_aerial_shot])
    
    
    player_tackle = X.copy()
    
    player_tackle['duel'].replace('', np.nan, inplace=True)
    player_tackle.dropna(subset=['duel'], inplace=True)
    
    length = len(player_tackle)-1


    
    for i in range(len(player_tackle)):
        
        I = length - i
        
        index_val = player_tackle.index[I]
        
        type_of_duel = player_tackle.iloc[I]['duel']['type']['name']
        
        if type_of_duel != 'Tackle':
            player_tackle = player_tackle.drop(index=index_val)
            
    length = len(player_aerial)-1
           
    for i in range(len(player_aerial)):
           
           I = length - i
           
           index_val = player_aerial.index[I]
           
           player_name = player_aerial.iloc[I]['player']['name']
           
           if player_name != player:
               player_aerial = player_aerial.drop(index=index_val)
               
    length = len(player_aerial_won)-1
               
    for i in range(len(player_aerial_won)):
        
        I = length - i
        
        index_val = player_aerial_won.index[I]
        
        player_name = player_aerial_won.iloc[I]['player']['name']
        
        if player_name != player:
            player_aerial_won = player_aerial_won.drop(index=index_val)
      
        
    big_dict = {}  
    
    no_aerial_won = len(player_aerial_won)
    no_aerial_loss = len(player_aerial)
    
    try:
        aerial_perc = (len(player_aerial_won)/(len(player_aerial)+len(player_aerial_won)))*100
        
    except:
        aerial_perc = 0
    
        
    overall_data = {'aerial_won':no_aerial_won,'aerial_lost':no_aerial_loss,'aerial_perc':aerial_perc}
    
    big_dict['overall'] = overall_data
    
    return big_dict


#compile data

def all_data(player,match,X):

    
    shots = player_shots(player, match,X)
    passes = player_pass_data(player, match,X)
    heatmap = player_heatmap(player, match,X)
    dribbles = player_dribbles(player, match, X)
    carries = player_carries(player, match, X)
    aerial = player_aerial(player, match, X)
    
    return shots, passes, heatmap, dribbles, carries,aerial

#plot heatmap

def plot_heat(heatmap):
    

    pitch = VerticalPitch (line_zorder=2,pitch_color='#22312b')
    
    
    fig, ax = pitch.draw()
    
    pcm = pitch.heatmap(heatmap, ax=ax,cmap='Greens')
    

#put compiled data into dataframe

def game_all_data(match,lineups,X):
    
    
        
    X['player'].replace('', np.nan, inplace=True)
    X.dropna(subset=['player'], inplace=True)
    
    
    lineups_list_all = pd.read_json(lineups)
    lineups_list = lineups_list_all.iloc[0]['lineup']
    
    df_MCWFC = pd.DataFrame()

        
    for j in range(len(lineups_list)):
        player = lineups_list[j]['player_name']

        
        shots, passes, heatmap, dribbles, carries,aerial = all_data(player, 'g',X)


    
    
        big_dict = {}
        
        big_dict['player'] = player
        
        for i in range(len(shots['overall'])):
            
            big_dict[list(shots['overall'].keys())[i]] = list(shots['overall'].values())[i]
            
        for i in range(len(passes['overall'])):
            
            big_dict[list(passes['overall'].keys())[i]] = list(passes['overall'].values())[i]
            
                
        for i in range(len(dribbles['overall'])):
            
            big_dict[list(dribbles['overall'].keys())[i]] = list(dribbles['overall'].values())[i]
            
        for i in range(len(carries['overall'])):
            
            big_dict[list(carries['overall'].keys())[i]] = list(carries['overall'].values())[i]
            
        for i in range(len(carries['overall'])):
            
            big_dict[list(carries['overall'].keys())[i]] = list(carries['overall'].values())[i]
            
        for i in range(len(aerial['overall'])):
            
            big_dict[list(aerial['overall'].keys())[i]] = list(aerial['overall'].values())[i]
           
            
           
        positions = []
        
        for i in range(len(lineups_list[j]['positions'])):
            positions.append(lineups_list[j]['positions'][0]['position_id'])
            
        try:
            big_dict['positions'] = positions[-1]
        except:
            big_dict['positions'] = np.nan
        
        df_MCWFC = df_MCWFC.append(big_dict,ignore_index=True)
        
    lineups_list = lineups_list_all.iloc[1]['lineup']
    
    df_other = pd.DataFrame()

        
    for j in range(len(lineups_list)):
        player = lineups_list[j]['player_name']

        
        shots, passes, heatmap, dribbles, carries,aerial = all_data(player, 'g',X)



    
        big_dict = {}
        
        big_dict['player'] = player
        
        for i in range(len(shots['overall'])):
            
            big_dict[list(shots['overall'].keys())[i]] = list(shots['overall'].values())[i]
            
        for i in range(len(passes['overall'])):
            
            big_dict[list(passes['overall'].keys())[i]] = list(passes['overall'].values())[i]
            
                
        for i in range(len(dribbles['overall'])):
            
            big_dict[list(dribbles['overall'].keys())[i]] = list(dribbles['overall'].values())[i]
            
        for i in range(len(carries['overall'])):
            
            big_dict[list(carries['overall'].keys())[i]] = list(carries['overall'].values())[i]
            
        for i in range(len(aerial['overall'])):
            
            big_dict[list(aerial['overall'].keys())[i]] = list(aerial['overall'].values())[i]
           
            
           
        positions = []
        
        for i in range(len(lineups_list[j]['positions'])):
            positions.append(lineups_list[j]['positions'][0]['position_id'])
            
        try:
            big_dict['positions'] = positions[-1]
        except:
            big_dict['positions'] = np.nan
        
        df_other = df_other.append(big_dict,ignore_index=True)
        
        
    return df_MCWFC,df_other

