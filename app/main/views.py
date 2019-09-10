from .forms import featureForm, sizeForm, teamForm
from flask import Flask, Markup, render_template, session, redirect, url_for, flash, request, Response
from . import main
from flask_login import login_required
from .functions import feature_rank
import json
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
import datetime
from .data.mlb.compare_teams import compare_teams
from config import config

abbreviations = {
'LAD':'Los Angeles Dodgers',
'NYY':'New York Yankees',
'HOU':'Houston Astros',
'MIN':'Minnesota Twins',
'ATL':'Atlanta Braves',
'CLE':'Cleveland Indians',
'OAK':'Oakland Athletics',
'TBR':'Tampa Bay Rays',
'WSN':'Washington Nationals',
'CHC':'Chicago Cubs',
'STL':'St. Louis Cardinals',
'NYM':'New York Mets',
'PHI':'Philadelphia Phillies',
'BOS':'Boston Red Sox',
'MIL':'Milwaukee Brewers',
'ARI':'Arizona Diamondbacks',
'SFG':'San Francisco Giants',
'TEX':'Texas Rangers',
'LAA':'Los Angeles Angels',
'CIN':'Cincinnati Reds',
'SDP':'San Diego Padres',
'COL':'Colorado Rockies',
'CHW':'Chicago White Sox',
'SEA':'Seattle Mariners',
'PIT':'Pittsburgh Pirates',
'TOR':'Toronto Blue Jays',
'MIA':'Miami Marlins',
'KCR':'Kansas City Royals',
'BAL':'Baltimore Orioles',
'DET':'Detroit Tigers',
}

@main.route('/', methods=['GET','POST'])
def index():
    session['SELECTED_FEATURES'] = []
    session['N_FEATURES'] = 0
    # form = sportForm()
    # if form.validate_on_submit():
    #     redirect(url_for('main.board'))
    return render_template('index.html')

@main.route('/features/<sport>',methods=['GET','POST'])
def features(sport):

    session['SPORT'] = sport

    result = None
    s_key = sport.upper() + '_FEATURES_SELECTED'
    f_key = sport.upper() + '_FEATURES'
    loc = "http://localhost:5000/features/" + sport
    feature_html = '<ul id="sortable1" class="connectedSortable">'
    iter = '00'
    if session.get(f_key) is not None:
        for feature in session.get(f_key):
            feature_html += '<li id="f_' + iter + '" class="ui-state-default">' + feature + '</li>'
            iter = str(int(iter)+1)
            if len(iter) == 1:
                iter = '0' + iter
    feature_html += '</ul>'
    feature_html = Markup(feature_html)

    if request.method == 'POST':
        f = request.form
        for key, value in f.items():
            print(value)
            result = []
            for char in range(len(value)-2):
                if value[char] == '=':
                    result.append(value[char+1]+value[char+2])
            session[s_key] = result
            return redirect(url_for('main.board',sport=sport))
    return render_template('features.html',loc=loc,result=result,feature_html=feature_html)

@main.route('/board/<sport>',methods=['GET','POST'])
def board(sport):

    s_key = sport.upper() + '_FEATURES_SELECTED'
    f_key = sport.upper() + '_FEATURES'
    to_features = "http://localhost:5000/features/" + sport

    session['SPORT'] = sport

    cwd = os.getcwd()
    session['DATAPATH'] = filename = cwd + '\\' + 'app\\main\\data\\' + sport + '\\all_data.csv'
    sport_template = sport + '/board.html'

    df = pd.read_csv(filename)
    session[f_key] = [i for i in df][1:]

    if session.get(s_key) is None:
        return redirect(url_for('main.features',sport=sport))

    team_form = teamForm()

    team_form.team1.choices = [(t,t) for t in df['Team']]
    team_form.team2.choices = [(t,t) for t in df['Team']]

    selected = [session.get(f_key)[int(i)] for i in session.get(s_key)]

    result = None
    for col in df:
        if col != 'Team' and col != 'League':
            df[col] = df[col]/df[col].median()

    if team_form.validate_on_submit():
        pass
        team1 = df[df['Team'] == team_form.team1.data]
        team2 = df[df['Team'] == team_form.team2.data]
        print(team1)
        team1_score = 0
        team2_score = 0
        for f in selected:
            team1_score += float(team1[f])
            team2_score += float(team2[f])
        if team1_score > team2_score:
            result = team_form.team1.data
        else:
            result = team_form.team2.data

    return render_template(sport_template,sport=sport,team_form=team_form,selected=selected,\
    result=result,to_features=to_features)

@main.route('/mlb',methods=['GET','POST'])
def mlb():
    games = []
    url = 'https://www.baseball-reference.com/previews/'

    # dff = pd.read_sql('sox',config['Dev1'].SQLALCHEMY_DATABASE_URI)
    # del dff['index']
    # print(dff)

    # cwd = os.getcwd()
    # filename = cwd + '\\' + 'app\\main\\data\\mlb\\CHW.csv'
    # df = pd.read_csv(filename)
    # df.to_sql('sox',config['Dev1'].SQLALCHEMY_DATABASE_URI)

    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content,"html.parser")
    previews = content.findAll('div',attrs={"class":"game_summary nohover"})
    for preview in previews:
        team_abrs = [i.text for i in preview.findAll('strong')]
        tables = preview.findAll('table',attrs={"class":"teams"})
        if len(team_abrs) != 2:
            continue
        for table in tables:
            teams = table.findAll('tr',attrs={"class":""})
            team_short_name = []
            records = []
            for team in teams:
                team_short_name.append(team.findAll('td')[0].find('a').text)
                records.append(team.findAll('td')[0].find('span').text.replace('\xa0',''))
                pos_time = team.findAll('td')[2].text
                if pos_time[0] in ['1','2','3','4','5','6','7','8','9','0']:
                    game_time = pos_time[:-4]


        link = '/'+'game' +'/'+team_abrs[0]+'-'+team_abrs[1]+'/'+str(datetime.date.today())
        game_dict={
        'abrs':team_abrs,
        'short_names':team_short_name,
        'records':records,
        'time':game_time,
        'link': link
        }
        games.append(game_dict)
    return render_template('mlb.html',games=games,abbreviations=abbreviations)

@main.route('/game/<teams>/<date>',methods=['GET','POST'])
def game(teams,date):
    away = abbreviations[teams[:3]]
    home = abbreviations[teams[4:]]
    return render_template('game.html',away=away,home=home)
