import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import poisson
import streamlit


def team(name, data):
    team1_= data[data['team1']==name]
    team2_= data[data['team2']==name]
    num_season = team1_['season'].max()
    season1= team1_[team1_['season']==num_season]
    season2= team2_[team2_['season']==num_season]
    return season1, season2

def scored_home_away(name, data):
    s1, s2= team(name, data)

    goals_home=s1[['score1', 'team1']].groupby(by='score1', as_index=False).count()
    goals_home.columns=['scored', 'home']
    goals_home

    goals_away= s2[['score2', 'team2']].groupby(by='score2', as_index=False).count()
    goals_away.columns= ['scored', 'away']
    goals_away

    goals_home_away= goals_home.merge(goals_away, on=['scored'], how='outer')
    goals_home_away.fillna(0, inplace=True)
    
    return goals_home_away


def conceded_home_away(name,data):
    s1, s2= team(name, data)

    goals_home=s1[['score2', 'team1']].groupby(by='score2', as_index=False).count()
    goals_home.columns=['conceded', 'home']
    goals_home

    goals_away= s2[['score1', 'team2']].groupby(by='score1', as_index=False).count()
    goals_away.columns= ['conceded', 'away']
    goals_away

    goals_home_away= goals_home.merge(goals_away, on=['conceded'], how='outer')
    goals_home_away.fillna(0, inplace=True)
    
    return goals_home_away

def goal_dist(mean, num_goals):
    ones= np.ones((1,num_goals+1))
    goals= np.linspace(0,num_goals,num_goals+1)
 
    return poisson.pmf(ones*goals, mean)


def bayes_table(df, goals):
    home_rate= df.drop(['away'], axis=1)
    home_rate=home_rate[home_rate['home'] != 0]
    home_rate= (home_rate.iloc[:, 0]*home_rate.iloc[:, 1]).sum()/ home_rate['home'].sum()

    away_rate= df.drop(['home'], axis=1)
    away_rate=away_rate[away_rate['away'] != 0]
    away_rate= (away_rate.iloc[:, 0]*away_rate.iloc[:, 1]).sum()/ away_rate['away'].sum()

    tbl= np.concatenate( [goal_dist(home_rate, goals), goal_dist(away_rate, goals)] ).T
    tbl= tbl/np.sum(tbl)

    return pd.DataFrame(tbl, columns=['home', 'away'])


def bayes(df, state) :   
    P_A=df.sum(axis=1)
    if state== 'home':
        P_B_A=df.iloc[:,0]/P_A
        P_B=df.iloc[:,0].sum()
        return (P_A*P_B_A)/P_B
    else:
        P_B_A=df.iloc[:,1]/P_A
        P_B=df.iloc[:,1].sum()
        return (P_A*P_B_A)/P_B



def dist(team1, team2, data):

    goals=7
    show=6
    
    home_score= scored_home_away(team1, data)
    home_score=bayes_table(home_score, goals)
    home_score=bayes(home_score, 'home')
    home_score

    away_concede= conceded_home_away(team2, data)
    away_concede=bayes_table(away_concede, goals)
    away_concede=bayes(away_concede, 'away')
    away_concede
    
    home_score=np.array(home_score*away_concede)

    home_concede= conceded_home_away(team1, data)
    home_concede=bayes_table(home_concede, goals)
    home_concede=bayes(home_concede, 'home')
    home_concede

    away_score= scored_home_away(team2, data)
    away_score=bayes_table(away_score, goals)
    away_score=bayes(away_score, 'away')
    away_score

    away_score= np.array(away_score*home_concede)

    ones=np.ones((goals+1,goals+1))
    team1_ones= ones*home_score
    team2_ones=ones*away_score
    goals_dist=team1_ones*team2_ones.T
    goals_dist =goals_dist/np.sum(goals_dist)
    
    disp= goals_dist[:show, :show]
    team1_win= np.triu(goals_dist,1).sum()*100
    draw= np.trace(goals_dist)*100
    team2_win= np.tril(goals_dist,-1).sum()*100

    fig=plt.figure(figsize=(30,20))  
    fig.suptitle(f'{team1} Vs {team2}', size=35)
    plt.rc('font', size=23)
    mylabels = [team1, "Draw", team2]
    mycolors = ["red", "purple", "blue"]
    plt.legend( mylabels, loc ="upper left")
    plt.subplot(2,2,1)
    y = [team1_win, draw, team2_win]
    mylabels = [team1, "Draw", team2]
    mycolors = ["red", "purple", "blue"]
    plt.pie(y, colors = mycolors,autopct='%1.1f%%')
    plt.legend( mylabels, loc ="upper left")
    plt.title('Odds Of Winning')
    plt.subplot(2,2,2)
    plt.bar(list(range(show)), disp.sum(axis=0)*100, color='red')
    title= team1+' Goal Distribution'
    plt.title(title)

    plt.subplot(2,2,3)
    plt.barh(list(range(show)), disp.sum(axis=1)*100, color='blue')
    title= team2+' Goal Distribution'
    plt.title(title)

    plt.subplot(2,2,4)
    color=sns.color_palette("Purples", as_cmap=True)
    sns.heatmap(disp*100, cmap=color, annot= True, fmt='.2f', cbar= False)
    plt.title('Aggregated Goal Distribution')
    plt.xlabel(team1)
    plt.ylabel(team2)
    
    #plt.show()
    streamlit.pyplot(fig)
