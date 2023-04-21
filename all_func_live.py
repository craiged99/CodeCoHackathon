
from get_data_json import game_all_data
from energy_function import energy
from involved_in_shot import involved_in_build_up
from oppo_defense_func import Oppisituion_Defender_Carries, Oppisituion_Defender_Passing,Oppositoin_Aerial
from add_columns import add_col
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
pd.options.mode.chained_assignment = None


import pandas as pd
import numpy as np

from all_strings import bot


#Define match files

match = 'ManCity Hackathon Json Files/ManCity_Arsenal_events.json'
lineups = 'ManCity Hackathon Json Files/ManCity_Arsenal_lineups.json'

#Define match_id

match_id = 'g2312135'


#Get squads
 
lineups_home = pd.read_json("MCI Women's Files/"+match_id+"_SecondSpectrum_meta.json", orient='index').loc['homePlayers'][0]
lineups_away = pd.read_json("MCI Women's Files/"+match_id+"_SecondSpectrum_meta.json", orient='index').loc['awayPlayers'][0]


home = {}
away = {}

home_start = {}
away_start = {}

#Get dictioanries of players ID's and their name (used laters)

for i in range(len(lineups)):
    
    try:
        id_player  = lineups_home[i]['ssiId']
        home[id_player] = lineups_home[i]['name']
        if lineups_home[i]['position'] != 'SUB':
            
            home_start[id_player] = lineups_home[i]['name']
        
    except:
        pass
    
    try:
        id_player  = lineups_away[i]['ssiId']
        away[id_player] = lineups_away[i]['name']
        if lineups_away[i]['position'] != 'SUB':
            away_start[id_player] = lineups_away[i]['name']
        
    except:
        pass

#Define text to save and send to backend and anomalies
text_dict = {}
anomaly_list = []

#

#For every minute of the game
for i in range(1):
    
    #Define starting minute (20) and period (hard-coded)
    minute= i+20

    period = 1
    
    
    #Read data and select data before the minute in question
    X = pd.read_json(match)
    X = X[X['minute'] < minute]
    
    X_update = X.copy()
    
    X_update = add_col(X_update)
    
        
    
    big_anomaly = {}
    
    #Get all the data from the 'game_all_data' function
    
    df_MCWFC,df_other = game_all_data(match, lineups,X)
    
    df_MCWFC['team'] = 0
    df_other['team'] = 1
    
    joined_data = pd.concat([df_MCWFC,df_other])
    
    #remove players who aren't playing using the no_of_passes
    
    df_MCWFC = df_MCWFC[df_MCWFC['number_passes']!=0]
    df_other = df_other[df_other['number_passes']!=0]
    
    #Define defenders for both teams by using positions
    
    #defender passing
    MCWFC_Def = df_MCWFC[df_MCWFC['positions'] <= 8]
    MCWFC_Def = MCWFC_Def[MCWFC_Def['positions'] != 1]
    other_Def = df_other[df_other['positions'] <= 8]
    other_Def = other_Def[other_Def['positions'] != 1]
    
    #Use functions to find anomolous players and anomaly scores
    
    o_defense_pass_worst, o_defense_pass_best = Oppisituion_Defender_Passing(other_Def,minute)
    o_defense_carry_worst, o_defense_carry_best = Oppisituion_Defender_Carries(other_Def)
    
    big_anomaly['o_defense_pass_worst'] = o_defense_pass_worst
    big_anomaly['o_defense_pass_best'] = o_defense_pass_best
    
    big_anomaly['o_defense_carry_worst'] = o_defense_carry_worst
    big_anomaly['o_defense_carry_best'] = o_defense_carry_best
    
    MCWFC_defense_pass_worst, MCWFC_defense_pass_best = Oppisituion_Defender_Passing(MCWFC_Def,minute)
    MCWFC_defense_carry_worst, MCWFC_defense_carry_best = Oppisituion_Defender_Carries(MCWFC_Def)
    
    big_anomaly['MCWFC_defense_pass_worst'] = MCWFC_defense_pass_worst
    big_anomaly['MCWFC_defense_pass_best'] = MCWFC_defense_pass_best
    
    big_anomaly['MCWFC_defense_carry_worst'] = MCWFC_defense_carry_worst
    big_anomaly['MCWFC_defense_carry_best'] = MCWFC_defense_carry_best
    
    
    o_pass_worst, o_pass_best = Oppisituion_Defender_Passing(df_other,minute)
    o_carry_worst, o_carry_best = Oppisituion_Defender_Carries(other_Def)
    
    big_anomaly['o_pass_worst'] = o_pass_worst
    big_anomaly['o_pass_best'] = o_pass_best
    
    big_anomaly['o_carry_worst'] = o_carry_worst
    big_anomaly['o_carry_best'] = o_carry_best
    
    MCWFC_pass_worst, MCWFC_pass_best = Oppisituion_Defender_Passing(df_MCWFC,minute)
    MCWFC_carry_worst, MCWFC_carry_best = Oppisituion_Defender_Carries(df_MCWFC)
    
    big_anomaly['MCWFC_pass_worst'] = MCWFC_pass_worst
    big_anomaly['MCWFC_pass_best'] = MCWFC_pass_best
    
    big_anomaly['MCWFC_carry_worst'] = MCWFC_carry_worst
    big_anomaly['MCWFC_carry_best'] = MCWFC_carry_best
    
    
    
    MCWFC_aerial_worst, MCWFC_aerial_best = Oppositoin_Aerial(df_MCWFC)
    o_aerial_worst, o_aerial_best = Oppositoin_Aerial(df_other)
    
    big_anomaly['MCWFC_aerial_worst'] = MCWFC_aerial_worst
    big_anomaly['MCWFC_aerial_best'] = MCWFC_aerial_best
    
    big_anomaly['o_aerial_worst'] = o_aerial_worst
    big_anomaly['o_aerial_best'] = o_aerial_best
    
    
    MCWFC_def_aerial_worst, MCWFC_def_aerial_best = Oppositoin_Aerial(MCWFC_Def)
    o_def_aerial_worst, o_def_aerial_best = Oppositoin_Aerial(other_Def)
    
    big_anomaly['MCWFC_def_aerial_worst'] = MCWFC_def_aerial_worst
    big_anomaly['MCWFC_def_aerial_best'] = MCWFC_def_aerial_best
    
    big_anomaly['o_def_aerial_worst'] = o_def_aerial_worst
    big_anomaly['o_def_aerial_best'] = o_def_aerial_best
    
    
    
    big_anomaly['MCWFC_energy_splits'] = {'anomaly_score':-10}
    
    #If minute is divisble by 10 or 5, do the energy function and find anomoulous players
    
    if minute % 10 == 0 and minute > 20:
        energy_splits_home,energy_splits_h_player = energy(match_id, 10,minute,period,'home')
        player = energy_splits_h_player['player']
        energy_splits_h_player['player'] = home[player]
        name_list = []
        
        for i in range(len(energy_splits_home)):
            
            name = home[energy_splits_home.index[i]]
            
            name_list.append(name)
            
        energy_splits_home.index = name_list
        
        
        energy_splits_h_player['all_team'] = energy_splits_home
        
        big_anomaly['MCWFC_energy_splits'] = energy_splits_h_player
    
        
    if minute % 10 == 5 and minute > 20:
        energy_splits_home,energy_splits_h_player = energy(match_id, 5,minute,period,'home')
        player = energy_splits_h_player['player']
        energy_splits_h_player['player'] = home[player]
        name_list = []
        
        for i in range(len(energy_splits_home)):
            
            name = home[energy_splits_home.index[i]]
            
            name_list.append(name)
            
        energy_splits_home.index = name_list
        
        
        energy_splits_h_player['all_team'] = energy_splits_home
        
        big_anomaly['MCWFC_energy_splits'] = energy_splits_h_player
    
    
    big_anomaly['o_energy_splits'] = {'anomaly_score':-10}
    
    if minute % 10 == 0 and minute > 20:
        energy_splits_away,energy_splits_a_player = energy(match_id, 10,minute,period,'away')
        player = energy_splits_a_player['player']
        energy_splits_a_player['player'] = away[player]
        
        name_list = []
        
        for i in range(len(energy_splits_away)):
            
            name = away[energy_splits_away.index[i]]
            
            name_list.append(name)
            
        energy_splits_away.index = name_list
        
        
        energy_splits_a_player['all_team'] = energy_splits_away
        
        big_anomaly['o_energy_splits'] = energy_splits_a_player
        
    if minute % 10 == 5 and minute > 20:
        energy_splits_away,energy_splits_a_player = energy(match_id, 5,minute,period,'away')
        player = energy_splits_a_player['player']
        energy_splits_a_player['player'] = away[player]
        
        name_list = []
        
        for i in range(len(energy_splits_away)):
            
            name = away[energy_splits_away.index[i]]
            
            name_list.append(name)
            
        energy_splits_away.index = name_list
        
        
        energy_splits_a_player['all_team'] = energy_splits_away
        
        big_anomaly['o_energy_splits'] = energy_splits_a_player
        
        
    
    #Find the anomoulous players in involvements to shots using onvolved_in_build_up function
    
    involved,gk_long,gk_short,gk_player_inv = involved_in_build_up(5, match,X)
    
    involved_2,gk_long,gk_short,gk_player_inv = involved_in_build_up(20, match,X)
    
    #Get surnames of players (easier to use as datasets have different naming formats)
    
    surnames_home = []
    surnames_away = []
    
    surnames_home_start = []
    surnames_away_start = []
    
    for i in range(len(home)):
        
        if list(home.values())[i].split(' ')[-1] == 'Angeldahl':
            surnames_home.append('Angeldal')
                    
        else:
            
            surnames_home.append(list(home.values())[i].split(' ')[-1])
        
    for i in range(len(away)):
        
        if list(away.values())[i].split(' ')[-1] == 'Houghton':
            pass
       
        else:
            surnames_away.append(list(away.values())[i].split(' ')[-1])
            
    for i in range(len(home_start)):
        
        if list(home_start.values())[i].split(' ')[-1] == 'Angeldahl':
            surnames_home_start.append('Angeldal')
                    
        else:
            
            surnames_home_start.append(list(home_start.values())[i].split(' ')[-1])
        
    for i in range(len(away_start)):
        
        if list(away_start.values())[i].split(' ')[-1] == 'Houghton':
            pass
       
        else:
            surnames_away_start.append(list(away_start.values())[i].split(' ')[-1])
            
            
    
    #Splits involvment scores into seperate teams and find anomolous playeres
    
    MCWFC_Inv = {}
    other_inv={}
    
    for i in range(len(involved)):
        if list(involved.keys())[i].split(' ')[-1] in surnames_home or list(involved.keys())[i].split(' ')[-2] in surnames_home:
            MCWFC_Inv[list(involved.keys())[i]] = list(involved.values())[i]
            
        if list(involved.keys())[i].split(' ')[-1] in surnames_away or list(involved.keys())[i].split(' ')[-2] in surnames_away:
            other_inv[list(involved.keys())[i]] = list(involved.values())[i]
            
    
    MCWFC_Inv = {k: v for k, v in sorted(MCWFC_Inv.items(), key=lambda item: item[1])}
    other_inv = {k: v for k, v in sorted(other_inv.items(), key=lambda item: item[1])}
    
    inv_anomaly_MCWFC = {}
    inv_anomaly_other = {}
    
    inv_anomaly_MCWFC['player'] = list(MCWFC_Inv.keys())[-1]
    inv_anomaly_MCWFC['worst_val'] = list(MCWFC_Inv.values())[-1]
    inv_anomaly_MCWFC['anomaly_score'] = round((np.max(list(MCWFC_Inv.values())) - np.average(list(MCWFC_Inv.values())))*1.5)
    
    inv_anomaly_other['player'] = list(other_inv.keys())[-1]
    inv_anomaly_other['worst_val'] = list(other_inv.values())[-1]
    inv_anomaly_other['anomaly_score'] = round((np.max(list(other_inv.values())) - np.average(list(other_inv.values())))*1.5)
    
    big_anomaly['MCWFC_involved'] = inv_anomaly_MCWFC
    big_anomaly['other_involved'] = inv_anomaly_other
    
    
    #Save all anomaly data in a pd.Dataframe
    
    data = pd.DataFrame(big_anomaly)
    data = data.transpose()
    
    #Run all the anomaly data through the bot_function 
    
    text,anomaly,plots = bot(data, MCWFC_Def, other_Def, joined_data,df_MCWFC,df_other, 
                             X_update, minute,anomaly_list,MCWFC_Inv,other_inv,surnames_home_start,surnames_away_start)
    
    
    #Save the outputs of the bot function (text and names of figures)
    
    anomaly_list.append(anomaly)
    
    text_dict[minute*60] = {'message':text,'imgs':plots}
