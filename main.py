import pandas as pd
import numpy as np
import streamlit as st
from bayes import dist

#data = pd.read_csv('spi_matches.csv')
dev= True

if dev==True:
    data = pd.read_csv('https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv')
    #data.to_csv('spi_matches.csv', index=False)
else:
    data = pd.read_csv('spi_matches.csv')

st.write('# Home')
'\n'
leagues=["FA Women\'s Super League", 'French Ligue 1', 'Barclays Premier League', 'Spanish Primera Division', 'Italy Serie A', 'German Bundesliga', 'UEFA Champions League', 'Mexican Primera Division Torneo Clausura', 'Major League Soccer', 'Swedish Allsvenskan', 'Norwegian Tippeligaen', "National Women's Soccer League", 'Brasileiro Série A', 'Russian Premier Liga', 'Mexican Primera Division Torneo Apertura', 'Austrian T-Mobile Bundesliga', 'Swiss Raiffeisen Super League', 'French Ligue 2', 'German 2. Bundesliga', 'English League Championship', 'Scottish Premiership', 'Portuguese Liga', 'Dutch Eredivisie', 'Turkish Turkcell Super Lig', 'Spanish Segunda Division', 'Italy Serie B', 'Argentina Primera Division', 'UEFA Europa League', 'United Soccer League', 'Danish SAS-Ligaen', 'Belgian Jupiler League', 'Japanese J League', 'Chinese Super League', 'English League One', 'South African ABSA Premier League', 'English League Two', 'Greek Super League', 'Australian A-League', 'NWSL Challenge Cup', 'UEFA Europa Conference League']
leagues=sorted(leagues)

league1 = st.selectbox('Home Team League',leagues)
'You selected: ', league1
l1=data[data['league']==league1]

teams1=list(l1['team1'].unique())
teams1=sorted(teams1)

team1 = st.selectbox('Home Team', teams1)
'You selected: ', team1
'\n'
st.write('# Away')
'\n'
league2 = st.selectbox('Away Team League',leagues)
'You selected: ', league2
l2=data[data['league']==league2]

teams2=list(l2['team1'].unique())
teams2=sorted(teams2)


team2 = st.selectbox('Away Team', teams2)
'You selected: ', team2


if st.button('Submit'):
    try:
        dist(team1, team2, data)
    except:
        pass
