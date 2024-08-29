from flask import render_template, redirect, url_for, flash, request
from app import app, db
from models import User, Player, Team
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists", "danger")
            return redirect(url_for("register"))
        
        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Login failed. Check your email and password.", "danger")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    user_teams = Team.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", teams=user_teams)

@app.route("/create_team", methods=["GET", "POST"])
@login_required
def create_team():
    if request.method == "POST":
        team_name = request.form.get("team_name")
        # Check if the team name already exists
        team = Team.query.filter_by(name=team_name, 
user_id=current_user.id).first()
        if team:
            flash("Team name already exists. Please choose a different name.", "danger")

            return redirect(url_for("create_team"))
        
        # Create a new team and add to the database
        new_team = Team(name=team_name, user_id=current_user.id)
        db.session.add(new_team)
        db.session.commit()
        flash("Team created successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("create_team.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

