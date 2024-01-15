
import sqlite3
from turtle import fd
from flask import Flask, render_template, redirect, request, session
from datetime import datetime, date
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error # lookup, usd
from collections import Counter, defaultdict

app = Flask(__name__)

con = sqlite3.connect('survey.db', check_same_thread=False)
# lets rows be dicts (row[0]['''hash'''])
con.row_factory = sqlite3.Row
#connection for executing SQL queries
db=con.cursor()



app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/burgerking", methods=["GET", "POST"])
@login_required
def bksurvey():
    """Take in survey info"""
    if request.method == "POST":

        # Ensure all fields are filled out
        if not request.form.get("fav-product"):
            return error("must fill all fields", 400)
        elif not request.form.get("fd-quality"):
            return error("must fill all fields", 400)
        elif not request.form.get("svc-quality"):
            return error("must fill all fields", 400)

        # Take in input from user
        id = session.get("user_id")
        place = 'Burger King'
        fav_product = request.form.get("fav-product")
        fd_quality = int(request.form.get("fd-quality"))
        svc_quality = int(request.form.get("svc-quality"))

        # Time the survey was taken
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()

        # Add data into sql database
        db.execute("INSERT INTO fast_food (fast_food_id, place, favoriteProduct, foodQuality, serviceQuality, time, date) VALUES(?, ?, ?, ?, ?, ?, ?)", 
        (id, place, fav_product, fd_quality, svc_quality, current_time, today))
        con.commit()
        return render_template("index.html")
    else:
        return render_template("burgerking.html")

@app.route("/chickfila", methods=["GET", "POST"])
@login_required
def cfasurvey():
    """Take in survey info"""
    if request.method == "POST":

        # Ensure all fields are filled out
        if not request.form.get("fav-product"):
            return error("must fill all fields", 400)
        elif not request.form.get("fd-quality"):
            return error("must fill all fields", 400)
        elif not request.form.get("svc-quality"):
            return error("must fill all fields", 400)

        # Take in input from user
        id = session.get("user_id")
        place = 'Chick-fil-A'
        fav_product = request.form.get("fav-product")
        fd_quality = int(request.form.get("fd-quality"))
        svc_quality = int(request.form.get("svc-quality"))

        # Time the survey was taken
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()

        # Add data into sql database
        db.execute("INSERT INTO fast_food (fast_food_id, place, favoriteProduct, foodQuality, serviceQuality, time, date) VALUES(?, ?, ?, ?, ?, ?, ?)", 
        (id, place, fav_product, fd_quality, svc_quality, current_time, today))
        con.commit()
        return render_template("index.html")
    else:
        return render_template("chickfila.html")

@app.route("/mcdonalds", methods=["GET", "POST"])
@login_required
def mcdonalds():
    """Take in survey info"""
    if request.method == "POST":

        # Ensure all fields are filled out
        if not request.form.get("fav-product"):
            return error("must fill all fields", 400)
        elif not request.form.get("fd-quality"):
            return error("must fill all fields", 400)
        elif not request.form.get("svc-quality"):
            return error("must fill all fields", 400)

        # Take in input from user
        id = session.get("user_id")
        place = "McDonald's"
        fav_product = request.form.get("fav-product")
        fd_quality = int(request.form.get("fd-quality"))
        svc_quality = int(request.form.get("svc-quality"))

        # Time the survey was taken
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()

        # Add data into sql database
        db.execute("INSERT INTO fast_food (fast_food_id, place, favoriteProduct, foodQuality, serviceQuality, time, date) VALUES(?, ?, ?, ?, ?, ?, ?)", 
        (id, place, fav_product, fd_quality, svc_quality, current_time, today))
        con.commit()
        return render_template("index.html")
    else:
        return render_template("mcdonalds.html")


@app.route("/arbys", methods=["GET", "POST"])
@login_required
def arbys():
    """Take in survey info"""
    if request.method == "POST":

        # Ensure all fields are filled out
        if not request.form.get("fav-product"):
            return error("must fill all fields", 400)
        elif not request.form.get("fd-quality"):
            return error("must fill all fields", 400)
        elif not request.form.get("svc-quality"):
            return error("must fill all fields", 400)

        # Take in input from user
        id = session.get("user_id")
        place = "Arby's"
        fav_product = request.form.get("fav-product")
        fd_quality = int(request.form.get("fd-quality"))
        svc_quality = int(request.form.get("svc-quality"))

        # Time the survey was taken
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()

        # Add data into sql database
        db.execute("INSERT INTO fast_food (fast_food_id, place, favoriteProduct, foodQuality, serviceQuality, time, date) VALUES(?, ?, ?, ?, ?, ?, ?)", 
        (id, place, fav_product, fd_quality, svc_quality, current_time, today))
        con.commit()
        return render_template("index.html")
    else:
        return render_template("arbys.html")


@app.route("/rankings")
@login_required
def rankings():
    db.execute("SELECT DISTINCT place FROM fast_food");
    places = db.fetchall()

    # Create dictionaries to loop through
    i = 0
    allPlaces = []
    foodVoteAdv = {}
    serviceVoteAdv = {}
    totalAdv =  {}
    totalVote = {}
    foodVoteSum = {}
    serviceVoteSum = {}
    htmlTotalAdv = {}
    htmlServiceVoteAdv = {}
    htmlFoodVoteAdv = {}
    favProduct = {}
    takenSurveys = {}

    product = defaultdict(list)  # Needed to create a dict with keys that have values as list to append to {key: []}

    for place in places:
        
        place = place[0] # Change it from memory location to value
        allPlaces.insert(i, place)  # Help loop through jinja2 statement in html file
        i += 1

        # Get total votes for eats place
        db.execute("SELECT COUNT(*) FROM fast_food WHERE place = ?", [place])
        totalVotes = db.fetchall()
        totalVote[place] = totalVotes[0][0]

        # Query fast food table to get food vote adverage
        db.execute("SELECT SUM(foodQuality) FROM fast_food WHERE place = ?", [place])
        foodVoteSums = db.fetchall()
        foodVoteSum[place] = foodVoteSums[0][0]
        foodVoteAdv[place] = ((float(foodVoteSum[place]) / float(totalVote[place])) - 1) # Need negative one because bar gragh starts at 1

        # Query fast food table to get service vote adverage
        db.execute("SELECT SUM(serviceQuality) FROM fast_food WHERE place = ?", [place])
        serviceVoteSums = db.fetchall()
        serviceVoteSum[place] = serviceVoteSums[0][0]
        serviceVoteAdv[place] = ((float(serviceVoteSum[place]) / float(totalVote[place])) - 1)

        # Get total overall rating for survey
        totalAdv[place] = (serviceVoteAdv[place] + foodVoteAdv[place]) / 2

        # Make values into percents for html and css
        htmlTotalAdv[place]= (((totalAdv[place]) / 5) * 100) 
        htmlServiceVoteAdv[place]= (((serviceVoteAdv[place]) / 5) * 100)
        htmlFoodVoteAdv[place]= (((foodVoteAdv[place]) / 5) * 100)

        # Get favorite product for each place
        db.execute("SELECT favoriteProduct FROM fast_food WHERE place = ?", [place])
        p = db.fetchall()
        for row in p:
            product[place].append(row[0])
        c = Counter(product[place])  # Interate only once through list with "Counter". Gets total for each product. Takes more memory but O(n) instead of O(n^2)
        favProduct[place] = c.most_common(1)  # Get first key:value which is most selected product

        # Get total surveys taken per place from adding favorite items total
        takenSurveys[place] = sum(c.values())

    # Get (sorted values list) from dict in highest to lowest order of rating
    sortedAdv = {}
    sorted_values = sorted(totalAdv.values(), reverse=True)

    # Get (dict with sorted keys and values) from highest to lowest overall rating
    for value in sorted_values:
        for place in totalAdv.keys():
            if totalAdv[place] == value:
                sortedAdv[place] = totalAdv[place]
            

    return render_template("rankings.html", htmlTotalAdv=htmlTotalAdv, htmlServiceVoteAdv=htmlServiceVoteAdv, htmlFoodVoteAdv=htmlFoodVoteAdv, totalVotes=totalVotes, places=allPlaces, sortedAdv=sortedAdv, favProduct=favProduct, takenSurveys = takenSurveys)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 400)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return error("must provide confirmation", 400)

        user = request.form.get("username")
        db.execute("SELECT username FROM users WHERE username = ?", [user])
        name = db.fetchall()

        # Ensure username does not exist already
        if name:
            return error("username already exist", 400)

        # Ensure a match
        elif  request.form.get("password") != request.form.get("confirmation"):
            return error("confirmation does not match password", 400)

        else:
            password = request.form.get("password")
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", (user, hash))
            con.commit()
            return render_template("login.html")
        
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 400)

        # Query database for username
        user = request.form.get("username")
        db.execute("SELECT * FROM users WHERE username = ?", [user])
        row = db.fetchall()

        # Ensure username exists and password is correct
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

        
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/profile")
def profile():
    return render_template("profile.html")



