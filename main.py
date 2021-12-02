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
class NameForm(FlaskForm):
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


@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    # create a database connection
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    #get sport names: 

    form = NameForm()
    message = ""
    if form.validate_on_submit():
        query = '''INSERT INTO Player VALUES
        ('{}', {}, {}, '{}', 0, '{}')'''.format(form.name.data, form.height.data, form.weight.data, form.team.data, form.sport.data)
        cursor.execute(query)
        conn.commit()
        print("inserted player: {} into db".format(form.name.data))
    conn.close()
    
    return render_template('index.html', form=form, message=message)


app.run()