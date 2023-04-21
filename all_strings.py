from Plotting import Defender_passing, Carries,Passes_pitch,Carries_pitch,Energy_plot,Involve_plot,Energy_heat

'''
The bot function: It takes alot of the generated data as inputs and finds the most anomolous variable.
Depending on the anomaly, it will run the anomaly through a function to create a text and plots for the 
anomaly.
'''


def bot(data,MCWFC_Def,other_Def,joined_data,df_MCWFC,df_other,X_update,minute,anomaly_list,MCWFC_Inv,other_inv,surnames_home_start,surnames_away_start):

    #Use the anomaly list to stop repeated anomlies    

    anomaly_list_drop = (anomaly_list)[-15:]

        
    anomaly_list_df = data.sort_values('anomaly_score',ascending=False)

    anomaly_list_df = anomaly_list_df.drop(anomaly_list_drop,axis=0)
    
    #Make sure player has played full game (not somebody just off the bench)
    
    length = len(anomaly_list_df)-1
    
    for i in range(len(anomaly_list_df)):
        
        I = length - i
        
        index_val = anomaly_list_df.index[I]
        
        try:
        
            player_name = anomaly_list_df.iloc[I]['player'].split()[-1]
            
        except:
            player_name = 'none'
            
        
        if player_name not in surnames_away_start and player_name not in surnames_home_start:
            anomaly_list_df = anomaly_list_df.drop(index=index_val)
    
    anomaly = anomaly_list_df.index[0]
    
    

    #seperate anomlies into different types (for plotting)
    
            
    passing = ['o_defense_pass_worst','o_defense_pass_best','MCWFC_defense_pass_worst',
               'MCWFC_defense_pass_best','MCWFC_pass_worst','MCWFC_pass_best','o_pass_best',
               'o_pass_worst']
    
    carries = ['o_defense_carry_worst','o_defense_carry_best','MCWFC_defense_carry_worst',
               'MCWFC_defense_carry_best','MCWFC_carry_worst','MCWFC_carry_best','o_carry_best',
               'o_carry_worst']
    
    aerial = ['o_def_aerial_worst','o_def_aerial_best','MCWFC_def_aerial_best',
               'MCWFC_def_aerial_worst','o_aerial_worst','o_aerial_best','MCWFC_aerial_best',
               'MCWFC_aerial_worst']
    
    energy = ['MCWFC_energy_splits','o_energy_splits']
    
    involved = ['MCWFC_involved','other_involved']
    
    #depending on the type of anomaly, produce plots/output text for the anomaly.
    #Plotting functions are in Plotting.py

    if anomaly in passing: 
        
        if anomaly == 'MCWFC_defense_pass_best' or anomaly == 'MCWFC_defense_pass_worst':
            dataset = MCWFC_Def
            text,plot_text = Defender_passing(data, anomaly, dataset,minute,0,joined_data)
            plot_text2 = Passes_pitch(data, anomaly, X_update,minute,0)
            
        if anomaly == 'o_defense_pass_best' or anomaly == 'o_defense_pass_worst':
            dataset = other_Def
            text,plot_text = Defender_passing(data, anomaly, dataset,minute,1,joined_data)
            plot_text2 = Passes_pitch(data, anomaly, X_update,minute,1)
            
        if anomaly == 'MCWFC_pass_best' or anomaly == 'MCWFC_pass_worst':
            dataset = df_MCWFC
            text, plot_text = Defender_passing(data, anomaly, dataset,minute,0,joined_data)
            plot_text2 = Passes_pitch(data, anomaly, X_update,minute,0)
            
        if anomaly == 'o_pass_best' or anomaly == 'o_pass_worst':
            dataset = df_other
            text,plot_text = Defender_passing(data, anomaly, dataset,minute,1,joined_data)
            plot_text2 = Passes_pitch(data, anomaly, X_update,minute,1)
        
        
        
    
    if anomaly in carries: 
        
        if anomaly == 'MCWFC_defense_carry_best' or anomaly == 'MCWFC_defense_carry_best':
            dataset = MCWFC_Def
            text,plot_text = Carries(data, anomaly, dataset,minute,0,joined_data)
            plot_text2 = Carries_pitch(data, anomaly, X_update,minute,0)
            
        if anomaly == 'o_defense_carry_best' or anomaly == 'o_defense_carry_best':
            dataset = other_Def
            text,plot_text = Carries(data, anomaly, dataset,minute,1,joined_data)
            plot_text2 = Carries_pitch(data, anomaly, X_update,minute,1)
            
        if anomaly == 'MCWFC_carry_best' or anomaly == 'MCWFC_carry_worst':
            dataset = df_MCWFC 
            text,plot_text = Carries(data, anomaly, dataset,minute,0,joined_data)
            plot_text2 = Carries_pitch(data, anomaly, X_update,minute,0)
            
        if anomaly == 'o_carry_best' or anomaly == 'o_carry_worst':
            dataset = df_other 
            text,plot_text = Carries(data, anomaly, dataset,minute,1,joined_data)
            plot_text2 = Carries_pitch(data, anomaly, X_update,minute,1)
            
        
        
        
    if anomaly in aerial:
        
        
        if anomaly == 'MCWFC_def_aerial_best':
            
            vals = data.loc['MCWFC_def_aerial_best']['worst_val']
            player = data.loc['MCWFC_def_aerial_best']['player']
            text = player + ' has been our best defender in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate'
            
        
        if anomaly == 'o_def_aerial_best':
            
            vals = data.loc['o_def_aerial_best']['worst_val']
            player = data.loc['o_def_aerial_best']['player']
            text = player + ' has been the best opposition defender in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate. It may be worth avoiding long balls in their direction.'
            
            
        if anomaly == 'MCWFC_def_aerial_worst':
    
            vals = data.loc['MCWFC_def_aerial_worst']['worst_val']
            player = data.loc['MCWFC_def_aerial_worst']['player']
            text = player + ' has been out worst defender in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate'
            
        
        if anomaly == 'o_def_aerial_worst':
    
            vals = data.loc['o_def_aerial_worst']['worst_val']
            player = data.loc['o_def_aerial_worst']['player']
            text = player + ' has been the worst opposition defender player in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate. It may be worth targetting long balls in their direction.'
        
        
        if anomaly == 'MCWFC_aerial_best':
            
            vals = data.loc['MCWFC_def_aerial_best']['worst_val']
            player = data.loc['MCWFC_def_aerial_best']['player']
            text = player + ' has been our best player in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate'
            
        
        if anomaly == 'o_aerial_best':
            
            vals = data.loc['o_def_aerial_best']['worst_val']
            player = data.loc['o_def_aerial_best']['player']
            text = player + ' has been the best opposition player in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate. It may be worth avoiding long balls in their direction.'
            
            
        if anomaly == 'MCWFC_aerial_worst':
    
            vals = data.loc['MCWFC_def_aerial_worst']['worst_val']
            player = data.loc['MCWFC_def_aerial_worst']['player']
            text = player + ' has been out worst player in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate. It may be worth avoiding long balls in their direction'
            
        
        if anomaly == 'o_aerial_worst':
    
            vals = data.loc['o_def_aerial_worst']['worst_val']
            player = data.loc['o_def_aerial_worst']['player']
            text = player + ' has been the worst opposition player in the air today, competing in ' +str(int(vals[0]+vals[1])) + ' air duels with a '+ str(round(vals[2]))+ '% success rate. It may be worth targetting long balls in their direction.'
        
        
    if anomaly in energy:
        
        text,plot_text = Energy_plot(data, anomaly, minute)
        
        if anomaly == 'o_energy_splits':
            plot_text2 = Energy_heat(data,anomaly,minute,X_update,1)
        
        if anomaly == 'MCWFC_energy_splits':
            plot_text2 = Energy_heat(data,anomaly,minute,X_update,0)
        
    if anomaly in involved: 
        
        if anomaly == 'MCWFC_involved':
            
            vals = data.loc['MCWFC_involved']['worst_val']
            player = data.loc['MCWFC_involved']['player']
            
            text,plot_text = Involve_plot(data,anomaly,minute,MCWFC_Inv,team=0)
            
        if anomaly == 'other_involved':
            
            vals = data.loc['other_involved']['worst_val']
            player = data.loc['other_involved']['player']
            
            text,plot_text = Involve_plot(data,anomaly,minute,other_inv,team=1)

    

    print('\nMinute = ' +str(minute) + '\n\n'+text)
    
    #Save names of plots into list
    
    try:
        plots = [plot_text,plot_text2]
        
    except:
        try:
            plots = [plot_text]
            
        except:
            plots = []
    
    
    return text,anomaly,plots