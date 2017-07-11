#all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#create the app
app = Flask(__name__)
app.config.from_object(__name__)


#load default config from enviroment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'bucket_list.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
app.config.from_envvar('BUCKETLIST_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

####################################################################
#create db
####################################################################

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

####################################################################
#views function
####################################################################

#show list
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select bucketlist_name, bucketlist_description from bucket_list order by id desc')
    entries = cur.fetchall()

    return render_template('index.html', entries=entries)

#add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into bucket_list (bucketlist_name, bucketlist_description) values (?, ?)',
                 [request.form['bucketlist_name'], request.form['bucketlist_description']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

#logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))




###################################################################
#Database Connections
###################################################################

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
