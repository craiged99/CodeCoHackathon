import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import matplotlib.patches as mpatches
from scipy.ndimage import gaussian_filter
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.image as image

#Plot for passing anomalies  - bar chart showing how players passing data compares to
#fellow teammates and opposition players

def Defender_passing(data,anomaly,data_values,minute,team,joined_data):
    
    minute = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']
    
    text1 = '\n\nNumber of Passes  - ' +str(int(vals['number_passes'])) + ' (' +str(int(vals['successful_passes'])) + '% success rate)'
    text2 = '\nProgressive Passes  - ' +str(int(vals['progressive_passes'])) + ' (' +str(int(vals['successful_progressive_passes'])) + '% success rate)'
    text3 = '\nKey Passes  - ' +str(int(vals['key_passes'])) 
    text4 = '\nxA  - ' +str(round(vals['xA'],3)) 
    
    
    
    columns = ['key_passes','xA','number_passes','successful_passes','progressive_passes','successful_progressive_passes']
    column_names = ['Key Passes', 'xA','No. of \nPasses','Passing Success \nRate','No. of \nProgressive Passes','Progressive Pass\nSuccess Rate']
    fig,ax= plt.subplots(figsize=(8,8))
    X_axis = np.arange(len(columns))


    for i in range(len(columns)):
        
        plotting_val = vals[columns[i]]
        
        
        
        plotting = (plotting_val/(np.average(data_values[columns[i]])))-1
        plotting_2 = (plotting_val/(np.average(joined_data[columns[i]])))-1
        
        if team == 0:

            if plotting_val == 0:
                plotting = 0
            
            if plotting < 0:
                color = '#97cad8'
            else:
                color = '#97cad8'
                
            if plotting_2 < 0:
                color2 = '#34798d'
                
            else:
                color2 = '#34798d'
                
        if team == 1:

            if plotting_val == 0:
                plotting = 0
            
            if plotting < 0:
                color = '#d45e5e'
                
            else:
                color = '#d45e5e'
                
                
            if plotting_2 < 0:
                color2 = '#781f25'
                
            else:
                color2 = '#781f25'
                
                
        hfont = {'fontname':'Helvetica Neue'}
        
        plt.axhline(y=0,color='black',label=None)
        plt.bar(X_axis[i] - 0.175,plotting*100,0.35,color=color,label='vs Other Opposition Defenders')
        plt.bar(X_axis[i] + 0.175,plotting_2*100,0.35,color=color2,label = 'vs All Other Players')
        plt.grid(alpha=0.8,zorder=-1.0,which='major')
        plt.xticks(X_axis,column_names,fontsize=8,**hfont)
        
    #Produce text for passing anomalies depending on what the anomaly is
    
    if anomaly == 'o_defense_pass_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
    
        text = player + ' has had poor distribution from the back, it may be worth focusing our press on other players.'
        plt.title(player + "'s passing numbers \nvs other opposition defenders",**hfont)
        plt.ylabel('% comparison compared to \nother opposition defenders',**hfont)
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
    
    if anomaly == 'o_defense_pass_best':
    
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
        
        text = player + ' has had good distribution from the back, it may be worth focusing our press on this player.'
        plt.title(player + "'s passing numbers \nvs other opposition defenders",**hfont)
        plt.ylabel('% comparison compared to \nother opposition defenders',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text =text+text1+text2+text3+text4
    
    if anomaly == 'MCWFC_defense_pass_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has had good distribution from the back, it may be worth focusing our play from the back on this player.'
        plt.title(player + "'s passing numbers \nvs other MCWFC defenders",**hfont)
        plt.ylabel('% comparison compared to \nother MCWFC defenders',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
    
    if anomaly == 'MCWFC_defense_pass_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has had poor distribution from the back, it may be worth focusing our play from the back on other players.'
        plt.title(player + "'s passing numbers \nvs other MCWFC defenders",**hfont)
        plt.ylabel('% comparison compared to \nother MCWFC defenders',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
        
    if anomaly == 'MCWFC_pass_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been very creative, it may be worth focusing our play on them.'
        plt.title(player + "'s passing numbers \nvs all players",**hfont)
        plt.ylabel('% comparison compared to \nall players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
    
    if anomaly == 'MCWFC_pass_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been our least creative player so far'
        plt.title(player + "'s passing numbers \nvs all players",**hfont)
        plt.ylabel('% comparison compared to \nall players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text =text+text1+text2+text3+text4
    
    if anomaly == 'o_pass_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been the most creative opposition player, it may be worth focusing defensive efforts on them.'
        plt.title(player + "'s passing numbers \nvs all players",**hfont)
        plt.ylabel('% comparison compared to \nall players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
    
    if anomaly == 'o_pass_worst':
    
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
        
        text = player + ' has been the least creative opposition player, it may be worth focusing defensive efforts elsewhere.'
        plt.title(player + "'s passing numbers \nvs all players",**hfont)
        plt.ylabel('% comparison compared to \nall players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
        
        


    plot_name = str(minute)+'.jpeg'
    
    return full_text,plot_name



#Plot for carry anomalies  - bar chart showing how players carry data compares to
#fellow teammates and opposition players

def Carries(data,anomaly,data_values,minute,team,joined_data):
    
    minute = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']
    
    text1 = '\n\nNumber of Carries  - ' +str(int(vals['number_carries'])) 
    text2 = '\nProgressive Carries  - ' +str(int(vals['progressive carries'])) 
    text3 = '\nTotal Distance With Ball  - ' +str(int(vals['total distance_with_ball']))+'m' 
    text4 = '\nSuccessful Take-Ons  - ' +str(round(vals['successful_take_ons'])) 
    
    
    columns = ['progressive carries','number_carries','total distance_with_ball','successful_take_ons']
    column_names = ['Progressive\nCarries','Number of\nCarries','Distance Carried\nWith Ball','Successful \nTake-Ons']
    
    fig,ax = plt.subplots(figsize=(8,8))
    X_axis = np.arange(len(columns))

    for i in range(len(columns)):
        
        plotting_val = vals[columns[i]]
        
        
        plotting = (plotting_val/(np.average(data_values[columns[i]])))-1
        plotting_2 = (plotting_val/(np.average(joined_data[columns[i]])))-1

        if team == 0:

            if plotting_val == 0:
                plotting = 0
            
            if plotting < 0:
                color = '#97cad8'
            else:
                color = '#97cad8'
                
            if plotting_2 < 0:
                color2 = '#34798d'
                
            else:
                color2 = '#34798d'
                
        if team == 1:

            if plotting_val == 0:
                plotting = 0
            
            if plotting < 0:
                color = '#d45e5e'
                
            else:
                color = '#d45e5e'
                
                
            if plotting_2 < 0:
                color2 = '#781f25'
                
            else:
                color2 = '#781f25'
                
                
        hfont = {'fontname':'Helvetica Neue'}
        
        plt.axhline(y=0,color='black',label=None)
        plt.bar(X_axis[i] - 0.175,plotting*100,0.35,color=color,label='vs Other Opposition Defenders')
        plt.bar(X_axis[i] + 0.175,plotting_2*100,0.35,color=color2,label = 'vs All Other Players')
        plt.grid(alpha=0.8,zorder=-1.0,which='major')
        plt.xticks(X_axis,column_names,fontsize=8,**hfont)
    
    
    #Produce text for carry anomalies depending on what the anomaly is
    
    
    if anomaly == 'o_defense_carry_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has struggled bringing it out from the back, it may be worth pressing this player.'
        plt.title(player + "'s on-the-ball numbers \nvs other opposition defenders",**hfont)
        plt.ylabel('% comparison compared to \n other opposition defenders',**hfont)
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    if anomaly == 'o_defense_carry_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been good at bringing it out from the back, it may be worth focusing on this player.'
        plt.title(player + "'s on-the-ball numbers \nvs other opposition defenders",**hfont)
        plt.ylabel('% comparison compared to \n other opposition defenders',**hfont)
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
        
    if anomaly == 'MCWFC_defense_carry_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has struggled bringing it out from the back, it may be worth focusing our out-ball elsewhere.'
        plt.title(player + "'s on-the-ball numbers \nvs other MCWFC defenders",**hfont)
        plt.ylabel('% comparison compared to \n other opposition defenders',**hfont)
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    if anomaly == 'MCWFC_defense_carry_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Defenders')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been our best defender at bringing it out from the back.'
        plt.title(player + "'s on-the-ball numbers \nvs other MCWFC defenders",**hfont)
        plt.ylabel('% comparison compared to \n other opposition defenders',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    
    if anomaly == 'MCWFC_carry_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been our most effective dribbler so far, it might be worth looking at giving them space.'
        plt.title(player + "'s on-the-ball numbers \nvs all other players",**hfont)
        plt.ylabel('% comparison compared to \n other other players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    if anomaly == 'MCWFC_carry_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other MCWFC Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been our least effective dribbler so far.'
        plt.title(player + "'s on-the-ball numbers \nvs all other players",**hfont)
        plt.ylabel('% comparison compared to \n other other players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    if anomaly == 'o_carry_best':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + ' has been the oppositions most effective dribbler so far, it might be worth getting tighter to them.'
        plt.title(player + "'s on-the-ball numbers \nvs all other players",**hfont)
        plt.ylabel('% comparison compared to \n other other players',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
        
    if anomaly == 'o_carry_worst':
        
        darkblue = mpatches.Patch(color=color, label='vs Other Opposition Players')
        lightblue = mpatches.Patch(color=color2, label='vs All Other Players')
        plt.legend(handles=[darkblue,lightblue],loc='upper left')
    
        text = player + " has been the oppositions least effective dribbler so far, it may be worth appling pressure to them."
        plt.title(player + "'s on-the-ball numbers \nvs all other players",**hfont)
        plt.ylabel('% comparison compared to \n other other players',**hfont)
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
        
        
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
        full_text = text+text1+text2+text3+text4
    
    
    

    plot_name = str(minute)+'.jpeg'
    
    return full_text,plot_name




#Produce second plot for carries - show the anomoulous player's carries on a pitch


def Carries_pitch(data,anomaly,X_update,minute,team):
    
    minute = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']
    
    
    X_update_2 = X_update.copy()
    
    length = len(X_update_2)-1


    hfont = {'fontname':'Helvetica Neue'}
    
    im = image.imread('kicksmarter-logo.png')
    
    for i in range(len(X_update_2)):
        
        I = length - i
        
        index_val = X_update_2.index[I]
        
        try:
        
            player_name = X_update_2.iloc[I]['player']['name']
        
        except:
            player_name = np.nan
        
        if player_name != player:
            X_update_2 = X_update_2.drop(index=index_val)
    
    
 
    prog_carries = X_update_2[X_update_2['prog_carry'] == True]
    
    X_update_2['carry'].replace('', np.nan, inplace=True)
    X_update_2.dropna(subset=['carry'], inplace=True)
       
    car_pos = np.array(prog_carries[['location']])
    car_pos_end = prog_carries['carry']
    
    
    all_pos = np.array(X_update_2[['location']])
    all_pos_end = X_update_2['carry']
    
    pitch = Pitch(pitch_color = '#e1eae4',goal_type='circle')
    fig, ax = pitch.draw(figsize=(8, 4))
    
    if team == 0:
        
        for i in range(len(X_update_2)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(all_pos[i][0][0],80-all_pos[i][0][1],all_pos_end.iloc[i]['end_location'][0],80-all_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 2,color = 'black',alpha=0.2)
            except:
                pass
        
        
        for i in range(len(car_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(car_pos[i][0][0],80-car_pos[i][0][1],car_pos_end.iloc[i]['end_location'][0],80-car_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 2,color = '#37637c')
            except:
                pass
      
        plt.text(y=-8,x=60,s=r'$\rightarrow\rightarrow\rightarrow\rightarrow\rightarrow$'
                 + '\nShotting Direction',horizontalalignment='center',**hfont)
        
        darkblue = mpatches.Patch(color='#8c3655', label='Key Pass')
        lightblue = mpatches.Patch(color='#37637c', label='Progressive Pass')
        lightblue2 = mpatches.Patch(color='black', label='All Passes',alpha=0.2)
        plt.legend(handles=[lightblue2,darkblue,lightblue],fontsize=8,markerscale=0.9,loc='lower left')
        
    if team  == 1:
        
        
        for i in range(len(X_update_2)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(120-all_pos[i][0][0],all_pos[i][0][1],120-all_pos_end.iloc[i]['end_location'][0],all_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 2,color = 'black',alpha=0.2)
            except:
                pass
        
        
        for i in range(len(car_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(120-car_pos[i][0][0],car_pos[i][0][1],120-car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 2,color = '#37637c')
                
            except:
                pass
            
            
        plt.text(y=-8,x=60,s=r'$\leftarrow\leftarrow\leftarrow\leftarrow\leftarrow$'
                 + '\nShotting Direction',horizontalalignment='center',**hfont)
        
        darkblue = mpatches.Patch(color='#8c3655', label='Key Pass')
        lightblue = mpatches.Patch(color='#37637c', label='Progressive Pass')
        lightblue2 = mpatches.Patch(color='black', label='All Passes',alpha=0.2)
        plt.legend(handles=[lightblue2,darkblue,lightblue],fontsize=8,markerscale=0.9,loc='lower right')
    
        

    
    
    
    plt.xlim([-1,121])
    plt.ylim([-1,81])
    plt.title(player + "'s Carries",fontsize=10,**hfont,y=1.01)
    im = image.imread('kicksmarter-logo.png')
    
    newax = fig.add_axes([0.66, 0.92, 0.12, 0.12], anchor='SE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig('Plots/' +str(minute)+'_2.jpeg', dpi=300,bbox_inches='tight')
    plt.show()
    
    plot_name = str(minute)+'_2.jpeg'
    
    return plot_name
  


#Produce second plot for passing - show the anomoulous player's carries on a pitch


def Passes_pitch(data,anomaly,X_update,minute,team):
    
    minute = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']
    
    
    X_update_2 = X_update.copy()
    
    length = len(X_update_2)-1


    hfont = {'fontname':'Helvetica Neue'}
    
    im = image.imread('kicksmarter-logo.png')

    
    for i in range(len(X_update_2)):
        
        I = length - i
        
        index_val = X_update_2.index[I]
        
        try:
        
            player_name = X_update_2.iloc[I]['player']['name']
        
        except:
            player_name = np.nan
        
        if player_name != player:
            X_update_2 = X_update_2.drop(index=index_val)
    
    
 
    prog_pass = X_update_2[X_update_2['prog_pass'] == True]
    key_pass = X_update_2[X_update_2['key_pass'] == True]
    X_update_2['pass'].replace('', np.nan, inplace=True)
    X_update_2.dropna(subset=['pass'], inplace=True)
    
   
    car_pos = np.array(prog_pass[['location']])
    car_pos_end = prog_pass['pass']
    
    k_pos = np.array(key_pass[['location']])
    k_pos_end = key_pass['pass']
    
    all_pos = np.array(X_update_2[['location']])
    all_pos_end = X_update_2['pass']
   
    

    
    pitch = Pitch(pitch_color = '#e1eae4')
    fig, ax = pitch.draw(figsize=(8, 4))
    
    
    if team == 0:
            
        for i in range(len(car_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(car_pos[i][0][0],80-car_pos[i][0][1],car_pos_end.iloc[i]['end_location'][0],80-car_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = '#37637c')
            except:
                pass
            
            
        for i in range(len(k_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(k_pos[i][0][0],80-k_pos[i][0][1],k_pos_end.iloc[i]['end_location'][0],80-k_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = '#8c3655')
            except:
                pass
        
            
        plt.text(y=-8,x=60,s=r'$\rightarrow\rightarrow\rightarrow\rightarrow\rightarrow$'
                 + '\nShotting Direction',horizontalalignment='center',**hfont)
        
        darkblue = mpatches.Patch(color='#8c3655', label='Key Pass')
        lightblue = mpatches.Patch(color='#37637c', label='Progressive Pass')
        lightblue2 = mpatches.Patch(color='black', label='All Passes',alpha=0.2)
        plt.legend(handles=[lightblue2,darkblue,lightblue],fontsize=8,markerscale=0.9,loc='lower left')
        
        for i in range(len(X_update_2)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(all_pos[i][0][0],80-all_pos[i][0][1],all_pos_end.iloc[i]['end_location'][0],80-all_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = 'black',alpha=0.2)
            except:
                pass
          
        
    if team == 1:
        
        for i in range(len(car_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(120-car_pos[i][0][0],car_pos[i][0][1],120-car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = '#37637c')
            except:
                pass
            
            
        for i in range(len(k_pos)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(120-k_pos[i][0][0],k_pos[i][0][1],120-k_pos_end.iloc[i]['end_location'][0],k_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = '#8c3655')
            except:
                pass
            
        for i in range(len(X_update_2)):
            
            
            
            try:
                #plt.plot(car_pos[i][0][0],car_pos[i][0][1],marker='x',color='blue')
                #plt.plot(car_pos_end.iloc[i]['end_location'][0],car_pos_end.iloc[i]['end_location'][1],marker='x',color='red')
                pitch.arrows(120-all_pos[i][0][0],all_pos[i][0][1],120-all_pos_end.iloc[i]['end_location'][0],all_pos_end.iloc[i]['end_location'][1],
                             ax=ax,width = 1.5,color = 'black',alpha=0.2)
            except:
                pass
            
        plt.text(y=-8,x=60,s=r'$\leftarrow\leftarrow\leftarrow\leftarrow\leftarrow$'
                 + '\nShotting Direction',horizontalalignment='center',**hfont)
    
  
        darkblue = mpatches.Patch(color='#8c3655', label='Key Pass')
        lightblue = mpatches.Patch(color='#37637c', label='Progressive Pass')
        lightblue2 = mpatches.Patch(color='black', label='All Passes',alpha=0.2)
        plt.legend(handles=[lightblue2,darkblue,lightblue],fontsize=8,markerscale=0.9,loc='lower right')
    
    
     
    
    plt.xlim([-1,121])
    plt.ylim([-1,81])
    plt.title(player + "'s Passes",fontsize=10,**hfont,y=1.01)
    
    im = image.imread('kicksmarter-logo.png')
    
    newax = fig.add_axes([0.66, 0.92, 0.12, 0.12], anchor='SE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig('Plots/'+str(minute)+'_2.jpeg', dpi=300,bbox_inches='tight')
    plt.show()
    
    plot_name = str(minute)+'_2.jpeg'
    
    return plot_name
    
        

#Produce energy plots - comparing the anomoulous player to their teamates 

def Energy_plot(data,anomaly,minute):
    
    minute_sec = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']
    
    full_team = data.loc[anomaly]['all_team']
    
    if anomaly == 'MCWFC_energy_splits':
        color = '#34798d'
            
    if anomaly == 'o_energy_splits':
        color = '#781f25'
    
        


    fig,ax = plt.subplots(figsize=(12,8))

    for i in range(len(full_team)):
        
        if full_team.index[i] == player:
            color = '#d45e5e'
        
        plt.bar(full_team.index[i].replace(' ','\n'),full_team[i],color='#37637c')
        plt.xticks(fontsize=8)
        
    
    hfont = {'fontname':'Helvetica Neue'}
    plt.grid()    
    
    if anomaly == 'o_energy_splits':
        
        if minute % 10 == 5:
            text = player + ' has had the biggest drop-off in their distance covered in the past 5 minutes - it might be worth targeting them.'
            plt.title("Opposition - % difference in distance covered in\nminutes "+str(minute-5)+'" - '+str(minute) + '" compared to ' +str(minute-10)+'" - '+str(minute-5)+'"',**hfont)
            plt.ylabel('% difference in distance covered',**hfont)
            
            im = image.imread('kicksmarter-logo.png')
            
            newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
            newax.imshow(im)
            newax.axis('off')
            
            plt.savefig('Plots/' +str(minute_sec)+'.jpeg', dpi=300,bbox_inches='tight')
            plt.show()
     
        if minute % 10 == 0:
            text = player + ' has had the biggest drop-off in their distance covered in the past 10 minutes - it might be worth targeting them.'
            plt.title("Opposition - % difference in distance covered in\nminutes "+str(minute-10)+'" - '+str(minute) + '" compared to ' +str(minute-20)+'" - '+str(minute-10)+'"',**hfont)
            plt.ylabel('% difference in distance covered',**hfont)
            
            im = image.imread('kicksmarter-logo.png')
            
            newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
            newax.imshow(im)
            newax.axis('off')
            
            plt.savefig('Plots/' +str(minute_sec)+'.jpeg', dpi=300,bbox_inches='tight')
            plt.show()
            
    if anomaly == 'MCWFC_energy_splits':
        
        if minute % 10 == 5:
            text = player + ' has had the biggest drop-off in their distance covered in the past 5 minutes, it might be worth taking them off.'
            plt.title("MCWFC - % difference in distance covered in\nminutes "+str(minute-5)+'" - '+str(minute) + '" compared to ' +str(minute-10)+'" - '+str(minute-5)+'"',**hfont)
            plt.ylabel('% difference in distance covered',**hfont)
            
            im = image.imread('kicksmarter-logo.png')
            
            newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
            newax.imshow(im)
            newax.axis('off')
            
            plt.savefig('Plots/' +str(minute_sec)+'.jpeg', dpi=300,bbox_inches='tight')
            plt.show()
     
        if minute % 10 == 0:
            text = player + ' has had the biggest drop-off in their distance covered in the past 10 minutes, it might be worth taking them off.'
            plt.title("MCWFC - % difference in distance covered in\nminutes "+str(minute-10)+'" - '+str(minute) + '" compared to ' +str(minute-20)+'" - '+str(minute-10)+'"',**hfont)
            plt.ylabel('% difference in distance covered',**hfont)
            
            im = image.imread('kicksmarter-logo.png')
            
            newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
            newax.imshow(im)
            newax.axis('off')
            
            plt.savefig('Plots/' +str(minute_sec)+'.jpeg', dpi=300,bbox_inches='tight')
            plt.show()
            
    plot_name = str(minute_sec)+'.jpeg'
                
    return text, plot_name


#Produce involvement plots - comparing the anomoulous player to their teamates 
  
def Involve_plot(data,anomaly,minute,team_data,team):
    
    minute = minute*60
    
    vals = data.loc[anomaly]['worst_val']
    player = data.loc[anomaly]['player']

    fig,ax = plt.subplots(figsize=(12,8))

    for i in range(len(team_data)):
        

        
        
        if team == 0:
            color = '#34798d'
        
            if list(team_data.keys())[i] == player:
                color = '#97cad8'
                
        if team == 1:
            color = '#781f25'
        
            if list(team_data.keys())[i] == player:
                color = '#d45e5e'
        
        plt.bar(list(team_data.keys())[i].replace(' ','\n'),list(team_data.values())[i],color=color)
        plt.xticks(fontsize=8)
        
    hfont = {'fontname':'Helvetica Neue'}
    plt.grid() 
    
    
    
    if anomaly == 'MCWFC_involved':
        
        text = player + ' has played a part in the build up to ' + str(vals) + ' shots so far - more than any other player for us.\n\nNote: Build-up = Played one of the last 5 passes in the build up to a shot.'
        plt.title("MCWFC - Players Involved in Shots\n (Involved in 5 passes prior to shot)",**hfont,y=1.01)
        plt.ylabel('Number of Shot Involvements',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
            
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()

        
    if anomaly == 'other_involved':
        
        text = player + ' has played a part in the build up to ' + str(vals) + ' shots so far - more than any other player for the opposition so far.\n\nNote: Build-up = Played one of the last 5 passes in the build up to a shot.'
        plt.title("Opposition - players involved in shots\n (Involved in 5 passes prior to shot)",**hfont,y=1.01)
        plt.ylabel('Number of shot involvements',**hfont)
        
        im = image.imread('kicksmarter-logo.png')
        
        newax = fig.add_axes([0.74, 0.885, 0.12, 0.12], anchor='SE')
        newax.imshow(im)
        newax.axis('off')
            
        plt.savefig('Plots/' +str(minute)+'.jpeg', dpi=300,bbox_inches='tight')
        plt.show()
   
    plot_name = str(minute)+'.jpeg'
    
    return text,plot_name



#Produce heatmap for the anomoulous player in energy

def Energy_heat(data,anomaly,minute,X_update,team):
    
    minute = 25
    
    player = 'Kerstin Yasmijn Casparij'
    
    X_update = X_update[X_update['minute'] < minute]
    
    X_update_2 = X_update.copy()
    
    minute = minute*60
    
    length = len(X_update_2)-1
    
    hfont = {'family':'Helvetica Neue'}

    
    for i in range(len(X_update_2)):
        
        I = length - i
        
        index_val = X_update_2.index[I]
        
        try:
        
            player_name = X_update_2.iloc[I]['player']['name']
        
        except:
            player_name = np.nan
        
        if player_name != player:
            X_update_2 = X_update_2.drop(index=index_val)
    


    
    player_pos = np.array(X_update_2[['location']])
    
    
    Xdata = []
    Ydata = []
    
    
        
        #plt.plot(player_pos[i][0][0],80-player_pos[i][0][1],marker='x',color='red')
    
    
    if team == 0:
        cmap = 'Blues'
        
        for i in range(len(player_pos)):
            
            try:
                Xdata.append(player_pos[i][0][0])
                Ydata.append(player_pos[i][0][1])
            except:
                pass
            
    
    if team == 1:
        cmap = 'Reds'
        
    
        for i in range(len(player_pos)):
            
            try:
                Xdata.append(120-player_pos[i][0][0])
                Ydata.append(80-player_pos[i][0][1])
            except:
                pass
            
        

    
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              )
    fig, ax = pitch.draw(figsize=(8, 4))
    stats = pitch.bin_statistic(Xdata, Ydata,bins=(20, 20))
    stats['statistic'] = gaussian_filter(stats['statistic'], 1)
    pcm = pitch.heatmap(stats, ax=ax,cmap=cmap)
    plt.title("Kerstin Casparij's Heatmap",y=0.96,fontsize=12.5,**hfont)
    plt.text(y=88,x=60,s=r'$\rightarrow\rightarrow\rightarrow\rightarrow\rightarrow$'
             + '\nShotting Direction',horizontalalignment='center',**hfont)
    im = image.imread('kicksmarter-logo.png')
    
    newax = fig.add_axes([0.66, 0.92, 0.12, 0.12], anchor='SE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig('Plots/' +str(minute)+'_2.jpeg', dpi=300,bbox_inches='tight')
    plt.show()
    
    plot_name = str(minute)+'_2.jpeg'
    
    return plot_name
  