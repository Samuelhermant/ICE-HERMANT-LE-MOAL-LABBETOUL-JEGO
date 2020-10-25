# -*- coding: utf-8 -*-
"""
Clémence Le Moal
Alexandra Labbetoul
Samuel Hermant
Martin Jego

M2 EFCE

"""
##################################################################
########KOKKO 5 = DYNAMIC OPTIMIZATION : OPTIMAL FORAGING#########
##################################################################


####IMPORT PACKAGES

import numpy as np
import matplotlib.pyplot as plt


def forage(dmin,dmax,c,f,maxt,maxc):

#EXPLANATION OF THE PARAMETERS :
# dmax= probability of death per time unit if you’re very heavy
# dmin= probability of death per time unit if you’re very lean
# c= rate of consuming resources
# f= feeding efficiency
# maxt= maximum time
# maxc= maximum condition



# This means that best condition is maxc but this is found at row maxc+1
# Terminal reward increases with condition so we already know the values for the last


    Reward_Mat = np.zeros((maxc+1,maxt+1))
    Reward_Mat[:,maxt] =  [x for x in range(0,maxc+1)]
    Reward_Mat #CREATION OF A MATRIX REWARD 
    
    
    # Calculate the robability of death wich increases linearly with body weight

    d = [np.linspace(dmin,dmax,maxc)]
    d = np.append([0], d) #Add 0 wich are the row for dead individuals
    
    # The individual who are alive can either improve or be the same
    P_eat_up = [(1 - d[i])* f for i in range(0,len(d))]
    P_eat_same = [(1 - d[i]) * (1-f) for i in range (0,len(d))]
    P_eat_dead = d
    P_rest_same = 1-c
    P_rest_down = c
    
    
    # Those who already are in top condition can't improve 
    Ptop_eat_same = 1 -d[-1]
    Ptop_eat_dead = d[-1]
    
    # We set the matrices as null
    Reward_If_Forage = np.zeros((maxc+1,maxt))
    Reward_If_Rest = np.zeros((maxc+1,maxt))
    ForageRule = np.zeros((maxc+1,maxt))
    
    # we start from the end of the day and continue backwards
    #Explanation of the backward matrix :
    #We counted the best probabilities by the end reward to the 1st state of the bird for the dynamic optimization
    
    for t in range (maxt-1, -1, -1):
    # individuals who are dead have index 1
    # individuals who are in top condition have index maxc+1
    # Rules for updating fitness values
    # first everyone except those who already are dead, or in top condition
    # We wish to compare two benefits: the expected reward
    # from now onwards if one forages, and if one rests
    
        for i in range(1,maxc):
            Reward_If_Forage[i,t]=P_eat_same[i]*Reward_Mat[i,t+1] +P_eat_up[i]*Reward_Mat[i+1,t+1]+ P_eat_dead[i]*0 
            Reward_If_Rest[i,t]=P_rest_same*Reward_Mat[i,t+1]+P_rest_down*Reward_Mat[i-1,t+1]
    
    #### Special cases
    
    # Dead individuals don’t get rewards
        Reward_If_Forage[0,t]=0 
        Reward_If_Rest[0,t]=0 
        
    
    # Top ones can’t improve their condition, they can be the same or down a condition
        Reward_If_Forage[maxc,t]=Ptop_eat_same*Reward_Mat[maxc,t+1]+Ptop_eat_dead*0 
        Reward_If_Rest[maxc,t]=P_rest_same*Reward_Mat[maxc,t+1]+P_rest_down*Reward_Mat[maxc-1,t+1] 

    
        ForageRule[:,t]= Reward_If_Forage[:,t] > Reward_If_Rest[:,t]
        ForageRule = ForageRule.astype(bool)
     # The output is the ForageRule matrix, with TRUE denoting foraging, and FLASE denoting resting.
  
            
        Reward_Mat[:,t]=ForageRule[:,t]*Reward_If_Forage[:,t] + ~ForageRule[:,t]*Reward_If_Rest[:,t]
    #Fill the matrix with the results of the ForageRule, matrix with TRUE for foraging and FALSE for resting for each condition in every time
    
    
######CREATION OF THE MATRIC PLOT ######
    
    # Setting the plot
    fig, ax = plt.subplots()
    
    ax.locator_params(nbins=3)
    #Setting plot labels
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Condition', fontsize=12)
    ax.set_title('Dynamic optimization model', fontsize=12)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1,)
   #Sets the number of ticks relative to the choice of maxt and maxc
    ax.set_xticks(np.arange(0, maxt+1,1));
    ax.set_yticks(np.arange(1, maxc+2,1));
    
    
    #Loop
    bound=1 #Indicates the width of the square, must be between 0 and 1
    for t in range(maxt) :
        for condition in range (0,maxc+1) : #We start after the dead line
        # Defines the outline of the square 
         xcoord=[t,t, t+bound, t+bound] 
         ycoord=[condition+bound, condition, condition, condition + bound] 
         #TRUE denoting foraging is blue, resting is white
         if (ForageRule[condition,t]==True) :
             ax.fill(xcoord,ycoord,"b") 
         else : 
             ax.fill(xcoord,ycoord,"w")

forage(0, 0.01, 0.4, 0.8, 5, 6) 
#Example with a linear augmentation of predation for the top condition individuals



####NOW YOU CAN CHNGE THE PARAMETERS TO SEE IF THERE ARE DIFFERENT STRATEGIES#####
##Example : you can change the parameter dmin and dmax equal to 0.01 to see if the decisions will change with a probability of 10% for the individual to be predated
