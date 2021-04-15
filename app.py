from flask import Flask, jsonify, request, session
import requests
from flask_debugtoolbar import DebugToolbarExtension
from secrets import API_SECRET_KEY
from forms import RegisterForm, LoginForm, PrefsForm
from models import connect_db, db, User, Preference, Login
from flask_cors import CORS, cross_origin
from sqlalchemy import exc



app = Flask(__name__)
cors = CORS(
    app,
    resources={r"*": {"origins": "http://localhost"}},
    expose_headers=["Content-Type", "X-CSRFToken"],
    supports_credentials=True,
)



API_BASE_URL = "https://statsapi.web.nhl.com/api/v1"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///statshot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = API_SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = False
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

debug = DebugToolbarExtension(app)

connect_db(app)




@app.route('/api/teams', methods=["GET"])
@cross_origin(origin='localhost', supports_credentials=True)
def get_teams():
    """Call NHL API to get lucky number"""
    if "user_id" not in session:
        access = {"access": "Please log in to access this feature"}
        return jsonify(access), 403
    else:
        res_teams = requests.get(f"{API_BASE_URL}/teams")
        teams_data = res_teams.json()
        return jsonify(teams_data)


@app.route('/api/teams/<int:team_id>', methods=["GET"])
@cross_origin(origin='localhost', supports_credentials=True)
def get_specified_team(team_id):
    """Call data for specific team by team id"""
    if "user_id" not in session:
        access = {"access": "Please log in to access this feature"}
        return jsonify(access), 403

    else:
        res_team = requests.get(f"{API_BASE_URL}/teams/{team_id}?expand=team.stats")
        team_data = res_team.json()
        return jsonify(team_data)


@app.route('/api/users/register', methods=["POST"])
@cross_origin(origin='http://localhost', supports_credentials=True)
def register():
    """Register a user:  receive JSON form data and submit to DB"""
    
    success = {'user':{}}
    form = RegisterForm()

    if form.validate_on_submit():

        username = request.json["username"]
        password = request.json["password"]

        try:
            user = User.register(username, password)
            db.session.add(user)
            db.session.commit()

            prefs = Preference(user_id=user.id)
            log = Login.record_login(user.id)
            db.session.add(prefs)
            db.session.commit()
            
        
            session['username'] = user.username
            session['user_id'] = user.id

            success['user']['login'] = True
            success['user']['username'] = session['username']
            success['user']['userId'] = session['user_id']
    
            return jsonify(success), 201
        except exc.IntegrityError:
            db.session.rollback()
            success['login'] = False
            success['message'] = "That username is already taken"
        return jsonify(success), 403
    else:
        success['login'] = False
        return jsonify(success), 403

    
@app.route('/api/users/login', methods=["POST"])
@cross_origin(origin='localhost', supports_credentials=True)
def login():
    """Login a user: recieve JSON form data and authenticate username/password."""

    success = {'user':{}}
    form = LoginForm()

    if form.validate_on_submit():

        username = request.json["username"]
        password = request.json["password"]

        user = User.authenticate(username, password)
        if user: 
            session['username'] = user.username
            session['user_id'] = user.id
            log = Login.record_login(user.id)
            db.session.commit()
            success['user']['login'] = True
            success['user']['username'] = session['username']
            success['user']['userId'] = session['user_id']

            return jsonify(success)
        else:
            success['login'] = False
            success['message'] = "The username/password is incorrect"
        
            return jsonify(success), 403
    else:
        success['login'] = False
        success['message'] = "The username/password is incorrect"
        return jsonify(success), 403

@app.route('/api/users/logout', methods=["POST"])
@cross_origin(origin='http://localhost', supports_credentials=True)
def logout():
    """Log a user out.  Remove user id from session."""

    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("fav_team", None)
    session['test'] = 'test'

    logout = {"logout": "You have been logged out"}

    resp = {'session':{}}
    for item in session:
        resp['session'] = item

    return jsonify(resp)

    # return jsonify(logout)

@app.route('/api/users/<int:user_id>/prefs', methods=["GET", "POST"])
@cross_origin(origin='localhost', supports_credentials=True)
def prefs(user_id):
    """Get user prefs on GET request"""

    if "user_id" not in session or user_id != session['user_id']:
        access = {"access": "Please log in to access this page"}
        return jsonify(access), 403
    else:
        prefs = Preference.query.get_or_404(user_id)
        form = PrefsForm()
        if form.validate_on_submit():
            new_fav_team_id = request.json["favTeamId"]
            prefs.fav_team_id = new_fav_team_id
            
            db.session.commit()


        
        fav_team_id = prefs.fav_team_id
        session['fav_team'] = fav_team_id
        prefs = {"prefs":{"favTeam": f"{fav_team_id}"}}
        return jsonify(prefs)

@app.route('/api/users/session')
@cross_origin(origin='localhost', supports_credentials=True)
def check_session():
    """Check if a user is stored in the session, return user information if so"""

    success = {'user':{}}

    if "user_id" not in session :
        success['user']['login'] = False
      
        return jsonify(success)
    else:
        success['user']['login'] = True 
        success['user']['username'] = session['username']
        success['user']['userId'] = session['user_id']
        
        return jsonify(success)

@app.route('/ping', methods=["GET"])
@cross_origin(origin='localhost', supports_credentials=True)
def ping():

    resp = {'session':{}}
    for item in session:
        resp['session'] = item

    return resp



