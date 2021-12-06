#flask imports
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired

#sql imports
import sqlite3
from sqlite3 import Error

#init db connection
database = r"test.db"

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'tanner-is-marginally-gay'

# Flask-Bootstrap requires this line
Bootstrap(app)

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
    if form.validate_on_submit():

        pre_check = '''SELECT count(*) from player where p_name = "{}" and p_sport = "{}" '''.format(form.name.data, form.sportName.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "You've already registered for {}!".format(form.SportName.data)
            return render_template('player.html', form=form, message=error_message)

        isCaptain = 0

        if form.isCaptain.data == "Yes":
            isCaptain = 1


        query = '''INSERT INTO Player VALUES
        ('{}', {}, {}, '{}', {}, '{}')'''.format(form.name.data, form.height.data, form.weight.data, form.teamName.data, isCaptain ,form.sportName.data)
        cursor.execute(query)
        conn.commit()
        print("inserted player: {} into db".format(form.name.data))
    conn.close()

    return render_template('player.html', form=form, message=message)


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

    message = ""
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


    return render_template('team.html', form=team, message=message)



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
    






'''
TOD-O:
 Pages for ingestion: match, record
 ***sorting page****
'''



app.run()