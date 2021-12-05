#flask imports
from flask import Flask, render_template, redirect, url_for
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
        team = StringField('Team Name (if free agent leave blank):')
        sport = SelectField('Sport Name:', choices=sportsNames)
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

        pre_check = '''SELECT count(*) from player where p_name = "{}" and p_sport = "{}" '''.format(form.name.data, form.sport.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "You've already registered for {}!".format(form.sport.data)
            return render_template('player.html', form=form, message=error_message)

        query = '''INSERT INTO Player VALUES
        ('{}', {}, {}, '{}', 0, '{}')'''.format(form.name.data, form.height.data, form.weight.data, form.team.data, form.sport.data)
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

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    form = SportForm()
    message = ""
    

    if form.validate_on_submit():

        pre_check = '''SELECT count(*) from sport where s_name = "{}" '''.format(form.name.data)
        result = conn.execute(pre_check)
        val = 0

        for row in result:
            val = row[0]

        if (val != 0):
            error_message = "The sport {} already exists.".format(form.name.data)
            return render_template('sport.html', form=form, message=error_message, sportNames=sportNames)

        query = '''INSERT INTO SPORT VALUES ('{}', 0, 0)'''.format(form.name.data)
        cursor.execute(query)
        conn.commit()
        print("created sport: {} in db".format(form.name.data))
    
    sportNames = []
    sportQuery = '''SELECT s_name from sport'''
    result = conn.execute(sportQuery)
    for row in result:
        sportNames.append(row[0])
    conn.close()

    print(sportNames)

    return render_template('sport.html', form=form, message=message, sportNames=sportNames)

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



'''
TOD-O:
 Pages for ingestion: league, match, record, team
 ***sorting page****
'''



app.run()