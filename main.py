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

#configuring form
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

class SportForm(FlaskForm):
    name = StringField('Sport Name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/player', methods=['GET', 'POST'])
def player():
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
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    form = SportForm()
    message = ""
    
    sportNames = []
    sportQuery = '''SELECT s_name from sport'''
    result = conn.execute(sportQuery)
    for row in result:
        sportNames.append(row[0])

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
    conn.close()

    return render_template('sport.html', form=form, message=message, sportNames=sportNames)


app.run()