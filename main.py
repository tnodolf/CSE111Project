#random
import random

#flask imports
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired

#sql imports
import sqlite3
from sqlite3 import Error

#init db connection
database = r"test.db"

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'secret-key'

# Flask-Bootstrap requires this line
Bootstrap(app)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')



@app.route('/player', methods=['GET', 'POST'])
def player():
    class PlayerForm(FlaskForm):
        query = '''select s_name from sport'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])

        name = StringField('Name:', validators=[DataRequired()])
        height = DecimalField('Height (inches):', validators=[DataRequired()])
        weight = DecimalField('Weight (lbs):', validators=[DataRequired()])
        sportName = SelectField('Sport Name:', choices=sportsNames)
        leagueName = SelectField('League name:', choices=[], validate_choice=False)
        teamName = SelectField('Team Name (if free agent select "free agent"):' , choices=[], validate_choice=False)
        isCaptain = SelectField('Are you the captain?:', choices= ["Yes", "No"])
        submit = SubmitField('Submit')
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    # create a database connection
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    #get sport names: 

    form = PlayerForm()
    message = ""
    success_message = ""
    if form.validate_on_submit():

        pre_check = '''SELECT count(*) from player where p_name = "{}" and p_sport = "{}" '''.format(form.name.data, form.sportName.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "You've already registered for {}!".format(form.SportName.data)
            return render_template('player.html', form=form, message=error_message, success_message="")

        isCaptain = 0

        if form.isCaptain.data == "Yes":
            isCaptain = 1


        query = '''INSERT INTO Player VALUES
        ('{}', {}, {}, '{}', {}, '{}')'''.format(form.name.data, form.height.data, form.weight.data, form.teamName.data, isCaptain ,form.sportName.data)
        cursor.execute(query)
        conn.commit()
        print("inserted player: {} into db".format(form.name.data))
        success_message = "created player: {}".format(form.name.data)

    conn.close()

    return render_template('player.html', form=form, message=message, success_message=success_message)


@app.route('/sport', methods=['GET', 'POST'])
def sport():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    # create a database connection

    class SportForm(FlaskForm):
        name = StringField('Sport Name:', validators=[DataRequired()])
        submit = SubmitField('Submit')

    class LeagueForm(FlaskForm):
        query = '''select s_name from sport order by s_name'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])
        leagueName = StringField('League Name:', validators=[DataRequired()])
        sport = SelectField('Sport Name:', choices=sportsNames, validators=[DataRequired()])
        submitLeague = SubmitField('Submit')
        

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    sportSubmit = SportForm()
    leagueSubmit = LeagueForm()
    message = ""

    sportNames = []
    sportQuery = '''SELECT s_name from sport order by s_name'''
    result = conn.execute(sportQuery)
    for row in result:
        sportNames.append(row[0])
    

    if sportSubmit.validate_on_submit():
        pre_check = '''SELECT count(*) from sport where s_name = "{}" '''.format(sportSubmit.name.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "The sport {} already exists.".format(sportSubmit.name.data)
            sportNames = []
            sportQuery = '''SELECT s_name from sport'''
            result = conn.execute(sportQuery)
            for row in result:
                sportNames.append(row[0])
            return render_template('sport.html', sportForm=sportSubmit, leagueForm=leagueSubmit, message=error_message, sportNames=sportNames)

        query = '''INSERT INTO SPORT VALUES ('{}', 0, 0)'''.format(sportSubmit.name.data)
        cursor.execute(query)
        conn.commit()
        print("created sport: {} in db".format(sportSubmit.name.data))
        class LeagueFormNew(FlaskForm):
            query = '''select s_name from sport order by s_name'''
            conn = sqlite3.connect(database)
            result = conn.execute(query)
            sportsNames = []
            for row in result:
                sportsNames.append(row[0])
            leagueName = StringField('League Name:', validators=[DataRequired()])
            sport = SelectField('Sport Name:', choices=sportsNames, validators=[DataRequired()])
            submitLeague = SubmitField('Submit')
        leagueSubmit = LeagueFormNew()
    

    if leagueSubmit.validate_on_submit():
        pre_check = '''SELECT count(*) from league where l_name = "{}" and l_sportsname = "{}" '''.format(leagueSubmit.leagueName.data, leagueSubmit.sport.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if val != 0:
            error_message = "The league {} already exists within the sport {}.".format(leagueSubmit.leagueName.data, leagueSubmit.sport.data)
            return render_template('sport.html', sportForm=sportSubmit, leagueForm=leagueSubmit, message=error_message, sportNames=sportNames)

        query = '''INSERT INTO LEAGUE VALUES ("{}", "{}", 0, IFNULL( ((SELECT MAX(l_leaguekey) from league) + 1), 0))'''.format(leagueSubmit.sport.data, leagueSubmit.leagueName.data)
        cursor.execute(query)
        conn.commit()
        print("created league: {} in db".format(leagueSubmit.leagueName.data))

        updateSport = '''UPDATE Sport SET s_numleagues = s_numleagues + 1 WHERE s_name = "{}" '''.format(leagueSubmit.sport.data)
        cursor.execute(updateSport)
        conn.commit()
        print("incremented sports")


    sportNames = []
    sportQuery = '''SELECT s_name from sport order by s_name'''
    result = conn.execute(sportQuery)
    for row in result:
        sportNames.append(row[0])
    conn.close()

    print(sportNames)

    return render_template('sport.html', sportForm=sportSubmit,leagueForm=leagueSubmit, message=message, sportNames=sportNames)

@app.route('/referee', methods=['GET', 'POST'])
def referee():
    class RefForm(FlaskForm):
        query = '''select l_name from league'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        leagueNames = []
        for row in result:
            leagueNames.append(row[0])

        name = StringField('Name:', validators=[DataRequired()])
        phonenumber = StringField('Phone Number:', validators=[DataRequired()])
        league = SelectField('League Name:', choices = leagueNames)
        submit = SubmitField('Submit')

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    form = RefForm()
    message = ""
    
    leagueNames = []
    leagueQuery = '''SELECT l_name from league'''.format(form.league.data)
    result = conn.execute(leagueQuery)
    
    for row in result:
        leagueNames.append(row[0])

    if form.validate_on_submit():

        pre_check = '''SELECT count(*) FROM league, referee WHERE r_leaguekey = l_leaguekey AND r_name = "{}" '''.format(form.name.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "The referee {} already exists in this league.".format(form.name.data)
            return render_template('referee.html', form=form, message=error_message, sportNames=sportNames)

        lKey = conn.execute('''SELECT l_leaguekey from league WHERE l_name = "{}" '''.format(form.league.data))
        lSport = conn.execute('''SELECT l_sportsname from league WHERE l_name = "{}" '''.format(form.league.data))
        
        keyTest = None
        for row in lKey:
            keyTest = row[0]

        sportName = ""
        for row in lSport:
            sportName = row[0]

        query = '''INSERT INTO referee VALUES ('{}', '{}', {}, {})'''.format(sportName, form.name.data, form.phonenumber.data, keyTest)
        cursor.execute(query)
        conn.commit()
        print("created referee: {} in db".format(form.name.data))

    conn.close()

    return render_template('referee.html', form=form, message=message, leagueNames=leagueNames)


@app.route('/team', methods=['GET', 'POST'])
def team():
    class teamForm(FlaskForm):
        query = '''select s_name from sport'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])
        sportName = SelectField('Sport Name:', choices = sportsNames)
        leagueName = SelectField('League Name:'  ,choices = [], validate_choice=False)
        teamName = StringField('Team Name:')
        submit = SubmitField('Submit')

    team = teamForm()

    success_message = ""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if team.validate_on_submit():
        findLeagueKey = '''select l_leaguekey from League where l_name="{}" and l_sportsname="{}" '''.format(team.leagueName.data, team.sportName.data)
        leagueKey = None
        result = conn.execute(findLeagueKey)
        for row in result:
            leagueKey = row[0]
        
        createTeam = '''INSERT INTO team values ("{}", 0, "{}")'''.format(leagueKey, team.teamName.data)
        cursor.execute(createTeam)
        conn.commit()
        print("created team {}".format(team.teamName.data))

        updateLeague = '''UPDATE League SET l_numteams = l_numteams + 1 WHERE l_leaguekey = "{}" '''.format(leagueKey)
        cursor.execute(updateLeague)
        conn.commit()
        print("updated league")

        updateSport = '''UPDATE Sport SET s_numteams = s_numteams + 1 WHERE s_name = "{}" '''.format(team.sportName.data)
        cursor.execute(updateSport)
        conn.commit()
        print("updated sport")

        createRecord = '''INSERT INTO Record VALUES ("{}", 0, 0)'''.format(team.teamName.data)
        cursor.execute(createRecord)
        conn.commit()
        print("created record")

        success_message = "created team {}".format(team.teamName.data)


    return render_template('team.html', form=team, message=success_message)


@app.route('/make-match', methods=['GET', 'POST'])
def match():
    class dateForm(FlaskForm):
        query = '''select s_name from sport'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])
        sportName = SelectField('Sport Name:', choices = sportsNames)
        leagueName = SelectField('League Name:'  ,choices = [], validate_choice=False)
        homeTeamName = SelectField('Home Team Name:' , choices=[], validate_choice=False)
        awayTeamName = SelectField('Away Team Name:' , choices=[], validate_choice=False)
        date = DateField('Start Date', format='%Y-%m-%d')
        submit = SubmitField('Submit')

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    matchForm = dateForm()
    error_message = ""
    success_message = ""

    if matchForm.validate_on_submit():
        if (matchForm.awayTeamName.data == matchForm.homeTeamName.data):
            error_message = "A team must play a different team"
            return render_template('match.html', form=matchForm, error_message=error_message, success_message=success_message)
        
        #Get league key for league name
        lKey = conn.execute('''SELECT l_leaguekey from league WHERE l_name = "{}" '''.format(matchForm.leagueName.data))
        for row in lKey:
            val = row[0]

        #Select all referees
        result = conn.execute('''select r_name from referee where r_leaguekey = "{}" '''.format(val))

        allRefs = []
        numRefs = 0
        refName = ""
        for ref in result:
            numRefs += 1
            allRefs.append(ref[0])
            refName = ref[0]
            print(refName)

        if numRefs > 0:
            refName = allRefs[random.randint(0, numRefs-1)]

        
        createMatch = '''INSERT INTO Match VALUES ('{}', '{}', '{}', 0, 0, '{}');'''.format(refName, matchForm.homeTeamName.data, matchForm.awayTeamName.data, matchForm.date.data )
        cursor.execute(createMatch)
        conn.commit()
        success_message = "Successfully created match!"


    return render_template('match.html', form=matchForm, error_message=error_message, success_message=success_message)


@app.route('/view-matches', methods=['GET','POST'])
def view_matches():
    class scheduleForm(FlaskForm):
        date = DateField('Start Date', format='%Y-%m-%d')
        submit = SubmitField('Submit')
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    scheduleForm = scheduleForm()
    allMatches = []
    
    if scheduleForm.validate_on_submit():
        rawMatches = conn.execute('''select * from match where m_date = "{}" '''.format(scheduleForm.date.data))

        for match in rawMatches:
            matchObj = {}
            matchObj['Referee'] = match[0]
            matchObj['homeTeam'] = match[1]
            matchObj['awayTeam'] = match[2]
            matchObj['homeScore'] = match[3]
            matchObj['awayScore'] = match[4]
            matchObj['date'] = match[5]
            allMatches.append(matchObj)

    return render_template('schedule.html', form=scheduleForm, allMatches=allMatches)


@app.route('/add-score', methods=['GET', 'POST'])
def add_score():
    class scoreForm(FlaskForm):
        date = DateField('Match Date', format='%Y-%m-%d')
        homeTeamName = SelectField('Home Team Name:' , choices=[], validate_choice=False)
        homeTeamScore = DecimalField('Home Team Score:')
        awayTeamName = SelectField('Away Team Name:' , choices=[], validate_choice=False)
        awayTeamScore = DecimalField('Away Team Score:')
        submit = SubmitField('Submit')
    
    scoreForm = scoreForm()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if scoreForm.validate_on_submit():
        query = '''update match set m_teamonescore = {} where m_teamone = "{}" and m_teamtwo = "{}" and m_date = "{}" '''.format(scoreForm.homeTeamScore.data, scoreForm.homeTeamName.data, scoreForm.awayTeamName.data, scoreForm.date.data)
        cursor.execute(query)
        conn.commit()

        query = '''update match set m_teamtwoscore = {} where m_teamone = "{}" and m_teamtwo = "{}" and m_date = "{}"'''.format(scoreForm.awayTeamScore.data, scoreForm.homeTeamName.data, scoreForm.awayTeamName.data, scoreForm.date.data)
        cursor.execute(query)
        conn.commit()

        winner = scoreForm.homeTeamName.data
        loser = scoreForm.awayTeamName.data
        if (scoreForm.awayTeamScore.data > scoreForm.homeTeamScore.data):
            winner = scoreForm.awayTeamName.data
            loser = scoreForm.homeTeamName.data

        query = '''update record set r_wins = r_wins+1 where r_teamname = "{}" '''.format(winner)
        cursor.execute(query)
        conn.commit()

        query2 = '''update record set r_losses = r_losses+1 where r_teamname = "{}" '''.format(loser)
        cursor.execute(query2)
        conn.commit()

        return render_template('score.html', form=scoreForm, success_message="successfully added score")

    return render_template('score.html', form=scoreForm, success_message="")


@app.route("/view-standings", methods=['GET', 'POST'])
def view_standings():
    class standingForm(FlaskForm):
        query = '''select s_name from sport'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])
        sportName = SelectField('Sport Name:', choices = sportsNames)
        leagueName = SelectField('League Name:'  ,choices = [], validate_choice=False)
        submit = SubmitField('Submit')

    standingForm = standingForm()
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    rankings = []

    if standingForm.validate_on_submit(): 
        #get teams in order of 1,0
        query = '''SELECT r_teamname, r_wins, r_losses FROM Record, Team, League WHERE
        r_teamname = t_name AND
        t_leaguekey = l_leaguekey AND
        l_name = '{}' GROUP BY r_teamname order by  r_wins - r_losses desc'''.format(standingForm.leagueName.data)
        counter = 1
        result = conn.execute(query)
        for row in result:
            rankObj = {}
            rankObj[counter] = row[0]
            rankObj["wins"] = row[1]
            rankObj["losses"] = row[2]
            counter += 1
            rankings.append(rankObj)
        
    return render_template('standings.html', form=standingForm, teamNames=rankings)

@app.route("/find-team", methods=['GET', 'POST'])
def view_team():
    class teamForm(FlaskForm):
        query = '''select s_name from sport'''
        conn = sqlite3.connect(database)
        result = conn.execute(query)
        sportsNames = []
        for row in result:
            sportsNames.append(row[0])
        sportName = SelectField('Sport Name:', choices = sportsNames)
        leagueName = SelectField('League Name:'  ,choices = [], validate_choice=False)
        teamName = SelectField('Team Name:', choices = [], validate_choice = False)
        submit = SubmitField('Submit')

    teamForm = teamForm()

    if teamForm.validate_on_submit():
        return redirect('//localhost:5000/get-roster/' + teamForm.teamName.data)
    
    return render_template('find-team.html', form=teamForm, success_message="")
        
    

@app.route('/get-roster/<team>')
def get_roster(team):
    team = team.replace('%20', ' ')
    conn = sqlite3.connect(database)
    query = '''select * from player where p_team = "{}" '''.format(team)
    rawPlayers = conn.execute(query)
    allPlayers = []
    for player in rawPlayers:
        playerObj = {}
        playerObj['name'] = player[0]
        playerObj['height'] = player[1]
        playerObj['weight'] = player[2]
        playerObj['team'] = player[3]
        playerObj['captain'] = player[4]
        playerObj['sport'] = player[5]
        allPlayers.append(playerObj)

    return render_template('roster.html', allPlayers=allPlayers)



#BACKEND ENDPOINTS ACCESSED VIA REQS ONLY
@app.route('/get-league/<sport>')
def get_league(sport):
    sport = sport.replace('%20', ' ')
    conn = sqlite3.connect(database)
    query = '''select l_name from league where l_sportsname = "{}" '''.format(sport)
    result = conn.execute(query)
    leagueNames = []
    for row in result:
        leagueObj = {}
        leagueObj['name'] = row[0]
        leagueNames.append(leagueObj)

    return jsonify({'league_names' : leagueNames})

@app.route('/get-team/<league>')
def get_teams(league):
    league = league.replace('%20', ' ')
    conn = sqlite3.connect(database)

    query = '''select l_leaguekey from league where l_name="{}" '''.format(league)
    result = conn.execute(query)
    leagueKey = None
    for row in result:
        leagueKey = row[0]

    query = '''select t_name from team where t_leaguekey = {}'''.format(leagueKey)
    result = conn.execute(query)
    teamNames = []
    for row in result:
        teamObj = {}
        teamObj['name'] = row[0]
        teamNames.append(teamObj)
    
    teamNames.append({'name':'Free Agent'})

    return jsonify({'team_names' : teamNames})

@app.route('/get-lineup/<date>')
def get_lineup(date):
    conn = sqlite3.connect(database)
    query = '''select * from match where m_date = "{}" '''.format(date)
    result = conn.execute(query)
    matchData = []
    for row in result:
        matchObj = {}
        matchObj['homeTeamName'] = row[1]
        matchObj['awayTeamName'] = row[2]
        matchObj['homeTeamScore'] = row[3]
        matchObj['awayTeamScore'] = row[4]
        matchData.append(matchObj)
    
    return jsonify({'matchData' : matchData})



    






'''
TOD-O:
 Page to show players on teams, filter down from sport
'''



app.run()